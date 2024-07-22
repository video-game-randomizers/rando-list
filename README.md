# The BIG List of Video Game Randomizers

- New website: <https://randomizers.debigare.com>
- New website (backup): <https://video-game-randomizers.github.io/rando-list/>
- Old website: <https://www.debigare.com/randomizers/>
- Discord Community Server: <https://discord.com/invite/YREMzGQ3gd>

## About

This repository contains the source code for [The BIG List of Video Game Randomizers](https://video-game-randomizers.github.io/rando-list/), a community project created and originally published in 2016 by [Guillaume Fortin-Debigaré](https://www.debigare.com/). The project has been continuously maintained by him based on countless contributions by the community over the years, up until it became open source in 2024.

The project is currently hosted on [Guillaume Fortin-Debigaré's personal website](https://www.debigare.com/randomizers/), although we are currently working on moving it to <https://video-game-randomizers.github.io/rando-list/>.

## How to contribute

Pull requests from the public are very welcome. If you want to become a maintainer of this project or you need help with contributing, please join the [official Discord Community Server](https://discord.com/invite/YREMzGQ3gd) and post in the `#list-maintenance` channel.

## Code structure

The actual code and content is located in the [`src`](https://github.com/video-game-randomizers/rando-list/tree/main/src) directory. The data about the games/randomizers is stored in `yml` files inside of [`src/series/`](https://github.com/video-game-randomizers/rando-list/tree/main/src/series), while the HTML code is built from [Jekyll](https://jekyllrb.com/docs/)/[Liquid](https://shopify.github.io/liquid/basics/introduction/) templates in [`src/index.html`](https://github.com/video-game-randomizers/rando-list/blob/main/src/index.html) and [`src/_includes/`](https://github.com/video-game-randomizers/rando-list/tree/main/src/_includes).

## Building

We use [Jekyll](https://jekyllrb.com/docs/) to build the website into static files. If you do not have Jekyll installed, you can just let GitHub Actions build the website for you, you can download and extract the artifact file from there and open the static HTML files. If you do have Jekyll installed then you can `cd` into the `src` folder, then run `bundle install`, and then run `bundle exec jekyll serve` and it will host the website on `http://127.0.0.1:4000/rando-list/`.
