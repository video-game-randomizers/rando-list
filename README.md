# The BIG List of Video Game Randomizers

- New website: <https://randomizers.debigare.com>
- New website (backup): <https://video-game-randomizers.github.io/rando-list/>
- Discord Community Server: <https://discord.com/invite/YREMzGQ3gd>

## About

This repository contains the source code for [The BIG List of Video Game Randomizers](https://randomizers.debigare.com), a community project created and [originally published](https://www.debigare.com/randomizers/) in 2016 by [Guillaume Fortin-Debigaré](https://www.debigare.com/).

The project has been continuously maintained by him based on countless contributions by the community over the years, and is now maintained directly via open-source contributions.

## How to contribute

You can request updates to the list either by submitting an issue with the [`Submit New Randomizer` template](https://github.com/video-game-randomizers/rando-list/issues/new/choose), or in the `#list-submissions` channel in the [Discord](https://discord.com/invite/YREMzGQ3gd).

Pull requests from the public are very welcome - if you wish to become a maintainer or need help contributing, please join the [Discord](https://discord.com/invite/YREMzGQ3gd) and see `#list-maintenance`. We recommend using VSCode if you wish to edit the series YAMLs, as the workspace contains configuration to use our schema by default.

If you really want to help maintain the list, go through [the submissions in our Issues list](https://github.com/video-game-randomizers/rando-list/issues?q=is%3Aissue%20state%3Aopen%20label%3Asubmission) and the [submissions in Discord](https://discord.com/channels/1140434800335917178/1147400990153248810). Make pull requests to add/update the randomizers to [the yml files](https://github.com/video-game-randomizers/rando-list/tree/main/src/series). Make sure the description of the pull request includes a link to the issue or Discord message so we know to mark it as done.

The available YAML properties are listed in [the schema file](https://github.com/video-game-randomizers/rando-list/blob/main/src/schemata/series.schema.json) but mostly you can just figure it out by reading the existing files. There is an optional property for `opensource` that is pretty common, see [Deus_Ex.yml](https://github.com/video-game-randomizers/rando-list/blob/main/src/series/Deus_Ex.yml) for a simple example.

## Code structure

The site's [Jekyll](https://jekyllrb.com/docs/)/[Liquid](https://shopify.github.io/liquid/basics/introduction/) templates are stored in [`src`](https://github.com/video-game-randomizers/rando-list/tree/main/src) and [`src/_includes/`](https://github.com/video-game-randomizers/rando-list/tree/main/src/_includes), while the data is stored as a YAML file per game series in [`src/series/`](https://github.com/video-game-randomizers/rando-list/tree/main/src/series).

Note that all games must be in a series; if a game does not belong to a series, give the series the same name as the game.

## Building

If you want to do full builds locally, you must install [Jekyll](https://jekyllrb.com/docs/) - if on Windows you probably want to use [WSL](https://learn.microsoft.com/en-us/windows/wsl/about). You also need to do `pip install -r requirements.txt`.

- `python validate-schema.py`
- `cd src`
- `bundle install` to install dependencies
- `bundle exec jekyll serve`

This will host the site on `http://127.0.0.1:4000/rando-list/`.

You can also run the `Jekyll Build & Deploy` GitHub action & download the outputted artifact if you do not wish to install Jekyll locally.
