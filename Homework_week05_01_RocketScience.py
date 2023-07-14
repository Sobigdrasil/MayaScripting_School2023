import maya.cmds as cmds


class Rocket(object):

    def __init__(self, body_nose_radius=2, body_parts=1, nose_height=1, fuel_tank_radius=1):
        self.body_parts = body_parts
        self.nose_height = nose_height
        self.fuel_tank_radius = fuel_tank_radius
        self.body_nose_radius = body_nose_radius

        self.create_nose()
        self.create_body()
        self.create_fuel_tanks()

    def create_nose(self):
        '''
        Create a nose of aspace rocket
        :return:
        '''
        #creating a nose
        rocket_nose = cmds.polyCone(name="Nose")

        # separating the name from a node to use it further
        self.rocket_nose_node = rocket_nose[1]
        self.rocket_nose_name = rocket_nose[0]

        #setting radius and height properly and moving up
        cmds.setAttr(self.rocket_nose_node + ".radius", self.body_nose_radius)
        cmds.setAttr(self.rocket_nose_node + ".height", self.nose_height)
        cmds.xform(self.rocket_nose_name, translation=[0, 16, 0], relative=True)

    def create_body(self):
        '''
        Create a body of a space rocket
        :return:
        '''
        rocket_body = cmds.polyCylinder(name="Body")

        self.bb_nose = cmds.xform(self.rocket_nose_name, query=True, boundingBox=True, worldSpace=True)
        # we are calculating bounding box for a nose
        # where [X_min, Y_min, Z_min, X_max, Y_max, Z_max]
        bb_body = cmds.xform(rocket_body, query=True, boundingBox=True, worldSpace=True)
        bb_center_point_n = (bb_body[1] - bb_body[4]) / 2

        bottom = self.bb_nose[1]
        offset = bottom + bb_center_point_n
        cmds.xform(rocket_body, translation=[0, offset, 0], relative=True)

        # we need full name which we could check with print() command. It's ['pCube1', 'polyCube1']
        self.rocket_body_node = rocket_body[1]
        self.rocket_body_name = rocket_body[0]

        cmds.setAttr(self.rocket_body_node + ".radius", self.body_nose_radius)
        
        #loop for getting the bounding_box of the last part to create more body parts
        for i in range(self.body_parts):

            #selecting the previous created part
            previous_part = cmds.ls(selection=True)

            self.bb_first_body = cmds.xform(previous_part, query=True, boundingBox=True, worldSpace=True)
            bb_body = cmds.xform(rocket_body, query=True, boundingBox=True, worldSpace=True)
            bb_center_point_n = (bb_body[1] - bb_body[4]) / 2

            bottom = self.bb_first_body[1]
            offset = bottom + bb_center_point_n

            # creating a body with a special name
            body_name = "Body_" + str(i+1)
            rocket_body = cmds.polyCylinder(name=body_name)

            # separating the name from a node to use it further
            self.rocket_body_node = rocket_body[1]
            self.rocket_body_name = rocket_body[0]

            # setting radius and translating the body part properly
            cmds.setAttr(self.rocket_body_node + ".radius", self.body_nose_radius)
            cmds.xform(rocket_body, translation=[0, offset, 0], relative=True)

            self.last_body_part = body_name

    def create_fuel_tanks(self):
        '''
        Create 4 fuel tanks (cones) for a space rocket
        :return:
        '''
        # we are calculating bounding box for a body
        # where [X_min, Y_min, Z_min, X_max, Y_max, Z_max]
        self.bb_body = cmds.xform(self.rocket_body_name, query=True, boundingBox=True, worldSpace=True)

        fuel_tanks_1 = cmds.polyCone(name="fuel_tanks_1", radius=self.fuel_tank_radius)[0]
        cmds.xform(fuel_tanks_1, worldSpace=True, translation=[0, self.bb_body[1], self.bb_body[2]])
        fuel_tanks_2 = cmds.polyCone(name="fuel_tanks_2", radius=self.fuel_tank_radius)[0]
        cmds.xform(fuel_tanks_2, worldSpace=True, translation=[self.bb_body[3], self.bb_body[1], 0])
        fuel_tanks_3 = cmds.polyCone(name="fuel_tanks_3", radius=self.fuel_tank_radius)[0]
        cmds.xform(fuel_tanks_3, worldSpace=True, translation=[self.bb_body[0], self.bb_body[1], 0])
        fuel_tanks_4 = cmds.polyCone(name="fuel_tanks_4 ", radius=self.fuel_tank_radius)[0]
        cmds.xform(fuel_tanks_4, worldSpace=True, translation=[0, self.bb_body[1], self.bb_body[5]])

class ExtraRocket(Rocket):
    def __init__(self, body_nose_radius=2, body_parts=1, nose_height=1, fuel_tank_radius=1, antenna=True, wings=True):
        #we are inheriting all variables of parent class
        super(ExtraRocket, self).__init__(body_nose_radius, body_parts, nose_height, fuel_tank_radius)
        self.antenna = antenna
        self.wings = wings

        self.create_antenna()
        self.create_wings()
        self.more_body_parts()
        self.add_fuel_tanks()
        self.generate_model()

    def create_antenna(self):
        '''
        Create a small long cylinder on a top of a nose
        :return:
        '''
        antenna = cmds.polyCylinder(name="Antenna")
        cmds.xform(scale=[0.1, 2.4, 0.1])
        self.bb_nose = cmds.xform(self.rocket_nose_name, query=True, boundingBox=True, worldSpace=True)
        antenna_bb = cmds.xform(antenna,  query=True, boundingBox=True, worldSpace=True)
        bb_center_point_n = (antenna_bb[1] - antenna_bb[4]) / 2
        top = self.bb_nose[4]
        offset = top + bb_center_point_n
        cmds.xform(antenna, translation=[0, top, 0], relative=True)

    def create_wings(self):
        '''
        Create 4 small wings on the side of the rocket's body
        :return:
        '''

        #body with the highest number in prefix
        self.bb_last_body = cmds.xform(self.last_body_part, query=True, boundingBox=True, worldSpace=True)

        #creating wings
        wing_1 = cmds.polyCube(name="wing_1")[0]
        cmds.xform(wing_1, worldSpace=True, scale=[0.1, 1.6, 1.1], translation=[0, self.bb_last_body[4], self.bb_last_body[2]])
        wing_2 = cmds.polyCube(name="wing_2")[0]
        cmds.xform(wing_2, worldSpace=True, scale=[1.1, 1.6, 0.1], translation=[self.bb_last_body[3], self.bb_last_body[4], 0])
        wing_3 = cmds.polyCube(name="wing_3")[0]
        cmds.xform(wing_3, worldSpace=True, scale=[1.1, 1.6, 0.1], translation=[self.bb_last_body[0], self.bb_last_body[4], 0])
        wing_4 = cmds.polyCube(name="wing_4")[0]
        cmds.xform(wing_4, worldSpace=True, scale=[0.1, 1.6, 1.1], translation=[0, self.bb_last_body[4], self.bb_last_body[5]])

    def more_body_parts(self):
        '''
        creates 2 more body parts for main rocket body
        :return:
        '''
        for i in range(1):
            #bounding box and center point for the last body part
            self.bb_last_body = cmds.xform(self.last_body_part, query=True, boundingBox=True, worldSpace=True)
            bb_center_point_n = (self.bb_last_body[1] - self.bb_last_body[4]) / 2

            bottom = self.bb_last_body[1]
            offset = bottom + bb_center_point_n

            #creating a body with a special name
            body_name = "Additional_Body_" + str(i+1)
            rocket_body = cmds.polyCylinder(name=body_name)

            #separating the name from a node to use it further
            self.rocket_body_node = rocket_body[1]
            self.rocket_body_name = rocket_body[0]

            #setting the right radius and moving body part in the right place
            cmds.setAttr(self.rocket_body_node + ".radius", self.body_nose_radius)
            cmds.xform(rocket_body, translation=[0, offset, 0], relative=True)

            self.last_body_part = body_name

    def add_fuel_tanks(self):
        '''
        Creates additional fuel tanks(cylinders) for the fuel tanks(cones) and put them right under cones
        for bounding box you use those -> [X_min, Y_min, Z_min, X_max, Y_max, Z_max]
        :return:
        '''
        #FIRST add an additional cylinder for a fuel tank and put it under the fuel tank
        add_fuel_tanks_1 = cmds.polyCylinder(name="add_fuel_tanks_1", radius=self.fuel_tank_radius)[0]
        fuel_tank_1_bb = cmds.xform("fuel_tanks_1", query=True, boundingBox=True, worldSpace=True)
        add_fuel_tank_1_bb = cmds.xform("fuel_tanks_1", query=True, boundingBox=True, worldSpace=True)
        bb_center_point_y = (add_fuel_tank_1_bb[1] - add_fuel_tank_1_bb[4]) / 2
        bb_center_point_z = (add_fuel_tank_1_bb[5] + add_fuel_tank_1_bb[2]) / 2
        bottom = fuel_tank_1_bb[1]
        offset = bottom + bb_center_point_y
        cmds.xform(add_fuel_tanks_1, translation=[0, offset, bb_center_point_z], relative=True)

        #SECOND add an additional cylinder for a fuel tank and put it under the fuel tank
        add_fuel_tanks_2 = cmds.polyCylinder(name="add_fuel_tanks_2", radius=self.fuel_tank_radius)[0]
        fuel_tank_2_bb = cmds.xform("fuel_tanks_2", query=True, boundingBox=True, worldSpace=True)
        add_fuel_tank_2_bb = cmds.xform("fuel_tanks_2", query=True, boundingBox=True, worldSpace=True)
        bb_center_point_y = (add_fuel_tank_2_bb[1] - add_fuel_tank_2_bb[4]) / 2
        bb_center_point_x = (add_fuel_tank_2_bb[3] + add_fuel_tank_2_bb[0]) / 2
        bottom = fuel_tank_2_bb[1]
        offset = bottom + bb_center_point_y
        cmds.xform(add_fuel_tanks_2, translation=[bb_center_point_x, offset, 0], relative=True)

        #THIRD add an additional cylinder for a fuel tank and put it under the fuel tank
        add_fuel_tanks_3 = cmds.polyCylinder(name="add_fuel_tanks_3", radius=self.fuel_tank_radius)[0]
        fuel_tank_3_bb = cmds.xform("fuel_tanks_3", query=True, boundingBox=True, worldSpace=True)
        add_fuel_tank_3_bb = cmds.xform("fuel_tanks_3", query=True, boundingBox=True, worldSpace=True)
        bb_center_point_y = (add_fuel_tank_3_bb[1] - add_fuel_tank_3_bb[4]) / 2
        bb_center_point_x = (add_fuel_tank_3_bb[3] + add_fuel_tank_3_bb[0]) / 2
        bottom = fuel_tank_3_bb[1]
        offset = bottom + bb_center_point_y
        cmds.xform(add_fuel_tanks_3, translation=[bb_center_point_x, offset, 0], relative=True)

        #FOURTH add an additional cylinder for a fuel tank and put it under the fuel tank
        add_fuel_tanks_4 = cmds.polyCylinder(name="add_fuel_tanks_4 ", radius=self.fuel_tank_radius)[0]
        fuel_tank_4_bb = cmds.xform("fuel_tanks_4", query=True, boundingBox=True, worldSpace=True)
        add_fuel_tank_4_bb = cmds.xform("fuel_tanks_4", query=True, boundingBox=True, worldSpace=True)
        bb_center_point_y = (add_fuel_tank_4_bb[1] - add_fuel_tank_4_bb[4]) / 2
        bb_center_point_z = (add_fuel_tank_4_bb[5] + add_fuel_tank_4_bb[2]) / 2
        bottom = fuel_tank_4_bb[1]
        offset = bottom + bb_center_point_y
        cmds.xform(add_fuel_tanks_4, translation=[0, offset, bb_center_point_z], relative=True)


#my_rocket = Rocket(body_nose_radius=3, body_parts=6, nose_height=10, fuel_tank_radius=1)
my_extra_rocket = ExtraRocket(body_nose_radius=2, body_parts=4, nose_height=5, fuel_tank_radius=1, antenna=True, wings=True)
