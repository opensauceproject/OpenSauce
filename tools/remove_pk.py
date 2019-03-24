"""
Mini script to remove the PK of Django dumpdata
"""

import json
import sys
import os

if len(sys.argv) < 2:
    print("File in arg needed")
    exit()

for filename in sys.argv[1:]:
    try:
        with open(filename) as f:
            j = json.load(f)
            for e in j:
                del e["pk"]
                # del e["fields"]["question"]

            name, extension = os.path.splitext(filename)
            with open(name + "_without_PK" + extension, "w") as f2:
                json.dump(j, f2)
    except:
        print("error while loading : ", filename)
