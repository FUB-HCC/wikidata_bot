import pywikibot
from pywikibot.data import api
import datetime


class ItemCreator:
    # Edit count = 1
    @staticmethod
    def new_item(site):
        # TODO: Clarify if bot flag is needed here
        item = pywikibot.ItemPage(site)
        return item

    # Edit count = 3
    @staticmethod
    def add_terms(item, data):
        # TODO: Clarify if bot flag is needed here
        item.editLabels(labels=data['labels'], bot=True, summary="Setting labels")
        if 'aliases' in data:
            item.editAliases(aliases=data['aliases'], bot=True, summary="Setting aliases")
        item.editDescriptions(descriptions=data['descriptions'], bot=True, summary="Setting descriptions")

    # Edit count = 1
    @staticmethod
    def add_claim(site, item, property, data):

        claim = pywikibot.Claim(site, property)

        if claim.type == 'wikibase-item':
            target = pywikibot.ItemPage(site, data)
        elif claim.type == 'time':
            year, month, day, model = data
            # TODO: Test if that works with wikidata.org (with test.wikidat.org it dosen't)
            # entity_uri = self.site.concept_base_uri + model
            # wb_time = pywikibot.WbTime(year=year, month=month, day=day, calendarmodel=entity_uri)
            target = pywikibot.WbTime(year=year, month=month, day=day)
        elif claim.type == 'quantity':
            value, uncert, unit = data
            value, uncert = float(value), float(uncert)
            entity_uri = site.concept_base_uri + unit
            target = pywikibot.WbQuantity(amount=value, unit=entity_uri, error=uncert)
        else:
            return None

        claim.setTarget(target)
        # TODO: Clarify if bot flag is needed here
        item.addClaim(claim, bot=True, summary='Creating claim')
        return claim

    # Edit count = 1
    @staticmethod
    def add_sources(site, claim, source_data):
        ref_url, trgt_item = source_data

        trgt_itempage = pywikibot.ItemPage(site, trgt_item)
        # item_source_claim = pywikibot.Claim(site, 'P143', isReference=True)
        item_source_claim = pywikibot.Claim(site, 'P9', isReference=True)
        item_source_claim.setTarget(trgt_itempage)

        # url_source_claim = pywikibot.Claim(site, 'P854', isReference=True)
        url_source_claim = pywikibot.Claim(site, 'P93', isReference=True)
        url_source_claim.setTarget(ref_url)

        # date_source_claim = pywikibot.Claim(site, 'P813', isReference=True)
        date_source_claim = pywikibot.Claim(site, 'P388', isReference=True)
        date = datetime.datetime.now()
        trgt_datetime = pywikibot.WbTime(year=date.year, month=date.month, day=date.day)
        date_source_claim.setTarget(trgt_datetime)

        # TODO: Clarify if bot flag is needed here
        claim.addSources([item_source_claim, url_source_claim, date_source_claim], bot=True, summary='Adding sources')

        return True

    # Edit count = 4 + (x * 2), x = ca. 20
    @staticmethod
    def create_item(site, data):
        item = ItemCreator.new_item(site)
        ItemCreator.add_terms(item, data)
        for key in data:
            if key != 'labels' and key != 'aliases' and key != 'descriptions' and key != 'source':
                claim = ItemCreator.add_claim(site, item, key, data[key])
                ItemCreator.add_sources(site, claim, data["source"])
        return item.getID()


class ItemHelper:
    @staticmethod
    def item_exist(site, row):
        name, name_with_affix = None, None

        if row['Vorname'] != '' and row['Nachname'] != '':
            name = row['Vorname'] + " " + row['Nachname']
            if row['Namenszusatz'] != '':
                name_with_affix = row['Vorname'] + " " + row['Namenszusatz'] + " " + row['Nachname']
        else:
            raise ValueError('The row has now qualified Name. First name and family name are both needed!')

        qids = ItemHelper.get_qids(APICaller.wbsearchentities(site, name, 'de'))
        qids += ItemHelper.get_qids(APICaller.wbsearchentities(site, name, 'en'))
        if name_with_affix is not None:
            qids += ItemHelper.get_qids(APICaller.wbsearchentities(site, name_with_affix, 'de'))
            qids += ItemHelper.get_qids(APICaller.wbsearchentities(site, name_with_affix, 'en'))
        qids = set(qids)

        return len(qids) is not 0

    @staticmethod
    def get_qid(site, name, mode):
        if name is None or name is '':
            return None

        if mode == "gender":
            if name.lower() == "weiblich":
                return "Q6581072"
            elif name.lower() == "männlich":
                return "Q6581097"
        else:
            qids = ItemHelper.get_qids(APICaller.wbsearchentities(site, name, 'de'))
            qids += ItemHelper.get_qids(APICaller.wbsearchentities(site, name, 'en'))
            if len(qids) != 0:
                result = APICaller.wbgetentities(site, qids)

            for qid in qids:
                # if 'P31' in result['entities'][qid]['claims']:
                    # for claim in result['entities'][qid]['claims']['P31']:
                if 'P81' in result['entities'][qid]['claims']:
                    for claim in result['entities'][qid]['claims']['P81']:
                        # if mode == 'city' and claim['mainsnak']['datavalue']['value']['id'] == "Q515":
                        if mode == 'city' and claim['mainsnak']['datavalue']['value']['id'] == "Q2215":
                            return qid
                        # elif mode == 'family_name' and claim['mainsnak']['datavalue']['value']['id'] == "Q101352":
                        elif mode == 'family_name' and claim['mainsnak']['datavalue']['value']['id'] == "Q72891":
                            return qid
                        # elif mode == 'given_name' and (
                                        # claim['mainsnak']['datavalue']['value']['id'] == "Q12308941" or
                                        # claim['mainsnak']['datavalue']['value']['id'] == "Q11879590"):
                        elif mode == 'given_name' and claim['mainsnak']['datavalue']['value']['id'] == "Q72890":
                            return qid

        return None

    @staticmethod
    def get_qids(json):
        qids = []
        for result in json["search"]:
            qids.append(result["id"])
        return qids


class APICaller:
    # get_item_data
    @staticmethod
    def wbgetentities(site, qids):
        params = {"action": "wbgetentities",
                  "format": "json",
                  "ids": '|'.join(qids)
                  }
        request = api.Request(site=site, **params)
        return request.submit()

    # get items
    @staticmethod
    def wbsearchentities(site, name, language):
        """
        Requires a site and search term (item_title) and returns the results.
        :param name:
        :return:
        """
        params = {"action": "wbsearchentities",
                  "format": "json",
                  "language": language,
                  "type": "item",
                  "search": name
                  }
        request = api.Request(site=site, **params)
        return request.submit()
