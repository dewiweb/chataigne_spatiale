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

        row = layout.row()
        col = row.column()
        col.operator("scene.add_spk_from_hol", text="Apply All")

    #    col = row.column()
    #    col.operator("object.cancel_all_mods", text="Cancel All")
        row = layout.row()
        col = row.column(align=True)
        col.operator("holo.import_hol", text="Choose *.hol file")

        row = layout.row()
        col = row.column()
        col.prop(context.scene,'["hol_filepath"]')
