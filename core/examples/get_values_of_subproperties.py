# -*- coding: utf-8  -*-
import pywikibot
site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()
item = pywikibot.ItemPage(repo, u"Q13515")
item.get()

sourcesid = 'P1343'
sourceid = 'Q17378135'
urlid = 'P854'
nameid = 'P1476'

# item.claims['P1343'][1].qualifiers.items():   # This are direct way to get list qualifiers. But '[1]' is hard link to index of list, it will break over time.
if sourcesid in item.claims:
    for source in item.claims[sourcesid]:
        if source.target.id == sourceid:
            s = source.qualifiers
            if urlid in s:     url  = s.get(urlid)[0].target
            if nameid in s:    name = s.get(nameid)[0].target['text']
            print (url, name)
