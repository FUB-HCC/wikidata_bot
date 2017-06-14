# -*- coding: utf-8  -*-
statedin = pywikibot.Claim(repo, u'P248')
itis = pywikibot.ItemPage(repo, "Q82575")
statedin.setTarget(itis)

retrieved = pywikibot.Claim(repo, u'P813')
date = pywikibot.WbTime(year=2014, month=3, day=20)
retrieved.setTarget(date)

claim.addSources([statedin, retrieved])
