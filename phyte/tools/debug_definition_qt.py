from PyQt4 import QtGui, QtCore

from editor_qt import Editor
from common import Component, WidgetItemComponent, TreeWidgetItemComponent, LambdaDef, TextLambdaDef
from engine.debug import DebugComponent
from engine.text import TextComponent
from event import Event, EVENT_MAPPING, EVENT_QUEUE, EVENT_MANAGER
import common


class DebugDefinitionEditor(Editor):
    def __init__(self, context):
        super(DebugDefinitionEditor, self).__init__(context, QtGui.QGroupBox('Debug'))
        # setup gui stuff
        self.layout = QtGui.QGridLayout()
        self.debug_name_label = QtGui.QLabel('Debug Name')
        self.debug_name_field = QtGui.QLineEdit()
        self.name_layout = QtGui.QVBoxLayout()
        self.component_tree_view = QtGui.QTreeWidget()
        self.component_tree_label = QtGui.QLabel('Choose Component or Property')
        self.component_layout = QtGui.QVBoxLayout()
        self.vector_list_view = QtGui.QListWidget()
        self.vector_list_label = QtGui.QLabel('Choose Position')
        self.vector_layout = QtGui.QVBoxLayout()
        self.color_list_view = QtGui.QListWidget()
        self.color_list_label = QtGui.QLabel('Choose Color')
        self.color_layout = QtGui.QVBoxLayout()
        self.debug_list_view = QtGui.QListWidget()
        self.add_debug_button = QtGui.QPushButton('Add Debug')
        self.edit_debug_button = QtGui.QPushButton('Edit Debug')
        self.remove_debug_button = QtGui.QPushButton('Remove Debug')
        self.button_layout = QtGui.QVBoxLayout()

        # setup layout
        self.name_layout.addWidget(self.debug_name_label)
        self.name_layout.addWidget(self.debug_name_field)
        self.layout.addLayout(self.name_layout,0,0)
        self.component_layout.addWidget(self.component_tree_label)
        self.component_layout.addWidget(self.component_tree_view)
        self.layout.addLayout(self.component_layout,1,0)
        self.vector_layout.addWidget(self.vector_list_label)
        self.vector_layout.addWidget(self.vector_list_view)
        self.layout.addLayout(self.vector_layout,1,1)
        self.color_layout.addWidget(self.color_list_label)
        self.color_layout.addWidget(self.color_list_view)
        self.layout.addLayout(self.color_layout,1,2)
        self.layout.addWidget(self.debug_list_view,2,0)
        self.button_layout.addWidget(self.add_debug_button)
        self.button_layout.addWidget(self.edit_debug_button)
        self.button_layout.addWidget(self.remove_debug_button)
        self.layout.addLayout(self.button_layout,2,1)

        self.group.setLayout(self.layout)

        # internal events
        EVENT_MAPPING.register_handler('selected_entity', self.set_entity)
        EVENT_MAPPING.register_handler('added_component', self.add_component)
        EVENT_MAPPING.register_handler('removed_component', self.remove_component)

        # wire up events
        self.add_debug_button.clicked.connect(self.add_debug)
        self.edit_debug_button.clicked.connect(self.edit_debug)
        self.remove_debug_button.clicked.connect(self.remove_debug)
        self.debug_list_view.currentItemChanged.connect(self.select_debug)

        # populate color list
        white = WidgetItemComponent('White', Component(common.WHITE, 'White'))
        red = WidgetItemComponent('Red', Component(common.RED, 'Red'))
        green = WidgetItemComponent('Green', Component(common.GREEN, 'Green'))
        blue = WidgetItemComponent('Blue', Component(common.BLUE, 'Blue'))
        yellow = WidgetItemComponent('Yellow', Component(common.YELLOW, 'Yellow'))
        black = WidgetItemComponent('Black', Component(common.BLACK, 'Black'))
        purple = WidgetItemComponent('Purple', Component(common.PURPLE, 'Purple'))
        self.color_list_view.addItem(white)
        self.color_list_view.addItem(red)
        self.color_list_view.addItem(green)
        self.color_list_view.addItem(blue)
        self.color_list_view.addItem(yellow)
        self.color_list_view.addItem(black)
        self.color_list_view.addItem(purple)

    def update(self):
        self.component_tree_view.clear()
        self.vector_list_view.clear()
        self._find_components()

    def _find_components(self):
        # set the currently selected entity, if any
        entity = self.context['selected_entity']
        if not entity:
            return

        # repopulate the tree view
        entity_components = self.context['entities'][entity]['components']
        for comp_type in entity_components.keys():
            components = entity_components[comp_type]
            tl_item = TreeWidgetItemComponent(comp_type, components)
            self.component_tree_view.addTopLevelItem(tl_item)
            for component in components:
                # first add this component as a child item to the
                # component type top level item
                component_item = TreeWidgetItemComponent(component.text, component)
                tl_item.addChild(component_item)
                # then add each property of this component as
                # an additional nested level of child items
                for name in (x for x in dir(component.component) if not x.startswith('_')):
                    val = LambdaDef(component, name)
                    component_attr_item = TreeWidgetItemComponent(name, val)
                    component_item.addChild(component_attr_item)

    def add_debug(self):
        entity = self.context['selected_entity']
        name = self.debug_name_field.text()
        component_item = self.component_tree_view.currentItem()
        lambda_component = component_item.component
        color = self.color_list_view.currentItem().component
        location_vec = self.vector_list_view.currentItem().component

        inner_component = lambda_component.component.component
        #component_type = component_wrapper.__class__.__name__
        attr = getattr(inner_component, lambda_component.attr).component
        component_type = attr.__class__.__name__
        # create the debug component
        # extract the real component from a LambdaDef
        if component_type == 'BoxComponent':
            rect = getattr(inner_component, lambda_component.attr)
            debug_component = DebugComponent(entity_id=entity,
                                             rect=rect,
                                             style={'color': color})
        else:
            lambda_name = lambda_component.attr
            text_lambda = TextLambdaDef(lambda_component, lambda_name, '{a}')
            text = str(getattr(lambda_component.component.component, lambda_name).component)
            text_comp = TextComponent(entity_id=entity,
                                      text=text,
                                      loc=location_vec,
                                      style={'color':color})
            text_wrapper = Component(text_comp, text)
            # add this text component to the context
            self.context['entities'][entity]['components']['text'].append(text_wrapper)
            new_event = Event('added_component',
                              entity=entity,
                              component_type='text',
                              component=text_wrapper)
            EVENT_MANAGER.fire_event(new_event)
            # finally create debug component
            debug_component = DebugComponent(entity_id=entity,
                                             text=text_wrapper,
                                             get_value=text_lambda,
                                             style={'color': color})

        debug_wrapper = Component(debug_component, name)
        widget_item = WidgetItemComponent(name, debug_wrapper)
        self.debug_list_view.addItem(widget_item)

        # add to context
        self.context['entities'][entity]['components']['debug'].append(debug_wrapper)
        # fire event
        new_event = Event('added_component',
                          entity=entity,
                          component_type='debug',
                          component=debug_wrapper)
        EVENT_MANAGER.fire_event(new_event)
                                 

    def edit_debug(self):
        pass

    def remove_debug(self):
        entity = self.context['selected_entity']
        selected_row = self.debug_list_view.currentRow()
        selected_item = self.debug_list_view.currentItem()
        selected_component = selected_item.component

        # first remove from debug list
        self.debug_list_view.takeItem(selected_row)

        # then remove from context
        debug_comps = self.context['entities'][entity]['components']['debug']
        for debug_comp in debug_comps:
            if debug_comp == selected_component:
                debug_comps.remove(debug_comp)

        # fire event
        new_event = Event('removed_component',
                          entity=entity,
                          component_type='debug',
                          component=selected_component)
        EVENT_MANAGER.fire_event(new_event)

    def select_debug(self):
        entity = self.context['selected_entity']
        selected_item = self.debug_list_view.currentItem()
        if not selected_item:
            return
        selected_component = selected_item.component

        # set name field
        self.debug_name_field.setText(selected_component.text)

        # set color
        for i in range(self.color_list_view.count()):
            item = self.color_list_view.item(i)
            color = item.component.component
            if color == selected_component.component.style['color'].component:
                self.color_list_view.setCurrentRow(i)
                break

        # set position
        for i in range(self.vector_list_view.count()):
            item = self.vector_list_view.item(i)
            vector = item.component
            if selected_component.component.text:
                if vector == selected_component.component.text.component.loc:
                    self.vector_list_view.setCurrentRow(i)
                    break
            elif selected_component.component.rect:
                rect_pos = (selected_component.component.rect.x,
                            selected_component.component.rect.y)
                if vector.component.x == rect_pos(0) and vector.component.y == rect_pos(1):
                    self.vector_list_view.setCurrentRow(i)
                    break

        # collapse component attribute tree
        for i in range(self.component_tree_view.topLevelItemCount()):
            tl_item = self.component_tree_view.topLevelItem(i)
            tl_item.setExpanded(False)
            for j in range(tl_item.childCount()):
                child_item = tl_item.child(j)
                child_item.setSelected(False)
                child_item.setExpanded(False)
                for k in range(child_item.childCount()):
                    child_attr = child_item.child(k)
                    child_attr.setSelected(False)

        # set component or propery
        tree_comp = selected_component.component.get_value.component
        tree_attr = selected_component.component.get_value.attr
        for i in range(self.component_tree_view.topLevelItemCount()):
            tl_item = self.component_tree_view.topLevelItem(i)
            for j in range(tl_item.childCount()):
                child_item = tl_item.child(j)
                # first check if this component is the selected one
                if child_item.component == tree_comp:
                    tl_item.setExpanded(True)
                    child_item.setExpanded(True)
                    for k in range(child_item.childCount()):
                        child_attr = child_item.child(k)
                        if child_attr.component.attr == tree_attr:
                            child_attr.setSelected(True)
                            break


    def set_entity(self, event):
        entity = event.entity
        entity_components = self.context['entities'][entity]['components']
        # clear views
        for i in range(self.component_tree_view.topLevelItemCount()-1,-1,-1):
            item = self.component_tree_view.takeTopLevelItem(i)
        for i in range(self.vector_list_view.count()-1,-1,-1):
            item = self.vector_list_view.takeItem(i)
        for i in range(self.debug_list_view.count()-1,-1,-1):
            item = self.debug_list_view.takeItem(i)

        # populate the component tree view
        self._find_components()

        # populate the vector list view
        vectors = entity_components['body']
        for vector in vectors:
            widget_item = WidgetItemComponent(vector.text, vector)
            self.vector_list_view.addItem(widget_item)

        # populate debug list view
        debugs = entity_components['debug']
        for deb in debugs:
            widget_item = WidgetItemComponent(deb.text, deb)
            self.debug_list_view.addItem(widget_item)

    def add_component(self, event):
        entity = event.entity
        component_type = event.component_type
        component = event.component
        if component_type == 'body':
            widget_item = WidgetItemComponent(component.text, component)
            self.vector_list_view.addItem(widget_item)

    def remove_component(self, event):
        entity = event.entity
        component_type = event.component_type
        component = event.component
        if component_type == 'body':
            for i in xrange(self.vector_list_view.count()):
                item = self.vector_list_view.item(i)
                comp = item.component
                if comp == component:
                    self.vector_list_view.takeItem(i)
                    break
