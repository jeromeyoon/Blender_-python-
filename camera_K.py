import bpy
import string
import numpy as np
from mathutils import *

def get_calibration_matrix_K_from_blender(camd):
    f_in_mm = camd.lens
    scene = bpy.context.scene
    resolution_x_in_px = scene.render.resolution_x
    resolution_y_in_px = scene.render.resolution_y
    scale = scene.render.resolution_percentage / 100
    sensor_width_in_mm = camd.sensor_width
    sensor_height_in_mm = camd.sensor_height
    aspect_ratio = scene.render.pixel_aspect_x / scene.render.pixel_aspect_y
    # the sensor width is fixed, the sensor height is effectively changed with the
    # aspect ratio
    s_u = resolution_x_in_px * scale / sensor_width_in_mm
    s_v = resolution_y_in_px * scale * aspect_ratio / sensor_height_in_mm

    # Parameters of intrinsic calibration matrix K
    alpha_u = f_in_mm * s_u
    alpha_v = f_in_mm * s_v
    u_0 = resolution_x_in_px * scale / 2
    v_0 = resolution_y_in_px * scale / 2
    skew = 0 # only use rectangular pixels
    K = Matrix(((alpha_u, skew,    u_0),(0, alpha_v, v_0),  ( 0  , 0,  1 )))
    return K