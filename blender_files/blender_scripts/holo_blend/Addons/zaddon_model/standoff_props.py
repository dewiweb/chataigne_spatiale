from bpy.props import PointerProperty, FloatProperty
from bpy.types import Mesh, PropertyGroup, Scene
from bpy.utils import register_class, unregister_class
from .standoff_mesh import Standoff

def prop_methods(call, prop=None):
    def getter(self):
        try:
            value = self[prop]
        except:
            set_default = prop_methods("SET", prop)
            set_default(self, self.defaults[prop])
            if hasattr(self, "on_load"):
                self.on_load()
            value = self[prop]
        finally:
            return value

    def setter(self, value):
        self[prop] = value

    def updater(self, context):
        self.update(context)

    methods = {
        "GET": getter,
        "SET": setter,
        "UPDATE": updater,
        }

    return methods[call]

class PG_Standoff(PropertyGroup):
    metric_diameter: FloatProperty(
        name="Inner Diameter (Metric)",
        min=2,
        max=5,
        step=50,
        precision=1,
        set=prop_methods("SET", "metric_diameter"),
        get=prop_methods("GET", "metric_diameter"),
        update=prop_methods("UPDATE"))
    height: FloatProperty(
        name="Standoff Height",
        min=2,
        max=6,
        step=25,
        precision=2,
        set=prop_methods("SET", "height"),
        get=prop_methods("GET", "height"),
        update=prop_methods("UPDATE"))
    mesh: PointerProperty(type=Mesh)

    defaults = { "metric_diameter": 2.5, "height": 3 }

    standoff = Standoff()

    def on_load(self):
        if self.height and self.metric_diameter:
            self.__set_mesh()

    def update(self, context):
        self.__set_mesh()

    def __set_mesh(self):
        self.mesh = self.standoff.mesh(self.height, self.metric_diameter)

def register():
    register_class(PG_Standoff)
    Scene.Standoff = PointerProperty(type=PG_Standoff)

def unregister():
    unregister_class(PG_Standoff)
    del Scene.Standoff