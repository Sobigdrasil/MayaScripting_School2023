import maya.cmds as cmds
import os
import json

json_data = {}
pose_name = "Pose_1"
pose_path = "D:/pose_folder"

def create_folder(json_file_path):
    """
    create a folder for the future pose
    """
    #create a folder if it does not exist yet
    if not os.path.exists(json_file_path):
        os.makedirs(json_file_path)
        print("Folder created:", json_file_path)
    else:
        print("Folder already exists:", json_file_path)
    return json_file_path

create_folder("D:/pose_folder")

def get_all_controls():
    """
    Get all control curves from a given rig
    :param rig: rig_name
    :return: list of control curves
    """
    selected_ctrls = cmds.ls(sl=1, l=0)
    if selected_ctrls:
        controls = []
        for i in selected_ctrls:
            controls.append(i)
            json_data[i] = {}
    else:
        cmds.error("please select controls")
    return controls

    #THE OTHER WAY how to select controls that didn't work out
    # don't forget to put (rig = "name of the rig from outliner") in function

    #children = cmds.listRelatives(rig, children=True, fullPath=True, allDescendents=True)
    #controls = []
    #for i in children:
    #    if cmds.nodeType(i) == "nurbsCurve":
    #        transform = cmds.listRelatives(i, parent=True, fullPath=True)[0]
    #        #add transform node to the list
    #        controls.append(transform)
    #return controls

def write_json(name=pose_name):
    """
    Write the pose data to a JSON file
    :param name:
    :return:
    """
    with open("D:/pose_folder" + "/" + name + ".json", 'w') as f:
        f.write(json.dumps(json_data, indent=4, sort_keys=True))
def p_transfer_save():
    """
    Saving the transformations of the pose in a json file
    :param rig_name:
    :return:
    """
    controls = get_all_controls()

    #go through all the selected controls and save the attributes
    for ctrl in controls:
        json_data[ctrl] = {}
        keys = cmds.listAttr(ctrl, keyable=True)
        if keys:
            for ch in keys:
                json_data[ctrl][ch] = cmds.getAttr(ctrl + "." + ch)
        else:
            continue

    write_json()

p_transfer_save()