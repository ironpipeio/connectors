#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""

import sys
import json
from jsonschema import validate
import ironpipe.extension

# JSON_Schema_Validator = Draft4Validator


#
# Read one or more JSON files from the input and check against schema
# If all JSON files pass, dump input text to output
#
def check_file(input, output, schema):
    '''
    '''
    # Read JSON text from input
    try:
        input_string = input.read()
    except Exception as err:
        ironpipe.extension.exit('Data read error: {}'.format(err))

    # Try parsing the string
    try:
        data = json.loads(input_string)

        if not isinstance(data, list):  # Need to always return a list
            data = [data]

    except Exception as err:
        # Check if the file might be stored in JSONL (line) format
        try:
            data = []

            for line in input_string.splitlines():
                data.append(json.loads(line))

        except Exception as err:
            ironpipe.extension.exit('Data read error: {}'.format(err))

    try:
        for row in data:
            validate(row, schema)

    except Exception as err:
        ironpipe.extension.exit('Data failed JSON Schema validation: {}'.format(err))

    # Write the origninal, validated string to the output
    try:
        output.write(input_string)

    except Exception as err:
        ironpipe.extension.exit('Data write error: {}'.format(err))


#
#
def check_schema():
    '''
    with open("/Users/eckart/src/ironpipe/connectors/test/billing.json") as f:
        check_file(f, sys.stdout,foo)
    '''

    schema = ironpipe.extension.get_config('schema')

    # argument is required
    if not schema:
        ironpipe.extension.exit("Missing required attribute 'schema'.")

    # Fix escape characters so that JSON parser preserves '\' characters
    # for regex strings
    schema = schema.replace("\\", "\\\\")

    # Confirm that schema pram is JSON and valid JSON Schema
    try:
        schema = json.loads(schema)

    except Exception as err:
        ironpipe.extension.exit("Required attribute 'schema' not valid JSON: {}".format(err))

    check_file(sys.stdin, sys.stdout, schema)

    return 0


#
#
def main():
    return check_schema()


if __name__ == '__main__':
    main()
