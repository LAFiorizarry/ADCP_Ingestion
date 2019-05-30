# -*- coding: utf-8 -*-
"""
Created on Mon May 20 16:30:16 2019

@author: Laura.Fiorentino
"""
import numpy as np


def rotate_sidelooker(v1_array, v2_array, rot_angle):
    c = np.cos(rot_angle)
    s = np.sin(rot_angle)
    rotation_matrix = np.matrix([[c, -s], [s, c]])
    


def rotate_bottom(v1_array, v2_array, v3_array, mag_dec):
    return 1
