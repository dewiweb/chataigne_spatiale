import bpy
import json
import os


################################################
## basic structure of *.lilnut  sequence file ##
################################################
basic_data ='{"modules": null, "customVariables": null, "states": null, "sequences": [{"niceName": "Sequence", "type": "Sequence", "layers": {"hideInEditor": true, "items": [{"parameters": [{"value": 200.0, "controlAddress": "/listSize"}, {"value": 200, "hexMode": false, "controlAddress": "/uiHeight"}, {"value": [0.2117647081613541, 0.2117647081613541, 0.2117647081613541, 1.0], "controlAddress": "/layerColor"}], "niceName": "Mapping 2D", "containers": {"recorder": {"editorIsCollapsed": true}, "mapping": {"niceName": "Mapping", "type": "Mapping", "im": {"hideInEditor": true, "items": [{"parameters": [{"value": "", "controlAddress": "/inputValue"}], "niceName": "Input Value", "type": "Input Value"}]}, "params": {"parameters": [{"value": 50, "hexMode": false, "controlAddress": "/updateRate"}], "editorIsCollapsed": true}, "filters": {}, "outputs": {}}, "curve2D": {"parameters": [{"value": false,"controlAddress": "/keySync"}],"items": ['
basic_data1 =']}},"type": "Mapping 2D"}]}, "cues": {"hideInEditor": true}, "editing": true}], "routers": null}'
################################################

#######################################################
## Prompt section to choose saving path and filename ##
#######################################################

# if you want to choose a fixed save path, uncomment the  next line : 

#save_path= "/your/default/path"

# and comment the next block

save_path = input("Where do you want to write the file?(choose a valid path, default= " + os.path.expanduser("~") + ": ")
if save_path == None:
    save_path = os.path.expanduser("~")
elif save_path:
    while not os.path.exists(save_path):
        print('invalid path')
save_path = save_path.replace(os.sep, '/')
#if you want to choose a fixed filename, uncomment the next line :

#filename= "your_filename"

# and comment the next block
filename = input("OK! Now, which name do you choose for your file(*.lilnut)? : ")
print("Ready,GO!")
########################################################

#################
##complete path##
#################
file_name= os.path.join(save_path, filename+".lilnut")
#################

###############
##Export Mode##
###############
export_mode = input("Do you want to export in 2D mode (1) or 3D mode (2)?(default = 1) : ")
if export_mode == None:
    export_mode = 1
elif export_mode:
    while not export_mode == 1 or export == 2:
        print('enter a valid number')


##################################################
## List coordinates of curve points and handles ##
##################################################
obj= bpy.context.active_object

if obj.type == 'CURVE':
    for subcurve in obj.data.splines:
        curvetype= subcurve.type
        print('curve type:', curvetype)

        if curvetype == 'BEZIER':
            print("curve is closed:", subcurve.use_cyclic_u)

            index= -1
            cox_list= []
            coy_list= []
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
                cox_list.append(bezpoint.co[0])
                # print("cox", cox_list)
                coy_list.append(bezpoint.co[1])
                # print("coy", coy_list)
                hlx_list.append(bezpoint.handle_left[0])
                # print("hlx", hlx_list)
                hly_list.append(bezpoint.handle_left[1])
                # print("hly", hly_list)
                hrx_list.append(bezpoint.handle_right[0])
                hry_list.append(bezpoint.handle_right[1])
                
            nb_of_points= len(cox_list)
            #print("length", nb_of_points)
            #print(range(nb_of_points))
####################################################################################################
##Format operations to convert blender coordinates to chataigne system and complete file structure##
####################################################################################################

            for i in range(len(cox_list)):
                if (i > 0) and (i != len(cox_list)-1):
                    print("cas i>0 et != de longueur-1")
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

                    basic_data = basic_data + ',' + json.dumps(data)
                elif (i == 0):
                    print("cas i=0")
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

                    basic_data = basic_data + json.dumps(data)
                else:
                    print("cas i= longueur-1")
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
                    basic_data = basic_data + ',' + json.dumps(data)
                    basic_data = basic_data + ',' + json.dumps(data1) + basic_data1
                    #print("basic_data : ",basic_data)
                    final_data = json.dumps(basic_data)
                    #print("final_data : ",final_data)
#########################################################################################

###########################
##Final writing operation##
###########################
                    with open(file_name, "w") as write_file:
                         write_file.write(basic_data)
                    
        elif curvetype =='POLY':
          print("curve is closed:", subcurve.use_cyclic_u)
          index= -1
          cox_list= []
          coy_list= []
          for point in subcurve.points:
            cox_list.append(point.co[0])
            coy_list.append(point.co[1])
            nb_of_points= len(cox_list)
          for i in range(len(cox_list)):
                if (i > 0) and (i != len(cox_list)-1):
                    print("cas i>0 et != de longueur-1")
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

                    basic_data = basic_data + ',' + json.dumps(data)
                elif (i == 0):
                    print("cas i=0")
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

                    basic_data = basic_data + json.dumps(data)
                else:
                    print("cas i= longueur-1")
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
                    basic_data = basic_data + ',' + json.dumps(data)
                    basic_data = basic_data + ',' + json.dumps(data1) + basic_data1
                    print("basic_data : ",basic_data)
                    final_data = json.dumps(basic_data)
                    with open(file_name, "w") as write_file:
                      write_file.write(basic_data)
