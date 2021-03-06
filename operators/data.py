#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implements built-in 'data' operator

Resource: operator

Transformer resources receive data from a stream and write the
data back into the stream. Transformers support the following properties:

This operator either validates or transforms a data file from one format
into another format.

Supports the following config arguments:

    input (string) One of csv, tsv, json, xml. Required.
    output (string) One of csv, tsv, json, xml. Required.
    schema (object): A JSON-Schema configuration that selects
    the desired data from the input file. Fields can be specified by
    position or name. Optional.

Note that if input and output specify the same data type, the tranformer will
validate the input, but will then directly copy the input file to the output
"""

import sys
from collections import OrderedDict

import csv
import json
import xml.etree.ElementTree as ET

import ironpipe.extension

# Data is stored as and OrderedDict to preserve the column sequence

#
#
def read_json(file):
    '''
    returns: list of Dictionaries
    '''
    data = []

    try:
        data = json.load(file)
        if not isinstance( data, list): # Need to always return a list
            data = [data]
    except Exception as err:
        # Check if the file might be stored in JSONL (line) format
        file.seek(0)
        try:
            for line in file:
                data.append(json.loads(line))
        except Exception as err:
            ironpipe.extension.exit('Data read error: {}'.format(err))

    return data

#
#
def write_json(data, file):
    '''
    '''
    try:
        # Write data in JSONL format
        for row in data:
            json.dump(row, file)
            file.write('\n')

        ironpipe.extension.set_metadata('content-type', 'application/json')

    except Exception as err:
        exit('Data write error: {}'.format(err))


#
#
def isInt(v):
    try:
        i = int(v)
    except:
        return False
    return True


#
#
def isFloat(v):
    try:
        i = float(v)
    except:
        return False
    return True


#
# convert int and float to native python formats
def convert_data(row):
    '''
    '''
    for i, v in enumerate(row):
        if isInt(v):
            row[i] = int(v)
        elif isFloat(v):
            row[i] = float(v)

    return row


#
#
def read_csv(file, delimiter=','):
    '''
    '''
    data = []
    field_names = []

    try:
        has_header = csv.Sniffer().has_header(file.read(1024))
        file.seek(0)
    except Exception as err:
        ironpipe.extension.exit('Data read error: {}'.format(err))

    try:
        # read first line
        reader = csv.reader(file, delimiter=delimiter)
        first_row = next(reader)

        # if the first row is empty, we are done
        if first_row:
            # if we have a header row, the first values are the field names
            if has_header:
                field_names = first_row
            # Otherwise we generate the field names
            else:
                num_columns = len(first_row)
                for i in range(num_columns):
                    field_names.append('FIELD_' + str(i))

                # Reset to beginning of file since the first row was actually data
                file.seek(0)
                reader = csv.reader(file, delimiter=delimiter)

            for row in reader:
                converted_row = convert_data(row)
                data_row = OrderedDict(zip(field_names, converted_row))
                data.append(data_row)

    except Exception as err:
        ironpipe.extension.exit('Data read error line {}: {}'.format(reader.line_num, err))

    return data


#
#
def write_csv(data, file, delimiter=','):
    '''
    '''
    if not data:  # Make sure we have at least one record
        return

    header = []  # DectWriter needs a list of field names

    # Extract the header - we assume that all rows in the data have the same names
    for field in data[0]:
        header.append(field)

    # Set up the CSV dictionary writer
    writer = csv.DictWriter(file, fieldnames=header, delimiter=delimiter)

    try:
        writer.writeheader()  # Write header
        for row in data:  # Write all records
            writer.writerow(row)

        ironpipe.extension.set_metadata('content-type', 'text/csv')

    except Exception as err:
        ironpipe.extension.exit('Data write error: ' + str(err))


#
#
def read_tsv(file):
    '''
    Requires that CSV file has a header
    '''
    return read_csv(file, delimiter='\t')


#
#
def write_tsv(data, file, delimiter=','):
    '''
    '''
    write_csv(data, file, delimiter='\t')
    ironpipe.extension.set_metadata('content-type', 'text/tab-separated-values')


#
# Reads flat XML files
#
def read_xml(file):
    '''
    '''
    try:
        tree = ET.parse(file)
        root = tree.getroot()
    except Exception as err:
        ironpipe.extension.exit('Data read error: {}'.format(err))

    data = []

    for row in root:
        rowDict = OrderedDict()

        for key, value in row.attrib.items():
            rowDict[key] = value

        for column in row:
            rowDict[column.tag] = column.text

        data.append(rowDict)

    return data


#
# Writes flat XML file
def write_xml(data, file):
    '''
    '''
    print('<?xml version="1.0"?>\n<data>')

    for row in data:
        print('<row>')

        for field, value in row.items():
            print('<{}>{}</{}>'.format(field, value, field))

        print('</row>')
    print('</data>')

    ironpipe.extension.set_metadata('content-type', 'application/xml')


#
# map data type to read and write function
#
DATA_MAP_FUNCTIONS = {
    'json':  {'read': read_json,  'write': write_json},
    'csv':   {'read': read_csv,   'write': write_csv},
    'tsv':   {'read': read_tsv,   'write': write_tsv},
    'xml':   {'read': read_xml,   'write': write_xml}
}


#
#
def transform_data():
    '''
    '''
    input = ironpipe.extension.get_config('input')
    if input:
        input = input.lower()
    if not input or input not in DATA_MAP_FUNCTIONS:
        types = ', '.join([i for i in DATA_MAP_FUNCTIONS])
        ironpipe.extension.exit("Required attribute 'input' must be one of: {}".format(types))

    output = ironpipe.extension.get_config('output')
    if output:
        output = output.lower()
    if not output or output not in DATA_MAP_FUNCTIONS:
        types = ', '.join([i for i in DATA_MAP_FUNCTIONS])
        ironpipe.extension.exit("Required attribute 'output' must be one of: {}".format(types))

    # Parse the input file
    data = DATA_MAP_FUNCTIONS[input]['read'](sys.stdin)

    # if input and output are the same format, write the original file into the output
    if input == output:
        sys.stdin.seek(0)
        try:
            for line in sys.stdin:
                sys.stdout.write(line)
        except Exception as err:
            ironpipe.extension.exit('Data write error: ' + str(err))
    else:
        DATA_MAP_FUNCTIONS[output]['write'](data, sys.stdout)

    return 0


#
#
def main():
    return transform_data()


if __name__ == '__main__':
    main()
