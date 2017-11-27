#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 18:58:42 2017

@author: eckart
"""

import ironpipe
import sys
import json
from jsonschema import validate

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
        ironpipe.exit('Data read error: {}'.format(err))
        
    # Try parsing the string
    try:
        data = json.loads(input_string)
        
        if not isinstance(data, list): # Need to always return a list
            data = [data]

    except Exception as err:
        # Check if the file might be stored in JSONL (line) format
        try:
            data = []

            for line in input_string.splitlines():
                data.append(json.loads(line))                

        except Exception as err:
            ironpipe.exit('Data read error: {}'.format(err))
    
    try:
        for row in data:
            print('validating row', row)
            validate(row, schema)  

    except Exception as err:
        ironpipe.exit('Invalid JSON schema: {}'.format(err))

    # Write the origninal, validated string to the output
    try:
        output.write(input_string)

    except Exception as err:
        ironpipe.exit('Data write error: {}'.format(err))

#
#
def check_schema():
    '''
    '''
    with open("/Users/eckart/src/ironpipe/connectors/test/billing.json") as f:
        check_file(f, sys.stdout,foo)
    '''
    schema = ironpipe.get_config('schema')
    
    # argument is required
    if not schema:
        ironpipe.exit('Missing schema configuration.')
        
    # Confirm that schema pram is JSON and valid JSON Schema
    try:
        schema = json.loads(schema)

    except Exception as err:
        ironpipe.exit('Schema not valid JSON: {}'.format(err))
                    
    check_file(sys.stdin, sys.stdout, schema)
    '''
    return 0

#
#        
def main():   
    return check_schema()

if __name__ == '__main__':
    main()

# , "pattern": "\b(?:3[47]\d{2}([\ \-]?)\d{6}\1\d|(?:(?:4\d|5[1-5]|65)\d{2}|6011)([\ \-]?)\d{4}\2\d{4}\2)\d{4}\b"
test_schema = '''
{
  "type": "object",
  "properties": {
    "date": { "type": "string", "format": "date-time" },
    "amount": { "type": "number", "minimum": 0 },
    "currency": {"type": "string", "enum": ["USD", "CAD", "MXN"]},
    "client id": { "type": "integer", "minimum": 0 },
    "client name": {"type": "string"},
    "card number": {"type": "string"}
  },
  "required": ["date", "amount", "currency", "client id", "client name", "card number"],
  "additionalProperties": false
}
'''

