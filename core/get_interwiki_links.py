# -*- coding: utf-8  -*-
import pywikibot
site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()
item = pywikibot.ItemPage(repo, u"Q42")
item.get()
print(item.sitelinks)
