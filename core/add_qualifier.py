# -*- coding: utf-8  -*-
import pywikibot
site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()
item = pywikibot.ItemPage(repo, u"Q42")
claim = pywikibot.Claim(repo, u'P19')
target = pywikibot.ItemPage(repo, u"Q350")
claim.setTarget(target)
item.addClaim(claim)

qualifier = pywikibot.Claim(repo, u'P678')
target = pywikibot.ItemPage(repo, "Q35409")
qualifier.setTarget(target)
claim.addQualifier(qualifier)
