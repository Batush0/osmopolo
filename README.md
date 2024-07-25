# Osmopolo

This cli stands for solving the problems which provides josm app.

## Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Tips](#tips)

## Features

- orders element by ids to solve this osmium error : out of order (smaller ids must come first).
- cleans extra elements which has multiple copies to solve this osmium error : Warning: Multiple objects with same id in input file
- adding necessary attributes to elements to solve this osmosis error : org.openstreetmap.osmosis.core.OsmosisRuntimeException: Node -26334 does not have a version attribute as OSM 0.6 are required to have. Is this a 0.5 file?

## Installation

git clone https://github.com/Batush0/osmopolo.git

## Usage

python index.py order -i path/to/input.osm -o path/to/output.osm

## Tips

get details for usage by this command : python index.py --help
