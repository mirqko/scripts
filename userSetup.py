# -*- coding: utf-8 -*-
__author__ = 'Mirqo'
__contributors__ = ['Mirko Di Giorgio']
"""File used to load a custom menu inside maya at opening.
   place this file inside %MAYA_APP_DIR%/<version>/scripts
"""
# Python built-in modules
from importlib import reload

# Python external modules
from maya import (cmds, mel, utils, OpenMayaUI)
from PySide2 import (QtWidgets, QtCore)
from shiboken2 import wrapInstance

# Python custom modules
import renamer
import utilities_functions


# def get_current_main_window():
#     main_window_pointer = OpenMayaUI.MQtUtil.mainWindow()
#     return wrapInstance(main_window_pointer, QtWidgets.QWidget)

def custom_down_menu(*args):
    cmds.setParent('MayaWindow')

    #widget_parent = get_current_main_window() #not sure if this is needed here

    menu = cmds.menu('scripts', label='🍤')
    base_tool_section = cmds.menuItem(divider=True, parent=menu)
    cmds.menuItem(label='test', command=lambda x: utilities_functions.test(), parent=menu)
    cmds.menuItem(label='Renamer', command=lambda x: reloading(), parent=menu)

def reloading():
    reload(renamer)
    renamer.main()

utils.executeDeferred(custom_down_menu)
