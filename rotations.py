# -*- coding: utf-8 -*-
"""
Created on Mon May 20 16:30:16 2019

@author: Laura.Fiorentino
"""
import numpy as np


def rotate_nortek(v1_array, v2_array, rot_angle):
    """ Applies x axis rotation to adcp current data to go from sensor
    oriented to True North  OR applies magnetic declination to go from
    ENU to True North"""
    c = np.cos(rot_angle * np.pi/180)
    s = np.sin(rot_angle * np.pi/180)
    v1_array_rot = v1_array * c - v2_array * s
    v2_array_rot = v1_array * s + v2_array * c
    return v1_array_rot, v2_array_rot


def calculate_magnitude(v1_array_rot, v2_array_rot):
    """calculate magnitude from u & v"""
    mag = np.sqrt(np.power(v1_array_rot, 2) + np.power(v2_array_rot, 2))
    return mag


def calculate_direction(v1_array_rot, v2_array_rot):
    """calculate direction from u & v"""
    direction = np.arctan2(v2_array_rot, v1_array_rot) * 180 / np.pi
    direction = np.array(direction)
    direction = 90 - direction
    direction[direction < 0] += 360
    return direction
