#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 11:32:41 2017

@author: eckart 
"""

import ironpipe
import sys
import graphene
import stripe

stripe.api_key = "sk_test_..."

# list charges
stripe.Charge.list()

# retrieve single charge
stripe.Charge.retrieve("ch_1A2PUG2eZvKYlo2C4Rej1B9d")

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
def get_secret(secret, type):
    '''
    Validate secrect structure and return secret value(s)
    
    {
         "resource": "secret",
         "name":     "secret-name",
         "type":     'token',
         "config": {
             "token": '...'
         }
     }
    '''
    type = type.lower()
    
    if not secret:
        ironpipe.exit('Missing secret resource.')
        
    secret_type = secret.get('type')
        
    if not secret_type or secret_type.lower() != type:
        ironpipe.exit('Secret resource type must be {}.'.format(type))
        
    config = secret.get('config')
    
    if not config:
        ironpipe.exit('Missing secret config parameters.')
        
    if type == 'token':       
        return config.get('token')
    elif type == 'basic':
        return (config.get('username'), config.get('password'))
    elif type == 'aws-key`':
        return (config.get('access_key_id'), config.get('secret_access_key'))
    else:
        ironpipe.exit('Unknown secret resource type {}.'.format(type))        

#
#
def query_stripe():
    '''
    '''
    query = ironpipe.get_config('query')
    secret = ironpipe.get_config('secret')
        
    if not query:
        ironpipe.exit('Missing query configuration.')

        
    stripe.api_key = get_secret(secret, 'token')


# list charges
stripe.Charge.list()

# retrieve single charge
stripe.Charge.retrieve("ch_1A2PUG2eZvKYlo2C4Rej1B9d")

    

        
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

