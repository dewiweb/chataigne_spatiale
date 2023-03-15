import bpy
import os

inner_path = 'NodeTree'
file_path = '/home/dewi/Github/chataigne_spatiale/blender_files/blender_scripts/holo_blend/holo_python_queue.blend'
name = 'AN Tree'
bpy.ops.wm.append(
            directory=os.path.join(file_path, inner_path),
            filename=name
            ) 