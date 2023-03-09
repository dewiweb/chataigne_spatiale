import bpy


from bpy.types import PropertyGroup
from bpy.props import (StringProperty, BoolProperty, IntProperty,
                       FloatProperty, EnumProperty, PointerProperty)


class PG_myProperties(PropertyGroup):
    file_path: StringProperty(name="File path",
                               description="Some elaborate description",
                               default="*.hol",
                               maxlen=1024,
                               subtype="FILE_PATH")
    my_bool = BoolProperty(
        name="Enable or Disable",
        description="A bool property",
        default=False
    )

    my_int = IntProperty(
        name="Int Value",
        description="A integer property",
        default=23,
        min=10,
        max=100
    )

    my_float = FloatProperty(
        name="Float Value",
        description="A float property",
        default=23.7,
        min=0.01,
        max=30.0
    )

    my_string = StringProperty(
        name="User Input",
        description=":",
        default="",
        maxlen=1024,
    )

    my_enum = EnumProperty(
        name="Dropdown:",
        description="Apply Data to attribute.",
        items=[('OP1', "Option 1", ""),
               ('OP2', "Option 2", ""),
               ('OP3', "Option 3", ""),
               ]
    )
