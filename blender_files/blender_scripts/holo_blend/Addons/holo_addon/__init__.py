# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Holophonix",
    "author" : "dewiweb",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Utils"
}

import bpy

from .holo_op import HOLO_OT_import_spk,HOLO_OT_hol_filechooser,TEST_OT_import_tst
from .holo_pnl import HOLO_PT_Panel
from .holo_props import PG_myProperties

classes = (PG_myProperties, HOLO_PT_Panel,HOLO_OT_import_spk, HOLO_OT_hol_filechooser,TEST_OT_import_tst)

def register():
    
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.my_props = bpy.props.PointerProperty(type = PG_myProperties)

        
def unregister():
    
    for c in classes:
        bpy.utils.unregister_class(c)
    del bpy.types.Scene.my_props

        