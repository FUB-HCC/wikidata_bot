import csv
import pywikibot
import ItemCreator
from pywikibot.data import api

site = pywikibot.Site("test", "wikidata")
repo = site.data_repository()

claims_ids = ['P19', 'P20', 'P31', 'P27', 'P106', 'P569', 'P570', 'P21', 'P734', 'P735']

def get_items(site, item_title):
    """
    Requires a site and search term (item_title) and returns the results.
    """
    params = {"action": "wbsearchentities",
              "format": "json",
              "language": "en",
              "type": "item",
              "search": item_title
              }
    request = api.Request(site=site, **params)
    return request.submit()

def get_qids(search_results):
    qids = []
    [qids.append(result["id"]) for result in search_results["search"]]
    return qids

def get_item_data(site, qids):

    params = {"action": "wbgetentities",
              "format": "json",
              "ids": '|'.join(qids)
              }
    request = api.Request(site=site, **params)
    return request.submit()

def get_qid(name, mode):
    if mode == "gender":
        if name.lower() == "weiblich":
            return "Q6581072"
        elif name.lower() == "männlich":
            return "Q6581097"
    else:

        qids = get_qids(get_items(site, name))
        result = get_item_data(site, qids)

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
                    if temp_result['mainsnak']['datavalue']['value']['id'] == "Q12308941" or temp_result['mainsnak']['datavalue']['value']['id'] == "Q11879590":
                        return qid

    return None

def parse_data(row, name=None, name_with_affix=None):

    data = {}
    # TODO: Klären, ob Label mit oder ohne Namenszusatz
    data['labels'] = {'de': name}
    data['aliases'] = {'de': name_with_affix}
    # TODO: Klären welche Beschreibung
    data['description'] = {'de': 'Deutsche(r) Richter(in)', 'en': 'German judge'}
    # P31 = instance of
    data['P31'] = "Q5"
    # TODO: Unterscheidung von day_of_birth und day_of_death
    # P569 = date of birth
    data['P569'] = [row['J'], row['M'], row['T'], "Q12138"]
    # P570 = date of death
    data['P570'] = [row['J'], row['M'], row['T'], "Q12138"]
    # TODO: Klären, ob diese Information überhaupt vorhanden ist
    # P21 = sex or gender
    data['P21'] = get_qid(row['Gender'], "gender")
    # TODO: Klären, ob Staatsangehörosgkeit bei allen Richtern deutsch ist
    # P27 = country ofcitizenship
    data['P27'] = "Q183"
    # P19 = place of birth
    data['P19'] = get_qid(row['Geburtsort'], "city")
    # P20 = place of death
    data['P20'] = get_qid(row['Sterbeort'], "city")
    # P735 = given name
    data['P735'] = get_qid(row['Vorname'], "given_name")
    # P734 = family name
    data['P734'] = get_qid(row['Namchname'], "family_name")
    # TODO: Klären, ob weitere Berufe angegeben werden können
    # P106 = occupation
    data['P106'] = "Q16533"

    # TODO: Source befüllen bzw. klären, ob nicht als globele Variable sinnvoller
    data['source'] = ["...", "..."]

    return data

data = {}
with open('namen.csv', newline='') as csvfile:

    reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')

    for row in reader:

        name, name_with_affix = None, None

        if row['Vorname'] != '' and row['Nachname'] != '':
            name = row['Vorname'] + " " + row['Nachname']
            if row['Namenszusatz'] != '':
                name_with_affix = row['Vorname'] + " " + row['Namenszusatz'] + " " + row['Nachname']

        if name != None:
            qids = []
            search_results = get_items(site, name)
            qids += get_qids(search_results)
            if name_with_affix != None:
                search_results = get_items(site, name_with_affix)
                qids += get_qids(search_results)
            qids = set(qids)

            if len(search_results["search"]) == 0:
                data[name] = parse_data(row, name, name_with_affix)
                print("An item with the name %s don't exist." % name)
            else:
                print("An item with the name %s may already exist." % name)
        else:
            print("No qualified name available to search.")

# TODO: auslagern

item_creator = ItemCreator(site)

for key in data:
    new_item_id = item_creator.create_item(data['labels'])

    for claim_id in claims_ids:
        claim = item_creator.set_item_claim(new_item_id, claim_id, data[key][claim_id])
        item_creator.create_source_claim(claim, data[key]["source"])