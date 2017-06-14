# -*- coding: utf-8  -*-
import pywikibot
site = pywikibot.Site("en", "wikipedia")
page = pywikibot.Page(site, u"Douglas Adams")
item = pywikibot.ItemPage.fromPage(page)
dictionary = item.get()
print(dictionary)
print(dictionary.keys())
print(item)

site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()
item = pywikibot.ItemPage(repo, u"Q42")
dictionary = item.get()
print(dictionary)
print(dictionary.keys())
print(item)
