import bpy
from bpy.types import Operator
from bpy.utils import register_class, unregister_class

class DEMORACK_OT_AddNewStandoff(Operator):
    """adds standoff to test add-on registered ok"""
    bl_idname = 'scene.add_new_standoff'
    bl_label = 'New Standoff'
    bl_options = { "REGISTER", "UNDO" }

    def execute(self, context):
        name = "Standoff"
        standoff = context.scene.Standoff # <- set in standoff_props.register()
        collection = context.scene.collection

        obj = bpy.data.objects.new(name, standoff.mesh)

        collection.objects.link(obj)
        obj.select_set(True)
        context.view_layer.objects.active = obj

        return { "FINISHED" }

def register():
    register_class(DEMORACK_OT_AddNewStandoff)

def unregister():
    unregister_class(DEMORACK_OT_AddNewStandoff)