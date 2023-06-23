import maya.cmds as cmds
import json

pose_name = "Pose_1"
pose_path = "D:/pose_folder"
json_data_open = {}

def read_json(path, name):
    """
    read json for a pose that was created in the save_pose file
    :param path:
    :param name:
    :return:
    """
    with open(pose_path + "/" + pose_name + ".json", 'r')as f:
        json_data_open = json.load(f)
    return json_data_open
def get_all_controls():
    '''
    Get all control curves from a given rig
    :param rig: rig_name
    :return: list of control curves
    '''
    selected_ctrls = cmds.ls(sl=1, l=0)
    if selected_ctrls:
        controls = []
        for i in selected_ctrls:
            controls.append(i)
            json_data_open[i] = {}
    else:
        cmds.error("please select controls")
    return controls

def p_transfer_open():
    '''
    Opening the transformations of the animation in a json file
    :param rig_name:
    :return:
    '''
    json_data_open = read_json(path = pose_path, name = pose_name)
    controls = get_all_controls()
    for ctrl in controls:
        keyed_channels = json_data_open[ctrl]
        for k_ch in keyed_channels:
            cmds.setAttr(ctrl + "." + k_ch, keyed_channels[k_ch])


p_transfer_open()

cmds.setKeyframe()