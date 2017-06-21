import csv
import pywikibot
import ItemCreator
import CSVParser

# TODO: Documentation
# TODO: Fulfil all bot requirements (https://www.wikidata.org/wiki/Wikidata:Bots)

site = pywikibot.Site("test", "wikidata")
item_creator = ItemCreator(site)
csv_parser = CSVParser(site)

# TODO: Set a limit for maximum edits per minute
with open('namen.csv', newline='') as csvfile:

    reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')

    for row in reader:

        name, name_with_affix = None, None

        if row['Vorname'] != '' and row['Nachname'] != '':
            name = row['Vorname'] + " " + row['Nachname']
            if row['Namenszusatz'] != '':
                name_with_affix = row['Vorname'] + " " + row['Namenszusatz'] + " " + row['Nachname']

        if name != None:
            qids = get_qids(get_items(site, name))
            if name_with_affix != None:
                qids += get_qids(get_items(site, name_with_affix))
            qids = set(qids)

            if len(qids) == 0:
                data = csv_parser.parse_data(row)
                print("An item with the name %s don't exist." % name)
                item_creator.create_item(data)
            else:
                print("An item with the name %s may already exist." % name)
        else:
            print("No qualified name available to search.")