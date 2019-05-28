import os
import re
from operator import itemgetter
from pathlib import Path

rfcs = []

top_paths = ["concepts", "features"]
status_list = ["PROPOSED", "ACCEPTED", "ADOPTED", "SUPERSEDED"]

for top_path in top_paths:
    rfc_paths = Path(top_path).iterdir()
    for rfc_path in rfc_paths:
        rfcs.append({
            'type': top_path,
            'path': rfc_path / "README.md",
            'number-title': rfc_path.name,
        })

#example status line - Status: [ACCEPTED](/README.md#rfc-lifecycle)
status_re = pattern = re.compile(r'Status:[ /[]*(\w+)')

for rfc in rfcs:

    # extract number and title from folder name
    rfc['number'], _, rfc['title'] = rfc['number-title'].partition("-")

    # read README file for status
    with open(rfc['path'], "r", encoding='utf-8') as rfc_text:
        for line in rfc_text.readlines():
            for matched_object in status_re.finditer(line):
                rfc['status'] = matched_object.group(1)

    print(rfc)

rfcs.sort(key=itemgetter('number'))
#group rfcs by status
fname = Path(os.path.dirname(__file__)).parent / 'index.md'
with fname.open('w', encoding='utf-8') as out:
    out.write("(This file is machine-generated; see [code/generate_index.py](code/generate_index.py).)\n\n")
    out.write("# Aries RFCs by Status\n")
    for status in status_list:
        out.write(f"\n## Status: {status}\n")
        for rfc in [rfc for rfc in rfcs if rfc['status'] == status]:
            out.write(f"* [{rfc['number']}: {rfc['title']}]({rfc['path'].as_posix()})\n")

print("Done")
