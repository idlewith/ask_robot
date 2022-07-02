import json
from pprint import pprint

a = json.load(open("covid_19.json", encoding="utf-8"))
pprint(a)
