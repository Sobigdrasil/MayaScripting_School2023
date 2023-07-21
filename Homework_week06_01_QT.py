import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore, QtGui


class BunnyWindow(QtWidgets.QDialog):

    def __init__(self):

        super(BunnyWindow, self).__init__()  # super is important to call the main class

        # calling functions for a window creation
        self.setup_ui()
        self.object_name_window()
        self.radio_buttons()
        self.scale_slider_complete()
        self.push_buttons()
        self.checkboxes()

    def setup_ui(self):
        # create a name for the window
        self.setWindowTitle("_*Super Mega Poly Objects*_")
        self.setStyleSheet("BunnyWindow {background: rgb(75, 72, 101)}")
        # self.setStyleSheet("BunnyWindowQtGui.QColor(255, 0, 0, 127)")
        # for borders you can use this ->
        # self.setStyleSheet("BunnyWindow {border: 3px solid rgb(150, 150, 45)}")

        # set size of the window
        self.setMinimumSize(500, 200)
        self.setMaximumSize(700, 500)
        self.resize(500, 200)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # window stays always on top

        # setting a layout for the main window
        self.main_layout = QtWidgets.QVBoxLayout()  # vertical layout
        self.main_layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.main_layout)

        # create and add horizontal(H) layout for the radio buttons
        self.name_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.name_layout)

        # create and add horizontal(H) layout for the radio buttons
        self.radio_buttons_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.radio_buttons_layout)

        # create slider layout
        self.slider_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.slider_layout)

        # create checkbox layout
        self.checkbox_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.checkbox_layout)

        # create and add horizontal(H) layout for the buttons
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.buttons_layout)

    def object_name_window(self):
        self.object_name = QtWidgets.QLineEdit("ObjectName")
        self.name_layout.addWidget(self.object_name)
        self.object_name.textChanged.connect(lambda x: self.object_name.displayText())

    def radio_buttons(self):
        # let's create radio buttons
        self.button_group_1 = QtWidgets.QButtonGroup()

        self.r_buttons_sphere = QtWidgets.QRadioButton("Sphere")
        self.r_buttons_sphere.setChecked(True)  # this button is checked when you open the window
        self.r_buttons_cube = QtWidgets.QRadioButton("Cube")
        self.r_buttons_cone = QtWidgets.QRadioButton("Cone")

        # setting colors for QRadiobuttons
        self.r_buttons_sphere.setStyleSheet("QRadioButton {color: rgb(189, 183, 255)}")
        self.r_buttons_cube.setStyleSheet("QRadioButton {color: rgb(189, 183, 255)}")
        self.r_buttons_cone.setStyleSheet("QRadioButton {color: rgb(189, 183, 255)}")

        self.button_group_1.addButton(self.r_buttons_sphere)
        self.button_group_1.addButton(self.r_buttons_cube)
        self.button_group_1.addButton(self.r_buttons_cone)

        # let's add radio buttons in the layout
        self.radio_buttons_layout.addWidget(self.r_buttons_sphere)
        self.radio_buttons_layout.addWidget(self.r_buttons_cube)
        self.radio_buttons_layout.addWidget(self.r_buttons_cone)

    def scale_slider_complete(self):
        '''
        creates slider that scales your mesh
        :return:
        '''
        self.scale_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.scale_numbers = QtWidgets.QLineEdit()

        self.scale_numbers.setFixedWidth(50) # Set the width to 150 pixels
        self.scale_numbers.setFixedHeight(30) # Set the height to 30 pixels

        self.slider_layout.addWidget(self.scale_slider)
        self.slider_layout.addWidget(self.scale_numbers)

        self.scale_slider.setRange(0, 999)

        self.scale_numbers.setPlaceholderText("scale")
        self.scale_numbers.setMaxLength(3)

        # When user tweaks using the slider
        self.scale_slider.valueChanged[int].connect(self.update_scale_numbers)
        # When user modify via the line edit
        self.scale_numbers.editingFinished.connect(self.update_slider)

        # Functions for each modification made towards slider and line edit

    def update_slider(self, value):
        # spinbox_value uses float/ doubles type
        # '*100' is used to convert it into integer as QSlider
        # only register integer type
        self.scale_numbers.value() * 100
        self.scale_slider.setSliderPosition(self.scale_numbers)
        print(value)

    def update_scale_numbers(self, value):
        # QSlider only uses integer type
        # Need to convert the value from integer into float
        # and divides it by 100
        self.scale_numbers.value = (float(value) / 100)
        print(value)

    def checkboxes(self):
        '''
        creating checkboxes for creating a layer and a group
        :return: self.checkbox_layer, self.checkbox_group
        '''
        self.checkbox_layer = QtWidgets.QCheckBox("add on layer")
        self.checkbox_group = QtWidgets.QCheckBox("add in group")

        # setting color for checkboxes
        self.checkbox_layer.setStyleSheet("QCheckBox {color: rgb(189, 183, 255)}")
        self.checkbox_group.setStyleSheet("QCheckBox {color: rgb(189, 183, 255)}")

        # adding created checkboxes on a layer
        self.checkbox_layout.addWidget(self.checkbox_layer)
        self.checkbox_layout.addWidget(self.checkbox_group)

    def push_buttons(self):
        '''
        creating push buttons for OK APLLY and CLOSE
        :return: self.button_ok, self.button_apply, self.button_cancel
        '''
        # let's create buttons
        self.button_ok = QtWidgets.QPushButton("OK")
        self.button_ok.clicked.connect(self.on_button_ok_clicked)  # to make button clickable
        # color for background and text it also appears the same on the lines 155 and 160
        self.button_ok.setStyleSheet(
            "QPushButton { background-color: rgb(43, 41, 57); color: rgb(128, 123, 171) }")

        self.button_apply = QtWidgets.QPushButton("Apply")
        self.button_apply.clicked.connect(self.on_button_apply_clicked)  # to make button clickable
        self.button_apply.setStyleSheet(
            "QPushButton { background-color: rgb(43, 41, 57); color: rgb(128, 123, 171) }")

        self.button_cancel = QtWidgets.QPushButton("Cancel")
        self.button_cancel.clicked.connect(self.close)  # connecting button to function close
        self.button_cancel.setStyleSheet(
            "QPushButton { background-color: rgb(43, 41, 57); color: rgb(128, 123, 171) }")

        # let's add buttons in the layout
        self.buttons_layout.addWidget(self.button_ok)
        self.buttons_layout.addWidget(self.button_apply)
        self.buttons_layout.addWidget(self.button_cancel)

    def on_button_ok_clicked(self):
        '''
        function that works on the moment when OK button clicked
        it creates the stuff you asked for, and close the window
        :return:
        '''
        # if radio button is checked then create a mesh and close the window
        self.on_button_apply_clicked()
        self.close()  # closing the window

    def on_button_apply_clicked(self):
        '''
        function that works on the APPLY button clicked
        it creates the stuff you asked for, that's it
        :return:
        '''
        # set the name for the object
        new_name = self.object_name.displayText()
        # replacing space with a "_"
        new_name = new_name.replace(' ', '_')
        if not new_name:
            return cmds.error("Type the new name")
        # if name is numbers
        if new_name.isdigit():
            return cmds.error("You can't use numbers, use letters")
        # if name starts with numbers
        if new_name[0].isdigit():
            return cmds.error("You can't use numbers, use letters")

        # if radio button is checked then create a mesh
        if self.r_buttons_sphere.isChecked():
            cmds.polySphere(name=new_name)
        elif self.r_buttons_cube.isChecked():
            cmds.polyCube(name=new_name)
        elif self.r_buttons_cone.isChecked():
            cmds.polyCone(name=new_name)

        #slider scale


        # checkbox for a layer
        if self.checkbox_layer.isChecked():
            cmds.createDisplayLayer(name=new_name)

        # checkbox for a group
        if self.checkbox_group.isChecked():
            cmds.group(name=new_name + "_group")


# remove window of the script if it exists
if cmds.window("BunnyWindow", query=True, exists=True):
    cmds.deleteUI("BunnyWindow")

if cmds.windowPref("BunnyWindow", exists=True):
    cmds.windowPref("BunnyWindow", remove=True)

a = BunnyWindow()
a.show()
