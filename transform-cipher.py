#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 23:31:52 2017

@author: eckart
"""

import ironpipe
import gnupg

#
# Encrypt/decrypt files using gpg
#

#
# 
def encrypt_file(input, output, secret):
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
def decrypt_file(input, output, secret):
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
    'encrypt': encrypt_file,
    'decrypt': decrypt_file
}

#
#
def cipher():
    '''
    '''
    action = ironpipe.get_config('action')
    secret = ironpipe.get_config('secret')
    
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
    return cipher()

if __name__ == '__main__':
    main()
    

