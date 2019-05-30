# -*- coding: utf-8 -*-
"""
Created on Mon May 20 15:32:32 2019

@author: Laura.Fiorentino
"""
import os
import numpy as np


def read_header(directory, filename):
    """ This function reads the .hdr file for the number of bins
    and measurements"""
    with open(os.path.join(directory, filename + '.hdr'), 'r') as header_file:
        for line in header_file:
            if 'Number of measurements' in line:
                num_meas = int(line.split()[-1])
            elif 'Number of cells' in line:
                num_cells = int(line.split()[-1])
    return num_cells, num_meas


def read_sen(directory, filename):
    """ This function reads the .sen file for the header information"""

    header_array = np.loadtxt(os.path.join(directory, filename + '.sen'))
    return header_array


def read_data2D(directory, filename):
    a1_array = np.loadtxt(os.path.join(directory, filename + '.a1'))
    a2_array = np.loadtxt(os.path.join(directory, filename + '.a2'))
    v1_array = np.loadtxt(os.path.join(directory, filename + '.v1'))
    v2_array = np.loadtxt(os.path.join(directory, filename + '.v2'))
    return a1_array, a2_array, v1_array, v2_array


def read_data3D(directory, filename):
    a1_array = np.loadtxt(os.path.join(directory, filename + '.a1'))
    a2_array = np.loadtxt(os.path.join(directory, filename + '.a2'))
    a3_array = np.loadtxt(os.path.join(directory, filename + '.a3'))
    v1_array = np.loadtxt(os.path.join(directory, filename + '.v1'))
    v2_array = np.loadtxt(os.path.join(directory, filename + '.v2'))
    v3_array = np.loadtxt(os.path.join(directory, filename + '.v3'))
    return a1_array, a2_array, a3_array, v1_array, v2_array, v3_array
