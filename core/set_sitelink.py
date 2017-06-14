# -*- coding: utf-8  -*-
import pywikibot
site = pywikibot.Site("en", "wikipedia")
repo = site.data_repository()
item = pywikibot.ItemPage(repo, u"Q42")
page = pywikibot.Page(site, u"Douglas Adams")
item.setSitelink(page)
