import bpy
import os
import json
import sys
import math
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty
from bpy.types import Operator

hol_file_ext = '.hol'
hol_file_path = ''


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
        
        

        inner_path = 'Object'



        return {'FINISHED'}
class HOLO_OT_hol_filechooser(Operator):
    bl_idname = "scene.choose_hol_filepath"
    bl_label = "Choose"
    bl_description = "choose a hol file for speakers import"
    
    @classmethod
    def poll(cls, context):
        obj = context.object

        if obj is not None:
            if obj.mode == "OBJECT":
                return True
        return False
    
    def execute(self, context):
        
        

        return {'FINISHED'}
    
class TEST_OT_import_tst(Operator, ImportHelper):
    bl_idname = 'test.import_tst'
    bl_label = 'test import test'
    bl_options = {'PRESET', 'UNDO'}
 
    filename_ext = '.hol'
    
    filter_glob: StringProperty(
        default='*.hol',
        options={'HIDDEN'}
    )
 
    def execute(self, context):
        print('imported file: ', self.filepath)
#        return str(self.filepath)
        return {'FINISHED'}