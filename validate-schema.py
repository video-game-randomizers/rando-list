"""
A simple script to validate all series YAMLs.

This does not enforce `format` as this is auto-off in JSON Schema's spec.

Note that this does some monkey-patching to dodge around features of PyYAML.
"""
import logging
from pathlib import Path
import re
import argparse
from jsonschema import FormatChecker
from jsonschema.validators import extend, validate, Draft202012Validator
import yaml, json
from yaml.constructor import ConstructorError

ALLOW_NOW = False
my_format_checker = FormatChecker()

@my_format_checker.checks("date")
def check_date_format(instance):
    if ALLOW_NOW and instance == 'NOW':
        return True
    return bool(re.match(r'^\d{4}-\d{2}-\d{2}$', instance))


class NoDuplicateSafeLoader(yaml.SafeLoader): # inherits from SafeLoader so we don't need to use yaml.safe_load
    def construct_mapping(self, node, deep=False):
        mapping = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in mapping:
                raise ConstructorError(
                    None, None,
                    f"Duplicate key found: '{key}' on line {key_node.start_mark.line + 1}",
                    key_node.start_mark
                )
            mapping[key] = self.construct_object(value_node, deep=deep)
        return mapping


def checkFile(schema, filename: Path):
    if filename.suffix!='.yml' or re.search(r'[^a-zA-Z0-9_\-\.\(\)]', filename.stem):
        raise ValueError("bad filename " + filename.name)
    with open(filename, encoding="utf-8") as f:
        series = yaml.load(f, Loader=NoDuplicateSafeLoader)
    validate(series, schema, format_checker=my_format_checker)

    # now check lists of games
    series_games = set(series['games'])
    found_games = set()
    for rando in series['randomizers']:
        rando_games = set(rando['games'])
        found_games.update(rando_games)
        undefined_games = rando_games.difference(series_games)
        if undefined_games:
            raise ValueError("undefined games in " + rando['identifier'] + " : " + ', '.join(undefined_games))
    
    unused_games = series_games.difference(found_games)
    if unused_games:
        raise ValueError("unused games: " + ', '.join(unused_games))



def runChecks(allow_now: bool):
    global ALLOW_NOW
    ALLOW_NOW = allow_now
    passed = 0
    errored = 0
    files = set()
    # Bodge to ignore dates and just read them as strings
    yaml.SafeLoader.yaml_implicit_resolvers = {
        k: [r for r in v if r[0] != 'tag:yaml.org,2002:timestamp'] for
        k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
    }
    with open("src/schemata/series.schema.json") as f:
        schema = json.load(f)
    
    for filename in Path("src/series/").glob("*"):
        try:
            checkFile(schema, filename)
            file_lowercase = str(filename).lower()
            assert file_lowercase not in files, 'filename collision for case-insensitive filesystems'
            files.add(file_lowercase)
            passed+=1
        except Exception as e:
            logging.basicConfig(format=filename.name + ": %(message)s\n\n---------\n", force=True)
            logging.error(e)
            errored+=1
    
    print('passed:', passed, 'errored:', errored)
    if errored:
        print('FAILED')
    return errored


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--allow-now", action="store_true", help="Allow 'NOW' as a valid date, used for checking PRs before merging.") # TODO: merging bot https://github.com/video-game-randomizers/rando-list/issues/41
    args = parser.parse_args()
    if runChecks(args.allow_now):
        exit(-1)  # Error code to cause gh actions failure
