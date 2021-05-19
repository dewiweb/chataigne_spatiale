import bpy
import json
import os


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

key_structure = {
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

key_structure1 = {
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
file_name= file_name.replace(os.sep, '/')

#print("Ready,GO!")
#################

###############
##Export Modes##
###############
export_mode = input("Do you want to export in 2D mode (1) or 3D mode (2)?(default = 2D mode) : ")
if export_mode == "":
    export_mode = 1
elif export_mode:
    while  export_mode !="1" and export_mode !="2":
        export_mode = input("Not a valid number! Choose 2D mode (1) or 3D mode (2)?(default = 2D mode) : ")
        if export_mode == "":
            export_mode = 1

if export_mode != 'int':
    export_mode = int(export_mode)

print("choosed export_mode : ", export_mode)


total_length = input("Do you want to override the standard length(30 sec)? if so, enter the desired length(in seconds) or press return : ")
if total_length.isnumeric() == True:
    total_length = total_length
elif total_length == "":
    total_length = "30.0"
else:
    while  total_length.isnumeric()!= True and total_length !="":
        total_length =  input("Not a number! Please, enter a valid number or press return : ")
print("total_length : ", total_length)

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
            if subcurve.use_cyclic_u == False:
                toClose = input("Curve is not closed, do you want to close it?(1) for 'Yes' or press return : ")

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
            print("Number of points : ", nb_of_points) 
            #print(range(nb_of_points))

            
######################################################################################################
##Formatting operations to convert blender coordinates to chataigne system and append file structure##
######################################################################################################

            data_2D = ''
            data_3Dx = ''
            data_3Dy = ''
            data_3Dz = ''

            for i in range(len(cox_list)):

                if (i > 0) and (i != len(cox_list)-1):

                    data = key2d_structure
                    data["parameters"][0]["value"][0] = cox_list[i]
                    data["parameters"][0]["value"][1] = coy_list[i]
                    data["niceName"] = "2DKey " + str(i)
                    data["containers"]["easing"]["parameters"][0]["value"][0] = (hrx_list[i] - cox_list[i])
                    data["containers"]["easing"]["parameters"][0]["value"][1] = (hry_list[i] - coy_list[i])
                    data["containers"]["easing"]["parameters"][1]["value"][0] = (hlx_list[i+1] - cox_list[i+1])
                    data["containers"]["easing"]["parameters"][1]["value"][1] = (hly_list[i+1] - coy_list[i+1])

                    x_data = key_structure
                    x_data["parameters"][0]["value"] = i*(int(float(total_length))/(nb_of_points))
                    x_data["parameters"][1]["value"] = cox_list[i]
                    x_data["niceName"] = "Key " + str(i)

                    y_data = key_structure
                    y_data["parameters"][0]["value"] = i*(int(float(total_length))/(nb_of_points))
                    y_data["parameters"][1]["value"] = coy_list[i]
                    y_data["niceName"] = "Key " + str(i)

                    z_data = key_structure
                    z_data["parameters"][0]["value"] = i*(int(float(total_length))/(nb_of_points))
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

                    x_data = key_structure
                    x_data["parameters"][0]["value"] = i*(int(float(total_length))/(nb_of_points))
                    x_data["parameters"][1]["value"] = cox_list[i]
                    x_data["niceName"] = "Key"

                    y_data = key_structure
                    y_data["parameters"][0]["value"] = i*(int(float(total_length))/(nb_of_points))
                    y_data["parameters"][1]["value"] = coy_list[i]
                    y_data["niceName"] = "Key"

                    z_data = key_structure
                    z_data["parameters"][0]["value"] = i*(int(float(total_length))/(nb_of_points))
                    z_data["parameters"][1]["value"] = coz_list[i]
                    z_data["niceName"] = "Key "

                    data_2D = data_2D + json.dumps(data)
                    data_3Dx = data_3Dx + json.dumps(x_data)
                    data_3Dy = data_3Dy + json.dumps(y_data)
                    data_3Dz = data_3Dz + json.dumps(z_data)

                else:

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

                    x_data = key_structure1
                    x_data["parameters"][0]["value"] = i*(int(float(total_length))/(nb_of_points))
                    x_data["parameters"][1]["value"] = cox_list[i]
                    x_data["niceName"] = "Key " + str(i)

                    y_data = key_structure1
                    y_data["parameters"][0]["value"] = i*(int(float(total_length))/(nb_of_points))
                    y_data["parameters"][1]["value"] = coy_list[i]
                    y_data["niceName"] = "Key " + str(i)

                    z_data = key_structure
                    z_data["parameters"][0]["value"] = i*(int(float(total_length))/(nb_of_points))
                    z_data["parameters"][1]["value"] = coz_list[i]
                    z_data["niceName"] = "Key " + str(i)


                    x_data1 = key_structure
                    x_data1["parameters"][0]["value"] = int(float(total_length))
                    x_data1["parameters"][1]["value"] = cox_list[i]
                    x_data1["niceName"] = "Key " + str(i+1)

                    y_data1 = key_structure
                    y_data1["parameters"][0]["value"] = int(float(total_length))
                    y_data1["parameters"][1]["value"] = coy_list[i]
                    y_data1["niceName"] = "Key " + str(i+1)

                    z_data1 = key_structure
                    z_data1["parameters"][0]["value"] = int(float(total_length))
                    z_data1["parameters"][1]["value"] = coz_list[i]
                    z_data1["niceName"] = "Key " + str(i+1)
                    
                    data_2D = data_2D + ',' + json.dumps(data) + ',' + json.dumps(data1)
                    data_3Dx = data_3Dx + ',' + json.dumps(x_data) + ',' + json.dumps(x_data1)
                    data_3Dy = data_3Dy + ',' + json.dumps(y_data) + ',' + json.dumps(y_data1)
                    data_3Dz = data_3Dz + ',' + json.dumps(z_data) + ',' + json.dumps(z_data1)
                    
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
                    if total_length != "30.0":
                        f_data["sequences"][0]["parameters"][0]["value"] = str(total_length)
                        f_data["sequences"][0]["parameters"][3]["value"] = str(total_length)
                    final_data = json.dumps(f_data)
                    with open(file_name, "w") as write_file:
                        write_file.write(final_data)
                        #print("So, your file path is : ", file_name)
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
                nb_of_points= len(cox_list)
            data_2D = ''
            data_3Dx = ''
            data_3Dy = ''
            data_3Dz = ''
            for i in range(len(cox_list)):

                if (i > 0) and (i != len(cox_list)-1):

                    data = key2d_structure
                    data["parameters"][0]["value"][0] = cox_list[i]
                    data["parameters"][0]["value"][1] = coy_list[i]
                    data["niceName"] = "2DKey " + str(i)
                    data["containers"]["easing"] = ""

                    x_data = key_structure
                    x_data["parameters"][0]["value"] = i*(int(float(total_length))/(nb_of_points))
                    x_data["parameters"][1]["value"] = cox_list[i]
                    x_data["niceName"] = "Key " + str(i)

                    y_data = key_structure
                    y_data["parameters"][0]["value"] = i*(int(float(total_length))/(nb_of_points))
                    y_data["parameters"][1]["value"] = coy_list[i]
                    y_data["niceName"] = "Key " + str(i)

                    z_data = key_structure
                    z_data["parameters"][0]["value"] = i*(int(float(total_length))/(nb_of_points))
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

                    x_data = key_structure
                    x_data["parameters"][0]["value"] = i*(int(float(total_length))/(nb_of_points))
                    x_data["parameters"][1]["value"] = cox_list[i]
                    x_data["niceName"] = "Key"

                    y_data = key_structure
                    y_data["parameters"][0]["value"] = i*(int(float(total_length))/(nb_of_points))
                    y_data["parameters"][1]["value"] = coy_list[i]
                    y_data["niceName"] = "Key"

                    z_data = key_structure
                    z_data["parameters"][0]["value"] = i*(int(float(total_length))/(nb_of_points))
                    z_data["parameters"][1]["value"] = coz_list[i]
                    z_data["niceName"] = "Key "

                    data_2D = data_2D + json.dumps(data)
                    data_3Dx = data_3Dx + json.dumps(x_data)
                    data_3Dy = data_3Dy + json.dumps(y_data)
                    data_3Dz = data_3Dz + json.dumps(z_data)

                else:

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

                    x_data = key_structure
                    x_data["parameters"][0]["value"] = i*(int(float(total_length))/(nb_of_points))
                    x_data["parameters"][1]["value"] = cox_list[i]
                    x_data["niceName"] = "Key " + str(i)

                    y_data = key_structure
                    y_data["parameters"][0]["value"] = i*(int(float(total_length))/(nb_of_points))
                    y_data["parameters"][1]["value"] = coy_list[i]
                    y_data["niceName"] = "Key " + str(i)

                    z_data = key_structure
                    z_data["parameters"][0]["value"] = i*(int(float(total_length))/(nb_of_points))
                    z_data["parameters"][1]["value"] = coz_list[i]
                    z_data["niceName"] = "Key " + str(i)


                    x_data1 = key_structure1
                    x_data1["parameters"][0]["value"] = int(float(total_length))
                    x_data1["parameters"][1]["value"] = cox_list[i]
                    x_data1["niceName"] = "Key " + str(i+1)

                    y_data1 = key_structure1
                    y_data1["parameters"][0]["value"] = int(float(total_length))
                    y_data1["parameters"][1]["value"] = coy_list[i]
                    y_data1["niceName"] = "Key " + str(i+1)

                    z_data1 = key_structure1
                    z_data1["parameters"][0]["value"] = int(float(total_length))
                    z_data1["parameters"][1]["value"] = coz_list[i]
                    z_data1["niceName"] = "Key " + str(i+1)
                    
                    data_2D = data_2D + ',' + json.dumps(data) + ',' + json.dumps(data1)
                    data_3Dx = data_3Dx + ',' + json.dumps(x_data) + ',' + json.dumps(x_data1)
                    data_3Dy = data_3Dy + ',' + json.dumps(y_data) + ',' + json.dumps(y_data1)
                    data_3Dz = data_3Dz + ',' + json.dumps(z_data) + ',' + json.dumps(z_data1)
                    
                    if export_mode == 1:
                        final_data = basic_data + mode2d_add + data_2D + mode2d_add1 + "]}," + basic_data1
                    else:
                        final_data = basic_data + mode3dx_add +  data_3Dx + mode3dx_add1 + ","+ mode3dy_add +  data_3Dy + mode3dy_add1 + "," + mode3dz_add +  data_3Dz + mode3dz_add1 + "]},"+ basic_data1


                    f_data = json.loads(final_data)
                    f_data["sequences"][0]["niceName"] = str(filename)
                    if total_length != "30.0":
                        f_data["sequences"][0]["parameters"][0]["value"] = str(total_length)
                        f_data["sequences"][0]["parameters"][3]["value"] = str(total_length)
                    final_data = json.dumps(f_data)
                    with open(file_name, "w") as write_file:
                        write_file.write(final_data)
                        #print("So, your file path is : ", file_name)
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
