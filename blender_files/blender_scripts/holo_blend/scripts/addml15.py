import bpy
import os
import json


 
file_path_rel = '//Assets/amadeus.blend'
preset_file_path_rel = '//hol/DEWI23.hol'
coord_convert_file_rel = '//scripts/holo_out.py'

print(bpy.path.abspath(file_path_rel))
file_path = bpy.path.abspath(file_path_rel)
preset_file_path = bpy.path.abspath(preset_file_path_rel)
coord_convert_file = bpy.path.abspath(coord_convert_file_rel)
coord_conv = bpy.data.texts[coord_convert_file].as_module()
inner_path = 'Object'
sph_coord = [0,0,0]
spk_type = ""

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
    speaker = '/speaker/'
    params = ['/azim','/elev','/dist','/view3D/file3D','/view3D/roll90deg','/view3D/pan','/view3D/tilt','/color']
    for param in params:
        tuple = (speaker,str(i),param)
        tuple = ''.join(tuple)
        
        if param == params[0]:
            if (tuple) in keys:
                p_tuple = preset_dict[tuple]
                sph_coord[0] = p_tuple[0]
                print(tuple,'azim:',p_tuple[0])
        elif param == params[1]:
            if (tuple) in keys:
                p_tuple = preset_dict[tuple]
                sph_coord[1] = p_tuple[0]
                print(tuple,'elev: ',p_tuple[0])
        elif param == params[2]:
            if (tuple) in keys:
                p_tuple = preset_dict[tuple]
                sph_coord[2] = p_tuple[0]
                print(tuple,'dist: ',p_tuple[0])
               
        elif param == params[3]:
            if (tuple) in keys:
                p_tuple = preset_dict[tuple]
                end_loc = len(p_tuple)-5
                spk_name = str(p_tuple[0])[19:end_loc]
                print(tuple,spk_name)
        elif param == params[7]:
            if (tuple) in keys:
                p_tuple = preset_dict[tuple]
                print(tuple,p_tuple)
                print("speaker",i,sph_coord)
        else:
            if (tuple) in keys:
                p_tuple = preset_dict[tuple]
                print(tuple,p_tuple[0])
                    
    
"""
retrieve list of speaker models in assets file
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

