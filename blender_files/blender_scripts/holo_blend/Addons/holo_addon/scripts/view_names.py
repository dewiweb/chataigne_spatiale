'''
Just a show/hide name of objects function called by a booleean AN
'''
objects = [obj.name for obj in bpy.context.scene.objects]
for x in objects:
    ob = bpy.data.objects[x]
    ob.show_name = show_hide