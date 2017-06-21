import pywikibot

# TODO: Documentation
class ItemCreator:

    def __init__(self, site):
        self.site = site

    def __new_item(self):
        # TODO: Clarify if botflag is needed here
        item = pywikibot.ItemPage(self.site, bot=True)
        return item

    def __set_claim(self, item, property, data):

        claim = pywikibot.Claim(self.site, property)

        if claim.type == 'wikibase-item':
            target = pywikibot.ItemPage(self.site, data)
        elif claim.type == 'time':
            year, month, day, model = data
            year, month, day = int(year), int(month), int(day),
            # TODO: Test if that works with wikidata.org (with test.wikidat.org it dosen't)
            # entity_uri = self.site.concept_base_uri + model
            # wb_time = pywikibot.WbTime(year=year, month=month, day=day, calendarmodel=entity_uri)
            target = pywikibot.WbTime(year=year, month=month, day=day)
        elif claim.type == 'quantity':
            value, uncert, unit = data
            value, uncert = float(value), float(uncert)
            entity_uri = self.site.concept_base_uri + unit
            target = pywikibot.WbQuantity(amount=value, unit=entity_uri, error=uncert)
        else:
            return None

        claim.setTarget(target)
        # TODO: Clarify if botflag is needed here
        item.addClaim(claim, bot=True, summary='Adding claim with property ' + property + '.')
        return claim

    def __create_source_claim(self, claim, property, source_data):
        trgt_item, ref_url = source_data
        trgt_itempage = pywikibot.ItemPage(self.site, trgt_item)
        source_claim = pywikibot.Claim(self.site, property, isReference=True)
        source_claim.setTarget(trgt_itempage)
        # TODO: Clarify what is needed (url or item)
        # source_claim = pywikibot.Claim(self.site, property, isReference=True)
        # source_claim.setTarget(ref_url)
        # TODO: Clarify if botflag is needed here
        claim.addSources([source_claim])
        return True

    def create_item(self, data):
        item = self.__new_item
        # TODO: Check if method names are correct
        # TODO: Clarify if botflag is needed here
        item.editLabels(labels=data['labels'], summary="Setting labels")
        item.editAliases(alsiases=data['aliases'], summary="Setting aliases")
        item.editDescription(description=data['descriptions'], summary="Setting descriptions")
        for key in data:
            if key != 'lables' and key != 'aliases' and key != 'descriptions' and key != 'source':
                claim = self.__set_claim(item, key, data[key])
                self.__create_source_claim(claim, data["source"])