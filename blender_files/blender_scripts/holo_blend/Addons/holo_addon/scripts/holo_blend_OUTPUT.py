''' 
    example of script creating a json file (importable in nodeOSC panel) containing :
        
     -message handlers controlling x,y,z coordinates (and other stuffs) 
     of all objects in scene with 'track' string in their names.
     
     -message handlers using internal texts declared functions.
       
'''
import bpy
import json
import os
from math import sqrt

tofile_datas = ''
datawrited = ''
last_file_datas = ''
default_path = os.path.expanduser("~")
default_path = default_path.replace(os.sep, '/')
default_path = default_path + "/Documents/blender3d" #here declare the folder where you want to save your file
file_name= os.path.join(default_path,"holo_blend_OUTPUT.json") #here choose the name of your file

objects = [obj.name for obj in bpy.context.scene.objects]
matching = [s for s in objects if "track" in s]
for x in matching:
    ob = bpy.data.objects[x]
    index = ((ob.name).split('.'))[1]
    id = int(index) 
    tofile_datas =  tofile_datas + '"/track/' + str(id) + '/x": {"data_path": "bpy.data.objects[\'' + ob.name +'\'].matrix_world.translation[0]","osc_type": "f","osc_index": "()","osc_direction": "OUTPUT","filter_repetition": false,"dp_format_enable": false,"dp_format": "args","loop_enable": false,"loop_range": "0, length, 1","enabled": true},"/track/' + str(id) + '/y": {"data_path": "bpy.data.objects[\'' + ob.name +'\'].matrix_world.translation[1]","osc_type": "f","osc_index": "()","osc_direction": "OUTPUT","filter_repetition": false,"dp_format_enable": false,"dp_format": "args","loop_enable": false,"loop_range": "0, length, 1","enabled": true},"/track/' + str(id) + '/z": {"data_path": "bpy.data.objects[\'' + ob.name +'\'].matrix_world.translation[2]","osc_type": "f","osc_index": "()","osc_direction": "OUTPUT","filter_repetition": false,"dp_format_enable": false,"dp_format": "args","loop_enable": false,"loop_range": "0, length, 1","enabled": true},"/track/' + str(id) + '/color": {"data_path": "bpy.data.objects[\'' + ob.name +'\'].color","osc_type": "f","osc_index": "(0,1,2,3)","osc_direction": "INPUT","filter_repetition": false,"dp_format_enable": false,"dp_format": "args","loop_enable": false,"loop_range": "0, length, 1","enabled": true},"/track/' + str(id) + '/name": {"data_path": "bpy.data.objects[\'' + ob.name +'\'].name","osc_type": "s","osc_index": "(0)","osc_direction": "INPUT","filter_repetition": false,"dp_format_enable": false,"dp_format": "args","loop_enable": false,"loop_range": "0, length, 1","enabled": false},'

tofile_datas = '"/dump": {"data_path": \"exec(\\"f=bpy.data.texts[\'holo_in\'].as_module()' + '\\\\n' + 'f.dump(\'{0}\',\'{1}\')\\")\", "osc_type": "f", "osc_index": "()", "osc_direction": "INPUT", "filter_repetition": false, "dp_format_enable": true, "dp_format": "address, args[0]", "loop_enable": false, "loop_range": "0, length, 1", "enabled": false}, "/track/*": {"data_path": \"exec(\\"f=bpy.data.texts[\'holo_in\'].as_module()' + '\\\\n' + 'f.track(\'{0}\',\'{1}\')\\")\", "osc_type": "f", "osc_index": "()", "osc_direction": "INPUT", "filter_repetition": false, "dp_format_enable": true, "dp_format": "address, str(args).replace(\\"\'\\",\\"\\")", "loop_enable": false, "loop_range": "0, length, 1", "enabled": false},"/frames/str": {"data_path": \"exec(\\"f=bpy.data.texts[\'reaperTC\'].as_module()' + '\\\\n' + 'f.tc_to_frames(\'{0}\')\\")\", "osc_type": "f", "osc_index": "()", "osc_direction": "INPUT", "filter_repetition": false, "dp_format_enable": true, "dp_format": "args", "loop_enable": false, "loop_range": "0, length, 1", "enabled": true},' + tofile_datas
with open(file_name, "w") as write_file:
    print('datas2 : ', tofile_datas)
    write_file.write(tofile_datas)
file = open(file_name, 'r')
datawrited = file.read()
print('datawrited',datawrited)
datawrited = datawrited[:-1]
last_file_datas = '{'+ datawrited +'}'
with open(file_name, "w") as write_file:
    write_file.write(last_file_datas)
