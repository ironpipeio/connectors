#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ironpipe JPEG connector
"""
import ironpipe
import PIL
import sys

def main():
    try:
        # read file meta data and file
        info = ironpipe.connector_read_metadata(sys.stdin)
        image = PIL.open(sys.stdin)
    except:
        return ironpipe.connector_error('bad image file')

    # update file metadata
    info['content-type'] = 'image/jpeg'
    info['width'] = image.width
    info['height'] = image.height

    try:
        # write meta data into stream]
        ironpipe.connector_write_metadata(sys.stdout, info)
        # push image back into stream
        image.save(sys.stdout, 'JPEG')
    except:
        return ironpipe.connector_error('write error')

    return 0

if __name__ == '__main__':
    # Remove program name from command line arguments
    sys.exit(main())
