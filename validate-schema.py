"""
A simple script to validate all series YAMLs.

This does not enforce `format` as this is auto-off in JSON Schema's spec.

Note that this does some monkey-patching to dodge around features of PyYAML.
"""
import logging
from pathlib import Path
import re
from jsonschema import FormatChecker
from jsonschema.validators import extend, validate, Draft202012Validator
import yaml, json

# Bodge to ignore dates and just use as-is.
# This makes this script unsafe to import!
yaml.SafeLoader.yaml_implicit_resolvers = {
    k: [r for r in v if r[0] != 'tag:yaml.org,2002:timestamp'] for
    k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}

Validator = extend(Draft202012Validator, format_checker=FormatChecker())

if __name__ == "__main__":
    errored = False
    with open("src/schemata/series.schema.json") as f:
        schema = json.load(f)
    
    series = {}
    for filename in Path("src/series/").glob("*"):
        try:
            if re.search(r'[^a-zA-Z0-9_\-\.\(\)]', filename.stem):
                raise RuntimeError("bad filename " + filename.name)
            with open(filename, encoding="utf-8") as f:
                series[filename] = yaml.safe_load(f)
            validate(series[filename], schema, cls=Validator)
        except Exception as e:
            logging.error("ERROR in", filename.name)
            logging.error(e)
            errored = True
    
    if errored:
        exit(-1)  # Error code to cause gh actions failure
