import csv
import ItemHelper


# TODO: Documentation
class CSVParser:
    def __init__(self, site):
        self.item_helper = ItemHelper(site)

    def parse_data(self, row):
        # TODO: Clarify if label should be with or without name affix
        data = {'labels': {'de': row['Vorname'] + " " + row['Nachname']}}
        if row['Namenszusatz'] != '':
            data['aliases'] = {'de': row['Vorname'] + " " + row['Namenszusatz'] + " " + row['Nachname']}
        # TODO: Clarify with description should be given and how to deal with differnent genders in german
        data['descriptions'] = {'de': 'Deutsche(r) Richter(in)', 'en': 'German judge'}
        # P31 = instance of
        data['P31'] = "Q5"
        # TODO: Enter a key distinction between date of birth and date of death
        # P569 = date of birth
        data['P569'] = [row['J'], row['M'], row['T'], "Q12138"]
        # P570 = date of death
        data['P570'] = [row['J'], row['M'], row['T'], "Q12138"]
        # TODO: Clarify if information is given at all
        # P21 = sex or gender
        data['P21'] = self.item_helper.get_qid(row['Gender'], "gender")
        # TODO: Clarify if Germany is country of citizenship of all judges
        # P27 = country of citizenship
        data['P27'] = "Q183"
        # P19 = place of birth
        data['P19'] = self.item_helper.get_qid(row['Geburtsort'], "city")
        # P20 = place of death
        data['P20'] = self.item_helper.get_qid(row['Sterbeort'], "city")
        # P735 = given name
        data['P735'] = self.item_helper.get_qid(row['Vorname'], "given_name")
        # P734 = family name
        data['P734'] = self.item_helper.get_qid(row['Namchname'], "family_name")
        # TODO: Clarify if other occupations can be set
        # P106 = occupation
        data['P106'] = "Q16533"
        # TODO: Fill field with a source
        data['source'] = ["...", "..."]
        return data


class CSVWriter:
    def __init__(self, csv_file):
        self.csv_file = csv_file

    def write_item_in_csv(self, qid, name):
        with open(self.csv_file, 'a') as cf:
            csv_writer = csv.writer(cf, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([qid, name])
