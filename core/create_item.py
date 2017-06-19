import pywikibot

class ItemCreator:

    def __init__(self, site):
        self.site = site
        self.repo = self.site.data_repository()


    def create_item(self, label_dict):
        new_item = pywikibot.ItemPage(self.site)
        new_item.editLabels(labels=label_dict, summary="Setting labels")
        # TODO: Beschreibung und Aliase hinzufügen
        return new_item.getID()

    def set_claim(self, item_id, property, data, mode):
        item = pywikibot.ItemPage(self.repo, item_id)
        if mode == 'item':
            target = pywikibot.ItemPage(self.repo, data)
            claim = pywikibot.Claim(self.repo, property)
        elif mode == 'point_in_time':
            year, month, day, model = data
            year, month, day = int(year), int(month), int(day),
            claim = pywikibot.Claim(self.repo, property)
            # TODO: testen, ob das mit dem richtiges Wikidata funktioniert
            # entity_helper_string = str('http://test.wikidata.org/entity/' + model).format()
            # wb_time = pywikibot.WbTime(year=year, month=month, day=day, calendarmodel=entity_helper_string)
            target = pywikibot.WbTime(year=year, month=month, day=day)
        elif mode == 'quantity':
            value, uncert, unit = data
            value, uncert = float(value), float(uncert)
            claim = pywikibot.Claim(self.repo, property)
            # TODO: URL auf richtiges Wikidata umstellen
            entity_helper_string = str('http://test.wikidata.org/entity/' + unit).format()
            target = pywikibot.WbQuantity(amount=value, unit=entity_helper_string, error=uncert)
        else:
            return None

        claim.setTarget(target)
        item.addClaim(claim, bot=True, summary='Adding claim with property ' + property + '.')
        return claim

    def create_source_claim(self, claim, property, source_data):
        trgt_item, ref_url = source_data
        trgt_itempage = pywikibot.ItemPage(self.repo, trgt_item)
        source_claim = pywikibot.Claim(self.repo, property, isReference=True)
        source_claim.setTarget(trgt_itempage)
        # TODO: klären was gebraucht wird
        # source_claim = pywikibot.Claim(repo, property, isReference=True)
        # source_claim.setTarget(ref_url)
        claim.addSources([source_claim])
        return True


# Test

# new_item_id = create_item(site, some_labels)

# some_labels = {"en": "Hamburg Main Station", "de": "Hamburg Hauptbahnhof"}
#_half_life = "P525"
# p_day_of_birth = "P35733"
# p_instance_of = "P82"
# p_stated_in = "P149"
# p_reference_url = "P93"

# data = {"uranium-240": {"half_life": ["14.1", "0.1", "Q1748"],
        #                         "source": ["Q1751", "http://www.nndc.bnl.gov/chart/reCenter.jsp?z=92&n=148"],
        #                         "day_of_birth": [1995, 12, 1, "Q70575"],
        #                         "instance_of": "Q1954"}
    #         }

# item_creator = ItemCreator(pywikibot.Site("test", "wikidata"))
# claim = item_creator.set_claim("Q70574", p_instance_of, data["uranium-240"]["instance_of"], 'item')
# item_creator.create_source_claim(claim, p_stated_in, data["uranium-240"]["source"])