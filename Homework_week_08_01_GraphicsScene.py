import os
import json
from PySide2 import QtWidgets, QtGui, QtCore
import maya.cmds as cmds
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

json_path = "D:/"
json_name = "DragAndDrop.json"

GLOBAL_LIST = ["Button1", "Button2", "Button3", "Button4"]

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

class MyCustomWidget(MayaQWidgetDockableMixin, QtWidgets.QDockWidget):
    def __init__(self, json_path, json_name):
        super(MyCustomWidget, self).__init__()

        self.setDockableParameters(width=200)
        self.setFloating(False)

        self.json_path = json_path
        self.json_name = json_name

        self.setup_ui()

        self.read_json()

    def setup_ui(self):
        self.setWindowTitle("Custom Bunny UI")
        self.setObjectName("MyCustomWidgetBunny")
        self.setMinimumSize(250, 400)
        self.resize(300, 500)

        self.main_widget = QtWidgets.QWidget()
        self.setWidget(self.main_widget)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setAlignment(QtCore.Qt.AlignTop)
        self.main_layout.setContentsMargins(0, 0, 0, 0)  # if you don't want any margins
        self.main_layout.setSpacing(3)  # margins between buttons
        self.main_widget.setLayout(self.main_layout)

        # * scroll area ----------------------------------------------- *#
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setMinimumHeight(400)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumWidth(290)
        self.scroll_area.setMaximumWidth(500)
        self.scroll_area.setFocusPolicy(QtCore.Qt.NoFocus)
        # self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

        self.scrollbar = QtWidgets.QScrollBar()
        self.scrollbar.setStyleSheet(scroll_style)
        self.scroll_area.setVerticalScrollBar(self.scrollbar)

        self.scroll_area_widget = QtWidgets.QWidget()
        self.scroll_area.setWidget(self.scroll_area_widget)

        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.scroll_layout.setAlignment(QtCore.Qt.AlignTop)
        self.scroll_layout.setContentsMargins(5, 0, 5, 0)
        self.scroll_layout.setSpacing(5)  # layout
        self.scroll_area_widget.setLayout(self.scroll_layout)

        self.main_layout.addWidget(self.scroll_area)
        # * -------------------------------------------------------------- *#

        # update button
        self.button_options = QtWidgets.QPushButton("Options")
        self.button_options.clicked.connect(self.openOptionsUI)
        self.main_layout.addWidget(self.button_options)

    def read_json(self):

        #clean up
        if self.scroll_layout.count():
            for i in range(self.scroll_layout.count()):
                item = self.scroll_layout.itemAt(i)
                widget = item.widget()
                widget.deleteLater()

        saved_json_data = []
        if os.path.isfile("D:/DragAndDrop.json"):
            with open("D:/" + "DragAndDrop.json", "r") as f:
                saved_json_data = json.load(f)

        #create buttons with right names with exec
        for i in saved_json_data:
            local_vars = {}
            exec("button = {0}(label = '{0}')".format(i), None, local_vars)
            button = local_vars['button']
            self.scroll_layout.addWidget(button)

    def on_button_options_clicked(self):
        self.my_ui.show()

    def openOptionsUI(self):
        if cmds.workspaceControl('MyCustomWidgetBunny', exists=True):
            cmds.deleteUI('MyCustomWidgetBunny', control=True)
            cmds.workspaceControlState('MyCustomWidgetBunny', remove=1)

        self.my_ui = MyDDWnd(class_list=GLOBAL_LIST)
        self.my_ui.MySignal.connect(self.read_json())
        self.my_ui.show()


class MyMIME(QtCore.QMimeData):
    """
    This class holds all the info that we need to transfer with a widget Drag
    """

    def __init__(self):
        super(MyMIME, self).__init__()
        self.someText = "none"
        self.fromWidget = None

    def set_text(self, text=None):
        self.someText = text

    def get_text(self):
        return self.someText


class ButtonWidget(QtWidgets.QWidget):
    """
    The button that we gonna Click | Drag | Drop
    When we click - our cursor carries MimeData that we need to feed with some custom info
    """

    def __init__(self, parent=None, label=""):
        super(ButtonWidget, self).__init__()

        self.setFixedSize(200, 40)

        # Background Color
        self.setAutoFillBackground(True)
        color = 80
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), QtGui.QColor(color, color, color))
        self.setPalette(self.p)

        # main layout
        self.tool_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.tool_layout)

        # label
        self.label = QtWidgets.QLabel(label)
        self.tool_layout.addWidget(self.label)

    def add_label(self, t=""):
        self.label.setText(t)  # for Drag and Drop

    def mousePressEvent(self, event):
        if event.buttons() != QtCore.Qt.LeftButton:
            return

        mimeData = MyMIME()  # create mimeData class | nothing too much happes here

        # Feed mimeData
        mimeData.set_text(self.label.text())

        # Create Ghosty image behind the moving mouse cursor
        self.pixmap = self.grab()
        painter = QtGui.QPainter(self.pixmap)
        painter.setCompositionMode(painter.CompositionMode_DestinationIn)
        painter.fillRect(self.pixmap.rect(), QtGui.QColor(80, 80, 80, 127))
        painter.end()

        # Here we create the actual Drag class that does Dragging
        drag = QtGui.QDrag(self)  # create Drag class to copy information between applications
        drag.setMimeData(mimeData)  # data to be sent with Drag
        drag.setPixmap(self.pixmap)  # set widget image
        drag.setHotSpot(event.pos())  #
        drag.exec_(QtCore.Qt.LinkAction | QtCore.Qt.MoveAction)  # starts the Drag and Drop operation

        """
        Qt::MoveAction          0x2  (2)    Move the data from the source to the target.
        Qt::LinkAction          0x4  (4)    Create a link from the source to the target.
        """
class Button1(ButtonWidget):
    def __init__(self, parent=None, label="TEST"):
        super(Button1, self).__init__(label=label)
    def mousePressEvent(self, event):
        print("ToolA")
        super(Button1,self).mousePressEvent(event)
class Button2(ButtonWidget):
    def __init__(self, parent=None, label="TEST"):
        super(Button2, self).__init__(label=label)
    def mousePressEvent(self, event):
        print("ToolA")
        super(Button2,self).mousePressEvent(event)
class Button3(ButtonWidget):
    def __init__(self, parent=None, label="TEST"):
        super(Button3, self).__init__(label=label)
    def mousePressEvent(self, event):
        print("ToolA")
        super(Button3,self).mousePressEvent(event)
class Button4(ButtonWidget):
    def __init__(self, parent=None, label="TEST"):
        super(Button4, self).__init__(label=label)
    def mousePressEvent(self, event):
        print("ToolA")
        super(Button4,self).mousePressEvent(event)
class FieldWidget(QtWidgets.QWidget):
    toolsSignal = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(FieldWidget, self).__init__()

        self.buttonsList = []

        # Some settings
        self.setFixedSize(240, 490)
        self.setAcceptDrops(True)  # this is important - we can now drop widgets here

        # Add background color
        self.setAutoFillBackground(True)
        color = 40
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), QtGui.QColor(color, color, color))
        self.setPalette(self.p)

        # Let's add main layout
        self.main_tools_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_tools_layout)

        # * scroll area
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setMinimumHeight(200)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setFocusPolicy(QtCore.Qt.NoFocus)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_area_widget = QtWidgets.QWidget()
        self.scrollArea.setWidget(self.scroll_area_widget)
        self.scroll_layout = QtWidgets.QGridLayout()
        self.scroll_layout.setAlignment(QtCore.Qt.AlignTop)
        self.scroll_layout.setContentsMargins(0, 0, 2, 0)
        self.scroll_layout.setSpacing(5)
        self.scroll_area_widget.setLayout(self.scroll_layout)  # * -> scroll_layout
        self.main_tools_layout.addWidget(self.scrollArea)

    def create_widget(self, label):
        button = ButtonWidget(label=label)
        self.scroll_layout.addWidget(button)

    '''DRAG & DROP'''

    def dragEnterEvent(self, e):
        # what happens when we start dragging our mouse
        # e - is QDragEnterEvent
        e.acceptProposedAction()  # accept dragEnter action

    def dropEvent(self, e):
        # pos = e.scenePos() #get position where we released mouse button
        mimeData = e.mimeData()  # get mime data from the cursor
        tool_mime_text = mimeData.get_text()
        self.toolsSignal.emit(tool_mime_text)
        # delete old widget
        e.source().deleteLater()

        # recreate button with Mime text and other data
        button = ButtonWidget()
        button.add_label(t=tool_mime_text)
        self.scroll_layout.addWidget(button)

        return tool_mime_text

    def dragMoveEvent(self, e):
        e.acceptProposedAction()

class MyDDWnd(MayaQWidgetBaseMixin, QtWidgets.QDialog):
    MySignal = QtCore.Signal(bool)
    def __init__(self, class_list = []):
        super(MyDDWnd, self).__init__()

        self.class_list = class_list

        self.json_data = {}
        self.json_path = json_path
        self.json_name = json_name

        self.setObjectName("myDragDropWnd_Ptr")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setFixedSize(500, 540)

        self.tool_layout = QtWidgets.QVBoxLayout()
        self.tool_layout.setSpacing(1)
        self.tool_layout.setContentsMargins(8, 8, 8, 8)
        self.setLayout(self.tool_layout)

        self.inner_tool_layout = QtWidgets.QHBoxLayout()
        self.tool_layout.addLayout(self.inner_tool_layout)

        self.first_list = FieldWidget()
        self.second_list = FieldWidget()

        self.inner_tool_layout.addWidget(self.first_list)
        self.inner_tool_layout.addWidget(self.second_list)

        # save json button
        self.button_save = QtWidgets.QPushButton("Save options")
        self.button_save.clicked.connect(self.save_to_json)
        self.tool_layout.addWidget(self.button_save)

        self.read_json()

    def read_json(self):
        saved_json_data = []
        if os.path.isfile("D:/DragAndDrop.json"):
            with open("D:/" + "DragAndDrop.json", "r") as f:
                saved_json_data = json.load(f)

        for i in self.class_list:
            if i in saved_json_data:
                self.second_list.create_widget(label=i)
            else:
                self.first_list.create_widget(label=i)

    def save_to_json(self):
        self.json_data = []
        self.MySignal.emit(True)
        if self.second_list.scroll_layout.count():
            for i in range(self.second_list.scroll_layout.count()):
                item = self.second_list.scroll_layout.itemAt(i)
                widget = item.widget()
                label = widget.label.text()
                self.json_data.append(label)
                self.write_json(path=self.json_path, name=self.json_name)
                print("JSON was saved")

    def write_json(self, path, name):
        # file_path = os.path.join(path, name)
        with open("D:/" + "DragAndDrop.json", 'w') as f:
            f.write(json.dumps(self.json_data, indent=4, sort_keys=True))



def main():
    if cmds.workspaceControl('MyCustomWidgetBunnyWorkspaceControl', exists=True):
        cmds.deleteUI('MyCustomWidgetBunnyWorkspaceControl', control=True)
        cmds.workspaceControlState('MyCustomWidgetBunnyWorkspaceControl', remove=1)

    my_ui = MyCustomWidget(json_path, json_name)
    my_ui.show(dockable=True, area='right', allowedArea='right', floating=True)

    cmds.workspaceControl('MyCustomWidgetBunnyWorkspaceControl',
                          label='WidgetBunny',
                          edit=1,
                          r=1,  # raise to the top and make it active
                          tabToControl=["AttributeEditor", -1],
                          floating=False,
                          initialWidth=300,
                          minimumWidth=300,
                          widthProperty="preferred")


main()
