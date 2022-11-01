
track = 'track'
args = args.replace('(','')
args = args.replace(')','')
args = args.replace(' ','')
args = args.split(',')
properties = ['color', 'x', 'y', 'z', 'name', 'xyz']
if track in addr:
    sepTerms = addr.split('/')
    if len(sepTerms[2]) == 1:
        id =  "00"+ sepTerms[2]
    elif len(sepTerms[2]) == 2:
        id =  "0"+ sepTerms[2]
    elif len(sepTerms[2]) == 3:
        id =   sepTerms[2] 
    objects = [obj.name for obj in bpy.context.scene.objects]
    matching = [s for s in objects if id in s]
    debug = matching
    if matching == []:
        debug = str(id)
        bpy.ops.mesh.primitive_ico_sphere_add(location=(0,0,0))
        if len(sepTerms[2]) == 1 :
            bpy.context.active_object.name = 'track.00'+ sepTerms[2]
        elif len(sepTerms[2]) == 2:
            bpy.context.active_object.name = 'track.0'+ sepTerms[2]
        else:
            bpy.context.active_object.name = 'track.'+ sepTerms[2]
        if sepTerms[3] == properties[5]:
            bpy.context.active_object.location.x = float(args[0])
            bpy.context.active_object.location.y = float(args[1])
            bpy.context.active_object.location.z = float(args[2])
        elif sepTerms[3] == properties[0]:
            bpy.context.active_object.color = (float(args[0]),float(args[1]),float(args[2]),float(args[3]))
        else:
            if sepTerms[3] == properties[4]:
                bpy.context.active_object.name = str(bpy.context.active_object.name) + "." + str(args[0]).replace("'",'')
    else:
        for x in objects:
            ob = bpy.data.objects[x]
            index = ((ob.name).split('.'))[1]
            
            if index == id:       
                    if sepTerms[3] == properties[5]:
                        ob.location.x = float(args[0])
                        ob.location.y = float(args[1])
                        ob.location.z = float(args[2])
                    elif sepTerms[3] == properties[0]:
                        ob.color = (float(args[0]),float(args[1]),float(args[2]),float(args[3]))
                    else:
                        if sepTerms[3] == properties[4]:
                            inname = str(args[0]).replace("'",'')
                            if len((ob.name).split('.')) == 3:
                                exname = str(((ob.name).split('.'))[2])
                                debug = exname
                                ob.name = (ob.name).replace( exname, inname)
                            else:
                                ob.name = (ob.name) + "." + inname
                    

                    
            
