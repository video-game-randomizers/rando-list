import json, yaml
from pathlib import Path

"""
Edit the below functions to execute on all series, games & randos respectively.

`**games` is a dict[game_name, game_dict]

Example;
def transform_series(series: dict):
    if "comment" in series:
        if series["comment"] is None:
            series["comment"] = ""
    if series.get("sub-series", None) is None:
        series["sub-series"] = []
"""

def transform_series(series: dict):
    ...

def transform_games(**games: dict):
    ...

def transform_randos(*randos: dict):
    ...


if __name__ == "__main__":
    with open("src/schemata/series.schema.json") as f:
        schema = json.load(f)
    
    for filename in Path("src/series/").glob("*"):
        with open(filename, "r+", encoding="utf-8") as f:
            data = yaml.full_load(f)
        transform_series(data)
        transform_games(**data["games"])
        transform_randos(*data["randomizers"])
        with open(filename, "w", encoding="utf-8") as f:
            yaml.dump(data, f, indent=4, allow_unicode=True, sort_keys=False, width=10000)
