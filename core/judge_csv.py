import csv
from judge_item import ItemHelper


class CSVParser:
    @staticmethod
    def parse_data(site, row):
        # Labels for the data
        # TODO: Clarify if label should be with or without name affix
        data = {'labels': {'de': "%s %s" % (row['Vorname'], row['Nachname'])}}

        # Aliases for the data
        if row['Namenszusatz'] != '':
            data['aliases'] = {'de': "%s %s %s" % (row['Vorname'], row['Namenszusatz'], row['Nachname'])}

        # Descriptions for the data
        # TODO: Clarify with description should be given and how to deal with different genders in german
        data['descriptions'] = {'de': 'Deutsche*r Richter*in', 'en': 'German judge', 'fr': 'Juge allemand*e'}

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
        # TODO: Clarify if information is given at all
        data['P21'] = ItemHelper.get_qid(site, row['Gender'], 'gender')

        # P27 = country of citizenship, Q183 = Germany
        # TODO: Clarify if Germany is country of citizenship of all judges
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
        # TODO: Clarify if other occupations can be set
        data['P106'] = 'Q16533'
        # data['P204'] = 'Q72884'

        # Source of the data
        # TODO: Fill qid field with a source
        data['source'] = ['http://www.richter-im-internet.de', '']
        # data['source'] = ['http://www.richter-im-internet.de', 'Q72885']

        return data

    @staticmethod
    def parse_date(year, month, day):
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
    @staticmethod
    def write_item_in_csv(csv_file, qid, first_name, family_name):
        with open(csv_file, 'a') as cf:
            csv_writer = csv.writer(cf, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([qid, first_name, family_name])
