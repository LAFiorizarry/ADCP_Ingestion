# -*- coding: utf-8 -*-
"""
Created on Mon May 20 16:30:16 2019

@author: Laura.Fiorentino
"""
import numpy as np


def rotate_sidelooker(v1_array, v2_array, rot_angle):
    """ Applies x axis rotation to adcp current data to go from sensor
    oriented to True North"""
    c = np.cos(rot_angle * np.pi/180)
    s = np.sin(rot_angle * np.pi/180)
    v1_array_rot = v1_array * c - v2_array * s
    v2_array_rot = v1_array * s + v2_array * c
    return v1_array_rot, v2_array_rot


def rotate_bottom(v1_array, v2_array, mag_dec):
    """ Applies magnetic declination to adcp current data to go from ENU
    oriented to True North"""
    c = np.cos(mag_dec * np.pi/180)
    s = np.sin(mag_dec * np.pi/180)
    v1_array_rot = v1_array * c - v2_array * s
    v2_array_rot = v1_array * s + v2_array * c
    return v1_array_rot, v2_array_rot
