#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ironpipe PNG connector
"""
import ironpipe as ip
import PIL
import sys

def main():
    try:
        # read file meta data and file
        image = PIL.open(ip.connector.input_file)
        info = ip.connector.input_file.metadata

    except:
        return ip.connector.error('bad image file')

    # update file metadata
    info['content-type'] = 'image/png'
    info['width'] = image.width
    info['height'] = image.height

    try:
        # write meta data into stream
        io.connector.output_file.metadata = info
        # push image back into stream
        image.save(ip.connector.output_file, 'PNG')
    except:
        return ip.connector.error('write error')

    return 0

if __name__ == '__main__':
    sys.exit(main())
