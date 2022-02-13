bl_info = {
    "name": "Export2Lilnut",
    "blender": (3, 0, 0),
    "category": "Object",
}

import bpy
import json
import os
from math import sqrt

"""panel section"""

class CurveExportLilnutPanel(bpy.types.Panel):
    """Creates a Panel in the data context of the properties editor"""

    bl_label = "Export2lilnut"
    bl_idname = 'DATA_PT_exportlilnut'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'

    def draw(self, context):
        """Draws the Export lilnut Panel"""

        scene = context.scene
        layout = self.layout
        selected_curve = False
        selected_other = False

        for obj in context.selected_objects:
            if obj.type == 'CURVE' :
                selected_curve = True
            else:
                selected_other = True

        if selected_curve:
            
            row = layout.row()
            row.prop(scene, 'export_lilnut_output', text="")

            row = layout.row()
            row.prop(scene, 'export_lilnut_2d')

#            row = layout.row()
#            row.prop(scene, 'export_pre_2poly')

            row = layout.row()
            row.prop(scene, 'export_lilnut_duration')

            row = layout.row()
            row.operator('curve.export_lilnut', text="Export")

            for subcurve in obj.data.splines:
                if subcurve.use_cyclic_u == False:
                    row = layout.row()
                    row.prop(scene, 'export_lilnut_closed')

            if selected_other:
                layout.label(icon='ERROR', text="Notice: only selected Curve will be exported")
        else:
            layout.label(icon='ERROR', text="You must select a Curve")


    @classmethod
    def poll(cls, context):
        """Checks if the Export lilnut Panel should appear"""

        return context.object.type == 'CURVE'

"""end of panel section"""

"""script section"""

class DATA_OT_CurveExportLilnut(bpy.types.Operator):
    """Generates a lilnut file from selected  Curve"""

    bl_label = "Export lilnut"
    bl_idname = 'curve.export_lilnut'

    # guide https://css-tricks.com/svg-path-syntax-illustrated-guide/
    # will be used: M L C S Z
    #commands = {
        #'moveto':     "M {x},{y}",
        #'lineto':     "L {x},{y}",
        #'lineto_h':   "H {x}",
        #'lineto_v':   "V {y}",
        #'curveto':    "C {h1x},{h1y} {h2x},{h2y} {x},{y}",       # h = handle_point
        #'curveto_s':  "S {h2x},{h2y} {x},{y}",                   # mirror handle from previous C or S
        #'curveto_q':  "Q {hx},{hy} {x},{y}",                     # both handles in same position
        #'curveto_qs': "T {x},{y}",                               # mirror handle from previous Q or T
        #'arc':        "A {rx},{ry} {rot} {arc} {sweep} {x},{y}", # arc, sweep -> 0 or 1. it's to choose between four possibilities of arc
        #'closepath':  "Z"}

    #handle_type = {'AUTO', 'ALIGNED', 'VECTOR', 'FREE'}

    def execute(self, context):
        """Exports selected  Curve to lilnut file"""

        scene = context.scene
        total_duration = scene.export_lilnut_duration
        export_mode = scene.export_lilnut_2d
        filename = scene.export_lilnut_output
        file_name = scene.export_lilnut_output
        filename = bpy.path.display_name_from_filepath(file_name)
        if scene.export_lilnut_closed:
            if (scene.export_lilnut_closed == True):
                toClose = 1
            else:
                toClose = ""
        else:
            toClose= "noworry"



        ################################################
        ## basic structure of *.lilnut  sequence file ##
        ################################################
        basic_data = '{"modules": null, "customVariables": null, "states": null, "sequences": [{"parameters": [{"value": 30.0,"controlAddress": "/totalTime"},{"value": true,"controlAddress": "/loop"},{"value": 0.0,"controlAddress": "/viewStartTime"},{"value": 30.0,"controlAddress": "/viewEndTime"}],"niceName": "Sequence", "type": "Sequence", "layers": {"hideInEditor": true, "items": ['
        mode2d_add = '{"parameters": [{"value": 200.0, "controlAddress": "/listSize"}, {"value": 200, "hexMode": false, "controlAddress": "/uiHeight"}, {"value": [0.2117647081613541, 0.2117647081613541, 0.2117647081613541, 1.0], "controlAddress": "/layerColor"}], "niceName": "Mapping XY", "containers": {"recorder": {"editorIsCollapsed": true}, "mapping": {"niceName": "Mapping", "type": "Mapping", "im": {"hideInEditor": true, "items": [{"parameters": [{"value": "", "controlAddress": "/inputValue"}], "niceName": "Input Value", "type": "Input Value"}]}, "params": {"parameters": [{"value": 50, "hexMode": false, "controlAddress": "/updateRate"}], "editorIsCollapsed": true}, "filters": {}, "outputs": {}}, "curve2D": {"parameters": [{"value": false,"controlAddress": "/keySync"}],"items": ['
        mode3dx_add = '{"parameters": [{"value": 120.0, "controlAddress": "/listSize"}, {"value": 120, "hexMode": false, "controlAddress": "/uiHeight"}, {"value": [0.2117647081613541, 0.2117647081613541, 0.2117647081613541, 1.0], "controlAddress": "/layerColor"}], "niceName": "Mapping X", "containers": {"automation": { "parameters": [{"value": 30.0,"controlAddress": "/length"},{"value": [0.0,1.0],"controlAddress": "/viewValueRange"},{"value": [0.0,1.0],"controlAddress": "/range","enabled": true}],"hideInEditor": true,"items": ['
        mode3dy_add = '{"parameters": [{"value": 120.0, "controlAddress": "/listSize"}, {"value": 120, "hexMode": false, "controlAddress": "/uiHeight"}, {"value": [0.2117647081613541, 0.2117647081613541, 0.2117647081613541, 1.0], "controlAddress": "/layerColor"}], "niceName": "Mapping Y", "containers": {"automation": { "parameters": [{"value": 30.0,"controlAddress": "/length"},{"value": [0.0,1.0],"controlAddress": "/viewValueRange"},{"value": [0.0,1.0],"controlAddress": "/range","enabled": true}],"hideInEditor": true,"items": ['
        mode3dz_add = '{"parameters": [{"value": 120.0, "controlAddress": "/listSize"}, {"value": 120, "hexMode": false, "controlAddress": "/uiHeight"}, {"value": [0.2117647081613541, 0.2117647081613541, 0.2117647081613541, 1.0], "controlAddress": "/layerColor"}], "niceName": "Mapping Z", "containers": {"automation": { "parameters": [{"value": 30.0,"controlAddress": "/length"},{"value": [0.0,1.0],"controlAddress": "/viewValueRange"},{"value": [0.0,1.0],"controlAddress": "/range","enabled": true}],"hideInEditor": true,"items": ['
        mode2d_add1 = ']}},"type": "Mapping 2D"}'
        mode3dx_add1 = ']},"recorder": {"editorIsCollapsed": true}, "mapping": {"niceName": "Mapping X", "type": "Mapping", "im": {"hideInEditor": true, "items": [{"parameters": [{"value": "", "controlAddress": "/inputValue"}], "niceName": "Input Value", "type": "Input Value"}]}, "params": {"parameters": [{"value": 50, "hexMode": false, "controlAddress": "/updateRate"}], "editorIsCollapsed": true},"filters": {},"outputs": {}}},"type": "Mapping"}'
        mode3dy_add1 = ']},"recorder": {"editorIsCollapsed": true}, "mapping": {"niceName": "Mapping Y", "type": "Mapping", "im": {"hideInEditor": true, "items": [{"parameters": [{"value": "", "controlAddress": "/inputValue"}], "niceName": "Input Value", "type": "Input Value"}]}, "params": {"parameters": [{"value": 50, "hexMode": false, "controlAddress": "/updateRate"}], "editorIsCollapsed": true},"filters": {},"outputs": {}}},"type": "Mapping"}'
        mode3dz_add1 = ']},"recorder": {"editorIsCollapsed": true}, "mapping": {"niceName": "Mapping Z", "type": "Mapping", "im": {"hideInEditor": true, "items": [{"parameters": [{"value": "", "controlAddress": "/inputValue"}], "niceName": "Input Value", "type": "Input Value"}]}, "params": {"parameters": [{"value": 50, "hexMode": false, "controlAddress": "/updateRate"}], "editorIsCollapsed": true},"filters": {},"outputs": {}}},"type": "Mapping"}'
        basic_data1 = '"cues": {"hideInEditor": true}, "editing": true}], "routers": null}'

        key_structure_x = {
            "parameters": [
                {
                    "value": "",
                    "controlAddress": "/position"
                },
                {
                    "value": "",
                    "controlAddress": "/value"
                },
                {
                    "value": "Linear",
                    "controlAddress": "/easingType"
                }
            ],
            "niceName": "",
                "containers": {
                    "easing": {
                    }
                },
            "type": "Key"
                }

        key_structure_y = {
            "parameters": [
                {
                    "value": "",
                    "controlAddress": "/position"
                },
                {
                    "value": "",
                    "controlAddress": "/value"
                },
                {
                    "value": "Linear",
                    "controlAddress": "/easingType"
                }
            ],
            "niceName": "",
                "containers": {
                    "easing": {
                    }
                },
            "type": "Key"
                }

        key_structure_z = {
            "parameters": [
                {
                    "value": "",
                    "controlAddress": "/position"
                },
                {
                    "value": "",
                    "controlAddress": "/value"
                },
                {
                    "value": "Linear",
                    "controlAddress": "/easingType"
                }
            ],
            "niceName": "",
                "containers": {
                    "easing": {
                    }
                },
            "type": "Key"
                }

        key_structure1_x = {
            "parameters": [
                {
                    "value": "",
                    "controlAddress": "/position"
                },
                {
                    "value": "",
                    "controlAddress": "/value"
                },
                {
                    "value": "Linear",
                    "controlAddress": "/easingType"
                }
            ],
            "niceName": "",
                "containers": {
                    "easing": {
                    }
                },
            "type": "Key"
                }

        key_structure1_y = {
            "parameters": [
                {
                    "value": "",
                    "controlAddress": "/position"
                },
                {
                    "value": "",
                    "controlAddress": "/value"
                },
                {
                    "value": "Linear",
                    "controlAddress": "/easingType"
                }
            ],
            "niceName": "",
                "containers": {
                    "easing": {
                    }
                },
            "type": "Key"
                }

        key_structure1_z = {
            "parameters": [
                {
                    "value": "",
                    "controlAddress": "/position"
                },
                {
                    "value": "",
                    "controlAddress": "/value"
                },
                {
                    "value": "Linear",
                    "controlAddress": "/easingType"
                }
            ],
            "niceName": "",
                "containers": {
                    "easing": {
                    }
                },
            "type": "Key"
                }

        key2d_structure = {"parameters": [{
                                "value": [
                                    "",
                                    ""
                                ],
                                "controlAddress": "/viewUIPosition"
                            },
                                {
                                "value": "Bezier",
                                "controlAddress": "/easingType"
                            }
                            ],
                                "niceName": "2DKey ",
                                "containers": {
                                "easing": {
                                    "parameters": [
                                        {
                                            "value": ["",
                                            ""
                                            ],
                                            "controlAddress": "/anchor1"
                                        },
                                        {
                                            "value": ["",
                                            ""
                                            ],
                                            "controlAddress": "/anchor2"
                                        }
                                    ]
                                }
                            },
                                "type": "2DKey"
                            }

        key2d_structure1 = {"parameters": [{
                                "value": [
                                    "",
                                    ""
                                ],
                                "controlAddress": "/viewUIPosition"
                            },
                                {
                                "value": "Bezier",
                                "controlAddress": "/easingType"
                            }
                            ],
                                "niceName": "2DKey ",
                                "containers": {
                                "easing": {
                                    "parameters": [
                                        {
                                            "value": ["",
                                            ""
                                            ],
                                            "controlAddress": "/anchor1"
                                        },
                                        {
                                            "value": ["",
                                            ""
                                            ],
                                            "controlAddress": "/anchor2"
                                        }
                                    ]
                                }
                            },
                                "type": "2DKey"
                            }

        ################################################

        #######################################################
        ## Prompt section to choose saving path and filename ##
        #######################################################

        # if you want to choose a fixed save path, uncomment the  next line : 

        #save_path= "/your/default/path"

        # and comment the next block
##        default_path = os.path.expanduser("~")
##        default_path = default_path.replace(os.sep, '/')
##        default_path = default_path + "/Documents"
##        isPath = os.path.isdir(default_path)
##        if isPath == False:
##            default_path = os.path.expanduser("~")
##            default_path = default_path.replace(os.sep, '/') 
##
##        save_path = input("Where do you want to write the file?(choose a valid path, default= " + default_path + ": ")
##        if save_path == '':
##            save_path = default_path
##        elif save_path:
##            while not os.path.exists(save_path):
##                save_path = input("Invalid path!(choose a valid path or press enter for default= " + default_path + "): ")
##                if save_path == None:
##                    save_path = default_path
##        #if you want to choose a fixed filename, uncomment the next line :
##
##        #filename= "your_filename"
##
##        # and comment the next block
##        filename = input("OK! Now, which name do you choose for your file(*.lilnut)? : ")
##        while filename == '':
##            filename = input("Choose a name for your file(*.lilnut)? : ")
##
##        #print("Ready,GO!")
##        ########################################################
##
##        #################
##        ##complete path##
##        #################
##        file_name= os.path.join(save_path, filename+".lilnut")
##        file_name= file_name.replace(os.sep, '/')
##
##        #print("Ready,GO!")
##        #################
##
##        ###############
##        ##Export Modes##
##        ###############
##        export_mode = input("Do you want to export in 2D mode (1) or 3D mode (2)?(default = 2D mode) : ")
##        if export_mode == "":
##            export_mode = 1
##        elif export_mode:
##            while  export_mode !="1" and export_mode !="2":
##                export_mode = input("Not a valid number! Choose 2D mode (1) or 3D mode (2)?(default = 2D mode) : ")
##                if export_mode == "":
##                    export_mode = 1
##
##        if export_mode != 'int':
##            export_mode = int(export_mode)
##
##        print("choosed export_mode : ", export_mode)
##
##
##        total_duration = input("Do you want to override the standard duration(30 sec)? if so, enter the desired duration(in seconds) or press return : ")
##        if total_duration.isnumeric() == True:
##            total_duration = total_duration
##        elif total_duration == "":
##            total_duration = "30.0"
##        else:
##            while  total_duration.isnumeric()!= True and total_duration !="":
##                total_duration =  input("Not a number! Please, enter a valid number or press return : ")
##        print("total_duration : ", total_duration)
##
##        ##################################################
##        ## List coordinates of curve points and handles ##
##        ##################################################
        obj= bpy.context.active_object
        ob_curve = bpy.data.objects.get(obj.name,None)
        if obj.type == 'CURVE':
            for subcurve in obj.data.splines:
                curvetype= subcurve.type
                print('curve type:', curvetype)

                if curvetype == 'BEZIER':
##                    if subcurve.use_cyclic_u == False:
##                        toClose = input("Curve is not closed, do you want to close it?(1) for 'Yes' or press return : ")
##                    else:
##                        toClose ="noworry"

                    index= -1
                    cox_list= []
                    coy_list= []
                    coz_list= []
                    hlx_list= []
                    hly_list= []
                    hlz_list= []
                    hrx_list= []
                    hry_list= []
                    hrz_list= []
                    for bezpoint in subcurve.bezier_points:
                        xyz = ob_curve.matrix_world @ bezpoint.co
                        xyz_left = ob_curve.matrix_world @ bezpoint.handle_left
                        xyz_right = ob_curve.matrix_world @ bezpoint.handle_right

                        cox_list.append(xyz[0])
                        coy_list.append(xyz[1])
                        coz_list.append(xyz[2])
                        hlx_list.append(xyz_left[0])
                        hly_list.append(xyz_left[1])
                        hlz_list.append(xyz_left[2])
                        hrx_list.append(xyz_right[0])
                        hry_list.append(xyz_right[1])
                        hrz_list.append(xyz_right[2])
                        
                    nb_of_points = len(cox_list)

                    
        ######################################################################################################
        ##Formatting operations to convert blender coordinates to chataigne system and append file structure##
        ######################################################################################################

                    data_2D = ''
                    data_3Dx = ''
                    data_3Dy = ''
                    data_3Dz = ''
                    steps_length = []
                    total_length = []

                    for i in range(len(cox_list)):
                        if (i>0):
                            steps_length.append(sqrt((cox_list[i]-cox_list[i-1])**2 + (coy_list[i]-coy_list[i-1])**2 +(coz_list[i]-coz_list[i-1])**2))
                    
                    if toClose != "" and i == len(cox_list)-1:
                        total_length = sum(steps_length) + sqrt((cox_list[i]-cox_list[0])**2 + (coy_list[i]-coy_list[0])**2 +(coz_list[i]-coz_list[0])**2)
                    else:
                        total_length = sum(steps_length)
                    
                    for i in range(len(cox_list)):
                        if (i > 0) and (i != len(cox_list)-1):
                            stp_lgth_slc = steps_length[0:i:1]
                            t_position = (float(total_duration)/total_length*sum(stp_lgth_slc))
                            data = key2d_structure
                            data["parameters"][0]["value"][0] = cox_list[i]
                            data["parameters"][0]["value"][1] = coy_list[i]
                            data["niceName"] = "2DKey " + str(i)
                            data["containers"]["easing"]["parameters"][0]["value"][0] = (hrx_list[i] - cox_list[i])
                            data["containers"]["easing"]["parameters"][0]["value"][1] = (hry_list[i] - coy_list[i])
                            data["containers"]["easing"]["parameters"][1]["value"][0] = (hlx_list[i+1] - cox_list[i+1])
                            data["containers"]["easing"]["parameters"][1]["value"][1] = (hly_list[i+1] - coy_list[i+1])

                            x_data = key_structure_x
                            x_data["parameters"][0]["value"] = t_position
                            x_data["parameters"][1]["value"] = cox_list[i]
                            x_data["niceName"] = "Key " + str(i)
                            
                            y_data = key_structure_y
                            y_data["parameters"][0]["value"] = t_position
                            y_data["parameters"][1]["value"] = coy_list[i]
                            y_data["niceName"] = "Key " + str(i)

                            z_data = key_structure_z
                            z_data["parameters"][0]["value"] = t_position
                            z_data["parameters"][1]["value"] = coz_list[i]
                            z_data["niceName"] = "Key " + str(i)

                            data_2D = data_2D + ',' + json.dumps(data)
                            data_3Dx = data_3Dx + ',' + json.dumps(x_data)
                            data_3Dy = data_3Dy + ',' + json.dumps(y_data)
                            data_3Dz = data_3Dz + ',' + json.dumps(z_data)

                        elif (i == 0):

                            data = key2d_structure
                            data["parameters"][0]["value"][0] = cox_list[i]
                            data["parameters"][0]["value"][1] = coy_list[i]
                            data["niceName"] = "2DKey"
                            data["containers"]["easing"]["parameters"][0]["value"][0] = (hrx_list[i] - cox_list[i])
                            data["containers"]["easing"]["parameters"][0]["value"][1] = (hry_list[i] - coy_list[i])
                            data["containers"]["easing"]["parameters"][1]["value"][0] = (hlx_list[i+1] - cox_list[i+1])
                            data["containers"]["easing"]["parameters"][1]["value"][1] = (hly_list[i+1] - coy_list[i+1])

                            x_data = key_structure_x
                            x_data["parameters"][0]["value"] = 0
                            x_data["parameters"][1]["value"] = cox_list[i]
                            x_data["niceName"] = "Key"

                            y_data = key_structure_y
                            y_data["parameters"][0]["value"] = 0
                            y_data["parameters"][1]["value"] = coy_list[i]
                            y_data["niceName"] = "Key"

                            z_data = key_structure_z
                            z_data["parameters"][0]["value"] = 0
                            z_data["parameters"][1]["value"] = coz_list[i]
                            z_data["niceName"] = "Key "

                            data_2D = data_2D + json.dumps(data)
                            data_3Dx = data_3Dx + json.dumps(x_data)
                            data_3Dy = data_3Dy + json.dumps(y_data)
                            data_3Dz = data_3Dz + json.dumps(z_data)

                        else:
                            if toClose !="":
                                stp_lgth_slc = steps_length[0:(len(cox_list)-1):1]
                                t_position = (float(total_duration)/total_length*sum(stp_lgth_slc))
                            else:
                                t_position = total_duration

                            data = key2d_structure
                            data["parameters"][0]["value"][0] = cox_list[i]
                            data["parameters"][0]["value"][1] = coy_list[i]
                            data["niceName"] = "2DKey " + str(i)
                            data["containers"]["easing"]["parameters"][0]["value"][0] = (hrx_list[i] - cox_list[i])
                            data["containers"]["easing"]["parameters"][0]["value"][1] = (hry_list[i] - coy_list[i])
                            data["containers"]["easing"]["parameters"][1]["value"][0] = (hlx_list[0] - cox_list[0])
                            data["containers"]["easing"]["parameters"][1]["value"][1] = (hly_list[0] - coy_list[0])

                            data1 = key2d_structure1
                            data1["parameters"][0]["value"][0] = cox_list[0]
                            data1["parameters"][0]["value"][1] = coy_list[0]
                            data1["niceName"] = "2DKey " + str(i+1)
                            data1["containers"]["easing"] = ""

                            x_data = key_structure_x
                            x_data["parameters"][0]["value"] = t_position 
                            x_data["parameters"][1]["value"] = cox_list[i]
                            x_data["niceName"] = "Key " + str(i)

                            y_data = key_structure_y
                            y_data["parameters"][0]["value"] = t_position
                            y_data["parameters"][1]["value"] = coy_list[i]
                            y_data["niceName"] = "Key " + str(i)

                            z_data = key_structure_z
                            z_data["parameters"][0]["value"] = t_position
                            z_data["parameters"][1]["value"] = coz_list[i]
                            z_data["niceName"] = "Key " + str(i)


                            x_data1 = key_structure1_x
                            x_data1["parameters"][0]["value"] = float(total_duration)
                            x_data1["parameters"][1]["value"] = cox_list[0]
                            x_data1["niceName"] = "Key " + str(i+1)

                            y_data1 = key_structure1_y
                            y_data1["parameters"][0]["value"] = float(total_duration)
                            y_data1["parameters"][1]["value"] = coy_list[0]
                            y_data1["niceName"] = "Key " + str(i+1)

                            z_data1 = key_structure1_z
                            z_data1["parameters"][0]["value"] = float(total_duration)
                            z_data1["parameters"][1]["value"] = coz_list[0]
                            z_data1["niceName"] = "Key " + str(i+1)
                            
                            if toClose != "":
                                data_2D = data_2D + ',' + json.dumps(data) + ',' + json.dumps(data1)
                                data_3Dx = data_3Dx + ',' + json.dumps(x_data) + ',' + json.dumps(x_data1)
                                data_3Dy = data_3Dy + ',' + json.dumps(y_data) + ',' + json.dumps(y_data1)
                                data_3Dz = data_3Dz + ',' + json.dumps(z_data) + ',' + json.dumps(z_data1)
                            else:
                                data_2D = data_2D + ',' + json.dumps(data)
                                data_3Dx = data_3Dx + ',' + json.dumps(x_data)
                                data_3Dy = data_3Dy + ',' + json.dumps(y_data)
                                data_3Dz = data_3Dz + ',' + json.dumps(z_data)
                            
                            if export_mode == 1:
                                final_data = basic_data + mode2d_add + data_2D + mode2d_add1 + "]}," + basic_data1
                            else:
                                final_data = basic_data + mode3dx_add +  data_3Dx + mode3dx_add1 + ","+ mode3dy_add +  data_3Dy + mode3dy_add1 + "," + mode3dz_add +  data_3Dz + mode3dz_add1 + "]},"+ basic_data1

        #########################################################################################

        ###########################
        ##Final writing operation##
        ###########################
                            f_data = json.loads(final_data)
                            f_data["sequences"][0]["niceName"] = str(filename)
                            if total_duration != "30.0":
                                f_data["sequences"][0]["parameters"][0]["value"] = str(total_duration)
                                f_data["sequences"][0]["parameters"][3]["value"] = str(total_duration)
                            final_data = json.dumps(f_data)
                            with open(file_name, "w") as write_file:
                                write_file.write(final_data)
                            if int(export_mode) != 1:
                                with open(file_name, "r") as read_file:
                                    datawrited = json.load(read_file)
                                    datawrited["sequences"][0]['layers']['items'][0]['containers']['automation']['parameters'][2]['value'] = [min(cox_list), max(cox_list)]
                                    datawrited["sequences"][0]['layers']['items'][1]['containers']['automation']['parameters'][1]['value'] = [min(coy_list), max(coy_list)]
                                    datawrited["sequences"][0]['layers']['items'][1]['containers']['automation']['parameters'][2]['value'] = [min(coy_list), max(coy_list)]
                                    datawrited["sequences"][0]['layers']['items'][2]['containers']['automation']['parameters'][1]['value'] = [min(coz_list), max(coz_list)]
                                    datawrited["sequences"][0]['layers']['items'][0]['containers']['automation']['parameters'][1]['value'] = [min(cox_list), max(cox_list)]
                                    datawrited["sequences"][0]['layers']['items'][2]['containers']['automation']['parameters'][2]['value'] = [min(coz_list), max(coz_list)]
                                with open(file_name, "w") as json_file: #write it back to the file
                                    json.dump(datawrited, json_file)
                    print("So, your file path is : ", file_name)
                    return {'FINISHED'}

        ###############################
        ##Same things for POLY curves##
        ###############################

                elif curvetype =='POLY':
                    print("curve is closed:", subcurve.use_cyclic_u)

##                    if subcurve.use_cyclic_u == False:
##                        toClose = input("Curve is not closed, do you want to close it?(1) for 'Yes' or press return : ")
##                    else:
##                        toClose ="noworry"


                    index= -1
                    cox_list= []
                    coy_list= []
                    coz_list= []

                    for point in subcurve.points:
                        xyz = ob_curve.matrix_world @ point.co
                        cox_list.append(xyz[0])
                        coy_list.append(xyz[1])
                        coz_list.append(xyz[2])
                        nb_of_points= len(cox_list)
                    data_2D = ''
                    data_3Dx = ''
                    data_3Dy = ''
                    data_3Dz = ''
                    steps_length = []
                    total_length = []

                    for i in range(len(cox_list)):
                        if (i>0):
                            steps_length.append(sqrt((cox_list[i]-cox_list[i-1])**2 + (coy_list[i]-coy_list[i-1])**2 +(coz_list[i]-coz_list[i-1])**2))
                    
                    if toClose != "" and i == len(cox_list)-1:
                        total_length = sum(steps_length) + sqrt((cox_list[i]-cox_list[0])**2 + (coy_list[i]-coy_list[0])**2 +(coz_list[i]-coz_list[0])**2)
                    else:
                        total_length = sum(steps_length)

                    for i in range(len(cox_list)):

                        if (i > 0) and (i != len(cox_list)-1):

                            stp_lgth_slc = steps_length[0:i:1]
                            t_position = (float(total_duration)/total_length*sum(stp_lgth_slc))

                            data = key2d_structure
                            data["parameters"][0]["value"][0] = cox_list[i]
                            data["parameters"][0]["value"][1] = coy_list[i]
                            data["niceName"] = "2DKey " + str(i)
                            data["containers"]["easing"] = ""

                            x_data = key_structure_x
                            x_data["parameters"][0]["value"] = t_position
                            x_data["parameters"][1]["value"] = cox_list[i]
                            x_data["niceName"] = "Key " + str(i)

                            y_data = key_structure_y
                            y_data["parameters"][0]["value"] = t_position
                            y_data["parameters"][1]["value"] = coy_list[i]
                            y_data["niceName"] = "Key " + str(i)

                            z_data = key_structure_z
                            z_data["parameters"][0]["value"] = t_position
                            z_data["parameters"][1]["value"] = coz_list[i]
                            z_data["niceName"] = "Key " + str(i)

                            data_2D = data_2D + ',' + json.dumps(data)
                            data_3Dx = data_3Dx + ',' + json.dumps(x_data)
                            data_3Dy = data_3Dy + ',' + json.dumps(y_data)
                            data_3Dz = data_3Dz + ',' + json.dumps(z_data)

                        elif (i == 0):

                            data = key2d_structure
                            data["parameters"][0]["value"][0] = cox_list[i]
                            data["parameters"][0]["value"][1] = coy_list[i]
                            data["niceName"] = "2DKey"
                            data["containers"]["easing"] = ""

                            x_data = key_structure_x
                            x_data["parameters"][0]["value"] = 0
                            x_data["parameters"][1]["value"] = cox_list[i]
                            x_data["niceName"] = "Key"

                            y_data = key_structure_y
                            y_data["parameters"][0]["value"] = 0
                            y_data["parameters"][1]["value"] = coy_list[i]
                            y_data["niceName"] = "Key"

                            z_data = key_structure_z
                            z_data["parameters"][0]["value"] = 0
                            z_data["parameters"][1]["value"] = coz_list[i]
                            z_data["niceName"] = "Key "

                            data_2D = data_2D + json.dumps(data)
                            data_3Dx = data_3Dx + json.dumps(x_data)
                            data_3Dy = data_3Dy + json.dumps(y_data)
                            data_3Dz = data_3Dz + json.dumps(z_data)

                        else:
                            if toClose !="":
                                stp_lgth_slc = steps_length[0:(len(cox_list)-1):1]
                                t_position = (float(total_duration)/total_length*sum(stp_lgth_slc))
                            else:
                                t_position = total_duration


                            data = key2d_structure
                            data["parameters"][0]["value"][0] = cox_list[i]
                            data["parameters"][0]["value"][1] = coy_list[i]
                            data["niceName"] = "2DKey " + str(i)
                            data["containers"]["easing"] = "" 

                            data1 = key2d_structure1
                            data1["parameters"][0]["value"][0] = cox_list[0]
                            data1["parameters"][0]["value"][1] = coy_list[0]
                            data1["niceName"] = "2DKey " + str(i+1)
                            data1["containers"]["easing"] = ""

                            x_data = key_structure_x
                            x_data["parameters"][0]["value"] = t_position
                            x_data["parameters"][1]["value"] = cox_list[i]
                            x_data["niceName"] = "Key " + str(i)

                            y_data = key_structure_y
                            y_data["parameters"][0]["value"] = t_position
                            y_data["parameters"][1]["value"] = coy_list[i]
                            y_data["niceName"] = "Key " + str(i)

                            z_data = key_structure_z
                            z_data["parameters"][0]["value"] = t_position
                            z_data["parameters"][1]["value"] = coz_list[i]
                            z_data["niceName"] = "Key " + str(i)


                            x_data1 = key_structure1_x
                            x_data1["parameters"][0]["value"] = float(total_duration)
                            x_data1["parameters"][1]["value"] = cox_list[0]
                            x_data1["niceName"] = "Key " + str(i+1)

                            y_data1 = key_structure1_y
                            y_data1["parameters"][0]["value"] = float(total_duration)
                            y_data1["parameters"][1]["value"] = coy_list[0]
                            y_data1["niceName"] = "Key " + str(i+1)

                            z_data1 = key_structure1_z
                            z_data1["parameters"][0]["value"] = float(total_duration)
                            z_data1["parameters"][1]["value"] = coz_list[0]
                            z_data1["niceName"] = "Key " + str(i+1)
                            
                            if toClose != "":
                                data_2D = data_2D + ',' + json.dumps(data) + ',' + json.dumps(data1)
                                data_3Dx = data_3Dx + ',' + json.dumps(x_data) + ',' + json.dumps(x_data1)
                                data_3Dy = data_3Dy + ',' + json.dumps(y_data) + ',' + json.dumps(y_data1)
                                data_3Dz = data_3Dz + ',' + json.dumps(z_data) + ',' + json.dumps(z_data1)
                            else:
                                data_2D = data_2D + ',' + json.dumps(data)
                                data_3Dx = data_3Dx + ',' + json.dumps(x_data)
                                data_3Dy = data_3Dy + ',' + json.dumps(y_data)
                                data_3Dz = data_3Dz + ',' + json.dumps(z_data)
                            
                            if export_mode == 1:
                                final_data = basic_data + mode2d_add + data_2D + mode2d_add1 + "]}," + basic_data1
                            else:
                                final_data = basic_data + mode3dx_add +  data_3Dx + mode3dx_add1 + ","+ mode3dy_add +  data_3Dy + mode3dy_add1 + "," + mode3dz_add +  data_3Dz + mode3dz_add1 + "]},"+ basic_data1


                            f_data = json.loads(final_data)
                            f_data["sequences"][0]["niceName"] = str(filename)
                            if total_duration != "30.0":
                                f_data["sequences"][0]["parameters"][0]["value"] = str(total_duration)
                                f_data["sequences"][0]["parameters"][3]["value"] = str(total_duration)
                            final_data = json.dumps(f_data)
                            with open(file_name, "w") as write_file:
                                write_file.write(final_data)
                            if int(export_mode) != 1:
                                with open(file_name, "r") as read_file:
                                    datawrited = json.load(read_file)
                                    datawrited["sequences"][0]['layers']['items'][0]['containers']['automation']['parameters'][2]['value'] = [min(cox_list), max(cox_list)]
                                    datawrited["sequences"][0]['layers']['items'][1]['containers']['automation']['parameters'][1]['value'] = [min(coy_list), max(coy_list)]
                                    datawrited["sequences"][0]['layers']['items'][1]['containers']['automation']['parameters'][2]['value'] = [min(coy_list), max(coy_list)]
                                    datawrited["sequences"][0]['layers']['items'][2]['containers']['automation']['parameters'][1]['value'] = [min(coz_list), max(coz_list)]
                                    datawrited["sequences"][0]['layers']['items'][0]['containers']['automation']['parameters'][1]['value'] = [min(cox_list), max(cox_list)]
                                    datawrited["sequences"][0]['layers']['items'][2]['containers']['automation']['parameters'][2]['value'] = [min(coz_list), max(coz_list)]


                                with open(file_name, "w") as json_file: #write it back to the file
                                    json.dump(datawrited, json_file)
                    print("So, your file path is : ", file_name)
                    return {'FINISHED'}

"""end of script section"""

"""registering section"""

def register():
    """Registers curve_to_lilnut Add-on"""

    bpy.types.Scene.export_lilnut_output = bpy.props.StringProperty(
            name="Output",
            description="Path to output file",
            default="output.lilnut",
            subtype='FILE_PATH')

    bpy.types.Scene.export_lilnut_2d = bpy.props.IntProperty(
            name="Export Mode",
            description="Choose (1) for 2D and (2) for 3D",
            default=2,
            min=1,
            max=2)

#    bpy.types.Scene.export_pre_2poly = bpy.props.BoolProperty(
#            name="Bezier2Poly",
#            description="Convert bezier curve to poly for best result",
#            default=False)

    bpy.types.Scene.export_lilnut_duration = bpy.props.IntProperty(
            name="Duration",
            description="Duration of lilnut sequence in seconds",
            default=30,
            min=1)

    bpy.types.Scene.export_lilnut_closed = bpy.props.BoolProperty(
        name="make cyclic",
        description="Convert unclosed curve to closed",
        default =False
    )

    bpy.utils.register_class(DATA_OT_CurveExportLilnut)
    bpy.utils.register_class(CurveExportLilnutPanel)


def unregister():
    """Unregisters curve_to_svg Add-on"""

    bpy.utils.unregister_class(CurveExportLilnutPanel)
    bpy.utils.unregister_class(DATA_OT_CurveExportLilnut)

    del bpy.types.Scene.export_lilnut_output
    del bpy.types.Scene.export_slilnut_2d
#    del bpy.types.Scene.export_pre_2poly
    del bpy.types.Scene.export_lilnut_duration


if __name__ == '__main__':
    register()

"""end of registering section"""