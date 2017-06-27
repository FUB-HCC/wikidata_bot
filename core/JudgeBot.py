import csv
import pywikibot
import ItemCreator
import CSVParser
import CSVWriter
import ItemHelper

# TODO: Documentation
# TODO: Fulfil all bot requirements (https://www.wikidata.org/wiki/Wikidata:Bots)

site = pywikibot.Site("test", "wikidata")
item_helper = ItemHelper(site)
item_creator = ItemCreator(site)
csv_parser = CSVParser(site)
csv_writer = CSVWriter('result.csv')

# TODO: Set a limit for maximum edits per minute
with open('namen.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')

    for row in reader:
        if item_helper.item_exist(row):
            data = csv_parser.parse_data(row)
            print("An item with the name %s don't exist." % data['labels']['de'])
            qid = item_creator.create_item(data)
            csv_writer.write_item_in_csv(qid, data['labels']['de'])
            print("An item with the qid %s was created." % qid)
        else:
            print("An item with the name %s may already exist." % data['labels']['de'])
