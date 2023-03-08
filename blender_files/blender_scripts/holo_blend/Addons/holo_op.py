import bpy
import os
import json
import sys
import math
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty
from bpy.types import Operator

class HOLO_OT_import_spk(Operator):
    bl_idname = "scene.add_spk_from_hol"
    bl_label = "Apply All"
    bl_description = "apply blabla"

    @classmethod
    def poll(cls, context):
        obj = context.object

        if obj is not None:
            if obj.mode == "OBJECT":
                return True
        return False

    def execute(self, context):
        for obj in bpy.context.scene.objects:
            if "spk" in obj.name:
                bpy.data.objects[obj.name].select_set(True)
                print(obj.name, ' deleted')
                bpy.ops.object.delete()
                for block in bpy.data.meshes:
                    if block.users == 0:
                        bpy.data.meshes.remove(block)
                for block in bpy.data.materials:
                    if block.users == 0:
                        bpy.data.materials.remove(block)
        
        
        assets_file_path_rel = '//Assets/amadeus.blend'
        assets_file_path = bpy.path.abspath(assets_file_path_rel)
        coord_conv_file_path_rel = '//scripts/coord_conversion.py'
        coord_convert_file = bpy.path.abspath(coord_conv_file_path_rel)
        sys.modules['coord_conv'] = bpy.data.texts['coord_conversion.py'].as_module()
        from coord_conv import sph2cart
        inner_path = 'Object



        return {'FINISHED'}