from jsonschema import validate
from jsonschema.exceptions import ValidationError
from pathlib import Path
import yaml
import subprocess
import datetime as datetime_module
from datetime import date
from datetime import datetime
import re
import traceback

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

genres = {
    "type": "array",
    "minItems": 0,
    "items": {
        "type": "string",
        "enum": [
            "Adventure", "RPG", "Platformer", "Shooter", "Strategy", "Puzzle",
        ]
    }
}

platforms = {
    "type": "array",
    "minItems": 0,
    "items": {
        "type": "string",
        "enum": [
            "PC",
            "NES", "SNES", "N64", "GameCube", "Wii", "Wii U", "Switch",
            "GameBoy", "GBA", "DS", "3DS",
            "Master System", "Genesis", "Saturn", "Dreamcast",
            "PS1", "PS2", "PS3", "PS4", "PS5",
            "PSP", "Vita",
            "Xbox", "Xbox 360", "Xbox One", "Xbox Series",
            "Arcade", "MSX",
        ]
    }
}

games_schema = {
    "type": "object",
    "additionalProperties": {
        "type": "object",
        "properties": {
            "genres": genres,
            "platforms": platforms,
            "release_year": {
                "type": ["number", 'null'],
                "minimum": 1900,
                "maximum": datetime.now().year + 1
            },
            "sub-series": ValidString
        },
        "required": ["genres", "platforms", "release_year"],
        "additionalProperties": False
    }
}

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
    if updated >= date(2024, 8, 1):
        ret['properties'].pop('sub-series') # deprecated, moving to games_schema, still need to fix html template to support both
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
            "games": games_schema,
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
    games = set()
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
        #raise # uncomment for bigger error messages
    
    for rando in data['randomizers']:
        try:
            validateRando(rando)
            for game in rando.get('games', []):
                if 'games' in data and game not in data['games']:
                    raise ValidationError('game: ' + game + ' is not defined')
                games.add(game)
        except ValidationError as e:
            failures += 1
            print('\nIn Randomizer definition:', rando)
            id = str(rando.get('game', ''))  + ' ' + str(rando.get('identifier', ''))
            print('\nERROR in', path, ': randomizer definition', id, '-\n', e.path, e.message)
            #raise # uncomment for bigger error messages

        # update rando data
        if not rando.get('info-updated'):
            writeback = True
            rando['info-updated'] = date(2024, 5, 25)
        if not rando.get('added-date'):
            writeback = True
            rando['added-date'] = date(2024, 5, 25)

    if 'games' not in data:
        newdata: dict = data.copy()
        newdata.pop('randomizers')
        games = {key: {'genres':[], 'platforms':[], 'release_year': None} for key in sorted(games)}
        newdata['games'] = games
        newdata['randomizers'] = data['randomizers']
        data = newdata
        writeback=True

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
            print(traceback.format_exc())
            print('\nERROR in', file, '-\n', e)
            #raise # uncomment for bigger error messages

    print('\n\n')
    assert success > 0
    assert failures == 0, 'got ' + str(failures) + ' failures'


if __name__ == "__main__":
    validateYamlFiles()
