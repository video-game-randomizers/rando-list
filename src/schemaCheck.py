from jsonschema import validate
from jsonschema.exceptions import ValidationError
from pathlib import Path
import yaml
import subprocess
import datetime as datetime_module
from datetime import date
from datetime import datetime
import re

# https://json-schema.org/learn/getting-started-step-by-step#going-deeper-with-properties
# https://cswr.github.io/JsonSchema/spec/introduction/

ValidString = { "type": "string", "minLength": 1, }

MaybeString = {
    "anyOf": [
        {
            "type": "string",
            "minLength": 1
        },
        {"type": "null"}, 
]}

def randomizer_schema(data):
    ret = {
        "type": "object",
        "properties": {
            "games": {
                "type": "array",
                "minItems": 1,
                "items": ValidString,
            },
            "identifier": ValidString,
            "url": ValidString,
            "comment": MaybeString,
            "multiworld": {
                "type": ["string", "boolean", "null"],
                "default": None
            },
            "obsolete": {"type": "boolean"},
            "sub-series": ValidString,
            "discord": ValidString,
            "community": ValidString,
            "contact": ValidString,
            "added-date": {},
            "info-updated": {}, # when we update our info, but we don't keep track of when the randomizers receive patches/new versions
            "opensource": {"type": "boolean"},
        },
        "required": ["games", "identifier", "url", "info-updated", "added-date"],
        "additionalProperties": False,
    }
    # new requirements can be checked by the added-date and info-updated dates
    updated = data.get('info-updated')
    if not updated:
        return ret
    if updated >= date(2024, 6, 19):
        ret['required'].append('opensource')
    return ret

def series_schema(data):
    ret = {
        "type": "object",
        "properties": {
            "name": ValidString,
            "comment": MaybeString,
            "sub-series": {
                "type": ["array", "null"],
            },
            "randomizers": {
                "type": "array",
                "minItems": 1,
                #"items": randomizer_schema,
            },
        },

        "required": ["name", "randomizers"],
        "additionalProperties": False,
    }
    return ret


def validateDate(rando, prop):
    if prop not in rando:
        return
    d = rando.get(prop)
    if not isinstance(d, date):
        raise ValidationError(prop + ' invalid date format: ' + repr(d))
    # we could check vs today, but it could get annoying with pull requests, ideally the date would be the date of merging
    # today = datetime.now(datetime_module.UTC).date()
    # if today < d:
    #     raise ValidationError(prop + ' date is in the future: ' + repr(d) + ", UTC today is: " + repr(today))
    return d


def get_modified_time(path: Path):
    ret = subprocess.run(["git", "status", "--porcelain", str(path)], stdout=subprocess.PIPE, check=True)
    ret = ret.stdout.decode()
    if ret:
        return datetime.now()

    ret = subprocess.run(["git", "log", "--pretty=%at", "-n1", "--", str(path)], stdout=subprocess.PIPE, check=True)
    ret = ret.stdout.decode()
    i = int(ret)
    return datetime.fromtimestamp(i)


def validateRando(rando):
    validate(rando, randomizer_schema(rando))
    updated = validateDate(rando, 'info-updated')
    added = validateDate(rando, 'added-date')
    if updated and updated < added:
        raise ValidationError('added-date ' + repr(added) + ' is newer than info-updated ' + repr(updated))


def validateSeriesConfig(path: Path):
    failures = 0
    #modified = get_modified_time(path) # currently we don't need this expensive check
    writeback = False
    text = path.read_text()
    data = yaml.load(text, Loader=yaml.CLoader)

    if re.search(r'[^a-zA-Z0-9_\-\.\(\)]', path.stem):
        failures += 1
        print('ERROR special characters in filename: ' + str(path.name))
    if path.suffix != '.yml':
        failures += 1
        print('ERROR filename does not end with .yml: ' + str(path.name))
    
    try:
        validate(data, series_schema(data))
    except ValidationError as e:
        failures += 1
        print('ERROR in', path, ': series definition -\n', e.path, e.message)
    
    for rando in data['randomizers']:
        try:
            validateRando(rando)
        except ValidationError as e:
            failures += 1
            print('\nIn Randomizer definition:', rando)
            id = str(rando.get('game', ''))  + ' ' + str(rando.get('identifier', ''))
            print('\nERROR in', path, ': randomizer definition', id, '-\n', e.path, e.message)

        # update rando data
        if not rando.get('info-updated'):
            writeback = True
            rando['info-updated'] = date(2024, 5, 25)
        if not rando.get('added-date'):
            writeback = True
            rando['added-date'] = date(2024, 5, 25)

    if failures == 0 and writeback:
        out = yaml.dump(data, sort_keys=False, indent=4)
        path.write_text(out)
        failures += 1 # make sure this fails the Github Actions test, because it won't commit back
        print('ERROR: ', path, ' needed update, run schemaCheck.py locally and commit the changes')
    return failures


def validateYamlFiles():
    failures = 0
    success = 0
    for file in Path('series').glob('*'):
        try:
            new_failures = validateSeriesConfig(file)
            if new_failures == 0:
                success += 1
            failures += new_failures
        except Exception as e:
            failures += 1
            print('\nERROR in', file, '-\n', e)

    print('\n\n')
    assert success > 0
    assert failures == 0, 'got ' + str(failures) + ' failures'


if __name__ == "__main__":
    validateYamlFiles()
