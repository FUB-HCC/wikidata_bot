import csv
import pywikibot
from judge_item import ItemHelper, ItemCreator
from judge_csv import CSVParser, CSVWriter
import time
import yaml
import logging

# TODO: Clarify if label can be in other languages
# TODO: Consider that Wikipedia data will be included as well
# TODO: Test again on test.wikidata
# TODO: Clarify if calender model attribute works in add_claim -> Will be proved while testing / bot request
# TODO: Start the bot request
# TODO: Clarify if bot flags are set right -> Will be proved while bot request
# TODO: Clarify if bot flag is needed for new_item -> Will be proved while bot request

with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.load(file)

logging.basicConfig(filename=config['log_file'], level=logging.INFO)
site = pywikibot.Site(config['site']['language'], config['site']['site'])

# One item creation with adding all known data takes ca. 20 edits,
# so if edit limit is 100, 5 items can be crated within a minute
item_creations_per_minute = config['edits_per_minute'] / 20

current_item_creations = 0
current_time = time.clock()

start_time = time.clock()
current_process_time = time.clock()

with open(config['data_file'], newline='') as file:
    count = len(list(csv.DictReader(file, delimiter=';', quotechar='"')))

with open(config['data_file'], newline='') as file:
    reader = csv.DictReader(file, delimiter=';', quotechar='"')

    for index, row in enumerate(reader):
        try:
            if not ItemHelper.item_exist(site, row):
                logging.info("Check if item with name %s %s exist: False" % (row['Vorname'], row['Nachname']))
                data = CSVParser.parse_data(site, row)
                logging.info('Data for item parsed.')

                if current_item_creations == item_creations_per_minute:
                    if time.clock() - current_time < 60:
                        time.sleep(60 - (time.clock() - current_time))
                        logging.info("Sleep for %i seconds" % (60 - (time.clock() - current_time)))
                        current_time = time.clock()
                        current_item_creations = 1
                        qid = ItemCreator.create_item(site, data)
                    else:
                        current_time = time.clock()
                        current_item_creations = 1
                        qid = ItemCreator.create_item(site, data)
                else:
                    if time.clock() - current_time >= 60:
                        current_time = time.clock()
                        current_item_creations = 1
                        qid = ItemCreator.create_item(site, data)
                    else:
                        current_item_creations += 1
                        qid = ItemCreator.create_item(site, data)

                logging.info("New item with was created, QID: %s " % qid)
                CSVWriter.write_item_in_csv(config['result_file'], qid, row['Vorname'], row['Nachname'])
                logging.info("The item was saved to csv file")
            else:
                logging.info("Check if item with name %s %s exist: True" % (row['Vorname'], row['Nachname']))
        except ValueError as error:
            logging.warning(repr(error))

        logging.info("%d of %d items processed in %fs" % (index + 1, count, (time.clock() - current_process_time)))
        current_process_time = time.clock()

    logging.info("Finished process in %fs" % (time.clock() - start_time))
