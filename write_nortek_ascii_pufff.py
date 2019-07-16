# -*- coding: utf-8 -*-
"""
Created on Mon May 20 15:49:27 2019

@author: Laura.Fiorentino
"""

import os
import sys
import numpy as np
from adcp_ingestion_code.read_ascii_awac_aquadopp import (read_header,
                                                          read_sen,
                                                          read_data2D,
                                                          read_data3D)
from adcp_ingestion_code.rotations import(rotate_nortek, calculate_magnitude,
                                          calculate_direction)


def write_nortek_ascii_pufff(station_information, file):
    """ This function writes the pufff file """

    # get header data from .hdr
    try:
        num_cells, num_meas = read_header(file.directory, file.filename)
    except OSError as ex:
        print(ex)
        sys.exit()

    DQA = '00000000000000000000000000000000'  # not sure what this needs to be
    DQAC = '000'  # not sure what this needs to be

    # get data from sen file
    try:
        header_array = read_sen(file.directory, file.filename)
    except OSError as ex:
        print(ex)
        sys.exit()

    # get data from a1 a2 a3 v1 v2 v3
    if station_information['adcp_type'] == 6:
        dimension = 2
        try:
            a1_array, a2_array, v1_array, v2_array = \
                read_data2D(file.directory, file.filename)
        except OSError as ex:
            print(ex)
            sys.exit()
        a3_array = np.ones(shape=np.shape(a1_array))*-999
        v3_array = np.ones(shape=np.shape(a1_array))*-999
    elif station_information['adcp_type'] == 5:
        dimension = 3
        try:
            a1_array, a2_array, a3_array, v1_array, v2_array, \
                v3_array = read_data3D(file.directory, file.filename)
        except OSError as ex:
            print(ex)
            sys.exit()
    else:
        print('wrong sensor type')
        sys.exit()
    # rotate or add magnetic declination
    try:
        v1_array_rot, v2_array_rot = rotate_nortek(v1_array, v2_array,
                                                   station_information
                                                   ['compass_deviation'])
    except Exception as ex:
        print(ex)
        sys.exit()

    # compute other values from data
    speed_array = calculate_magnitude(v1_array_rot, v2_array_rot)
    direction_array = calculate_direction(v1_array_rot, v2_array_rot)
    std_beam1_array = np.ones(shape=np.shape(a1_array))*-999
    std_beam2_array = np.ones(shape=np.shape(a1_array))*-999
    std_beam3_array = np.ones(shape=np.shape(a1_array))*-999
    water_temp_array = np.ones(shape=np.shape(a1_array))
    DQA_array = np.zeros(shape=np.shape(a1_array))

    # write pufff file
    with open(os.path.join(file.directory, file.filename + '.cu'),
              'a') as puff_file:
        for n in range(num_meas):
            puff_file.write("{}\n".format(station_information['ports_name']))
            puff_file.write("{} {}\n\n\n".
                            format(station_information['station_id'],
                                   station_information['station_name']))
            puff_file.write("{:6.0f} {:6.0f} {:6.0f} {:6.0f} {:6.0f} {:6.0f} "
                            "{:6.0f} {:6.0f} {:6.0f} {:6.0f} {:6.0f} {:10.0f} "
                            "{:10.0f}\n".
                            format(header_array[n][10]*10,   # heading *10
                                   header_array[n][11]*10,   # pitch *10
                                   header_array[n][12]*10,   # roll *10
                                   header_array[n][14]*100,  # temp *100
                                   header_array[n][13]*100,  # pressure *100
                                   -999,   # std heading *10
                                   -999,   # std pitch *10
                                   -999,   # std roll *10
                                   -999,  # std temp *100
                                   -999,  # std pressure *100
                                   header_array[n][9]*10,    # sound speed *10
                                   -999,  # pressure sensor offset
                                   -999))  # pressure sensor scale
            puff_file.write("{:5.0f} {:02.0f} {:02.0f} {:02.0f} {:02.0f} {} "
                            "{} {}\n".
                            format(header_array[n][2],  # year
                                   header_array[n][0],  # month
                                   header_array[n][1],  # day
                                   header_array[n][3],  # hour
                                   header_array[n][4],  # min
                                   num_cells,           # num of current bins
                                   DQA,                 # DQA
                                   DQAC))               # DQCC
            new_array = np.zeros(shape=(num_cells, 14))
            new_array[:, 0] = range(num_cells+1)[1:]
            new_array[:, 1] = v1_array_rot[n, :]*1000
            new_array[:, 2] = v2_array_rot[n, :]*1000
            if dimension == '3':
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
            new_array[:, 12] = water_temp_array[n, :] * header_array[n][14]*100  # should be -999
            new_array[:, 13] = DQA_array[n, :]
            current_format = '%4.0f' + 12*' %6.0f' + ' %032.0f'
            np.savetxt(puff_file, new_array, fmt=current_format)
