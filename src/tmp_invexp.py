import os
import json
from pprint import pprint
from rpgtoolbox.latexexport import inventory
with open("./data/Marcus/Kaylea Orinka2.json","r") as fp:
	testchar=json.load(fp)

test=inventory(testchar)

