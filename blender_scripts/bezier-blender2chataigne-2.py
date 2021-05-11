
import bpy
import json
import os

obj = bpy.context.active_object

if obj.type == 'CURVE':
    for subcurve in obj.data.splines:
        curvetype = subcurve.type
        print('curve type:', curvetype)

        if curvetype == 'BEZIER':
            print("curve is closed:", subcurve.use_cyclic_u)

            # print(dir(subcurve))
            
            save_path = '/home/dewi/Bureau/ChampsLibres/mai2021/chataigne'
            file_name = os.path.join(save_path, "export_data.json")
            index = -1
            cox_list = []
            coy_list = []
            hlx_list = []
            hly_list = []
            hrx_list = []
            hry_list = []
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
                print ("cox", cox_list)
                coy_list.append(bezpoint.co[1])
                print("coy", coy_list)
                hlx_list.append(bezpoint.handle_left[0])
                print ("hlx",hlx_list)
                hly_list.append(bezpoint.handle_left[1])
                print("hly", hly_list)
                hrx_list.append(bezpoint.handle_right[0])
                hry_list.append(bezpoint.handle_right[1])
                #index +=1
               # print('co_xy ' + str(index), bezpoint.co[0], bezpoint.co[1] )
               # print('handle_left_xy ' + str(index), bezpoint.handle_left[0], bezpoint.handle_left[1])
               # print('handle_right_xy ' + str(index), bezpoint.handle_right[0], bezpoint.handle_right[1])
            nb_of_points = len(cox_list)
            print("length", nb_of_points)
            print(range(nb_of_points))
            
            for i in range(len(cox_list)):
                if (i > 0) and (i != len(cox_list)-1) :
                    print("cas i>0 et != de longueur-1")
                    data ={"parameters":[{
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
                                            "niceName": "2DKey "+ str(i),
                                            "containers": {
                                                "easing": {
                                                    "parameters": [
                                                        {
                                                            "value": [
                                                                hrx_list[i]-cox_list[i],
                                                                hry_list[i]-coy_list[i]
                                                            ],
                                                            "controlAddress": "/anchor1"
                                                        },
                                                        {
                                                            "value": [
                                                                hlx_list[i+1]-cox_list[i+1],
                                                                hly_list[i+1]-coy_list[i+1]
                                                            ],
                                                            "controlAddress": "/anchor2"
                                                        }
                                                    ]
                                                }
                                            },
                                            "type": "2DKey"
                                        }
                    with open(file_name, "a") as file_object:
                        file_object.write(",")
                        file_object.write(json.dumps(data))
                elif (i == 0):
                    print("cas i=0")
                    data ={"parameters":[{
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
                                                                hrx_list[i]-cox_list[i],
                                                                hry_list[i]-coy_list[i]
                                                            ],
                                                            "controlAddress": "/anchor1"
                                                        },
                                                        {
                                                            "value": [
                                                                hlx_list[i+1]-cox_list[i+1],
                                                                hly_list[i+1]-coy_list[i+1]
                                                            ],
                                                            "controlAddress": "/anchor2"
                                                        }
                                                    ]
                                                }
                                            },
                                            "type": "2DKey"
                                        }
                    with open(file_name, "w") as write_file:
                        json.dump(data, write_file)
                else:
                    print("cas i= longueur-1")
                    data ={"parameters":[{
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
                                            "niceName": "2DKey "+ str(i),
                                            "containers": {
                                                "easing": {
                                                    "parameters": [
                                                        {
                                                            "value": [
                                                                hrx_list[i]-cox_list[i],
                                                                hry_list[i]-coy_list[i]
                                                            ],
                                                            "controlAddress": "/anchor1"
                                                        },
                                                        {
                                                            "value": [
                                                                hlx_list[0]-cox_list[0],
                                                                hly_list[0]-coy_list[0]
                                                            ],
                                                            "controlAddress": "/anchor2"
                                                        }
                                                    ]
                                                }
                                            },
                                            "type": "2DKey"
                                        }
                                        
                    data1 ={"parameters": [{
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
                                            "niceName": "2DKey "+ str(i+1),
                                            "containers": {
                                                "easing": {
                                                }
                                            },
                                            "type": "2DKey"
                                            }
                                            
                                        
                    with open(file_name, "a") as file_object:
                        file_object.write(",")
                        file_object.write(json.dumps(data))
                        file_object.write(",")
                        file_object.write(json.dumps(data1))
                        
                                
                            
                  
                #else: print (all_data est vide)
                                        
                        