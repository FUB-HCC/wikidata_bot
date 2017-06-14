# -*- coding: utf-8  -*-
import pywikibot
site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()
item = pywikibot.ItemPage(repo, u"Q42")
item.get()
mydescriptions = {u'en': u'English writer and humorist', u'de': u'Keine Panik!'}
item.editDescriptions(mydescriptions)
