import pywikibot
site = pywikibot.Site("test", "wikidata")

def create_item(site, label_dict):
    new_item = pywikibot.ItemPage(site)
    new_item.editLabels(labels=label_dict, summary="Setting labels")
    # Add description here or in another function
    return new_item.getID()

some_labels = {"en": "Hamburg Main Station", "de": "Hamburg Hauptbahnhof"}
new_item_id = create_item(site, some_labels)
