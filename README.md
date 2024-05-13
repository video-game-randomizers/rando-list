# The BIG List of Video Game Randomizers

- Home page: <https://www.debigare.com/randomizers/>
- Discord Community Server: <https://discord.com/invite/YREMzGQ3gd>

## About

This repository contains the source code for [The BIG List of Video Game Randomizers](https://www.debigare.com/randomizers/), a community project created and originally published in 2016 by [Guillaume Fortin-Debigaré](https://www.debigare.com/). The project has been continuously maintained by him based on countless contributions by the community over the years, up until it became open source in 2024.

The project is currently hosted on Guillaume Fortin-Debigaré's personal website, although we are considering moving it to a separate domain or subdomain as part of the open source transition as soon as possible.

## How to contribute

If you want to improve or become a maintainer of this project, please join the [official Discord Community Server](https://discord.com/invite/YREMzGQ3gd) and post in the `#list-maintenance` channel. Pull requests from the public are also welcome.

The current code, from a development and from an end-user perspective, was never designed to handle as much data as it currently handles. As such, any contributions that fundamentally change its structure and build pipeline will be considered.

## Code structure

The actual code and content is located in the `src` directory. It is currently exclusively composed of Markdown documents conforming with the [CommonMark specifications](https://commonmark.org/), with an added [Jekyll-style Front Matter](https://jekyllrb.com/docs/front-matter/) YAML header for metadata used during building.

Links between internal pages are currently based on the `permalink` Front Matter metadata, used to generate the final URLs.

## Building

The current build pipeline is private, due to multiple dependencies with Guillaume Fortin-Debigaré's personal website. However, any static site generator with Front Matter support should be able to properly convert the Markdown documents into HTML documents, including Hugo, Jekyll and Metalsmith.

Contributions for a new open source build pipeline that would remove this dependency would be appreciated.