import pywikibot
from pywikibot.data import api
import yaml

with open('../config.yaml', 'r', encoding='utf-8') as config_file:
    config = yaml.load(config_file)


class MediaWikiAPI(object):
    """
    Wrapper Class for The MediaWiki action API.
    """

    SITE = pywikibot.site.DataSite(config['language'], config['site'])

    def __init__(self):
        self.response = None

    def extract(self):
        return [result['id'] for result in self.response['search']]

    def wbgetentities(self, ids):
        """
        Helper function to make a request with action wbgetentities.

        @:param ids: item ids
        @:type ids: list

        @:return: self
        @:rtype: MediaWikiAPI
        """
        params = {'action': 'wbgetentities',
                  'format': 'json',
                  'ids': '|'.join(ids)
                  }
        request = api.Request(site=self.SITE, **params)
        self.response = request.submit()
        return self

    def wbsearchentities(self, label, language):
        """
        Helper function to make a request with action wbgetentities.

        @:param label: The text string to search for
        @:type label: string
        @:param language: The language to search in
        @:type language: string

        @:return: self
        @:rtype: MediaWikiAPI
        """
        params = {'action': 'wbsearchentities',
                  'format': 'json',
                  'language': language,
                  'type': 'item',
                  'search': label
                  }
        request = api.Request(site=self.SITE, **params)
        self.response = request.submit()
        return self

