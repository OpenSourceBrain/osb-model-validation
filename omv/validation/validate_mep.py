#!/usr/bin/env python
import sys
from omv.validation.validate import OMVValidator
from os.path import dirname


def validate(mep_src):
    s = OMVValidator()
    print("Validating document againt mep schema: ")
    # schema = resource_filename("omv", "schemata/mep.yaml")
    schema = dirname(dirname(__file__)) + "/schemata/mep.yaml"
    print(s.validate(schema, mep_src))


if __name__ == "__main__":
    validate(sys.argv[1])
