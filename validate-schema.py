import logging
from pathlib import Path
from jsonschema import ValidationError
import jsonschema.protocols
import jsonschema.validators
import yaml, json

if __name__ == "__main__":
    errored = False
    with open("src/schemata/series.schema.json") as f:
        schema = json.load(f)
    
    series = {}
    for filename in Path("src/series/").glob("*"):
        with open(filename, encoding="utf-8") as f:
            series[filename] = yaml.full_load(f)
            try:
                jsonschema.validators.validate(series[filename], schema)
            except ValidationError as e:
                logging.error(e, exc_info=True)
                errored = True
    
    if errored:
        exit(-1)  # Error code to cause gh actions failure
