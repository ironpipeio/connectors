#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 15:22:32 2017

@author: eckart
"""

from PIL import Image
import sys
import ironpipe.extension

IMAGE_FILE_TYPES = {'JPEG', 'PNG', 'GIF'}


#
#
def transform_image():
    '''
    Transforms jpg, png, and gif images to jpg, png, and gif images
    If input format and output format are not specified, simply copies
    file without parsing. Both input and output must be specified.
    '''

    # Read and validate image input format
    input = ironpipe.extension.get_config('input')
    if input:
        input = input.upper()
    if not input or input not in IMAGE_FILE_TYPES:
        image_types = ', '.join([i for i in IMAGE_FILE_TYPES])
        ironpipe.extension.exit("Required attribute 'input' must be one of: {}.".format(image_types))

    # Read and validate image output format
    output = ironpipe.extension.get_config('output')
    if output:
        output = output.upper()
    if not output or output not in IMAGE_FILE_TYPES:
        image_types = ', '.join([i for i in IMAGE_FILE_TYPES])
        ironpipe.extension.exit("Required attribute 'output' must be one of: {}.".format(image_types))

    compression = ironpipe.extension.get_config('compression')

    if compression is None:
        compression = 75

    try:
        # read image file in binary mode
        image = Image.open(sys.stdin.buffer)
    except Exception as err:
        ironpipe.extension.exit('Image read error: {}'.format(err))

    # Confirm that input file format matches input arg
    if image.format != input:
        ironpipe.extension.exit('Input not a {} file.'.format(input))

    # update file metadata
    ironpipe.extension.set_metadata('content-type', 'image/' + output)
    ironpipe.extension.set_metadata('width', image.width)
    ironpipe.extension.set_metadata('height', image.height)

    try:
        # push image back into stream in binary mode
        image.save(sys.stdout.buffer, output)
    except Exception as err:
        ironpipe.extension.exit('Image write error: {}'.format(err))

    return 0


#
#
def main():
    return transform_image()


if __name__ == '__main__':
    main()
