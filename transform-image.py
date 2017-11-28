#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 15:22:32 2017

@author: eckart
"""

import ironpipe
from PIL import Image
import sys

IMAGE_FILE_TYPES = {'JPEG', 'PNG', 'GIF'}

#
#
def transform_image():
    '''
    Transforms jpg, png, and gif images to jpg, png, and gif images
    If input format and output format are not specified, simply copies 
    file without parsing. Both input and output must be specified. 
    '''
    
    input = ironpipe.get_config('input')
    output = ironpipe.get_config('output')
    
    if not input or not output:
        ironpipe.exit('Need to specify input and output format.')

    input = input.upper()
    output = output.upper()

    if input not in IMAGE_FILE_TYPES or output not in IMAGE_FILE_TYPES:
        ironpipe.exit("Image format must be one of: {}.".format(IMAGE_FILE_TYPES))                
        
    compression = ironpipe.get_config('compression')
    if compression is None:
        compression = 75    

    try:
        # read image file in binary mode
        image = Image.open(sys.stdin.buffer)        
    except Exception as err:
        ironpipe.exit('Image read error: {}'.format(err))
    
    # Confirm that input file format matches input arg
    if image.format != input:
        ironpipe.exit('Input not a {} file.'.format(input))
                    
    # update file metadata
    ironpipe.set_metadata('content-type', 'image/' + output)
    ironpipe.set_metadata('width', image.width)
    ironpipe.set_metadata('height', image.height)

    try:
        # push image back into stream in binary mode
        image.save(sys.stdout.buffer, output)
    except Exception as err:
        ironpipe.exit('Image write error: {}'.format(err))

    
    return 0

#
#
def main():   
    return transform_image()

if __name__ == '__main__':
    main()
