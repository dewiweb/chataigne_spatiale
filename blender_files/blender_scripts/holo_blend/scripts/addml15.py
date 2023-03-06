import bpy
import os
 
file_path_rel = '//Assets/amadeus.blend'

print(bpy.path.abspath(file_path_rel))
file_path = bpy.path.abspath(file_path_rel)

inner_path = 'Object'
object_name = 'ML 15'
 
bpy.ops.wm.append(
    directory=os.path.join(file_path, inner_path),
    filename=object_name
    )

for obj in bpy.context.selected_objects:
    obj.name = "speaker"
    obj.data.name = "speaker"

