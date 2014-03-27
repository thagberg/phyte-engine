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
        print self.entity_name_field.text()
        new_entity = QtGui.QListWidgetItem()
        new_entity.setText(self.entity_name_field.text())
        #self.entity_list_model.appendRow(new_entity)
        self.entity_list_view.addItem(new_entity)
        print 'Added new entity'
