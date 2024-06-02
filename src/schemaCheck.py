from jsonschema import validate, exceptions
from pathlib import Path
import yaml
from datetime import date

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

randomizer_schema = {
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
        "sub-series": MaybeString,
        "discord": ValidString,
        "community": ValidString,
        "contact": ValidString,
        "infoupdated": {}, # we update the info, but we don't keep track of when the randomizers receive patches/new versions
    },
    "required": ["games", "identifier", "url" ],
    "additionalProperties": False,
}

series_schema = {
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


def validateDate(rando, prop):
    d = rando.get(prop)
    if not d:
        return
    if not isinstance(d, date):
        raise exceptions.ValidationError(prop + ' invalid date format: ' + repr(d))
    if date.today() < d:
        raise exceptions.ValidationError(prop + ' date is in the future: ' + repr(d))


def validateSeriesConfig(path: Path):
    failures = 0
    text = path.read_text()
    data = yaml.load(text, Loader=yaml.CLoader)
    try:
        validate(data, series_schema)
        for rando in data['randomizers']:
            try:
                validate(rando, randomizer_schema)
                validateDate(rando, 'infoupdated')
            except exceptions.ValidationError as e:
                failures += 1
                print('\nIn Randomizer definition:', rando)
                id = str(rando.get('game', ''))  + ' ' + str(rando.get('identifier', ''))
                print('\nERROR in', path, ': randomizer definition', id, '-', e.message)
    except exceptions.ValidationError as e:
        failures += 1
        print('ERROR in', path, ': series definition -', e.message)
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
            print('\nERROR in', file, e)

    assert success > 0
    return failures


if __name__ == "__main__":
    exit(validateYamlFiles())
