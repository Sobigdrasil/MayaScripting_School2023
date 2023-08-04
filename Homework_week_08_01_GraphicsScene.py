import os
import json
from PySide2 import QtWidgets, QtGui, QtCore
import maya.cmds as cmds
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

json_path = "D:/"
json_name = "DragAndDrop.json"

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

        self.setDockableParameters(width = 200)
        self.setFloating(False)

        self.json_data = {}
        self.json_path = json_path
        self.json_name = json_name

        self.setup_ui()

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
        self.button_options.clicked.connect(self.on_button_options_clicked)
        self.main_layout.addWidget(self.button_options)

        if os.path.exists(self.json_path + self.json_name):
            self.json_data = self.read_json()
            for i in self.json_data["w2"]:
                widget = MyDDWnd(i)
                self.scroll_layout.addWidget(widget)

    def on_button_options_clicked(self):
        myDragDropWnd.show()

    def read_json(self):
        with open("D:/" + "DragAndDrop.json", "r") as f:
            saved_json_data = json.load(f)
        return saved_json_data


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

    def __init__(self, parent=None, label="TEST"):
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


class FieldWidget(QtWidgets.QWidget):

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

    def feed_buttons(self):
        # We will create Drag&Drop buttons here

        for i in range(5):
            self.button = ButtonWidget()
            self.button.add_label(t="Button {}".format(i))
            self.buttonsList.append(self.button)
            self.scroll_layout.addWidget(self.button)

    # def get_label_text(self):
    #     return self.add_label

    '''DRAG & DROP'''

    def dragEnterEvent(self, e):
        # what happens when we start dragging our mouse
        # e - is QDragEnterEvent
        e.acceptProposedAction()  # accept dragEnter action

    def dropEvent(self, e):
        # pos = e.scenePos() #get position where we released mouse button
        mimeData = e.mimeData()  # get mime data from the cursor
        tool_mime_text = mimeData.get_text()
        # mimeFrom = mimeData.getFrom()
        # print (e.source, self)
        e.source().deleteLater()

        # recreate button with Mime text and other data
        button = ButtonWidget()
        button.add_label(t=tool_mime_text)
        self.scroll_layout.addWidget(button)

        # push a signal saying we should delete widget which is no longer in use
        self.toolsFiledSignal.emit(tool_mime_text)
        # delete old widget
        e.source().deleteLater()

        new_tool = FieldWidget()
        self.scroll_layout.addWidget(new_tool)
        return tool_mime_text

    def dragMoveEvent(self, e):
        e.acceptProposedAction()

    def get_button_state(self):
        button_states = []
        for button in self.buttonsList:
            label_text = button.label.text()
            button_info = {"label": label_text}
            button_states.append(button_info)

        return button_states



class MyDDWnd(MayaQWidgetBaseMixin, QtWidgets.QDialog):

    def __init__(self):
        super(MyDDWnd, self).__init__()

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

        self.w1 = FieldWidget()
        self.w1.feed_buttons()  # add Drag&Drop buttons to the first field

        self.w2 = FieldWidget()

        self.inner_tool_layout.addWidget(self.w1)
        self.inner_tool_layout.addWidget(self.w2)
        
        # save json button
        self.button_save = QtWidgets.QPushButton("Save options")
        self.button_save.clicked.connect(self.save_to_json)
        self.tool_layout.addWidget(self.button_save)

    def save_to_json(self):
        self.json_data["w1"] = self.w1.get_button_state()
        self.json_data["w2"] = self.w2.get_button_state()
        self.write_json(path = self.json_path, name = self.json_name)
        print("JSON was saved")

    def write_json(self, path, name):
        # file_path = os.path.join(path, name)
        with open("D:/" + "DragAndDrop.json", 'w') as f:
            f.write(json.dumps(self.json_data, indent=4, sort_keys=True))

def main():

    if cmds.workspaceControl('MyCustomWidgetBunnyWorkspaceControl', exists=True):
        cmds.deleteUI('MyCustomWidgetBunnyWorkspaceControl', control=True)
        cmds.workspaceControlState('MyCustomWidgetBunnyWorkspaceControl', remove=1)

    global my_ui
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

myDragDropWnd = MyDDWnd()
main()