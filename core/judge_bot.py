import pywikibot
from pywikibot.data import api
import pprint

# FIXME Hardcoded for test.wikidata
# Define properties and data
p_stated_in = "P149"
p_half_life = "P525"
p_ref_url = "P93"
precision = 10 ** -10
# data = [quantity, uncertainty, unit (Q1748 = hours)]
# source = [stated in item, ref url]
half_life_data = {"uranium-240": {"data": ["14.1", "0.1", "Q1748"],
                                  "source": ["Q1751", "http://www.nndc.bnl.gov/chart/reCenter.jsp?z=92&n=148"]}
                  }

site = pywikibot.Site("test", "wikidata")
repo = site.data_repository()



for key in half_life_data:
    search_results = get_items(site, key)
    if len(search_results["search"]) == 1:
        item = pywikibot.ItemPage(repo, search_results["search"][0]["id"])
        data = half_life_data[key]["data"]
        source_data = half_life_data[key]["source"]

        claim = check_claim_and_uncert(item, p_half_life, data)
        if claim:
            source = check_source_set(claim, key, source_data)
            if source:
                pass
            else:
                create_source_claim(claim, source_data)
        else:
            claim = set_claim(item, p_half_life, data)
            create_source_claim(claim, source_data)
    else:
        print("No result or too many found for {}.", key)
