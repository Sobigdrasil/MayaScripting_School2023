import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore, QtGui


button_style = """
    QPushButton#MyCustomButtonWidgetID{
        background-color: rgb(109,113,168);
        border-radius: 10px;
        min-width: 30px;
        min-height: 30px;
        font-weight: 900;


    }
    QPushButton#MyCustomButtonWidgetID:hover {
        background-color: rgb(255,133,198);
        min-width: 30px;
        min-height: 30px;  
    }
    """



class SelectionWidget(QtWidgets.QWidget):
    buttonSignal = QtCore.Signal(str)  # create a static attribute

    def __init__(self):
        super(SelectionWidget, self).__init__()

        self.selection = []
        self.get_selection()
        self.create_selection_list = {}
        self.i = 0

        self.object_path = cmds.ls(sl=True, l=True)
        self.display_name = [obj.split("|")[-1] for obj in self.selection] #to display a short name

        self.setup_ui()

    def setup_ui(self):

        self.setMinimumSize(228,90)
        self.setMaximumHeight(90)

        self.setAutoFillBackground(True) #to set color we need this

        #set color
        self.set_background()

        #layout
        self.main_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.main_layout)

        #text on the widget
        self.short_names_label = QtWidgets.QLabel()
        self.update_short_names_label()  # Update the label text with the short names
        self.main_layout.addWidget(self.short_names_label)
        self.short_names_label.setAlignment(QtCore.Qt.AlignCenter)
        self.short_names_label.setStyleSheet(''' font-size: 12px; ''')

    def get_selection(self):
        self.selection = cmds.ls(sl=True, l=True)

    def update_short_names_label(self):
        # Convert the list of short names to a single string with comma separator
        names_str = ", ".join(self.display_name)
        self.short_names_label.setText(names_str)

    def set_background(self, r=60, g=60, b=60):
        # set background
        self.p = QtGui.QPalette()
        self.color = QtGui.QColor(r, g, b)
        self.p.setColor(self.backgroundRole(), self.color)
        self.setPalette(self.p)

    def mouseReleaseEvent(self, event):
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), QtGui.QColor(90, 90, 90))
        self.setPalette(self.p)

        # if self.state == True:
        #     self.run_selection()

    def enterEvent(self, event):
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.set_background(80, 80, 80)

    def leaveEvent(self, event):
        self.setCursor(QtCore.Qt.ArrowCursor)
        self.set_background(60, 60, 60)

    def mousePressEvent(self, event):
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), QtGui.QColor(100, 100, 100))
        self.setPalette(self.p)

        # that's pretty important for mouseReleaseEvent on 44rd string
        if event.button() == QtCore.Qt.LeftButton:
            self.state = True


        elif event.button() == QtCore.Qt.RightButton:
            self.state = False  # we are blocking the button's pressing

            self.create_context_menu()  # instead we are creating pop-up context menu
            self.pop_menu.exec_(self.mapToGlobal(event.pos()))

    def create_context_menu(self):
        '''
        create a pop-up context menu with two new options in the button
        :return:
        '''
        self.pop_menu = QtWidgets.QMenu(self)

        self.pop_menu_add = QtWidgets.QAction('Add Selection', self)  # QAction is a menu type
        self.pop_menu.addAction(self.pop_menu_add)
        self.pop_menu_add.triggered.connect(self.add_selection)

        self.pop_menu_remove = QtWidgets.QAction('Remove Selection', self)
        self.pop_menu.addAction(self.pop_menu_remove)
        self.pop_menu_remove.triggered.connect(self.remove_selection)

        self.pop_menu_remove = QtWidgets.QAction('Rename', self)
        self.pop_menu.addAction(self.pop_menu_remove)
        self.pop_menu_remove.triggered.connect(self.rename_selection)

        self.pop_menu_delete = QtWidgets.QAction('Delete', self)
        self.pop_menu.addAction(self.pop_menu_delete)
        self.pop_menu_delete.triggered.connect(self.delete_selection)


    def add_selection(self):
        print("TEST A")

    def remove_selection(self):
        print("TEST A")

    def rename_selection(self):
        print("TEST B")

    def delete_selection(self):
        self.deleteLater()  # to delete widget

class PlusSelectionWidget(QtWidgets.QWidget):
    clicked = QtCore.Signal() # Define a custom clicked signal

    def __init__(self):
        super(PlusSelectionWidget, self).__init__()

        self.setup_ui()

    def setup_ui(self):

        self.setMinimumSize(228,90)
        self.setMaximumHeight(90)

        self.setAutoFillBackground(True) #to set color we need this

        #set color
        self.set_background()

        #layout
        self.main_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.main_layout)

        #text on the widget
        self.plus_label = QtWidgets.QLabel("+")
        self.main_layout.addWidget(self.plus_label)
        self.plus_label.setAlignment(QtCore.Qt.AlignCenter)
        self.plus_label.setStyleSheet(''' font-size: 24px; ''')

        self.mousePressEvent = self.on_widget_clicked

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

    def mouseReleaseEvent(self, event):
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), QtGui.QColor(80, 80, 80))
        self.setPalette(self.p)


scroll_style = """
    QScrollBar:vertical {
        background: rgb(10,10,10);
        width: 5px;
        margin: 0px 0 0px 0;
        }

    QScrollBar::handle:vertical {
        border: 1px rgb(0, 0, 0);
        background: rgb(255, 85, 85);
        }
"""

class SelectionToolWindow(QtWidgets.QDialog):

    def __init__(self, parent=None):
        #creates window for a work with selection sets
        super(SelectionToolWindow, self).__init__()  # super is important to call the main class

        self.setup_ui() #main window and layouts
    def setup_ui(self):
        self.setWindowTitle("Custom Bunny UI")
        self.setObjectName("MyCustomWidgetBunny")
        self.setMinimumSize(250,400)
        self.resize(300,500)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)


        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setAlignment(QtCore.Qt.AlignTop)
        self.main_layout.setContentsMargins(0, 0, 0, 0) #if you don't want any margins
        self.main_layout.setSpacing(3) #margins between buttons
        self.setLayout(self.main_layout)

        #* scroll area ----------------------------------------------- *#
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setMinimumHeight(400)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumWidth(290)
        self.scroll_area.setMaximumWidth(500)
        self.scroll_area.setFocusPolicy(QtCore.Qt.NoFocus)
        #self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

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

        self.plus_button = PlusSelectionWidget()
        self.scroll_layout.addWidget(self.plus_button)
        self.plus_button.clicked.connect(self.on_widget_clicked)

    def on_widget_clicked(self):
        # self.get_selection()
        self.add_selection_widget()

    def add_selection_widget(self):
        self.selection_set_wgt = SelectionWidget()
        self.scroll_layout.addWidget(self.selection_set_wgt)


def main():
    if cmds.window("MyCustomWidgetBunny", query=True, exists=True):
       cmds.deleteUI("MyCustomWidgetBunny")

    if cmds.windowPref("MyCustomWidgetBunny", exists=True):
       cmds.windowPref("MyCustomWidgetBunny", remove=True)

    global my_ui
    my_ui = SelectionToolWindow()
    my_ui.show()

main()
