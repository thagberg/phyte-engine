from PyQt4 import QtGui

from editor_qt import Editor
from engine.entity import Entity


class EntityDefinitionEditor(Editor):
    def __init__(self, context):
        super(EntityDefinitionEditor, self).__init__(context)        
        self.group = QtGui.QGroupBox('Entity')
        self.layout = QtGui.QGridLayout()
        self.entity_name_field = QtGui.QLineEdit()
        self.entity_name_label =  QtGui.QLabel('Entity Name')
        self.add_entity_button = QtGui.QPushButton('Add Entity')
        self.entity_list_view = QtGui.QListWidget()
        #self.entity_list_model = QtGui.QStandardItemModel()
        #self.entity_list_view.setModel(self.entity_list_model)

        self.layout.addWidget(self.entity_name_label,0,0)
        self.layout.addWidget(self.entity_name_field,0,1)
        self.layout.addWidget(self.add_entity_button,0,2)
        self.layout.addWidget(self.entity_list_view,1,0)

        self.group.setLayout(self.layout)

        # register events
        self.add_entity_button.clicked.connect(self.add_entity)

    def add_entity(self, checked):
        entity_name = self.entity_name_field.text()
        new_entity_item = QtGui.QListWidgetItem(entity_name)
        new_entity = Entity(entity_name)
        self.entity_list_view.addItem(new_entity_item)
        self.context[entity_name] = dict()
        self.context[entity_name]['entity'] = new_entity 

    def select_entity(self, previous, current):
        self.context['selected_entity'] = current.text()
