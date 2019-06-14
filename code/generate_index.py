import os
import re
from operator import itemgetter
from pathlib import Path

rfcs = []

root_path = Path(os.path.dirname(__file__)).parent
# We need all paths that we walk and store to be relative to the root
# of the repo, even if that's not where we're running the script.
os.chdir(root_path)
top_paths = ["concepts", "features"]
status_list = ["PROPOSED", "ACCEPTED", "ADOPTED", "SUPERSEDED"]

for top_path in top_paths:
    for rfc_path in Path(top_path).iterdir():
        rfcs.append({
            'type': top_path,
            'path': rfc_path / "README.md",
            'number-title': rfc_path.name,
        })

#example status line - Status: [ACCEPTED](/README.md#rfc-lifecycle)
status_re = pattern = re.compile(r'^\s*(?:[-*]\s*)?Status:[ \t/[]*(\w+)', re.I | re.M)

for rfc in rfcs:

    # extract number and title from folder name
    rfc['number'], _, rfc['title'] = rfc['number-title'].partition("-")

    # read README file for status
    with open(rfc['path'], "rt", encoding='utf-8') as f:
        rfc_text = f.read()

    m = status_re.search(rfc_text)
    if m:
        rfc['status'] = m.group(1).upper()
    else:
        print("Didn't find status line in %s" % rfc['path'])
    #print(rfc)

rfcs.sort(key=itemgetter('number'))
#group rfcs by status
fname = root_path / 'index.md'
with fname.open('w', encoding='utf-8') as out:
    out.write("(This file is machine-generated; see [code/generate_index.py](code/generate_index.py).)\n\n")
    out.write("# Aries RFCs by Status\n")
    for status in status_list:
        out.write(f"\n## Status: {status}\n")
        for rfc in [rfc for rfc in rfcs if rfc['status'] == status]:
            out.write(f"* [{rfc['number']}: {rfc['title']}]({rfc['path'].as_posix()})\n")

print("Done")
