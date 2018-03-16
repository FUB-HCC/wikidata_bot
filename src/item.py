import pywikibot
import yaml

from api import MediaWikiAPI

with open('../config.yaml', 'r', encoding='utf-8') as config_file:
    config = yaml.load(config_file)


class WikidataItem(object):

    SITE = pywikibot.site.DataSite(config['language'], config['site'])

    def __init__(self, item, data=None):
        self.item = item
        if data:
            self.update(data)
        self.id = item.getID()

    def update(self, data):
        """
        Function to update the item with labels, aliases, descriptions and claims with sources.

        @:param data: data to update the item
        @:type data: dict
        """

        self.add_labels(data['labels'])
        self.add_descriptions(data['descriptions'])
        if 'aliases' in data:
            self.add_aliases(data['aliases'])

        self.add_claims(data['claims'], data['references'])

    def add_labels(self, labels):
        """
        Function to add labels to the item.

        @:param labels: labels
        @:type labels: dict
        """
        self.item.editLabels(
            labels=labels,
            bot=True,
            summary='New labels added by JudgeBot'
        )

    def add_descriptions(self, descriptions):
        """
        Function to add descriptions to the item.

        @:param descriptions: description
        @:type descriptions: dict
        """

        self.item.editDescriptions(
            descriptions=descriptions,
            bot=True,
            summary='New descriptions added by JudgeBot'
        )

    def add_aliases(self, aliases):
        """
        Function to add aliases to the item.

        @:param aliases: aliases
        @:type aliases: dict
        """

        self.item.editAliases(
            aliases=aliases,
            bot=True,
            summary='New aliases added by JudgeBot'
        )


    def add_claims(self, claims, references):

        for claim in claims:
            wd_claim = self.add_claim(claim)

            if 'qualifiers' in claim:
                self.add_qualifiers(wd_claim, claim['qualifiers'])
                self.add_references(wd_claim, references)

    def add_claim(self, claim):
        """
        Function to add a claim to the item.

        @:param claim: claim
        @:type claim: dict

        @:return: wd_claim
        @:rtype: pywikibot.page.Claim
        """

        wd_claim = pywikibot.Claim(self.SITE, claim['id'])
        wd_claim.setTarget(self.get_target(wd_claim, claim['value']))

        self.item.addClaim(
            wd_claim,
            bot=True,
            summary='New claim added by JudgeBot'
        )

        return wd_claim

    def add_qualifiers(self, claim, qualifiers):
        """
        Function to add qualifiers to a claim.

        @:param claim: claim
        @:type claim: pywikibot.page.Claim
        @:param qualifiers: qualifiers
        @:type qualifiers: dict
        """

        for qualifier in qualifiers:
            self.add_qualifier(claim, qualifier)

    def add_qualifier(self, claim, qualifier):

        wd_qualifier = pywikibot.Claim(self.SITE, qualifier['id'], isQualifier=True)
        wd_qualifier.setTarget(self.get_target(wd_qualifier, qualifier['value']))

        claim.addQualifier(
            wd_qualifier,
            bot=True,
            summary='New qualifier added by JudgeBot'
        )

    def add_references(self, claim, references):
        """
        Function to add sources to a claim.

        @:param claim: claim
        @:type claim: pywikibot.page.Claim
        @:param references: references
        @:type references: dict
        """

        wd_references = []

        for reference in references:
            wd_reference = pywikibot.Claim(self.SITE, reference['id'], isReference=True)
            wd_reference.setTarget(self.get_target(wd_reference, reference['value']))
            wd_references.append(wd_reference)

        claim.addSources(
            wd_references,
            bot=True,
            summary='New references added by JudgeBot'
        )

    def get_target(self, wd_claim, claim):

        if wd_claim.type == 'wikibase-item':
            return pywikibot.ItemPage(self.SITE, claim)
        elif wd_claim.type == 'time':
            year, month, day = claim
            return pywikibot.WbTime(year=year, month=month, day=day)
        elif wd_claim.type == 'url':
            return claim
        else:
            raise TypeError('claim type ' + wd_claim.type + ' not implemented yet')

    @classmethod
    def new(cls, data=None):
        """
        Function to create a new item.

        @:return: a new wikidata item
        @:rtype: WikidataItem
        """
        return WikidataItem(item=pywikibot.ItemPage(cls.SITE), data=data)

    @classmethod
    def exists(cls, data):

        """
        Function to check if an item with specific data already exists.

        @:param data: data to check if item exists
        @:type data: dict

        @:return: True if item exists, else False
        @:rtype: bool
        """
        name, name_with_affix = None, None

        if data['Vorname'] != '' and data['Nachname'] != '':
            name = "%s %s" % (data['Vorname'], data['Nachname'])
            if data['Namenszusatz'] != '':
                name_with_affix = "%s %s %s" % (data['Vorname'], data['Namenszusatz'], data['Nachname'])
        else:
            raise ValueError('The data has now qualified Name. First name and family name are both needed!')

        qids = MediaWikiAPI().wbsearchentities(name, 'de').extract() \
            + MediaWikiAPI().wbsearchentities(name, 'en').extract()

        if name_with_affix:
            qids += MediaWikiAPI().wbsearchentities(name_with_affix, 'de').extract() \
                + MediaWikiAPI().wbsearchentities(name_with_affix, 'en').extract()

        return len(qids) != 0


