import bpy

from bpy.types import Panel


class HOLO_PT_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "HOLO"
    bl_category = "Holophonix Utils"
    
    def draw(self, context):
        
        layout = self.layout
        scene = context.scene
        scene['hol_filepath'] = "choose *.hol file"

        row = layout.row()
        col = row.column()
        col.operator("scene.add_spk_from_hol", text="Clear Speakers")

    #    col = row.column()
    #    col.operator("object.cancel_all_mods", text="Cancel All")
        row = layout.row()
        col = row.column()
        row.operator("holo.import_hol", text="", icon = "FILEBROWSER")
        row.prop(context.scene,'["hol_filepath"]')
