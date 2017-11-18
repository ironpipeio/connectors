#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 11:32:41 2017

@author: eckart 
"""

import ironpipe
import sys
import gzip

#
# 
def compress_file(input, output, compression):
    '''
    '''
    try:
        data = input.buffer.read()
    except Exception as err:
        ironpipe.exit('Data read error: {}'.format(err))

    try:
        data = gzip.compress(data, compresslevel=compression)
        output.buffer.write(data)     
    except Exception as err:
        ironpipe.exit('Data write error: {}'.format(err))
    
#
#
def decompress_file(input, output, compression):
    '''
    '''
    try:
        with gzip.open(input.buffer) as file:
            data = file.read()
    except Exception as err:
        ironpipe.exit('Data read error: {}'.format(err))

    try:
        output.buffer.write(data)     
    except Exception as err:
        ironpipe.exit('Data write error: {}'.format(err))

    
#
# map action appropriate function
#
ACTION_MAP_FUNCTIONS = {
    'compress':   compress_file,
    'decompress': decompress_file
}

#
#
def gzip_data():
    '''
    '''
    action = ironpipe.get_config('action')
    compressionlevel = ironpipe.get_config('compression')
    
    # Confirm that both input and output are set
    if not action:
        ironpipe.exit('Need to specify action.')
    else:
        action = action.lower()
        
    if compressionlevel:
        # If it is not an int, try to convert
        if not isinstance(compressionlevel, int):
            try: 
                compressionlevel = int(compressionlevel)
            except ValueError:
                ironpipe.exit('Compression level must be an integer.')
    else:
        compressionlevel = 9 # default compression level
        
    # Confirm that level is 0-9
    if not 0 <= compressionlevel <= 9:
        ironpipe.exit('Compression level must be 0-9.')

    # Confirm that action is known
    if action not in ACTION_MAP_FUNCTIONS:
        actions = ', '.join([i for i in ACTION_MAP_FUNCTIONS])
        ironpipe.exit("Action must be one of {}.".format(actions))              

    # Compress / uncompress data the input file        
    ACTION_MAP_FUNCTIONS[action](sys.stdin, sys.stdout, compressionlevel)

    return 0

#
#        
def main():   
    return gzip_data()

if __name__ == '__main__':
    main()

