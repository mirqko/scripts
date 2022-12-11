# Python built-in modules
import sys
import random
import os

# Python external modules
from PySide2 import (QtWidgets, QtGui, QtCore)
from shiboken2 import wrapInstance
import maya.cmds as cmds
from maya import OpenMayaUI

RESOURCES_LOCATION = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')


# Python custom modules

def get_maya_win():
    win_ptr = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(int(win_ptr), QtWidgets.QMainWindow)


def delete_workspace_control(control):
    if cmds.workspaceControl(control, q=True, exists=True):
        cmds.workspaceControl(control, e=True, close=True)
        cmds.deleteUI(control, control=True)


class MyDockableWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        delete_workspace_control('Maya selection renamer' + 'WorkspaceControl')
        super(self.__class__, self).__init__(parent=parent)
        self.parent_obj = parent
        self.setWindowTitle('Maya selection renamer')
        self.setWindowFlags(QtCore.Qt.Window)
        self.setFixedSize(450, 400)
        self.init_ui()
        self.get_maya_selection()

    def init_ui(self):
        # Setting up main Widget and his layout
        self.main_widget = QtWidgets.QWidget()
        self.main_widget.setObjectName('main_widget')
        self.setCentralWidget(self.main_widget)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setObjectName('main_layout')

        # Set the main layout as the default one for the main widget
        self.main_widget.setLayout(self.main_layout)

        # add other widgets
        random_img = str(random.randint(1, len(os.listdir(RESOURCES_LOCATION))))
        print(random_img)
        self.banner_widget = BannerWidget(
            widget_name='breakdown_tool_banner',
            banner_txt='LIL RENAMER',
            txt_point_size=20,
            txt_weight=65,
            txt_family_font='Montserrat',
            icon_filepath=os.path.join(RESOURCES_LOCATION, random_img),
            icon_label_sizes=[39, 30],
            txt_label_sizes=[340, 60],
            parent_obj=self)
        self.banner_widget.setToolTip('SELECTION RULES:\n'
                                      'single node selection:     it is a group, child nodes will be renamed\n'
                                      'multiple nodes selected: selected nodes will be renamed\n\n'
                                      'double click inside the renamer window to refresh the selection inside maya')
        self.main_layout.addWidget(self.banner_widget)

        self.selection_label = QtWidgets.QLabel('')
        self.main_layout.addWidget(self.selection_label)

        # find and replace groupbox
        self.find_input = QtWidgets.QLineEdit()
        self.repalce_input = QtWidgets.QLineEdit()
        self.replace_button = QtWidgets.QPushButton('Replace!')
        self.replace_button.clicked.connect(self.find_and_replace_action)

        self.find_replace_groupbox = QtWidgets.QGroupBox("Find And Replace")
        self.find_replace_groupbox.setFixedHeight(150)
        self.find_replace_layout = QtWidgets.QGridLayout()

        self.find_replace_layout.addWidget(QtWidgets.QLabel("Find:"), 0, 0)
        self.find_replace_layout.addWidget(self.find_input, 0, 1)
        self.find_replace_layout.addWidget(QtWidgets.QLabel("Replace:"), 1, 0)
        self.find_replace_layout.addWidget(self.repalce_input, 1, 1)
        self.find_replace_layout.addWidget(self.replace_button, 2, 1)

        self.find_replace_groupbox.setLayout(self.find_replace_layout)
        self.main_layout.addWidget(self.find_replace_groupbox)

        # suffix groupbox
        self.suffix_input = QtWidgets.QLineEdit()
        self.suffix_button = QtWidgets.QPushButton('Add Suffix!')
        self.suffix_button.clicked.connect(self.add_suffix_action)

        self.suffix_groupbox = QtWidgets.QGroupBox("Add Suffix")
        self.suffix_groupbox.setFixedHeight(100)
        self.suffix_layout = QtWidgets.QGridLayout()

        self.suffix_layout.addWidget(QtWidgets.QLabel("Suffix:"), 0, 0)
        self.suffix_layout.addWidget(self.suffix_input, 0, 1)
        self.suffix_layout.addWidget(self.suffix_button, 1, 1)

        self.suffix_groupbox.setLayout(self.suffix_layout)
        self.main_layout.addWidget(self.suffix_groupbox)

    def mouseDoubleClickEvent(self, e):
        print('refresh selection')
        self.get_maya_selection()

    def get_maya_selection(self):
        print('maya selection')
        selection = cmds.ls(selection=True)
        if len(selection) == 0:
            self.selection_label.setText('No selection')
            self.selection_label.setStyleSheet("color: yellow;")
        else:
            self.selection_label.setText('transforms selected')
            self.selection_label.setStyleSheet("color: cyan;")
            self.nodes_to_rename = cmds.listRelatives(selection, allDescendents=True)

    def find_and_replace_action(self):
        if self.nodes_to_rename != [] and self.nodes_to_rename != None:
            for node in self.nodes_to_rename:
                new_name = node.replace(self.find_input.text(), self.repalce_input.text())
                cmds.rename(node, new_name)
        self.get_maya_selection()

    def add_suffix_action(self):
        if self.nodes_to_rename != [] and self.nodes_to_rename != None:
            for node in self.nodes_to_rename:
                new_name = '{}_{}'.format(node,self.suffix_input.text())
                cmds.rename(node, new_name)
        self.get_maya_selection()


class BannerWidget(QtWidgets.QWidget):
    def __init__(self,
                 widget_name,
                 banner_txt,
                 txt_point_size=20,
                 txt_weight=65,
                 txt_family_font='Montserrat',
                 icon_filepath=os.path.join(RESOURCES_LOCATION),
                 icon_label_sizes=[150, 150],
                 txt_label_sizes=[250, 300],
                 parent_obj=None):
        """ Class Constructor

        :param banner_txt:
        :param txt_point_size:
        :param txt_weight:
        :param txt_family_font:
        :param icon_filepath:
        :param icon_label_sizes:
        :param txt_label_sizes:
        :param parent_obj:
        """

        super().__init__(parent=parent_obj)

        self.parent_obj = parent_obj
        self.widget_name = widget_name

        self.setObjectName(self.widget_name)

        self.label_basic_font = QtGui.QFont()
        self.label_basic_font.setFamily(txt_family_font)
        self.label_basic_font.setPointSize(txt_point_size)
        self.label_basic_font.setWeight(txt_weight)

        self.banner_layout = QtWidgets.QHBoxLayout()
        self.banner_layout.setObjectName('banner_layout')
        self.setLayout(self.banner_layout)
        self.banner_layout.setAlignment(QtCore.Qt.AlignTop)

        self.title_label_icon_widget = QtWidgets.QLabel()
        self.title_label_icon_widget.setObjectName('banner_title_icon')
        self.title_icon_pixmap = QtGui.QPixmap(icon_filepath)
        self.title_icon_pixmap.scaledToHeight(icon_label_sizes[1])
        self.title_label_icon_widget.setPixmap(self.title_icon_pixmap)
        # self.title_label_icon_widget.setFixedSize(icon_label_sizes[0], icon_label_sizes[1])

        self.title_label_widget = QtWidgets.QLabel()
        self.title_label_widget.setObjectName('banner_title_label')
        self.title_label_widget.setText(banner_txt)
        self.title_label_widget.setFont(self.label_basic_font)
        self.title_label_widget.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.title_label_widget.setFixedSize(txt_label_sizes[0], txt_label_sizes[1])

        self.banner_layout.addWidget(self.title_label_icon_widget)
        self.banner_layout.addWidget(self.title_label_widget)

def main():
    my_win = MyDockableWindow(parent=get_maya_win())
    my_win.show()