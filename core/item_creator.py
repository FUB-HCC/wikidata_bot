import pywikibot
import datetime


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

    def __create_source_claim(self, claim, source_data):
        # TODO: Clarify what is needed (url or item)
        # TODO: Clarify if P854 (reference URL) or P143 (imported from) or P813 (retrieved) or all are needed
        trgt_item, ref_url = source_data

        trgt_itempage = pywikibot.ItemPage(self.site, trgt_item)
        item_source_claim = pywikibot.Claim(self.site, 'P143', isReference=True)
        item_source_claim.setTarget(trgt_itempage)

        url_source_claim = pywikibot.Claim(self.site, 'P854', isReference=True)
        url_source_claim.setTarget(ref_url)

        date_source_claim = pywikibot.Claim(self.site, 'P813', isReference=True)
        date = datetime.datetime.now()
        trgt_datetime = pywikibot.WbTime(year=date.year, month=date.month, day=date.day)
        date_source_claim.setTarget(trgt_datetime)

        # TODO: Clarify if botflag is needed here
        claim.addSources([item_source_claim, url_source_claim, trgt_datetime])

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
                self.__create_source_claim(claim,data["source"])
