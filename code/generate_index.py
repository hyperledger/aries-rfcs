import os
import re

rfcs = []

top_paths = ["concepts"]
status_list = ["PROPOSED", "ACCEPTED", "ADOPTED", "SUPERSEDED"]

for top_path in top_paths:
    rfc_paths = os.listdir(top_path)
    for rfc_path in rfc_paths:
        rfcs.append({
            'type': top_path,
            'path': os.path.join(top_path, rfc_path, "README.md"),
            'number-title': rfc_path,
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


#group rfcs by status
fname = os.path.join(os.path.dirname(__file__), '..', 'index.md')
with open(fname, 'w', encoding='utf-8') as out:
    out.write("(This file is machine-generated; see [code/generate_index.py](code/generate_index.py).)\n\n")
    out.write("# Aries RFCs by Status\n")
    for status in status_list:
        out.write(f"\n## Status: {status}\n")
        for rfc in [rfc for rfc in rfcs if rfc['status'] == status]:
            out.write(f"* [{rfc['number']}: {rfc['title']}]({rfc['path']})\n")

print("Done")
