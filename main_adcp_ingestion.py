# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 10:36:57 2019

@author: Laura.Fiorentino

This is will convert ADCP raw data to pufff files.
As of 5/30/2019 this will only go from ADCP ascii created from AquadoppPro or
AWACAST to puff. Later modules will convert raw binary to ascii first.

"""

import argparse
import os
import sys
from adcp_ingestion_code.write_nortek_ascii_pufff import write_nortek_ascii_pufff


def adcp_conversion(station_information, file):
    """ converts raw adcp to pufff. For now needs ascii"""
    if station_information['adcp_type'] in [5, 6]:
#        awac_wpr_ascii(station_information)
        write_nortek_ascii_pufff(station_information, file)
    else:  # future instruments
        sys.exit()


def read_locat(file):
    """ reads relevant information from the locat file"""
#    global station_information
    station_info = {}
    with open(os.path.join(file.directory, file.filename + '.locat')) as locat:
        for line in locat:
            if 'station id' in line:
                station_info['station_id'] = line.split()[:-2][0]
            elif 'station name' in line:
                station_info['station_name'] = ' '.join(line.split()[:-2])
            elif 'adcp type' in line:
                station_info['adcp_type'] = int(line.split()[0])
            elif 'compass deviation' in line:
                station_info['compass_deviation'] = float(line.split()[1])
    station_info['ports_name'] = 'NOAA/NOS PORTS'  # not sure if this changes
    print('Station Name: {} and Station ID: {}\n'.
          format(station_info['station_name'], station_info['station_id']))
    return station_info


def parse_cmd_arguments():
    '''
    Parse command line arguments
    '''
    parser = argparse.ArgumentParser(description='Get input files')
    parser.add_argument('-f', '--filename', help='input file, no extension',
                        required=True)
    parser.add_argument('-d', '--directory', help='full directory of files',
                        required=True)
    return parser.parse_args()


if __name__ == '__main__':
    print('---------- Convert Nortek Files------------')
    print('WARNING: Currently (as of 5/30/2019), this will only accept '
          'ascii files created with AquadoppPro or AWACAST. Module to '
          'convert directly from raw WPR files will be implemented in the '
          'future.\n')
    args = parse_cmd_arguments()
    print('Processing {}\n'.format(os.path.join(args.directory,
                                                args.filename)))
    adcp_conversion(read_locat(args), args)
    print('Puff file created: {}'.format(os.path.join(args.directory,
                                                      args.filename + '.txt')))
