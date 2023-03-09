from bpy.types import Panel
from bpy.utils import register_class, unregister_class

class DemoRackPanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DemoRack"

class StandoffPanel(DemoRackPanel, Panel):
    bl_idname = "DEMORACK_PT_standoff_panel"
    bl_label = "Standoff"

    def draw(self, context):
        layout = self.layout
        standoff_data = context.scene.Standoff # <- set in standoff_props.register()

        layout.operator("scene.add_new_standoff") # <- registered in standoff_operator.py
        layout.prop(standoff_data, "metric_diameter")
        layout.prop(standoff_data, "height")

def register():
    register_class(StandoffPanel)

def unregister():
    unregister_class(StandoffPanel)