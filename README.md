# wikidata_bot

Wikidata_bot is a bot to import data to Wikidata about judges who work or worked at the Federal Court of Justice of Germany. It was created in the course of the project http://www.richter-im-internet.de.

## Data-Format

To be able to import your data, your csv file should have the same structure as the one you can find under the following link: http://www.richter-im-internet.de/data/fs50.csv.

## Installation

```
$ git clone https://github.com/FUB-HCC/wikidata_bot.git
$ pip install -r requirements.txt
```

## Configuration

```
$ cp config.yaml.sample config.yaml
```
Fill out the config.yaml. The mail parameters only need to be set if you run the script with --mail (see below).

## Usage

The calling syntax is
```
$ python src/main.py [--mail]
```
where when the --mail flag is set, an email will be send if an error occurs or the update is finished.

## License

The source code is licensed under the terms of the GNU GENERAL PUBLIC LICENSE Version 3.