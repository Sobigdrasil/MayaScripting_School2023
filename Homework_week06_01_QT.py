import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore, QtGui

class BunnyWindow(QtWidgets.QDialog):

    def __init__(self):

        super(BunnyWindow, self).__init__() #super is important to call the main class

        #calling functions for a window creation
        self.delete_window()
        self.setup_ui()
        self.object_name_window()
        self.radio_buttons()
        self.scale_slider()
        self.push_buttons()

    def delete_window(self):
        # remove window of the script if it exists
        if cmds.window("BunnyWindow", query=True, exists=True):
            cmds.deleteUI("BunnyWindow")

        if cmds.windowPref("BunnyWindow", exists=True):
            cmds.windowPref("BunnyWindow", remove=True)

    def setup_ui(self):
        # create a name for the window
        self.setWindowTitle("_*Super Mega Poly Objects*_")
        # set size of the window
        self.setMinimumSize(300, 200)
        self.setMaximumSize(700, 500)
        self.resize(300, 200)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # window stays always on top

        # setting a layout for the main window
        self.main_layout = QtWidgets.QVBoxLayout()  # vertical layout
        self.main_layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.main_layout)

        # create and add horizontal(H) layout for the radio buttons
        self.radio_buttons_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.radio_buttons_layout)

        #create slider layout
        self.slider_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.slider_layout)

        # create and add horizontal(H) layout for the buttons
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.buttons_layout)

    def object_name_window(self):
        pass

    def radio_buttons(self):
        # let's create radio buttons
        self.button_group_1 = QtWidgets.QButtonGroup()

        self.r_buttons_sphere = QtWidgets.QRadioButton("Sphere")
        self.r_buttons_sphere.setChecked(True)  # this button is checked when you open the window
        self.r_buttons_cube = QtWidgets.QRadioButton("Cube")
        self.r_buttons_cone = QtWidgets.QRadioButton("Cone")

        self.button_group_1.addButton(self.r_buttons_sphere)
        self.button_group_1.addButton(self.r_buttons_cube)
        self.button_group_1.addButton(self.r_buttons_cone)

        # let's add radio buttons in the layout
        self.radio_buttons_layout.addWidget(self.r_buttons_sphere)
        self.radio_buttons_layout.addWidget(self.r_buttons_cube)
        self.radio_buttons_layout.addWidget(self.r_buttons_cone)

    def scale_slider(self):
        self.scale_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.scale_numbers = QtWidgets.QLineEdit()

        self.slider_layout.addWidget(self.scale_slider)
        self.slider_layout.addWidget(self.scale_numbers)

        self.scale_slider.setRange(0, 999)

        self.scale_numbers.setPlaceholderText("scale")
        self.scale_numbers.setMaxLength(3)


    def push_buttons(self):
        # let's create buttons
        self.button_ok = QtWidgets.QPushButton("OK")
        self.button_ok.clicked.connect(self.on_button_ok_clicked)  # to make button clickable

        self.button_apply = QtWidgets.QPushButton("Apply")
        self.button_apply.clicked.connect(self.on_button_apply_clicked)  # to make button clickable

        self.button_cancel = QtWidgets.QPushButton("Cancel")
        self.button_cancel.clicked.connect(self.close)  # conncecting button to function close

        # let's add buttons in the layout
        self.buttons_layout.addWidget(self.button_ok)
        self.buttons_layout.addWidget(self.button_apply)
        self.buttons_layout.addWidget(self.button_cancel)

    def on_button_ok_clicked(self):
        #if radio button is checked then create a mesh and close the window
        self.on_button_apply_clicked()
        self.close() #closing the window

    def on_button_apply_clicked(self):
        # if radio button is checked then create a mesh
        if self.r_buttons_sphere.isChecked():
            cmds.polySphere()
        elif self.r_buttons_cube.isChecked():
            cmds.polyCube()
        elif self.r_buttons_cone.isChecked():
            cmds.polyCone()


a = BunnyWindow()
a.show()