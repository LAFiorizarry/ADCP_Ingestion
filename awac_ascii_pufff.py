# -*- coding: utf-8 -*-
"""
Created on Wed May  8 15:45:50 2019

@author: Laura.Fiorentino
"""
import sys
import numpy as np
import os
from read_ascii_awac_aquadopp import (read_header, read_sen, read_data2D,
                                      read_data3D)
from rotations import rotate_sidelooker, rotate_bottom


def write_awac_ascii_pufff(directory, filename, station_name, station_id,
                           ports_name, dimension, mag_dec, rot_angle):
    """ This function writes the pufff file """

    # get header data from .hdr
    try:
        num_cells, num_meas = read_header(directory, filename)
    except OSError as ex:
        print(ex)
        sys.exit()

    DQA = '00000000000000000000000000000000'  # not sure what this needs to be
    DQAC = '000'  # not sure what this needs to be

    # get data from sen file
    try:
        header_array = read_sen(directory, filename)
    except OSError as ex:
        print(ex)
        sys.exit()

    # get data from a1 a2 a3 v1 v2 v3
    if dimension is '2':
        try:
            a1_array, a2_array, v1_array, v2_array = \
                read_data2D(directory, filename)
        except OSError as ex:
            print(ex)
            sys.exit()
        a3_array = np.ones(shape=np.shape(a1_array))*-999
        v3_array = np.ones(shape=np.shape(a1_array))*-999
    else:
        try:
            a1_array, a2_array, a3_array, v1_array, v2_array, \
                v3_array = read_data3D(directory, filename)
        except OSError as ex:
            print(ex)
            sys.exit()

    # rotate data from v1,v2,v3
    if dimension is '2':
        v1_array_ro, v2_array_ro = rotate_sidelooker(v1_array, v2_array,
                                                     rot_angle)
    else:
        v1_array_ro, v2_array_ro, v3_array_ro = rotate_bottom(v1_array,
                                                              v2_array,
                                                              v3_array,
                                                              mag_dec)

    # compute other values from data
    speed_array = np.sqrt(v1_array**2 + v2_array**2)
    direction_array = np.sqrt(v1_array**2 + v2_array**2)

    # empty arrays
    std_beam1_array = np.ones(shape=np.shape(a1_array))*-999
    std_beam2_array = np.ones(shape=np.shape(a1_array))*-999
    std_beam3_array = np.ones(shape=np.shape(a1_array))*-999
    water_temp_array = np.ones(shape=np.shape(a1_array))*-999
    DQA_array = np.zeros(shape=np.shape(a1_array))

    # write pufff file
    with open(os.path.join(directory, filename + '.txt'), 'a') as puff_file:
        for n in range(num_meas):
            puff_file.write("{}\n".format(ports_name))
            puff_file.write("ZZZ0001 {} - {}\n\n".
                            format(station_id, station_name))
            puff_file.write("{:.0f} {:.0f} {:.0f} {:.0f} {:.0f} {} {} {}\n".
                            format(header_array[n][2],  # year
                                   header_array[n][0],  # month
                                   header_array[n][1],  # day
                                   header_array[n][3],  # hour
                                   header_array[n][4],  # min
                                   num_cells,           # num of current bins
                                   DQA,                 # DQA
                                   DQAC))               # DQCC
            puff_file.write("{:.0f} {:.0f} {:.0f} {:.0f} {:.0f} {:.0f} {:.0f} "
                            "{:.0f} {:.0f} {:.0f} {:.0f} {:.0f} {:.0f}\n".
                            format(header_array[n][10]*10,   # heading *10
                                   header_array[n][11]*10,   # pitch *10
                                   header_array[n][12]*10,   # roll *10
                                   header_array[n][14]*100,  # temp *100
                                   header_array[n][13]*100,  # pressure *100
                                   header_array[n][10]*10,   # std heading *10
                                   -999,   # std pitch *10
                                   -999,   # std roll *10
                                   -999,  # std temp *100
                                   -999,  # std pressure *100
                                   header_array[n][9]*10,    # sound speed *10
                                   -999,  # pressure sensor offset
                                   -999))  # pressure sensor scale
            new_array = np.zeros(shape=(num_cells, 14))
            new_array[:, 0] = range(num_cells+1)[1:]
            new_array[:, 1] = v1_array[n, :]*1000
            new_array[:, 2] = v2_array[n, :]*1000
            if dimension is '3':
                new_array[:, 3] = v3_array[n, :]*1000
            else:
                new_array[:, 3] = v3_array[n, :]  # should be -999
            new_array[:, 4] = direction_array[n, :]
            new_array[:, 5] = speed_array[n, :]*1000
            new_array[:, 6] = a1_array[n, :]
            new_array[:, 7] = a2_array[n, :]
            new_array[:, 8] = a3_array[n, :]  # should be -999
            new_array[:, 9] = std_beam1_array[n, :]  # should be -999
            new_array[:, 10] = std_beam2_array[n, :]  # should be -999
            new_array[:, 11] = std_beam3_array[n, :]  # should be -999
            new_array[:, 12] = water_temp_array[n, :]  # should be -999
            new_array[:, 13] = DQA_array[n, :]
            np.savetxt(puff_file, new_array, fmt='%-6.0f')
