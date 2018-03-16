import logging
import yaml

from parser import CSVParser
from importer import Import

with open('../config.yaml', 'r', encoding='utf-8') as config_file:
        config = yaml.load(config_file)

logging.basicConfig(filename=config['log'], level=logging.INFO)


def run():
    logging.info(' Parsing files started.')

    for file in config['files']:
        CSVParser(*file.values()).parse_csv().save_as_json(file['save_path'])
        logging.info(' Parsed file ' + file['path'] + ' finished.')

    logging.info(' importing files started')

    for file in config['files']:
        Import(file['save_path']).start()
        logging.info(' Importing file ' + file['path'] + ' finished.')
