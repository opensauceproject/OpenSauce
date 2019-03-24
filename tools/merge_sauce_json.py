"""
Mini script to merge jsons of Sauces
"""

import json
import sys
import os

if len(sys.argv) < 3:
    print("At least 2 json are needed to be merge")
    exit()

data = []

for filename in sys.argv[1:]:
    with open(filename) as f:
        j = json.load(f)
        data.extend(j)

with open("merged.json", "w") as f2:
    json.dump(data, f2)
