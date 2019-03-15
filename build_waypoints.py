#!/usr/bin/env python3

"""
Pulls the contents of two of the kumay3305 sheets as TSV files and then 
mash them together to build a wayout file
"""

import requests
import util
import json

ROUTE_URL = "https://docs.google.com/spreadsheets/d/1bK_AA8bMIoLzvtL6fRC4hYzUrnwlzGN18MVRZ04kQR0/export?format=tsv&id=1bK_AA8bMIoLzvtL6fRC4hYzUrnwlzGN18MVRZ04kQR0&gid=1153043136"

MAIN_URL="https://docs.google.com/spreadsheets/d/1bK_AA8bMIoLzvtL6fRC4hYzUrnwlzGN18MVRZ04kQR0/export?format=tsv&id=1bK_AA8bMIoLzvtL6fRC4hYzUrnwlzGN18MVRZ04kQR0&gid=0"

r = requests.get(ROUTE_URL)
lines = r.text.split("\n")

route = []
for line in lines[1:]:
    fields = line.split("\t")
    if len(fields) >= 2:
        route.append({"id": fields[0], "name": fields[1]})

r = requests.get(MAIN_URL)
lines = r.text.split("\n")

for line in lines[1:]:
    fields = line.split("\t")
    if len(fields) > 5:
        id = fields[0]
        for e in route:
            if id == e['id']:
                e["description"] = fields[2]
                if len(fields[3].strip()) > 0:
                    e['lat'] = fields[3]
                if len(fields[4].strip()) > 0:
                    e['lon'] = fields[4] 

with open("waypoints.json", "wt") as wp_file:
    json.dump(route, wp_file, indent=2, sort_keys=True)




