import bpy
import string
import numpy as np
from mathutils import *

def Extrinsic():
    bpy.context.screen.scene = bpy.data.scenes['Scene'] # changing scene 
    cam_loc = bpy.data.objects['Left_up_cam'].matrix_world
    bpy.context.screen.scene = bpy.data.scenes['Scene.001'] # changing scene 
    cam_loc1 = bpy.data.objects['Right_up_cam'].matrix_world

    tmp = np.asarray(cam_loc)
    rotCam = tmp[:3,:3]
    tranCam = tmp[0:3,3]
    tmp1 = np.asarray(cam_loc1)
    rotCam1 = tmp1[:3,:3]
    tranCam1 = tmp1[0:3,3]

    R = np.dot( np.transpose(rotCam), rotCam1 ) 
    T = tranCam1 - tranCam
 
    RT = np.zeros((4,4))
    RT[0:3,0:3]=R
    RT[0:3,3]=T
    RT[3][3] = 1
    
    #print('JH')
    #print(RT)
    return RT
	
	
	
