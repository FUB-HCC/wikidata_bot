import csv
from judge_item import ItemHelper



class CSVParser:
    """
    Helper Class for parsing data out of a csv dict.
    """

    @staticmethod
    def parse_data(site, row):
        """
        Helper function to parse data out of one csv row.

        @param site: The data repository where data is pared from.
        @type site: pywikibot.site.DataSite
        @param row: The row which will be parsed.
        @type row: dict

        @return: The parsed data
        @rtype: dict
        """
        # Labels for the data
        if row['Namenszusatz'] != '':
            label = "%s %s %s" % (row['Vorname'], row['Namenszusatz'], row['Nachname'])
        else:
            label = "%s %s" % (row['Vorname'], row['Nachname'])

        data = {'labels': {'de': label,
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

        # Aliases for the data
        if row['Namenszusatz'] != '':
            aliases = ["%s %s" % (row['Vorname'], row['Nachname'])]
            data['aliases'] = {'de': aliases,
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

        # Descriptions for the data
        if row['Geschlecht'] == '1':
            data['descriptions'] = {'de': 'deutscher Jurist, Richter am Bundesgerichtshof',
                                    'en': 'German judge, Federal Court of Justice',
                                    'fr': 'juge allemand, Cour Fédérale de Justice',
                                    'it': 'giudice tedesco, Corte di Cassazione Federale',
                                    'es': 'juez alemán, Tribunal Federal Supremo',
                                    'pl': 'niemiecki sędzia, Trybunał Federalny',
                                    'nl': 'Duits rechter, Federale Gerechtshof',
                                    'zh': '德国法律学者, 德国联邦最高法院'}
        else:
            data['descriptions'] = {'de': 'deutsche Juristin, Richterin am Bundesgerichtshof',
                                    'en': 'German judge, Federal Court of Justice',
                                    'fr': 'juge allemande, Cour Fédérale de Justice',
                                    'it': 'giudice tedesca, Corte di Cassazione Federale',
                                    'es': 'jueza alemana, Tribunal Federal Supremo',
                                    'pl': 'niemiecki sędzia, Trybunał Federalny',
                                    'nl': 'Duits rechter, Federale Gerechtshof',
                                    'zh': '德国法律学者, 德国联邦最高法院'
                                    }

        # P31 = instance of, Q5 = human
        # data['P31'] = {'value': 'Q5'}
        data['P82'] = {'value': 'Q26'}

        # P569 = date of birth
        date_of_birth = CSVParser.parse_date(row['G-J'], row['G-M'], row['G-T'])
        if date_of_birth is not None:
            # data['P569'] = {'value': date_of_birth}
            data['P18'] = {'value': date_of_birth}

        # P570 = date of death
        date_of_death = CSVParser.parse_date(row['T-J'], row['T-M'], row['T-T'])
        if date_of_death is not None:
            # data['P570'] = {'value': date_of_death}
            data['P25'] = {'value': date_of_death}

        # P21 = sex or gender
        # data['P21'] = {'value': ItemHelper.get_qid(site, row['Geschlecht'], 'gender')}
        data['P192'] = {'value': ItemHelper.get_qid(site, row['Geschlecht'], 'gender')}

        # P27 = country of citizenship, Q183 = Germany
        # data['P27'] = {'value': 'Q183'}
        data['P196'] = {'value': 'Q343'}

        # P19 = place of birth
        place_of_birth = ItemHelper.get_qid(site, row['G-Ort'], 'city')
        if place_of_birth is not None:
            # data['P19'] = {'value': place_of_birth}
            data['P342'] = {'value': place_of_birth}

        # P20 = place of death
        # place_of_death = ItemHelper.get_qid(site, row['S-Ort'], 'city')
        # if place_of_death is not None:
        # data['P20'] = place_of_death
        # data['P764'] = place_of_death

        # P735 = given name
        given_name = ItemHelper.get_qid(site, row['Vorname'], 'given_name')
        if given_name is not None:
            # data['P735'] = {'value': given_name}
            data['P187'] = {'value': given_name}

        # P734 = family name
        family_name = ItemHelper.get_qid(site, row['Nachname'], 'family_name')
        if family_name is not None:
            # data['P734'] = {'value': family_name}
            data['P36616'] = {'value': family_name}

        # P106 = occupation, Q16533 = judge
        # data['P106'] = {'value': 'Q16533'}
        data['P204'] = {'value': 'Q72884'}

        # P108 = employer, Q687323 = Federal Court of Justice of Germany
        # data['P108'] = {'value': 'Q687323'}
        data['P40101'] = {'value': 'Q79795'}

        accession_date = CSVParser.parse_date(row['B-J'], row['B-M'], row['B-T'])
        if accession_date is not None:
            # P580 = start time
            # data['P108']['qualifiers'] = {'P580': accession_date}
            data['P40101']['qualifiers'] = {'P355': accession_date}

        withdrawal_date = CSVParser.parse_date(row['A-J'], row['A-M'], row['A-T'])
        if withdrawal_date is not None:
            # P582 = end time
            # data['P108']['qualifiers']['P582'] = withdrawal_date
            data['P40101']['qualifiers']['P356'] = withdrawal_date

        # Source of the data
        if row['Wikipedia'] == '0':
            # data['source'] = {'reference_url': 'http://www.richter-im-internet.de',
            #                  'stated_in': 'Q32961325',
            #                  'imported_from': None}
            data['source'] = {'reference_url': 'http://www.richter-im-internet.de',
                              'stated_in': 'Q72885',
                              'imported_from': None}

        else:
            # data['source'] = {'reference_url': None,
            #                  'stated_in': None,
            #                  'imported_from': 'Q48183'}
            data['source'] = {'reference_url': None,
                              'stated_in': None,
                              'imported_from': 'Q74404'}

        return data

    @staticmethod
    def parse_date(year, month, day):
        """
        Helper function to parse a date.

        @param year: The year which should be parsed.
        @type year: string
        @param month: The month which should be parsed.
        @type month: string
        @param day: The day which should be parsed.
        @type day: string

        @return: The parsed date
        @rtype: array
        """
        if year == '':
            return None
        elif month == '':
            # Q12138 = Gregorian Calender Model
            return [int(year), None, None, 'Q12138']
            # return [int(year), None, None, 'Q72886']
        elif day == '':
            return [int(year), int(month), None, 'Q12138']
            # return [int(year), int(month), None, 'Q72886']
        else:
            return [int(year), int(month), int(day), 'Q12138']
            # return [int(year), int(month), int(day), 'Q72886']


class CSVWriter:
    """
    Helper Class for writing data into csv.
    """

    @staticmethod
    def write_item_in_csv(csv_file, qid, first_name, family_name):
        """
        Helper function to write an item into a csv.

        @param csv_file: The file where the item should be written in.
        @type csv_file: string
        @param qid: The qid of the item which will be written in the file.
        @type qid: string
        @param first_name: The first name of the item which will be written in the file.
        @type first_name: string
        @param first_name: The family name of the item which will be written in the file.
        @type family_name: string
        """

        with open(csv_file, 'a') as cf:
            csv_writer = csv.writer(cf, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([qid, first_name, family_name])
