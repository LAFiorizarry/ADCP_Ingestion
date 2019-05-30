# -*- coding: utf-8 -*-
"""
Created on Fri May  3 14:46:07 2019

@author: Laura.Fiorentino

This is will convert ADCP raw data to pufff files.
As of 5/30/2019 this will only go from ADCP ascii created from AquadoppPro or
AWACAST to puff. Later modules will convert raw binary to ascii first.
"""
import sys
# from awac_wpr_ascii import awac_wpr_ascii
from awac_ascii_pufff import write_awac_ascii_pufff


def awac_conversion():
    """ converts input awac file"""
    directory = input("Full directory of file for conversion>")
    filename = input("File name for conversion (no extension)>")
    station_id = input("Station ID>")
    station_name = input("Station Name>")
    ports_name = input("PORTS Name>")
    while True:
        dimension = input("[2] 2D sidelooker  or [3] 3D bottom/buoy mount ?")
        if dimension not in ('2', '3'):
            print('please type 2 or 3')
            continue
        else:
            break
    if dimension is '3':
        mag_dec = input("What is the magnetic declination?>")
        rot_angle = None
    elif dimension is '2':
        rot_angle = input("What is the x-axis correction angle?>")
        mag_dec = None
#    awac_wpr_ascii(filename)
    write_awac_ascii_pufff(directory, filename, station_name, station_id,
                           ports_name, dimension, mag_dec, rot_angle)


def aquadopp_conversion():
    """ converts input aquadopp file"""
#    directory = input("Full directory of file for conversion>")
#    filename = input("File name for conversion (no extension)>")
#    station_id = input("Station ID>")
#    station_name = input("Station Name>")
#    ports_name = input("PORTS Name>")
#    while True:
#        dimension = input("[2] 2D sidelooker  or [3] 3D bottom/buoy mount ?")
#        if dimension not in ('2', '3'):
#            print('please type 2 or 3')
#            continue
#        else:
#            break
#    if dimension is '3':
#        mag_dec = input("What is the magnetic declination?>")
#    elif dimension is '2':
#        rot_angle = input("What is the x-axis correction angle?>")
#    aquadopp_wpr_ascii(filename)
#    write_aquadopp_ascii_pufff(directory, filename, station_name, station_id,
#                           ports_name, dimension, mag_dec, rot_angle)

    sys.exit()


def signature_conversion():
    """ converts input signature file"""
#    filename = input("File name for conversion (no extension)>")
    sys.exit()


def quit_program():
    """ quits """
    sys.exit()


def main():
    """Main function, input file name and choose input file type"""
    print('---------- Convert Nortek Files------------')
    print('WARNING: Currently (as of 5/30/2019), this will only accept '
          'ascii files created with AquadoppPro or AWACAST. Module to '
          'convert directly from raw WPR files will be implemented in the '
          'future.')

    task_dict = {'1': awac_conversion, '2': aquadopp_conversion,
                 '3': signature_conversion, '4': quit_program}
    while True:
        task = input("Choose input file type: [1] AWAC; [2] Aquadopp "
                     "[3] Signature; [4] Quit>")
        try:
            task_dict[task]()
            break
        except KeyError:
            print('Error: Please choose 1-4')


if __name__ == '__main__':
    main()
