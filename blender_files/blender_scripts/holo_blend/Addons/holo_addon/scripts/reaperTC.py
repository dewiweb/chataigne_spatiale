'''
A script called by an OSC handler to 'synchronise' blender to reaper!
A bit choppy....
'''
import bpy
def tc_to_frames(args):
    tc_str = args.split(':')
    bpy.data.scenes["Scene"].frame_current=(int(tc_str[0])*90000+int(tc_str[1])*1500+int(tc_str[2])*25+int(tc_str[3]))