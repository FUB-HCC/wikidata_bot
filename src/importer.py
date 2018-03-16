import json
import logging

from item import WikidataItem


class Import(object):

    def __init__(self, json_file):
        with open(json_file) as file:
            self.json = json.load(file)

    def start(self):
        for data in self.json:
            item = WikidataItem.new(data)
            logging.info(' Item with id = ' + item.id + ' imported.')

