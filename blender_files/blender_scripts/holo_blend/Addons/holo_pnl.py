import bpy

from bpy.types import Panel

class Property_group(bpy.types.PropertyGroup):
    file_path: bpy.props.StringProperty(name="File path",
                                        description="Some elaborate description",
                                        default="",
                                        maxlen=1024,
                                        subtype="FILE_PATH")

class HOLO_PT_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "HOLO"
    bl_category = "Holophonix Utils"

    def draw(self, context):
        layout = self.layout
    
        row = layout.row()
        col = row.column()
        col.operator("scene.add_spk_from_hol", text="Apply All")
    
    #    col = row.column()
    #    col.operator("object.cancel_all_mods", text="Cancel All")
        row = layout.row()
        col = row.column(align=True)
        col.operator("scene.choose_hol_filepath", text="Choose hol file")
        col = row.column()
        col.prop(Property_group,'file_path', text="")