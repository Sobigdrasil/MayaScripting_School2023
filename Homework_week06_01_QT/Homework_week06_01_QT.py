import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore, QtGui

class BunnyWindow(QtWidgets.QDialog):

    def __init__(self):
        #creates window for a work with simple objects
        super(BunnyWindow, self).__init__()  # super is important to call the main class

        # calling functions for a window creation
        self.setup_ui() #main window and layouts
        self.object_name_window() #text window for object naming
        self.radio_buttons() #buttons for object creation
        self.scale_slider_complete() #slider for object scaling
        self.checkboxes() #put object on a layer or in a group
        self.push_buttons() #main buttons: ok, apply, cancel

    def setup_ui(self):
        '''
        create a main window and all the layouts
        :return: self.main_layout, self.radio_buttons_layout, self.slider_layout,
                 self.slider_layout, self.checkbox_layout, self.buttons_layout
        '''
        # create a name for the window
        self.setWindowTitle("_*Super Mega Poly Objects*_")
        self.setStyleSheet("BunnyWindow {background: rgb(75, 72, 101)}")
        # for borders you can use this ->
        #self.setStyleSheet("BunnyWindow {border: 3px solid rgb(150, 150, 45)}")

        # set size of the window
        self.setMinimumSize(250, 100)
        self.setMaximumSize(700, 200)
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
        '''
        creating a window for an object name
        :return: self.object_name
        '''
        self.object_name = QtWidgets.QLineEdit("ObjectName")
        self.name_layout.addWidget(self.object_name) #adding window on a layout
        self.object_name.textChanged.connect(lambda x: self.object_name.displayText()) #ability to change text

        self.object_name.setStyleSheet(
            "QLineEdit { background-color: rgb(43, 41, 57); color: rgb(128, 123, 171) }")

    def radio_buttons(self):
        '''
        radio buttons for objects creation
        :return: self.button_group_1, self.r_buttons_sphere, self.r_buttons_cube, self.r_buttons_cone
        '''
        # let's create radio buttons
        self.button_group_1 = QtWidgets.QButtonGroup()

        self.r_buttons_sphere = QtWidgets.QRadioButton("Sphere")
        self.r_buttons_sphere.setChecked(True)  # this button is checked when you open the window
        self.r_buttons_cube = QtWidgets.QRadioButton("Cube")
        self.r_buttons_cone = QtWidgets.QRadioButton("Cone")

        # setting colors for QRadiobuttons through variable
        radio_battons_style = """
            QRadioButton::indicator {
                width: 14px;
                height: 14px;
                border-radius: 7px;
                background-color: rgb(43, 41, 57);
            }
            QRadioButton::indicator:checked {
                background-color: rgb(189, 183, 255);
            }
            QRadioButton {color: rgb(189, 183, 255)}
        """
        self.r_buttons_sphere.setStyleSheet(radio_battons_style)
        self.r_buttons_cube.setStyleSheet(radio_battons_style)
        self.r_buttons_cone.setStyleSheet(radio_battons_style)

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
        :return: self.scale_slider, self.scale_numbers
        '''
        self.scale_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.scale_numbers= QtWidgets.QLineEdit()

        self.scale_slider.setStyleSheet(
            "QSlider { add-page:vertical; background: rgb(43, 41, 57); color: rgb(128, 123, 171); height: 10px}")
        self.scale_numbers.setStyleSheet(
            "QLineEdit { background-color: rgb(43, 41, 57); color: rgb(128, 123, 171) }")

        self.scale_numbers.setFixedWidth(60)  # Set the width to 150 pixels
        self.scale_numbers.setFixedHeight(30)  # Set the height to 30 pixels
        self.scale_numbers.setReadOnly(True)  # Make the QLineEdit non-editable

        self.slider_layout.addWidget(self.scale_slider)
        self.slider_layout.addWidget(self.scale_numbers)

        self.scale_slider.setRange(0, 999)

        self.scale_numbers.setPlaceholderText("scale")
        self.scale_numbers.setMaxLength(2)

        # Connect the valueChanged signal of the slider to the update_line_edit slot
        self.scale_slider.valueChanged.connect(self.update_line_edit)

    def update_line_edit(self, value):
        '''
        Update the line edit text when the slider value changes, uses in self.scale_slider_complete()
        :param value:
        :return: self.scale_value
        '''
        self.scale_numbers.setText(str(value))
        self.scale_value = value / 10

    def checkboxes(self):
        '''
        creating checkboxes for creating a layer and a group
        :return: self.checkbox_layer, self.checkbox_group
        '''
        self.checkbox_layer = QtWidgets.QCheckBox("add on layer")
        self.checkbox_group = QtWidgets.QCheckBox("add in group")

        #variable that we use for unchecked style for checkboxes
        status_unchecked = """
            QCheckBox::indicator {
                background-color: rgb(43, 41, 57);
            }
            QCheckBox {color: rgb(189, 183, 255)}
        """
        # setting color and style for checkboxes
        self.checkbox_layer.setStyleSheet(status_unchecked)
        self.checkbox_group.setStyleSheet(status_unchecked)

        #assign the style when the checkbox is checked
        self.checkbox_layer.stateChanged.connect(self.update_checkbox_state)
        self.checkbox_group.stateChanged.connect(self.update_checkbox_state)

        # adding created checkboxes on a layer
        self.checkbox_layout.addWidget(self.checkbox_layer)
        self.checkbox_layout.addWidget(self.checkbox_group)

    def update_checkbox_state(self):
        '''
        Update the checkbox appearance when the state changes
        :return:
        '''
        #variable that we use for checked style for checkboxes
        status_checked = """
            QCheckBox::indicator {
                background-color: rgb(43, 41, 57);
            }
            QCheckBox::indicator:checked {
                background-color: rgb(189, 183, 255);
                image: url(D:/tick_ui.png); /* image is 19px */
            }
            QCheckBox {color: rgb(189, 183, 255)}
        """
        self.checkbox_layer.setStyleSheet(status_checked)
        self.checkbox_group.setStyleSheet(status_checked)

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
        :return: new_name
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

        # slider scale
        cmds.scale(self.scale_value, self.scale_value, self.scale_value)

        # checkbox for a layer
        if self.checkbox_layer.isChecked():
            cmds.createDisplayLayer(name=new_name)

        # checkbox for a group
        if self.checkbox_group.isChecked():
            cmds.group(name=new_name + "_group")


# remove window of the script if it exists in maya
if cmds.window("BunnyWindow", query=True, exists=True):
    cmds.deleteUI("BunnyWindow")

if cmds.windowPref("BunnyWindow", exists=True):
    cmds.windowPref("BunnyWindow", remove=True)

a = BunnyWindow()
a.show()
