'''
functions used by message handlers
'''
import bpy
import asyncio
import queue
from NodeOSC import *



def populate(address, args):
    data_file = open("received.txt", "rb")
    datas = pickle.load(data_file)
    data_file.close()
    data_file = open('received.txt', 'wb')
    pickle.dump(datas +[[address,args]], data_file)
    data_file.close()
    data_file = open("received.txt", "rb")
    datas = pickle.load(data_file)
    data_file.close()
    print("received datas :", datas)
    

def dump(address, args):
    
    print("dump received :",address, args)
    bpy.data.node_groups["AN Tree"].nodes["Data Input"].inputs[0].value = args

def track(address, args):
#    print("queue length :",q.qsize())
#    q.put(address,args)
    print("address :" + address + "; args :" + args)
#    print(type(args))
    arguments = args.replace('(','')
    arguments = arguments.replace(')','')
    arguments = arguments.split(',')
    arguments = [x for x in arguments if x]
#    print("arguments : ",arguments)
    properties = ['color', 'x', 'y', 'z', 'name', 'xyz']
    track = 'track'
    if track in address:
        sepTerms = address.split('/')
        if len(sepTerms[2]) == 1:
            id =  "00"+ sepTerms[2]
        elif len(sepTerms[2]) == 2:
            id =  "0"+ sepTerms[2]
        elif len(sepTerms[2]) == 3:
            id =   sepTerms[2] 
#        print("id :",id)
        objects = [obj.name for obj in bpy.context.scene.objects]
#        print("objects :",objects)
        matching = [s for s in objects if id in s]
#        print("matching :", matching)
        if matching == []:
            debug = str(id)
            bpy.ops.mesh.primitive_ico_sphere_add(location=(0,0,0))
            if len(sepTerms[2]) == 1 :
                bpy.context.active_object.name = 'track.00'+ sepTerms[2]
                bpy.context.active_object.show_name = True
            elif len(sepTerms[2]) == 2:
                bpy.context.active_object.name = 'track.0'+ sepTerms[2]
                bpy.context.active_object.show_name = True
            else:
                bpy.context.active_object.name = 'track.'+ sepTerms[2]
                bpy.context.active_object.show_name = True
            if sepTerms[3] == properties[5]:
                bpy.context.active_object.location.x = float(arguments[0])
                bpy.context.active_object.location.y = float(arguments[1])
                bpy.context.active_object.location.z = float(arguments[2])
                return
            elif sepTerms[3] == properties[1]:
                bpy.context.active_object.location.x = float(arguments[0])
                return
            elif sepTerms[3] == properties[2]:
                bpy.context.active_object.location.y = float(arguments[0])
                return
            elif sepTerms[3] == properties[3]:
                bpy.context.active_object.location.z = float(arguments[0])
                return
            elif sepTerms[3] == properties[0]:
                bpy.context.active_object.color = (float(arguments[0]),float(arguments[1]),float(arguments[2]),float(arguments[3]))
                return
            else:
                if sepTerms[3] == properties[4]:
                    bpy.context.active_object.name = str(bpy.context.active_object.name) + "." + str(arguments[0]).replace("'",'')
                    return
        else:
            for x in objects:
                ob = bpy.data.objects[x]
                index = ((ob.name).split('.'))[1]
#                print("index :",index)
#                print("septerm :", sepTerms)
                if index == id:       
                        if sepTerms[3] == properties[5]:
                            ob.location.x = float(arguments[0])
                            ob.location.y = float(arguments[1])
                            ob.location.z = float(arguments[2])
                            return
                        elif sepTerms[3] == properties[1]:
                            ob.location.x = float(arguments[0])
                            return
                        elif sepTerms[3] == properties[2]:
                            ob.location.y = float(arguments[0])
                            return
                        elif sepTerms[3] == properties[3]:
                            ob.location.z = float(arguments[0])
                            return
                        elif sepTerms[3] == properties[0]:
                            ob.color = (float(arguments[0]),float(arguments[1]),float(arguments[2]),float(arguments[3]))
                            return
                        else:
                            if sepTerms[3] == properties[4]:
                                inname = str(arguments[0]).replace("'",'')
                                if len((ob.name).split('.')) == 3:
                                    exname = str(((ob.name).split('.'))[2])
                                    debug = exname
                                    ob.name = (ob.name).replace( exname, inname)
                                    return
                                else:
                                    ob.name = (ob.name) + "." + inname
                                    return
                                
if server.OSC_callback_queue.queue != []:
    print("overflow")
    for q_item in server.OSC_callback_queue.queue:
        print(" queued;",q_item[6])
        track(q_item[2],str(q_item[6]))    