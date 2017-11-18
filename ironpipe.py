#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 13:10:44 2017
@author: eckart

Ironpipe python library

The Ironpipe Python library provides a number of helper functions that simplify 
interaction with the command line arguments and environment variables. 
Extensions do not need to use the Ironpipe library. 

get_resource(arg=None)
	A dictionary containing the parsed name / value pairs of the --resource 
    argument. 
    
get_config(arg=None)
    A dictionary containg the parsed name / value pairs of the 'config'
    part of the --resource element, or parsed value of the --config argument

get_metadata(arg=None)
    Returns dictionary containing the name/value pairs of any metadata 
    associated with input stream. This function is a shortcut for 
    parsing $IRONPIPE_INPUT_METADATA.

set_metadata(name, value)
    Update the metadata for any data written to the output stream. This 
    function is a shortcut for writing a JSON string into 
    `$IRONPIPE_OUTPUT_METADATA`.

exit([error_message])
    Terminate execution either successfully (return 0 or no argument) or 
    with error error_message. This function is a shortcut for writing 
    error_message to stderr and then calling the exit() function with either 
    a SUCCESS or FAILURE status.
"""

import sys
from os import environ 
import json
import argparse

# Define system contants
RESOURCE_ARG_STRING = '--resource'
CONFIG_ARG_STRING = '--config'
IRONPIPE_INPUT_METADATA = 'IRONPIPE_INPUT_METADATA'
IRONPIPE_OUTPUT_METADATA = 'IRONPIPE_OUTPUT_METADATA'

#
# 
def parse_args():
    '''
    '''
    parser = argparse.ArgumentParser(description='Run Ironpipe Extension.')
    parser.add_argument(RESOURCE_ARG_STRING, default=None)
    parser.add_argument(CONFIG_ARG_STRING, default=None)
    args = parser.parse_args()
    
    resource = args.resource
    config = args.config
    
    # Try to parse passed JSON strings
    if resource:
        try:
            resource = json.loads(resource)
        except:
            resource = None
    if config:
        try:
            config = json.loads(config)
        except:
            config = None            
        
    # If both resource and config are defined, config overrides resource
    if resource and config:
        resource['config'] = config
    # else if only resource is defined, extract 'config' arguments
    elif resource:
        config = resource.get('config')
                
    return resource, config

#
#
def get_resource(arg=None):
    '''
    returns: Either a dictionary containing the parsed name / value pairs of 
        the --resource argument or the value of 'arg'. Returns None if no 
        argument was passed or the JSON could not be parsed.
    '''
    resource, config = parse_args()

    if resource and arg:
        return resource.get(arg)
    else:
        return resource

#
#
def get_config(arg=None):
    '''
    <arg>: 
    returns: Either a dictionary containing the parsed name / value pairs of 
        the 'config' dictionary argument or the value of 'arg'. Returns 
        None if no argument was passed or the JSON could not be parsed.
    '''
    resource, config = parse_args()

    if config and arg:
        return config.get(arg)
    else:
        return config

#
#
def read_metadata_from_variable(variable):
    '''
    Helper function that parses JSON string from environ variable 'variable'
    '''
    metadata = environ.get(variable)

    if metadata:
        try:
            metadata = json.loads(metadata)
        except:
            metadata = None

    return metadata

#
#    
def get_metadata(arg=None):
    '''
    Returns either a dictionary containing the name/value pairs of any metadata 
    associated with the input stream or the value of 'arg'. This function is a 
    shortcut for parsing `$IRONPIPE_INPUT_METADATA`. Returns None if the 
    variable has not been set the JSON string could not be parsed.
    '''
    metadata = read_metadata_from_variable(IRONPIPE_INPUT_METADATA)

    # if a arg was specified, return the value of arg
    if metadata and arg:
        metadata = metadata.get(arg)
            
    return metadata

#
#    
def set_metadata(name, value):
    '''
    Update the metadata for any data written to the output stream. This 
    function is a shortcut for writing a JSON string into 
    `$IRONPIPE_OUTPUT_METADATA`.
    '''
    metadata = read_metadata_from_variable(IRONPIPE_OUTPUT_METADATA)
    
    if metadata is None:
        metadata = {}
    
    # Add new attribute or update value    
    metadata[name] = value
    
    # Write update metadata values back into environ variable as JSON string
    metadata_json = json.dumps(metadata)
    environ[IRONPIPE_OUTPUT_METADATA] = metadata_json

    return metadata
    
    
#
#
def exit(error_message):
    '''
    Terminate execution either successfully (return 0 or no argument) or with
    `error error_message`. This function is a shortcut for writing
    `error_message` to `stderr` and then calling the `exit()` function with
    either a `SUCCESS` or `FAILURE` status.
    '''
    if error_message:
        sys.stderr.write(error_message)
        sys.stderr.flush()
        sys.exit(1)
    else:
        sys.exit(0)
    
    
