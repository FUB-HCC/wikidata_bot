import pywikibot
import yaml
import csv
import logging
import datetime
import json

from api import MediaWikiAPI
from item import WikidataItem

with open('../config.yaml', 'r', encoding='utf-8') as config_file:
    config = yaml.load(config_file)


class CSVParser(object):
    """
    Class for parsing csv.
    """

    SITE = pywikibot.site.DataSite(config['language'], config['site'])

    def __init__(self, csv_path, buffer=False, buffer_path=None):
        with open(csv_path, newline='') as file:
            self.data = [_ for _ in csv.reader(file, delimiter=';', quotechar='"')]
        self.parsed_data = None

        if buffer and not buffer_path:
            raise ValueError(' If buffer is set to True, buffer_path has to be set as well.')

        self.buffer = buffer
        self.buffer_path = buffer_path

    def parse_csv(self):

        self.parsed_data = []

        for index, line in enumerate(self.data):

            if WikidataItem.exists(line):
                continue

            self.parsed_data.append(self.parse_line(line))

            if self.buffer:
                self.save_as_json(self.buffer_path)

            logging.info(' Line with index = ' + str(index) + ' parsed.')

        return self

    def parse_line(self, line):
        """
        Function to parse a line.

        @:param line: line
        @:type line: dict

        @:return: parsed line
        @:rtype: dict
        """

        # Labels
        if line['Namenszusatz'] != '':
            label = "%s %s %s" % (line['Vorname'], line['Namenszusatz'], line['Nachname'])
        else:
            label = "%s %s" % (line['Vorname'], line['Nachname'])

        parsed_line = {'labels': {'de': label,
                                  'en': label,
                                  'af': label,
                                  'an': label,
                                  'ast': label,
                                  'bar': label,
                                  'br': label,
                                  'ca': label,
                                  'cs': label,
                                  'da': label,
                                  'de-ch': label,
                                  'de-at': label,
                                  'es': label,
                                  'dsb': label,
                                  'eo': label,
                                  'et': label,
                                  'eu': label,
                                  'ext': label,
                                  'fi': label,
                                  'fr': label,
                                  'frc': label,
                                  'frp': label,
                                  'fy': label,
                                  'frr': label,
                                  'ga': label,
                                  'gl': label,
                                  'hr': label,
                                  'hu': label,
                                  'hsb': label,
                                  'stq': label,
                                  'is': label,
                                  'it': label,
                                  'id': label,
                                  'lb': label,
                                  'ms': label,
                                  'nds': label,
                                  'nl': label,
                                  'no': label,
                                  'nn': label,
                                  'oc': label,
                                  'pdc': label,
                                  'pl': label,
                                  'pap': label,
                                  'pdt': label,
                                  'pt': label,
                                  'ro': label,
                                  'sco': label,
                                  'sk': label,
                                  'sl': label,
                                  'sv': label,
                                  'tr': label
                                  }}

        # Aliases
        if line['Namenszusatz'] != '':
            aliases = ["%s %s" % (line['Vorname'], line['Nachname'])]
            parsed_line['aliases'] = {'de': aliases,
                                      'en': aliases,
                                      'af': aliases,
                                      'an': aliases,
                                      'ast': aliases,
                                      'bar': aliases,
                                      'br': aliases,
                                      'ca': aliases,
                                      'cs': aliases,
                                      'da': aliases,
                                      'de-ch': aliases,
                                      'de-at': aliases,
                                      'es': aliases,
                                      'dsb': aliases,
                                      'eo': aliases,
                                      'et': aliases,
                                      'eu': aliases,
                                      'ext': aliases,
                                      'fi': aliases,
                                      'fr': aliases,
                                      'frc': aliases,
                                      'frp': aliases,
                                      'fy': aliases,
                                      'frr': aliases,
                                      'ga': aliases,
                                      'gl': aliases,
                                      'hr': aliases,
                                      'hu': aliases,
                                      'hsb': aliases,
                                      'stq': aliases,
                                      'is': aliases,
                                      'it': aliases,
                                      'id': aliases,
                                      'lb': aliases,
                                      'ms': aliases,
                                      'nds': aliases,
                                      'nl': aliases,
                                      'no': aliases,
                                      'nn': aliases,
                                      'oc': aliases,
                                      'pdc': aliases,
                                      'pl': aliases,
                                      'pap': aliases,
                                      'pdt': aliases,
                                      'pt': aliases,
                                      'ro': aliases,
                                      'sco': aliases,
                                      'sk': aliases,
                                      'sl': aliases,
                                      'sv': aliases,
                                      'tr': aliases,
                                      }

        # Descriptions
        if line['Geschlecht'] == '1':
            parsed_line['descriptions'] = {'de': 'deutscher Jurist, Richter am Bundesgerichtshof',
                                           'en': 'German judge, Federal Court of Justice',
                                           'fr': 'juge allemand, Cour Fédérale de Justice',
                                           'it': 'giudice tedesco, Corte di Cassazione Federale',
                                           'es': 'juez alemán, Tribunal Federal Supremo',
                                           'pl': 'niemiecki sędzia, Trybunał Federalny',
                                           'nl': 'Duits rechter, Federale Gerechtshof',
                                           'zh': '德国法律学者, 德国联邦最高法院'}
        else:
            parsed_line['descriptions'] = {'de': 'deutsche Juristin, Richterin am Bundesgerichtshof',
                                           'en': 'German judge, Federal Court of Justice',
                                           'fr': 'juge allemande, Cour Fédérale de Justice',
                                           'it': 'giudice tedesca, Corte di Cassazione Federale',
                                           'es': 'jueza alemana, Tribunal Federal Supremo',
                                           'pl': 'niemiecki sędzia, Trybunał Federalny',
                                           'nl': 'Duits rechter, Federale Gerechtshof',
                                           'zh': '德国法律学者, 德国联邦最高法院'
                                           }

        parsed_line['claims'] = []

        # P31 = instance of, Q5 = human
        parsed_line['claims'].append({'id': 'P31', 'value': 'Q5'})

        # P569 = date of birth
        date_of_birth = self.get_date(line['G-J'], line['G-M'], line['G-T'])
        if date_of_birth is not None:
            parsed_line['claims'].append({'id': 'P569', 'value': date_of_birth})

        # P570 = date of death
        date_of_death = self.get_date(line['T-J'], line['T-M'], line['T-T'])
        if date_of_death is not None:
            parsed_line['claims'].append({'id': 'P570', 'value': date_of_death})

        # P21 = sex or gender
        parsed_line['claims'].append({'id': 'P21', 'value': self.get_qid(line['Geschlecht'], 'gender')})

        # P27 = country of citizenship, Q183 = Germany
        parsed_line['claims'].append({'id': 'P27', 'value': 'Q183'})

        # P19 = place of birth
        place_of_birth = self.get_qid(line['G-Ort'], 'city')
        if place_of_birth is not None:
            parsed_line['claims'].append({'id': 'P19', 'value': place_of_birth})

        # P735 = given name
        given_name = self.get_qid(line['Vorname'], 'given_name')
        if given_name is not None:
            parsed_line['claims'].append({'id': 'P735', 'value': given_name})

        # P734 = family name
        family_name = self.get_qid(line['Nachname'], 'family_name')
        if family_name is not None:
            parsed_line['claims'].append({'id': 'P734', 'value': family_name})

        # P106 = occupation, Q16533 = judge
        parsed_line['claims'].append({'id': 'P106', 'value': 'Q16533'})

        # P108 = employer, Q687323 = Federal Court of Justice of Germany
        claim = {'id': 'P108', 'value': 'Q687323'}

        accession_date = self.get_date(line['B-J'], line['B-M'], line['B-T'])
        if accession_date is not None:
            # P580 = start time
            claim['qualifiers'] = [{'id': 'P580', 'value': accession_date}]

        withdrawal_date = CSVParser.parse_date(line['A-J'], line['A-M'], line['A-T'])
        if withdrawal_date is not None:
            # P582 = end time
            claim['qualifiers'].append({'id': 'P582', 'value': withdrawal_date})

        parsed_line['claims'].append(claim)

        # References
        parsed_line['references'] = self.get_references(line['Wikipedia'])

        return parsed_line

    def save_as_json(self, save_path):

        if self.parsed_data is None:
            raise ValueError('data not parsed yet')

        with open(save_path, 'w') as file:
            json.dump(self.parsed_data, file)

    @classmethod
    def get_date(cls, year=None, month=None, day=None, date=None):
        """
        Function to parse a date.

        @:param year: year
        @:type year: string
        @:param month: month
        @:type month: string
        @:param day: day
        @:type day: string
        @:param date: date
        @:type date: datetime.datetime

        @:return: parsed date
        @:rtype: array
        """
        if isinstance(date, datetime.datetime):
            return date.year, date.month, date.day

        if year == '':
            return None
        elif month == '':
            return int(year), None, None
        elif day == '':
            return int(year), int(month), None
        else:
            return int(year), int(month), int(day)

    @classmethod
    def get_id(cls, label, mode):
        """
        Function to search an existing item with the title item_titel and return its id.

        @param label: The label to search for.
        @type label: string
        @param mode: The mode to specify which instance the item should be from (e.g. mode=city -> item should have claim: instance of
        city)
        @type mode: string

        @return: The matching id or None if no one was found
        @rtype: string, None
        """
        if label is None or label is '':
            return None

        if mode == 'gender':
            if label == '0':
                return 'Q6581072'
            elif label == '1':
                return 'Q6581097'
        else:
            ids = MediaWikiAPI().wbsearchentities(label, 'de').extract() \
                  + MediaWikiAPI().wbsearchentities(label, 'en').extract()

            if len(ids) != 0:
                result = MediaWikiAPI().wbgetentities(ids).response

            for id in ids:
                if 'P31' in result['entities'][id]['claims']:
                    for claim in result['entities'][id]['claims']['P31']:
                        if mode == 'city' and claim['mainsnak']['datavalue']['value']['id'] == 'Q515':
                            return id
                        elif mode == 'family_name' and claim['mainsnak']['datavalue']['value']['id'] == 'Q101352':
                            return id
                        elif mode == 'given_name' and (claim['mainsnak']['datavalue']['value']['id'] == 'Q12308941'
                                                       or claim['mainsnak']['datavalue']['value'][
                                'id'] == 'Q11879590'):
                            return id

        return None

    @classmethod
    def get_references(cls, code):

        if code == '0':
            parsed_references = [
                {
                    'id': 'P854',
                    'value': 'http://www.richter-im-internet.de'
                },
                {
                    'id': 'P248',
                    'value': 'Q32961325'
                }
            ]
        else:
            parsed_references = [
                {
                    'id': 'P143',
                    'value': 'Q48183'
                }
            ]

        parsed_references.append(
            {
                'id': 'P813',
                'value': cls.get_date(date=datetime.datetime.now())
            }
        )

        return parsed_references
