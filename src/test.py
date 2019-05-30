# -*- coding: utf-8 -*-
"""
Created on Thu May 30 15:58:00 2019

@author: Laura.Fiorentino
"""

import aquadopp_ascii_pufff
filename = 'STX21a01'
station_name = 'Station Name'
station_id = 'Station ID'
ports_name = 'Ports Name'
dimension = '2'
mag_dec = '1'
rot_angle = '1'
directory = directory = 'C:/Users/Laura.Fiorentino/Documents/Projects/ADCP_Ingestion/STX1821/'
aquadopp_ascii_pufff.write_aquadopp_ascii_pufff(directory, filename, station_name, station_id,
                                        ports_name, dimension, mag_dec, rot_angle)
