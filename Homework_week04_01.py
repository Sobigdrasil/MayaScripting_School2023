import maya.cmds as cmds

def apply_expression(create_sphere, create_cube, create_cone, create_cylinder, create_torus, create_plane):
    '''
    function that work when you press _apply_ button in maya UI
    '''
    # create a name and assign it to the mesh

    # dict for a name of 1st selected object
    first_object_name = {}
    selected_object = cmds.ls(selection=True)
    if selected_object:
        first_object_name['name'] = selected_object[0]

    #creating name for name UI
    new_name = cmds.textField("namer", query=True, text=True)
    cmds.textField("namer", edit=True, text="")

    # create a mesh based on the radio button that you chose
    if cmds.radioButton(create_sphere, query=True, select=True):
        cmds.polySphere(name=new_name)
    elif cmds.radioButton(create_cube, query=True, select=True):
        cmds.polyCube(name=new_name)
    elif cmds.radioButton(create_cone, query=True, select=True):
        cmds.polyCone(name=new_name)
    elif cmds.radioButton(create_cylinder, query=True, select=True):
        cmds.polyCylinder(name=new_name)
    elif cmds.radioButton(create_torus, query=True, select=True):
        cmds.polyTorus(name=new_name)
    elif cmds.radioButton(create_plane, query=True, select=True):
        cmds.polyPlane(name=new_name)

    # scale the object
    slider_value_scale = cmds.intSliderGrp("scale_slider", query=True, value=True)
    cmds.scale(slider_value_scale, slider_value_scale, slider_value_scale)

    # put into a group
    group_box = cmds.checkBox("group", query=True, value=True)
    if group_box:
        cmds.group(name=new_name + "_group")

    # or constrain to a chosen control without maintaining offset
    constrain_box = cmds.checkBox("constrain", query=True, value=True)
    if constrain_box:
        if cmds.checkBox("group", query=True, value=True):
            cmds.parentConstraint(first_object_name['name'], new_name + "_group", maintainOffset=False)
        else:
            cmds.parentConstraint(first_object_name['name'], new_name, maintainOffset=False)

    # or create on a separate layer
    layer_box = cmds.checkBox("layer", query=True, value=True)
    if layer_box:
        cmds.createDisplayLayer(name=new_name)

    # create shader node if it doesn't exist
    shader_name = "lambertPink"
    if not cmds.objExists(shader_name):
        shader = cmds.shadingNode("lambert", n="lambertPink", asShader=1)

        # set color attribute - now shader has "pink" color
        cmds.setAttr(shader + ".color", 1, 0.5, 0.6, type="double3")

        # select object and assign shader to it
        cmds.select(new_name)
        cmds.hyperShade(assign=shader)
    else:
        cmds.select(new_name)
        cmds.hyperShade(assign=shader_name)

    # change transparency for the object
    slider_value_trans = cmds.floatSliderGrp("transparency_slider", query=True, value=True)
    cmds.setAttr('lambertPink.transparency',  slider_value_trans, slider_value_trans, slider_value_trans,
                 type="double3")

    cmds.select(deselect=True)

def clean_space():
    '''
    removing all existing UI for this script
    :return:
    '''
    if cmds.window("BunnyObjectCreatorID", exists=True):
        cmds.deleteUI("BunnyObjectCreatorID")

    if cmds.windowPref("BunnyObjectCreatorID", exists=True):
        cmds.windowPref("BunnyObjectCreatorID", remove=True)


def create_window():
    '''
    Creating a main window for a script with all the buttons, sliders etc.
    '''

    cmds.window("BunnyObjectCreatorID", title="_*simple_objects*_", width=270, tlb=True)
    main_layout = cmds.columnLayout(adjustableColumn=True,
                                    backgroundColor=[1, 0.5, 0.6], rowSpacing=12)

    #layout for a name line
    expression_layout = cmds.columnLayout(adjustableColumn=True,
                                          columnAlign="left",
                                          columnOffset=["both", 10],
                                          rowSpacing=5,
                                          statusBarMessage="Use * as an original object name",
                                          parent=main_layout)
    #name UI
    cmds.text("name:", font="fixedWidthFont")
    cmds.textField("namer", backgroundColor=[0.9, 0.8, 0.8], placeholderText="name your simple object(*'__'*)",
                   font="fixedWidthFont", parent=expression_layout)

    #layout for circle buttons, first line
    radio_layout_1 = cmds.rowLayout(numberOfColumns=3, columnWidth3=(90, 90, 90), adjustableColumn=True,
                                    columnAttach=[(1, 'left', 15), (2, 'both', 20), (3, 'right', 15)],
                                    parent=main_layout)
    #to collect radio buttons
    radio_button_group = cmds.radioCollection()
    #objects creation UI
    create_sphere = cmds.radioButton(label='sphere', parent=radio_layout_1, select=True)
    create_cube = cmds.radioButton(label='cube', parent=radio_layout_1, select=True)
    create_cone = cmds.radioButton(label='cone', parent=radio_layout_1, select=True)

    #layout for circle buttons, second line
    radio_layout_2 = cmds.rowLayout(numberOfColumns=3, columnWidth3=(90, 90, 90), adjustableColumn=True,
                                    columnAttach=[(1, 'left', 15), (2, 'both', 20), (3, 'right', 15)],
                                    parent=main_layout)
    # objects creation UI
    create_cylinder = cmds.radioButton(label='cylinder', parent=radio_layout_2, select=True)
    create_torus = cmds.radioButton(label='torus', parent=radio_layout_2, select=True)
    create_plane = cmds.radioButton(label='plane', parent=radio_layout_2, select=True)
    #if radio button was chosen
    cmds.radioCollection(radio_button_group, q=1, sl=True)

    # layout for scaling UI
    scale_layout = cmds.rowLayout(numberOfColumns=1, columnWidth1=20, adjustableColumn=True,
                                   columnAttach=[(1, 'both', 0)],
                                   parent=main_layout)
    # scale UI
    cmds.intSliderGrp("scale_slider", label='scale', field=True, min=1, max=100, value=1,
                      changeCommand=lambda y: cmds.scale(), width=40, cw3=(30, 30, 30),
                      columnAttach=[(1, 'right', 0), (2, 'both', 0), (3, 'right', 10)],
                      parent=scale_layout)

    # layout for transparency UI
    transparency_layout = cmds.rowLayout(numberOfColumns=1, columnWidth1=20, adjustableColumn=True,
                                   columnAttach=[(1, 'both', 0)],
                                   parent=main_layout)
    # transparency UI
    cmds.floatSliderGrp("transparency_slider", label='transparent', field=True, min=0, max=1, value=0,
                      width=40, cw3=(60, 30, 0),
                      columnAttach=[(1, 'right', 0), (2, 'both', 0), (3, 'right', 10)],
                       parent=transparency_layout)

    #layout for group,constrain and layer commands
    check_box_layout = cmds.columnLayout(adjustableColumn=True,
                                         columnAlign="left",
                                         columnOffset=["both", 10],
                                         rowSpacing=5,
                                         statusBarMessage="Use * as an original object name",
                                         parent=main_layout)
    #check boxes for group, constrain and layer
    cmds.checkBox("group", label="put into a group", parent=check_box_layout)
    cmds.checkBox("constrain", label="attach to selected object", parent=check_box_layout)
    cmds.checkBox("layer", label="create on a layer", parent=check_box_layout)

    # horizontal layout for buttons
    buttons_l = cmds.columnLayout(parent=main_layout, rowSpacing=3, adjustableColumn=True)
    #execution UI
    cmds.button(label="Apply", parent=buttons_l,
                command=lambda x: apply_expression(create_sphere, create_cube, create_cone, create_cylinder,
                                                   create_torus, create_plane),
                backgroundColor=[0.9, 0.8, 0.8])
    cmds.button(label="Cancel", parent=buttons_l, command="cmds.deleteUI(\'BunnyObjectCreatorID\')",
                backgroundColor=[0.9, 0.8, 0.8])

    # create window
    cmds.showWindow("BunnyObjectCreatorID")


def main():
    '''
    program execution
    '''
    clean_space()
    create_window()


main()
