import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore, QtGui
import maya.OpenMayaUI as OpenMayaUI # for maya_main_window()
import shiboken2 #used to integrate C++ programs to Python

def maya_main_window():
    # To make our main window a child to maya so we can make it hover above maya
	main_window_ptr=OpenMayaUI.MQtUtil.mainWindow()
	return shiboken2.wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

def deleteUI(my_ui):
    if cmds.window(my_ui, exists=1):
        cmds.deleteUI(my_ui)
    if cmds.windowPref(my_ui, exists=1):
        cmds.windowPref(my_ui, remove=1)

scroll_style = """
    QScrollBar:vertical {
        background: rgb(10,10,10);
        width: 5px;
        margin: 0px 0 0px 0;
        }

    QScrollBar::handle:vertical {
        border: 1px rgb(0, 0, 0);
        background: rgb(128, 123, 171);
        }
"""

class SelectionWidget(QtWidgets.QWidget):
    #create a selection set
    buttonSignal = QtCore.Signal(str)  # create a static attribute
    selectionClicked = QtCore.Signal(list)   # Create a custom signal to select the set

    def __init__(self, objects, count, ):
        super(SelectionWidget, self).__init__()

        self.objects = objects
        self.count = count
        self.state = True

        self.selection = []
        self.get_selection()

        self.object_path = self.get_selection()
        self.display_name = [obj.split("|")[-1] for obj in self.selection] #to display a short name

        self.setup_ui()

    def setup_ui(self):
        '''
        setting up UI for selection widget
        '''
        self.setMinimumSize(228,90)
        self.setMaximumHeight(90)
        self.setAutoFillBackground(True) #to set color we need this
        self.set_background() #set color

        #layout
        self.main_layout = QtWidgets.QHBoxLayout()
        self.setContentsMargins(5, 0, 5, 0)
        self.setLayout(self.main_layout)

        #text on the widget
        self.short_names_label = QtWidgets.QLineEdit()
        self.short_names_label.textChanged.connect(lambda x: self.short_names_label.displayText())
        self.short_names_label.setReadOnly(True)  # Set the QLineEdit as read-only initially

        self.short_names_label.setStyleSheet(
            "QLineEdit { "
            "border: 0px;"
            "background-color: rgb(60, 60, 60); "
            "color: rgb(128, 123, 171);"
            "font-size: 16px;  "
            "}")
        self.update_short_names_label()  # Update the label text with the short names
        self.main_layout.addWidget(self.short_names_label)
        self.short_names_label.setAlignment(QtCore.Qt.AlignCenter)

    def get_selection(self):
        '''
        With that one we create selection set
        '''
        self.selection = cmds.ls(sl=True, l=True)

    def update_short_names_label(self):
        '''
        Creates a name based on all the controllers that you selected.
        Convert the list of short names to a single string with comma separator.
        '''
        names_str = ", ".join(self.display_name)
        self.short_names_label.setText(names_str)

    def select_objects_back(self):
        cmds.select(self.objects)

    def set_background(self, r=60, g=60, b=60):
        self.p = QtGui.QPalette()
        self.color = QtGui.QColor(r, g, b)
        self.p.setColor(self.backgroundRole(), self.color)
        self.setPalette(self.p)

    def mouseReleaseEvent(self, event):
        '''
        selecting the set by releasing the button with function select_objects_back()
        '''
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), QtGui.QColor(90, 90, 90))
        self.setPalette(self.p)

        if self.state == True:
            self.select_objects_back()

    def enterEvent(self, event):
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.set_background(80, 80, 80)

    def leaveEvent(self, event):
        self.setCursor(QtCore.Qt.ArrowCursor)
        self.set_background(60, 60, 60)

    def mousePressEvent(self, event):
        '''
        we are calling pop menu on this event
        '''
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), QtGui.QColor(100, 100, 100))
        self.setPalette(self.p)

        if event.button() == QtCore.Qt.LeftButton:
            self.state = True

        elif event.button() == QtCore.Qt.RightButton:
            self.state = False  # we are blocking the button's pressing

            self.create_context_menu()  # instead we are creating pop-up context menu
            self.pop_menu.exec_(self.mapToGlobal(event.pos()))

    def separator_line(self):
        '''
        separator for create_context_menu()
        '''
        self.separator = QtWidgets.QAction(self)
        self.separator.setSeparator(True)
        self.pop_menu.addAction(self.separator)

    def create_context_menu(self):
        '''
        create a pop-up context menu with five new options for the selection set
        '''
        self.pop_menu = QtWidgets.QMenu(self)

        self.pop_menu_add = QtWidgets.QAction('Add Selection', self)  # QAction is a menu type
        self.pop_menu.addAction(self.pop_menu_add)
        self.pop_menu_add.triggered.connect(self.add_selection)

        self.pop_menu_remove = QtWidgets.QAction('Remove Selection', self)
        self.pop_menu.addAction(self.pop_menu_remove)
        self.pop_menu_remove.triggered.connect(self.remove_selection)

        self.separator_line()

        self.pop_menu_remove = QtWidgets.QAction('Rename', self)
        self.pop_menu.addAction(self.pop_menu_remove)
        self.pop_menu_remove.triggered.connect(self.rename_selection)

        self.pop_menu_delete = QtWidgets.QAction('Delete', self)
        self.pop_menu.addAction(self.pop_menu_delete)
        self.pop_menu_delete.triggered.connect(self.delete_selection)

        self.separator_line()

        self.pop_menu_close = QtWidgets.QAction('Close window', self)
        self.pop_menu.addAction(self.pop_menu_close)
        self.pop_menu_close.triggered.connect(self.close_window)

    def add_selection(self):
        '''
        'Add Selection'
        '''
        self.selection = cmds.ls(sl=True, l=True)
        for obj in self.selection:
            if obj not in self.objects:
                self.objects.append(obj)

    def remove_selection(self):
        '''
        'Remove Selection' on pop menu
        '''
        self.selection = cmds.ls(sl=True, l=True)
        for obj in self.selection:
            if obj in self.objects:
                self.objects.remove(obj)

    def rename_selection(self):
        '''
        'Rename' on pop menu
        '''
        self.short_names_label.setFocus()
        self.short_names_label.setReadOnly(False)
        self.short_names_label.editingFinished.connect(self.finish_editing)

    def finish_editing(self):
        '''
        This one we call in rename selection, it helps us to finish editing and reset focus
        '''
        self.short_names_label.setReadOnly(True)
        self.setFocus()

    def delete_selection(self):
        '''
        'Delete' on pop menu
        '''
        self.deleteLater()  # to delete widget

    def close_window(self):
        '''
        'Close window' on pop menu
        '''
        my_ui.close()  # close window

class PlusSelectionWidget(QtWidgets.QWidget):
    #create "+" widget for adding new sets of controls
    clicked = QtCore.Signal() # Define a custom clicked signal

    def __init__(self, icon=None, sub=False):
        super(PlusSelectionWidget, self).__init__()
        self.state = False
        self.sub = sub
        self.setup_ui()

    def setup_ui(self):
        '''
        Setting up UI for "+" widget
        '''
        self.setMinimumSize(228, 90)
        self.setMaximumHeight(90)
        self.setAutoFillBackground(True)  # to set color we need this
        self.set_background()  # set color
        self.main_layout = QtWidgets.QHBoxLayout()
        self.setContentsMargins(5, 0, 5, 0)
        self.setLayout(self.main_layout)

        # text on the widget
        self.plus_label = QtWidgets.QLabel("+")
        self.main_layout.addWidget(self.plus_label)
        self.plus_label.setAlignment(QtCore.Qt.AlignCenter)
        self.plus_label.setStyleSheet(''' font-size: 24px; ''')

    def mouseReleaseEvent(self, event):
        '''
        This one we use only for changing style on button released
        '''
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), QtGui.QColor(80, 80, 80))
        self.setPalette(self.p)

    def mousePressEvent(self, event):
        '''
        Style for the button and
        '''
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), QtGui.QColor(100, 100, 100))
        self.setPalette(self.p)

        # that's pretty important for mouseReleaseEvent on 44rd string
        if event.button() == QtCore.Qt.LeftButton:
            self.state = True
            self.on_widget_clicked(event)

        elif event.button() == QtCore.Qt.RightButton:
            self.state = False  # we are blocking the button's pressing

    def on_widget_clicked(self, event):
        # Emit the custom clicked signal when the widget is clicked
        self.clicked.emit()

    def set_background(self, r=60, g=60, b=60):
        # set background
        self.p = QtGui.QPalette()
        self.color = QtGui.QColor(r, g, b)
        self.p.setColor(self.backgroundRole(), self.color)
        self.setPalette(self.p)

    def enterEvent(self, event):
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.set_background(80, 80, 80)

    def leaveEvent(self, event):
        self.setCursor(QtCore.Qt.ArrowCursor)
        self.set_background(60, 60, 60)


class SelectionToolWindow(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        #creates window for a work with selection sets
        super(SelectionToolWindow, self).__init__(parent=parent)  # super is important to call the main class

        #to create a selection set
        self.selection = []
        self.get_selection()
        self.create_selection_list = {}
        self.num = 1

        #here we create translucent window but for real just removing the top part of the window
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.offset = QtCore.QPoint(0, 0)
        self.pressed = False
        self.background_color = QtGui.QColor(45, 44, 44, 200)
        self.setAutoFillBackground(True)

        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), QtGui.QColor(45, 44, 44))
        self.setPalette(self.p)

        #that will help us to frag the window
        self.setAcceptDrops(True)
        self.setMouseTracking(True)  # Track mouse movements
        self.draggable = False
        self.offset = None

        self.setup_ui() #main window and layouts
    def setup_ui(self):
        self.setWindowTitle("Custom Bunny UI")
        self.setObjectName("MyCustomWidgetBunny")

        self.setMinimumSize(250,250)
        self.setMaximumSize(250, 900)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setAlignment(QtCore.Qt.AlignTop)
        self.main_layout.setContentsMargins(0, 0, 0, 0) #if you don't want any margins
        self.main_layout.setSpacing(3) #margins between buttons
        self.setLayout(self.main_layout)

        #* --------------------scroll area----------------------------- *#
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setMinimumHeight(400)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumWidth(250)
        self.scroll_area.setMaximumWidth(250)
        self.scroll_area.setFocusPolicy(QtCore.Qt.NoFocus)

        self.scrollbar = QtWidgets.QScrollBar()
        self.scrollbar.setStyleSheet(scroll_style)
        self.scroll_area.setVerticalScrollBar(self.scrollbar)

        self.scroll_area_widget = QtWidgets.QWidget()
        self.scroll_area.setWidget(self.scroll_area_widget)

        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.scroll_layout.setAlignment(QtCore.Qt.AlignTop)
        self.scroll_layout.setContentsMargins(5, 0, 5, 0)
        self.scroll_layout.setSpacing(5) #layout
        self.scroll_area_widget.setLayout(self.scroll_layout)

        self.main_layout.addWidget(self.scroll_area)
        #* -------------------------------------------------------------- *#

        #adding plus widget
        self.plus_button = PlusSelectionWidget()
        self.main_layout.addWidget(self.plus_button)
        self.plus_button.clicked.connect(self.on_widget_clicked)

    def mousePressEvent(self, event):
        '''
        This one either drags window LB, either open a pop menu RB
        '''
        if event.button() == QtCore.Qt.LeftButton and event.y() <= 400:
            self.draggable = True
            self.offset = event.pos()

        elif event.button() == QtCore.Qt.RightButton:
            self.state = False  # we are blocking the button's pressing

            self.create_main_context_menu()  # instead we are creating pop-up context menu
            self.pop_main_menu.exec_(self.mapToGlobal(event.pos()))

    def mouseReleaseEvent(self, event):
        '''
        Need to support the window moving
        '''
        if event.button() == QtCore.Qt.LeftButton:
            self.draggable = False
            self.offset = None

    def mouseMoveEvent(self, event):
        '''
        Need to support the window moving
        '''
        if self.draggable and self.offset is not None:
            # Calculate the new window position based on the mouse movement
            new_pos = event.globalPos() - self.offset
            self.move(new_pos)

    def paintEvent(self, event):
        '''
        Painting boarders? not sure
        '''
        super(SelectionToolWindow, self).paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.begin(self)
        painter.fillRect(0, 0, self.width(), self.height(), QtGui.QColor(68, 68, 68, 150))
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_Source)
        painter.end()

    def on_widget_clicked(self):
        '''
        What's happening when you click "+" widget
        '''
        self.get_selection()
        self.add_selection_widget()

    def get_selection(self):
        self.selection = cmds.ls(sl=1, l=1) #duh

    def add_selection_widget(self):
        '''
        This one creates selection set by using SelectionWidget class and create_selection_list var
        '''
        self.selection_widget = SelectionWidget(self.selection, self.num)
        self.create_selection_list[self.num] = self.selection_widget
        self.num =+ 1

        self.scroll_layout.addWidget(self.selection_widget)

    def create_main_context_menu(self):
        '''
        create a pop-up context menu with a close option
        '''
        self.pop_main_menu = QtWidgets.QMenu(self)

        self.pop_main_menu_close = QtWidgets.QAction('Close window', self)
        self.pop_main_menu.addAction(self.pop_main_menu_close)
        self.pop_main_menu_close.triggered.connect(self.close_main_window)

    def close_main_window(self):
        '''
        To close window from pop up menu in the main window
        '''
        my_ui.close()

#---------------------------------THE-END------------------------------------------

deleteUI("MyCustomWidgetBunny")
global dialog
#also creating var for close_window() and close_main_window()
my_ui = SelectionToolWindow()
my_ui.show()
