import pywikibot
from pywikibot.data import api
import datetime
import logging


class ItemCreator:
    """
    Wrapper Class for creating and editing an item.
    """

    # edit_count = 1
    @staticmethod
    def new_item(site):
        """
        Helper function to create a new item.

        @param site: The data repository where the new item will be created
        @type site: pywikibot.site.DataSite

        @return: The new ItemPage
        @rtype: pywikibot.page.ItemPage
        """
        item = pywikibot.ItemPage(site)
        return item

    # edit_count = 3
    @staticmethod
    def add_terms(item, data):
        """
        Helper function to add labels, aliases and descriptions to an item.

        @param item: The item to which the terms will be added
        @type item: pywikibot.page.ItemPage
        @param data: The data which will be added to the item
        @type data: dict
        """
        item.editLabels(labels=data['labels'], bot=True, summary='Labels were edited by a bot')
        if 'aliases' in data:
            item.editAliases(aliases=data['aliases'], bot=True, summary='Aliases were edited by a bot')
        item.editDescriptions(descriptions=data['descriptions'], bot=True, summary='Descriptions were edited by a bot')

    # edit_count = 1
    @staticmethod
    def add_claim(site, item, pid, data):
        """
        Helper function to add a claim to an item.

        @param site: The data repository where the new claim will be added
        @type site: pywikibot.site.DataSite
        @param item: The item to which the claim will be added
        @type item: pywikibot.page.ItemPage
        @param pid: property id of the property which belongs to the claim
        @type pid: string
        @param data: The data which will be added to the item
        @type data: dict

        @return: The new Claim or None, if no Claim was created
        @rtype: pywikibot.page.Claim, None
        """
        claim = pywikibot.Claim(site, pid)

        if claim.type == 'wikibase-item':
            target = pywikibot.ItemPage(site, data)
        elif claim.type == 'time':
            year, month, day, model = data
            # model_uri = "%s%s" % (site.concept_base_uri, model)
            # target = pywikibot.WbTime(year=year, month=month, day=day, calendarmodel=model_uri)
            target = pywikibot.WbTime(year=year, month=month, day=day)
        elif claim.type == 'quantity':
            value, uncert, unit = data
            value, uncert = float(value), float(uncert)
            entity_uri = site.concept_base_uri + unit
            target = pywikibot.WbQuantity(amount=value, unit=entity_uri, error=uncert)
        else:
            return None

        claim.setTarget(target)
        item.addClaim(claim, bot=True, summary='A new claim was created by a bot')
        return claim

    # edit_count = 1
    @staticmethod
    def add_sources(site, claim, data):
        """
        Helper function to add sources to a claim.

        @param site: The data repository where the sources will be added
        @type site: pywikibot.site.DataSite
        @param claim: The claim to which the sources will be added
        @type claim: pywikibot.page.Claim
        @param data: The data which will be added to the claim
        @type data: dict

        @return: A value which indicates if adding the claim was successful
        @rtype: bool
        """

        if data['reference_url'] is not None:
            # P854 = reference URL
            # url_source_claim = pywikibot.Claim(site, 'P854', isReference=True)
            url_source_claim = pywikibot.Claim(site, 'P93', isReference=True)
            url_source_claim.setTarget(data['reference_url'])

        if data['stated_in'] is not None:
            # P248 = stated in
            trgt_itempage = pywikibot.ItemPage(site, data['stated_in'])
            # item_source_claim = pywikibot.Claim(site, 'P248', isReference=True)
            item_source_claim = pywikibot.Claim(site, 'P149', isReference=True)
            item_source_claim.setTarget(trgt_itempage)

        if data['imported_from'] is not None:
            # P143 = imported from
            trgt_itempage = pywikibot.ItemPage(site, data['imported_from'])
            # item_source_claim = pywikibot.Claim(site, 'P143', isReference=True)
            item_source_claim = pywikibot.Claim(site, 'P9', isReference=True)
            item_source_claim.setTarget(trgt_itempage)

        # P813 = retrieved
        # date_source_claim = pywikibot.Claim(site, 'P813', isReference=True)
        date_source_claim = pywikibot.Claim(site, 'P388', isReference=True)
        date = datetime.datetime.now()
        trgt_datetime = pywikibot.WbTime(year=date.year, month=date.month, day=date.day)
        date_source_claim.setTarget(trgt_datetime)

        if data['reference_url'] is None:
            claim.addSources([item_source_claim, date_source_claim], bot=True,
                             summary='New sources were added to a claim by a bot')
        else:
            claim.addSources([item_source_claim, url_source_claim, date_source_claim], bot=True,
                         summary='New sources were added to a claim by a bot')

        return True

    # edit_count = 4 + (x * 2), x = ca. 20
    @staticmethod
    def create_item(site, data):
        """
        Helper function to create a new item with labels, aliases, descriptions and claims with sources.

        @param site: The data repository where the sources will be added
        @type site: pywikibot.site.DataSite
        @param data: The data which will be added to item
        @type data: dict

        @return: The id of the new created item
        @rtype: string
        """
        item = ItemCreator.new_item(site)
        ItemCreator.add_terms(item, data)
        for key in data:
            if key != 'labels' and key != 'aliases' and key != 'descriptions' and key != 'source':
                claim = ItemCreator.add_claim(site, item, key, data[key])
                if claim is not None:
                    ItemCreator.add_sources(site, claim, data['source'])
        return item.getID()


class ItemHelper:
    """
    Helper Class for an item.
    """

    @staticmethod
    def item_exist(site, data):
        """
        Helper function to check if an item with specific data already exists.

        @param site: The data repository where it will be checked if item exist.
        @type site: pywikibot.site.DataSite
        @param data: The data with which it will be checked if item exist.
        @type data: dict

        @return: A value which indicates if item exist.
        @rtype: bool
        """
        name, name_with_affix = None, None

        if data['Vorname'] != '' and data['Nachname'] != '':
            name = "%s %s" % (data['Vorname'], data['Nachname'])
            if data['Namenszusatz'] != '':
                name_with_affix = "%s %s %s" % (data['Vorname'], data['Namenszusatz'], data['Nachname'])
        else:
            raise ValueError('The data has now qualified Name. First name and family name are both needed!')

        qids = ItemHelper.get_qids(APICaller.wbsearchentities(site, name, 'de'))
        qids += ItemHelper.get_qids(APICaller.wbsearchentities(site, name, 'en'))
        if name_with_affix is not None:
            qids += ItemHelper.get_qids(APICaller.wbsearchentities(site, name_with_affix, 'de'))
            qids += ItemHelper.get_qids(APICaller.wbsearchentities(site, name_with_affix, 'en'))
        qids = set(qids)

        return len(qids) is not 0

    @staticmethod
    def get_qid(site, item_title, mode):
        """
        Helper function to search an existing item with the title item_titel and return its id.

        @param site: The data repository where to search for an existing item with item_title.
        @type site: pywikibot.site.DataSite
        @param item_title: The title to search for. @type item_title: string @param mode: The
        mode to specify which instance the item should be from (e.g. mode=city -> item should have claim: instance of
        city)
        @type mode: string

        @return: The matching QID or None if no one was found
        @rtype: string, None
        """
        if item_title is None or item_title is '':
            return None

        if mode == 'gender':
            if item_title == '0':
                # return 'Q6581072'
                return 'Q1341'
            elif item_title == '1':
                # return 'Q6581097'
                return 'Q505'
        else:
            qids = ItemHelper.get_qids(APICaller.wbsearchentities(site, item_title, 'de'))
            qids += ItemHelper.get_qids(APICaller.wbsearchentities(site, item_title, 'en'))
            if len(qids) != 0:
                result = APICaller.wbgetentities(site, qids)

            for qid in qids:
                # if 'P31' in result['entities'][qid]['claims']:
                # for claim in result['entities'][qid]['claims']['P31']:
                if 'P81' in result['entities'][qid]['claims']:
                    for claim in result['entities'][qid]['claims']['P81']:
                        # if mode == 'city' and claim['mainsnak']['datavalue']['value']['id'] == 'Q515':
                        if mode == 'city' and claim['mainsnak']['datavalue']['value']['id'] == 'Q2215':
                            return qid
                        # elif mode == 'family_name' and claim['mainsnak']['datavalue']['value']['id'] == 'Q101352':
                        elif mode == 'family_name' and claim['mainsnak']['datavalue']['value']['id'] == 'Q72891':
                            return qid
                            # elif mode == 'given_name' and (
                            # claim['mainsnak']['datavalue']['value']['id'] == 'Q12308941' or
                            # claim['mainsnak']['datavalue']['value']['id'] == 'Q11879590'):
                        elif mode == 'given_name' and claim['mainsnak']['datavalue']['value']['id'] == 'Q72890':
                            return qid

        return None

    @staticmethod
    def get_qids(response):
        """
        Helper function to get all qids out of an response dict from API request with action wbsearchentities.

        @param response: The response from API request with action wbsearchentities.
        @type response: dict

        @return: All QIDs
        @rtype: array
        """
        qids = []
        for result in response['search']:
            qids.append(result['id'])
        return qids


class APICaller:
    """
    Wrapper Class for The MediaWiki action API.
    """

    @staticmethod
    def wbgetentities(site, ids):
        """
        Helper function to make a request with action wbgetentities.

        @param site: The Site to which the request will be submitted.
        @type site: string
        @param ids: The QIDs of the items which should be requested.
        @type ids: array

        @return: a dict containing data retrieved from api.php
        @rtype: dict
        """
        params = {'action': 'wbgetentities',
                  'format': 'json',
                  # 'assert': 'user',
                  'ids': '|'.join(ids)
                  }
        request = api.Request(site=site, **params)
        return request.submit()

    @staticmethod
    def wbsearchentities(site, item_title, language):
        """
        Helper function to make a request with action wbgetentities.

        @param site: The Site to which the request will be submitted.
        @type site: string
        @param item_title: The text string to search for.
        @type item_title: string
        @param language: The language to search in.
        @type language: string

        @return: a dict containing data retrieved from api.php
        @rtype: dict
        """
        params = {'action': 'wbsearchentities',
                  'format': 'json',
                  'language': language,
                  'type': 'item',
                  'search': item_title
                  }
        request = api.Request(site=site, **params)
        return request.submit()
