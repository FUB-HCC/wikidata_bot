from pywikibot.data import api


# TODO: Documentation
class CSVParser:
    def __init__(self, site):
        self.site = site

    def __get_items(self, name):
        """
        Requires a site and search term (item_title) and returns the results.
        :param name:
        :return:
        """
        params = {"action": "wbsearchentities",
                  "format": "json",
                  "language": "en",
                  "type": "item",
                  "search": name
                  }
        request = api.Request(site=self.site, **params)
        return request.submit()

    def __get_qids(self, json):
        qids = []
        return [qids.append(result["id"]) for result in json["search"]]

    def __get_item_data(self, qids):

        params = {"action": "wbgetentities",
                  "format": "json",
                  "ids": '|'.join(qids)
                  }
        request = api.Request(site=self.site, **params)
        return request.submit()

    def __get_qid(self, name, mode):
        if mode == "gender":
            if name.lower() == "weiblich":
                return "Q6581072"
            elif name.lower() == "männlich":
                return "Q6581097"
        else:

            qids = self.__get_qids(self.__get_items(name))
            result = self.__get_item_data(qids)

            for qid in qids:
                temp_results = result['entities'][qid]['claims']['P31']
                for temp_result in temp_results:
                    if mode == 'city':
                        if temp_result['mainsnak']['datavalue']['value']['id'] == "Q515":
                            return qid
                    elif mode == 'family_name':
                        if temp_result['mainsnak']['datavalue']['value']['id'] == "Q101352":
                            return qid
                    elif mode == 'given_name':
                        if temp_result['mainsnak']['datavalue']['value']['id'] == "Q12308941" or \
                                        temp_result['mainsnak']['datavalue']['value']['id'] == "Q11879590":
                            return qid

        return None

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
        data['P21'] = self.__get_qid(row['Gender'], "gender")
        # TODO: Clarify if Germany is country of citizenship of all judges
        # P27 = country of citizenship
        data['P27'] = "Q183"
        # P19 = place of birth
        data['P19'] = self.__get_qid(row['Geburtsort'], "city")
        # P20 = place of death
        data['P20'] = self.__get_qid(row['Sterbeort'], "city")
        # P735 = given name
        data['P735'] = self.__get_qid(row['Vorname'], "given_name")
        # P734 = family name
        data['P734'] = self.__get_qid(row['Namchname'], "family_name")
        # TODO: Clarify if other occupations can be set
        # P106 = occupation
        data['P106'] = "Q16533"
        # TODO: Fill field with a source
        data['source'] = ["...", "..."]
        return data
