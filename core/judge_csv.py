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
            data = {'labels': {'de': "%s %s %s" % (row['Vorname'], row['Namenszusatz'], row['Nachname'])}}
        else:
            data = {'labels': {'de': "%s %s" % (row['Vorname'], row['Nachname'])}}

        # Aliases for the data
        if row['Namenszusatz'] != '':
            data['aliases'] = {'de': "%s %s %s" % (row['Vorname'], row['Nachname'])}

        # Descriptions for the data
        if row['Geschlecht'] == '1':
            data['descriptions'] = {'de': 'deutscher Jurist, Richter am Bundesgerichtshof',
                                    'en': 'German judge, Federal Court of Justice',
                                    'fr': 'Juge allemand, Cour Fédérale de Justice',
                                    'it': 'Giudice tedesco, Corte di Cassazione Federale',
                                    'es': 'Juez alemán, Tribunal Federal Supremo',
                                    'pl': 'Niemiecki sędzia, Trybunał Federalny',
                                    'nl': 'Duits rechter, Federale Gerechtshof',
                                    'zh': '德国法律学者, 德国联邦最高法院'}
        else:
            data['descriptions'] = {'de': 'deutsche Juristin, Richterin am Bundesgerichtshof',
                                    'en': 'German judge, Federal Court of Justice',
                                    'fr': 'Juge allemande, Cour Fédérale de Justice',
                                    'it': 'Giudice tedesca, Corte di Cassazione Federale',
                                    'es': 'Jueza alemana, Tribunal Federal Supremo',
                                    'pl': 'Niemiecki sędzia, Trybunał Federalny',
                                    'nl': 'Duits rechter, Federale Gerechtshof',
                                    'zh': '德国法律学者, 德国联邦最高法院'
                                    }

        # P31 = instance of, Q5 = human
        data['P31'] = 'Q5'
        # data['P82'] = 'Q26'

        # P569 = date of birth
        date_of_birth = CSVParser.parse_date(row['G-J'], row['G-M'], row['G-T'])
        if date_of_birth is not None:
            data['P569'] = date_of_birth
            # data['P18'] = date_of_birth

        # P570 = date of death
        date_of_death = CSVParser.parse_date(row['T-J'], row['T-M'], row['T-T'])
        if date_of_death is not None:
            data['P570'] = date_of_death

        # P21 = sex or gender
        data['P21'] = ItemHelper.get_qid(site, row['Geschlecht'], 'gender')

        # P27 = country of citizenship, Q183 = Germany
        data['P27'] = 'Q183'
        # data['P196'] = 'Q343'

        # P19 = place of birth
        place_of_birth = ItemHelper.get_qid(site, row['G-Ort'], 'city')
        if place_of_birth is not None:
            data['P19'] = place_of_birth
            # data['P342'] = place_of_birth

        # P20 = place of death
        place_of_death = ItemHelper.get_qid(site, row['S-Ort'], 'city')
        if place_of_death is not None:
            data['P20'] = place_of_death

        # P735 = given name
        given_name = ItemHelper.get_qid(site, row['Vorname'], 'given_name')
        if given_name is not None:
            data['P735'] = given_name
            # data['P187'] = given_name

        # P734 = family name
        family_name = ItemHelper.get_qid(site, row['Nachname'], 'family_name')
        if family_name is not None:
            data['P734'] = family_name
            # data['P36616'] = family_name

        # P106 = occupation, Q16533 = judge
        data['P106'] = 'Q16533'
        # data['P204'] = 'Q72884'

        # Source of the data
        data['source'] = ['http://www.richter-im-internet.de', 'Q32961325']
        # data['source'] = ['http://www.richter-im-internet.de', 'Q72885']

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
