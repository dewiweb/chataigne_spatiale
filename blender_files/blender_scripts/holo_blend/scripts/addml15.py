import bpy
import os
import json
import sys
import math


 
file_path_rel = '//Assets/amadeus.blend'
preset_file_path_rel = '//hol/DEWI23.hol'
coord_convert_file_rel = '//scripts/holo_out.py'

print(bpy.path.abspath(file_path_rel))
file_path = bpy.path.abspath(file_path_rel)
preset_file_path = bpy.path.abspath(preset_file_path_rel)
coord_convert_file = bpy.path.abspath(coord_convert_file_rel)
sys.modules['coord_conv'] = bpy.data.texts['holo_out.py'].as_module()
from coord_conv import sph2cart
inner_path = 'Object'


"""
Read *.hol file content
"""
with open(preset_file_path) as f:
    preset_content = json.load(f)
    preset_dict = preset_content['hol']
    keys = list(preset_dict.keys())
    
"""
Search in content for matching parameters
"""
for i in range(1,128):
    sph_coord = [0,0,0]
    cart_coord = [0,0,0]
    spk_type = ""
    spk_color = [0,0,0]
    spk_pan = 0
    spk_tilt = 0
    spk_roll90deg = False
    speaker = '/speaker/'
    params = ['/color','/azim','/elev','/dist','/view3D/file3D','/view3D/roll90deg','/view3D/pan','/view3D/tilt']
    for param in params:
        tuple = (speaker,str(i),param)
        tuple = ''.join(tuple)
        
        if param == params[1]:
            if (tuple) in keys:
                p_tuple = preset_dict[tuple]
                sph_coord[0] = p_tuple[0]
                print(tuple,'azim:',p_tuple[0])
        elif param == params[2]:
            if (tuple) in keys:
                p_tuple = preset_dict[tuple]
                sph_coord[1] = p_tuple[0]
                print(tuple,'elev: ',p_tuple[0])
        elif param == params[3]:
            if (tuple) in keys:
                p_tuple = preset_dict[tuple]
                sph_coord[2] = p_tuple[0]
                print(tuple,'dist: ',p_tuple[0])
                cart_coord = sph2cart(float(sph_coord[1]),float(sph_coord[0]),float(sph_coord[2]))
                print('cartesian coordinates: ',cart_coord)
        elif param == params[4]:
            if (tuple) in keys:
                p_tuple = preset_dict[tuple]
                end_loc = len(p_tuple)-5
                spk_name = str(p_tuple[0])[19:end_loc]
                print(tuple,spk_name)
                bpy.ops.wm.append(
                    directory=os.path.join(file_path, inner_path),
                    filename=spk_name
                    )
                for obj in bpy.context.selected_objects:
                    obj.name = 'spk_'+str(i)+'_'+spk_name
                    obj.data.name = 'spk_'+str(i)+'_'+spk_name
                    obj.location.x = cart_coord[1]
                    obj.location.y = cart_coord[0]
                    obj.location.z = cart_coord[2]
                    material = bpy.data.materials.new(name = 'spk_'+str(i)+'_'+spk_name+'_mat')
                    obj.data.materials.append(material)
                    bpy.data.materials['spk_'+str(i)+'_'+spk_name+'_mat'].diffuse_color = color
                    
        elif param == params[0]:
            if (tuple) in keys:
                p_tuple = preset_dict[tuple]
                print(tuple,p_tuple)
                color = p_tuple
                
        elif param == params[7]:
            if (tuple) in keys:
                p_tuple = preset_dict[tuple]
                print(tuple,p_tuple)
                spk_tilt = p_tuple[0]
                for obj in bpy.context.selected_objects:
                    obj.rotation_mode = 'XYZ'
                    if spk_roll90deg == True:
                        obj.rotation_euler[1] = math.radians(-float(spk_tilt))
                    else:
                        obj.rotation_euler[2] = math.radians(float(spk_tilt))
        elif param == params[6]:
            if (tuple) in keys:
                p_tuple = preset_dict[tuple]
                print(tuple,p_tuple)
                spk_pan = p_tuple[0]
                for obj in bpy.context.selected_objects:
                    obj.rotation_mode = 'XYZ'
                    if spk_roll90deg == True:
                        obj.rotation_euler[0] = math.radians(float(spk_pan))
                    else:
                        obj.rotation_euler[1] = math.radians(-float(spk_pan))
        elif param == params[5]:
            if (tuple) in keys:
                p_tuple = preset_dict[tuple]
                print(tuple,p_tuple)
                spk_roll90deg = p_tuple[0]
                if spk_roll90deg == True:
                    for obj in bpy.context.selected_objects:
                        obj.rotation_mode = 'XYZ'
                        obj.rotation_euler[2] = math.radians(90)
                    
        else:
            if (tuple) in keys:
                p_tuple = preset_dict[tuple]
                print(tuple,p_tuple[0])
                    
    
"""
retrieve list of speaker models in assets file
"""
"""
with bpy.data.libraries.load(file_path) as (data_from, data_to):
    object_names = [name for name in data_from.objects]
#print(object_names)



i = 17
object_name = object_names[i]
 
bpy.ops.wm.append(
    directory=os.path.join(file_path, inner_path),
    filename=object_name
    )

for obj in bpy.context.selected_objects:
    obj.name = object_name
    obj.data.name = object_name
"""
