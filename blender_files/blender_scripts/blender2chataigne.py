import bpy
import json
import os


################################################
## basic structure of *.lilnut  sequence file ##
################################################
basic_data = '{"modules": null, "customVariables": null, "states": null, "sequences": [{"niceName": "Sequence", "type": "Sequence", "layers": {"hideInEditor": true, "items": ['
mode2d_add = '{"parameters": [{"value": 200.0, "controlAddress": "/listSize"}, {"value": 200, "hexMode": false, "controlAddress": "/uiHeight"}, {"value": [0.2117647081613541, 0.2117647081613541, 0.2117647081613541, 1.0], "controlAddress": "/layerColor"}], "niceName": "Mapping 2D", "containers": {"recorder": {"editorIsCollapsed": true}, "mapping": {"niceName": "Mapping", "type": "Mapping", "im": {"hideInEditor": true, "items": [{"parameters": [{"value": "", "controlAddress": "/inputValue"}], "niceName": "Input Value", "type": "Input Value"}]}, "params": {"parameters": [{"value": 50, "hexMode": false, "controlAddress": "/updateRate"}], "editorIsCollapsed": true}, "filters": {}, "outputs": {}}, "curve2D": {"parameters": [{"value": false,"controlAddress": "/keySync"}],"items": ['
mode3d_add = '{"parameters": [{"value": 120.0, "controlAddress": "/listSize"}, {"value": 120, "hexMode": false, "controlAddress": "/uiHeight"}, {"value": [0.2117647081613541, 0.2117647081613541, 0.2117647081613541, 1.0], "controlAddress": "/layerColor"}], "niceName": "Mapping", "containers": {"automation": { "parameters": [{"value": 30.0,"controlAddress": "/length"},{"value": [0.0,1.0],"controlAddress": "/viewValueRange"},{"value": [0.0,1.0],"controlAddress": "/range","enabled": true}],"hideInEditor": true,"items": ['
mode2d_add1 = ']}},"type": "Mapping 2D"}'
mode3d_add1 = ']},"recorder": {"editorIsCollapsed": true}, "mapping": {"niceName": "Mapping", "type": "Mapping", "im": {"hideInEditor": true, "items": [{"parameters": [{"value": "", "controlAddress": "/inputValue"}], "niceName": "Input Value", "type": "Input Value"}]}, "params": {"parameters": [{"value": 50, "hexMode": false, "controlAddress": "/updateRate"}], "editorIsCollapsed": true},"filters": {},"outputs": {}}},"type": "Mapping"}]},'
basic_data1 = '"cues": {"hideInEditor": true}, "editing": true}], "routers": null}'

################################################

#######################################################
## Prompt section to choose saving path and filename ##
#######################################################

# if you want to choose a fixed save path, uncomment the  next line : 

#save_path= "/your/default/path"

# and comment the next block
default_path = os.path.expanduser("~")
default_path = default_path.replace(os.sep, '/')
default_path = default_path + "/Documents"
print("default_path", default_path)
isPath = os.path.isdir(default_path)
print("isPath", isPath)
if isPath == False:
    default_path = os.path.expanduser("~")
    default_path = default_path.replace(os.sep, '/') 

save_path = input("Where do you want to write the file?(choose a valid path, default= " + default_path + ": ")
if save_path == '':
    save_path = default_path
elif save_path:
    while not os.path.exists(save_path):
        save_path = input("Invalid path!(choose a valid path or press enter for default= " + default_path + "): ")
        if save_path == None:
            save_path = default_path
print("save_path : ",save_path)
#if you want to choose a fixed filename, uncomment the next line :

#filename= "your_filename"

# and comment the next block
filename = input("OK! Now, which name do you choose for your file(*.lilnut)? : ")
while filename == '':
    filename = input("Choose a name for your file(*.lilnut)? : ")

#print("Ready,GO!")
########################################################

#################
##complete path##
#################
file_name= os.path.join(save_path, filename+".lilnut")

#print("Ready,GO!")
#################

###############
##Export Modes##
###############
export_mode = input("Do you want to export in 2D mode (1) or 3D mode (2)?(default = 2D mode) : ")
if save_path == None:
    export_mode = int(1)
elif export_mode:
    while not export_mode != 1 and export_mode != 2:
        export_mode = input("Not a valid number! Choose 2D mode (1) or 3D mode (2)?(default = 2D mode) : ")
export_mode = str(export_mode)
print("choosed export_mode : ", export_mode)


##################################################
## List coordinates of curve points and handles ##
##################################################
obj= bpy.context.active_object
ob_curve = bpy.data.objects.get(obj.name,None)
if obj.type == 'CURVE':
    for subcurve in obj.data.splines:
        curvetype= subcurve.type
        print('curve type:', curvetype)

        if curvetype == 'BEZIER':
            print("curve is closed:", subcurve.use_cyclic_u)

            index= -1
            cox_list= []
            coy_list= []
            coz_list= []
            hlx_list= []
            hly_list= []
            hrx_list= []
            hry_list= []
            for bezpoint in subcurve.bezier_points:
                """
                'handle_left_type',      # kind of handles
                'handle_right_type',     #
                'hide',                  # is it hidden?
                'radius',                # what's the radius
                'select_control_point',  # is it selected?
                'select_left_handle',    #
                'select_right_handle',   #
                'tilt'                   # investigate :)
                # use     print(dir(bezpoint))  to see all
                """
                xyz = ob_curve.matrix_world @ bezpoint.co
                xyz_left = ob_curve.matrix_world @ bezpoint.handle_left
                xyz_right = ob_curve.matrix_world @ bezpoint.handle_right
                print("xyz", xyz)
                print("xyz_left", xyz_left)
                print("xyz_right", xyz_right)

                cox_list.append(xyz[0])
                # print("cox", cox_list)
                coy_list.append(xyz[1])
                # print("coy", coy_list)
                coz_list.append(xyz[2])
                print("coz_list",coz_list)
                hlx_list.append(xyz_left[0])
                # print("hlx", hlx_list)
                hly_list.append(xyz_left[1])
                # print("hly", hly_list)
                hrx_list.append(xyz_right[0])
                hry_list.append(xyz_right[1])
                
            nb_of_points = len(cox_list)
            print("Number of points : ", nb_of_points) 
            #print(range(nb_of_points))

            
####################################################################################################
##Format operations to convert blender coordinates to chataigne system and complete file structure##
####################################################################################################

            data_2D = ''
            data_3Dz = ''

            for i in range(len(cox_list)):
                if (i > 0) and (i != len(cox_list)-1):
                    #print("cas i>0 et != de longueur-1")
                    data= {"parameters": [{
                        "value": [
                            cox_list[i],
                            coy_list[i]
                        ],
                        "controlAddress": "/viewUIPosition"
                    },
                        {
                        "value": "Bezier",
                        "controlAddress": "/easingType"
                    }
                    ],
                        "niceName": "2DKey " + str(i),
                        "containers": {
                        "easing": {
                            "parameters": [
                                {
                                    "value": [
                                        hrx_list[i] -
                                        cox_list[i],
                                        hry_list[i] -
                                        coy_list[i]
                                    ],
                                    "controlAddress": "/anchor1"
                                },
                                {
                                    "value": [
                                        hlx_list[i+1] -
                                        cox_list[i+1],
                                        hly_list[i+1] -
                                        coy_list[i+1]
                                    ],
                                    "controlAddress": "/anchor2"
                                }
                            ]
                        }
                    },
                        "type": "2DKey"
                    }

                    z_data = {
                        "parameters": [
                            {
                                "value": i*(30/(nb_of_points)),
                                "controlAddress": "/position"
                            },
                            {
                                "value": coz_list[i],
                                "controlAddress": "/value"
                            },
                            {
                                "value": "Linear",
                                "controlAddress": "/easingType"
                            }
                        ],
                        "niceName": "Key " + str(i),
                            "containers": {
                                "easing": {
                                }
                            },
                        "type": "Key"
                    }

                    #basic_data = basic_data + ',' + json.dumps(data)
                    data_2D = data_2D + ',' + json.dumps(data)
                    data_3Dz = data_3Dz + ',' + json.dumps(z_data)
                elif (i == 0):
                    #print("cas i=0")
                    data ={"parameters": [{
                        "value": [
                            cox_list[i],
                            coy_list[i]
                        ],
                        "controlAddress": "/viewUIPosition"
                    },
                        {
                        "value": "Bezier",
                        "controlAddress": "/easingType"
                    }
                    ],
                        "niceName": "2DKey",
                        "containers": {
                        "easing": {
                            "parameters": [
                                {
                                    "value": [
                                        hrx_list[i] -
                                        cox_list[i],
                                        hry_list[i] -
                                        coy_list[i]
                                    ],
                                    "controlAddress": "/anchor1"
                                },
                                {
                                    "value": [
                                        hlx_list[i+1] -
                                        cox_list[i+1],
                                        hly_list[i+1] -
                                        coy_list[i+1]
                                    ],
                                    "controlAddress": "/anchor2"
                                }
                            ]
                        }
                    },
                        "type": "2DKey"
                    }

                    z_data = {
                        "parameters": [
                            {
                                "value": 0,
                                "controlAddress": "/position"
                            },
                            {
                                "value": coz_list[i],
                                "controlAddress": "/value"
                            },
                            {
                                "value": "Linear",
                                "controlAddress": "/easingType"
                            }
                        ],
                        "niceName": "Key",
                            "containers": {
                                "easing": {
                                }
                            },
                        "type": "Key"
                    }

                    data_2D = data_2D + json.dumps(data)
                    #print("data2D_firststep : ",data_2D)
                    data_3Dz = data_3Dz + json.dumps(z_data)
                    #if export_mode == 1:
                    #    basic_data = basic_data + mode2d_add + json.dumps(data)
                    #else:
                    #    basic_data = basic_data + mode3d_add + json.dumps(data)
                else:
                    #print("cas i= longueur-1")
                    data = {"parameters": [{
                        "value": [
                            cox_list[i],
                            coy_list[i]
                        ],
                        "controlAddress": "/viewUIPosition"
                    },
                        {
                        "value": "Bezier",
                        "controlAddress": "/easingType"
                    }
                    ],
                        "niceName": "2DKey " + str(i),
                        "containers": {
                        "easing": {
                            "parameters": [
                                {
                                    "value": [
                                        hrx_list[i] -
                                        cox_list[i],
                                        hry_list[i] -
                                        coy_list[i]
                                    ],
                                    "controlAddress": "/anchor1"
                                },
                                {
                                    "value": [
                                        hlx_list[0] -
                                        cox_list[0],
                                        hly_list[0] -
                                        coy_list[0]
                                    ],
                                    "controlAddress": "/anchor2"
                                }
                            ]
                        }
                    },
                        "type": "2DKey"
                    }

                    data1 = {"parameters": [{
                        "value": [
                            cox_list[0],
                            coy_list[0]
                        ],
                        "controlAddress": "/viewUIPosition"
                    },
                        {
                        "value": "Bezier",
                        "controlAddress": "/easingType"
                    }
                    ],
                        "niceName": "2DKey " + str(i+1),
                        "containers": {
                        "easing": {
                        }
                    },
                        "type": "2DKey"
                    }

                    z_data = {
                        "parameters": [
                            {
                                "value": i*(30/nb_of_points),
                                "controlAddress": "/position"
                            },
                            {
                                "value": coz_list[i],
                                "controlAddress": "/value"
                            },
                            {
                                "value": "Linear",
                                "controlAddress": "/easingType"
                            }
                        ],
                        "niceName": "Key " + str(i),
                            "containers": {
                                "easing": {
                                }
                            },
                        "type": "Key"
                    }

                    z_data1 = {
                        "parameters": [
                            {
                                "value": 30,
                                "controlAddress": "/position"
                            },
                            {
                                "value": coz_list[i],
                                "controlAddress": "/value"
                            },
                            {
                                "value": "Linear",
                                "controlAddress": "/easingType"
                            }
                        ],
                        "niceName": "Key " + str(i+1),
                            "containers": {
                                "easing": {
                                }
                            },
                        "type": "Key"
                    }

                    data_2D = data_2D + ',' + json.dumps(data) + ',' + json.dumps(data1)
                    #print("data2D_finaltstep : ",data_2D)
                    data_3Dz = data_3Dz + ',' + json.dumps(z_data) + ',' + json.dumps(z_data1)
                    #print("export_mode_log",export_mode)
                    if int(export_mode) == 1:
                        print("Ready for Bezier2D!")
                        final_data = basic_data + mode2d_add + data_2D + mode2d_add1 + "]}," + basic_data1
                    else:
                        print("Ready for Bezier3D!")
                        final_data = basic_data + mode2d_add + data_2D + mode2d_add1 + "," + mode3d_add +  data_3Dz + mode3d_add1 + basic_data1

                    #basic_data = basic_data + ',' + json.dumps(data)
                    #basic_data = basic_data + ',' + json.dumps(data1) + basic_data1
                    #print("basic_data : ",basic_data)
                    #final_data = json.dumps(basic_data)
                    #print("final_data : ",final_data)
#########################################################################################

###########################
##Final writing operation##
###########################
                    with open(file_name, "w") as write_file:
                        write_file.write(final_data)
                    if int(export_mode) != 1:
                        with open(file_name, "r") as read_file:
                            datawrited = json.load(read_file)
                            datawrited["sequences"][0]['layers']['items'][1]['containers']['automation']['parameters'][1]['value'] = [min(coz_list), max(coz_list)]
                            datawrited["sequences"][0]['layers']['items'][1]['containers']['automation']['parameters'][2]['value'] = [min(coz_list), max(coz_list)]
                        with open(file_name, "w") as json_file: #write it back to the file
                            json.dump(datawrited, json_file)
                            print("So, your file path is : ", file_name)

###############################
##Same things for POLY curves##
###############################

        elif curvetype =='POLY':
            print("curve is closed:", subcurve.use_cyclic_u)
            index= -1
            cox_list= []
            coy_list= []
            coz_list= []
            for point in subcurve.points:
                cox_list.append(point.co[0])
                coy_list.append(point.co[1])
                coz_list.append(point.co[2])
                #print("coz_list",coz_list)
                nb_of_points= len(cox_list)
            data_2D = ''
            data_3Dz = ''
            for i in range(len(cox_list)):
                if (i > 0) and (i != len(cox_list)-1):
                    #print("cas i>0 et != de longueur-1")
                    data= {"parameters": [{
                        "value": [
                            cox_list[i],
                            coy_list[i]
                        ],
                        "controlAddress": "/viewUIPosition"
                    },
                        {
                        "value": "Bezier",
                        "controlAddress": "/easingType"
                    }
                    ],
                        "niceName": "2DKey " + str(i),
                        "containers": {
                        "easing": {
                        }
                    },
                        "type": "2DKey"
                    }

                    z_data = {
                        "parameters": [
                            {
                                "value": i*(30/(nb_of_points)),
                                "controlAddress": "/position"
                            },
                            {
                                "value": coz_list[i],
                                "controlAddress": "/value"
                            },
                            {
                                "value": "Linear",
                                "controlAddress": "/easingType"
                            }
                        ],
                        "niceName": "Key " + str(i),
                            "containers": {
                                "easing": {
                                }
                            },
                        "type": "Key"
                    }

                    data_2D = data_2D + ',' + json.dumps(data)
                    data_3Dz = data_3Dz + ',' + json.dumps(z_data)

                elif (i == 0):
                    #print("cas i=0")
                    data ={"parameters": [{
                        "value": [
                            cox_list[i],
                            coy_list[i]
                        ],
                        "controlAddress": "/viewUIPosition"
                    },
                        {
                        "value": "Bezier",
                        "controlAddress": "/easingType"
                    }
                    ],
                        "niceName": "2DKey",
                        "containers": {
                        "easing": {
                        }
                    },
                        "type": "2DKey"
                    }

                    z_data = {
                        "parameters": [
                            {
                                "value": 0,
                                "controlAddress": "/position"
                            },
                            {
                                "value": coz_list[i],
                                "controlAddress": "/value"
                            },
                            {
                                "value": "Linear",
                                "controlAddress": "/easingType"
                            }
                        ],
                        "niceName": "Key",
                            "containers": {
                                "easing": {
                                }
                            },
                        "type": "Key"
                    }

                    data_2D = data_2D + json.dumps(data)
                    #print("polydata2d.1",data_2D)
                    data_3Dz = data_3Dz + json.dumps(z_data)
                    #print("polydata3dz.1", data_3Dz)
                else:
                    #print("cas i= longueur-1")
                    data = {"parameters": [{
                        "value": [
                            cox_list[i],
                            coy_list[i]
                        ],
                        "controlAddress": "/viewUIPosition"
                    },
                        {
                        "value": "Bezier",
                        "controlAddress": "/easingType"
                    }
                    ],
                        "niceName": "2DKey " + str(i),
                        "containers": {
                        "easing": {
                        }
                    },
                        "type": "2DKey"
                    }

                    data1 = {"parameters": [{
                        "value": [
                            cox_list[0],
                            coy_list[0]
                        ],
                        "controlAddress": "/viewUIPosition"
                    },
                        {
                        "value": "Bezier",
                        "controlAddress": "/easingType"
                    }
                    ],
                        "niceName": "2DKey " + str(i+1),
                        "containers": {
                        "easing": {
                        }
                    },
                        "type": "2DKey"
                    }

                    z_data = {
                        "parameters": [
                            {
                                "value": i*(30/nb_of_points),
                                "controlAddress": "/position"
                            },
                            {
                                "value": coz_list[i],
                                "controlAddress": "/value"
                            },
                            {
                                "value": "Linear",
                                "controlAddress": "/easingType"
                            }
                        ],
                        "niceName": "Key " + str(i),
                            "containers": {
                                "easing": {
                                }
                            },
                        "type": "Key"
                    }

                    z_data1 = {
                        "parameters": [
                            {
                                "value": 30,
                                "controlAddress": "/position"
                            },
                            {
                                "value": coz_list[i],
                                "controlAddress": "/value"
                            },
                            {
                                "value": "Linear",
                                "controlAddress": "/easingType"
                            }
                        ],
                        "niceName": "Key " + str(i+1),
                            "containers": {
                                "easing": {
                                }
                            },
                        "type": "Key"
                    }

                    data_2D = data_2D + ',' + json.dumps(data) + ',' + json.dumps(data1)
                    #print("data2D_finaltstep : ",data_2D)
                    data_3Dz = data_3Dz + ',' + json.dumps(z_data) + ',' + json.dumps(z_data1)
                    #print("export_mode_log",export_mode)
                    if int(export_mode) == 1:
                        print("Ready for Poly2D!")
                        final_data = basic_data + mode2d_add + data_2D + mode2d_add1 + "]}," + basic_data1
                    else:
                        print("Ready for Poly3D!")
                        final_data = basic_data + mode2d_add + data_2D + mode2d_add1 + "," + mode3d_add +  data_3Dz + mode3d_add1 + basic_data1

                    with open(file_name, "w") as write_file:
                        write_file.write(final_data)
                    if int(export_mode) != 1:
                        with open(file_name, "r") as read_file:
                            datawrited = json.load(read_file)
                            datawrited["sequences"][0]['layers']['items'][1]['containers']['automation']['parameters'][1]['value'] = [min(coz_list), max(coz_list)]
                            datawrited["sequences"][0]['layers']['items'][1]['containers']['automation']['parameters'][2]['value'] = [min(coz_list), max(coz_list)]
                        with open(file_name, "w") as json_file: #write it back to the file
                            json.dump(datawrited, json_file)
                            print("So, your file path is : ", file_name)
