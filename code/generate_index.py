import os
from operator import itemgetter
from pathlib import Path
import re
import sys

status_list = ["PROPOSED", "ACCEPTED", "ADOPTED", "SUPERSEDED"]

def collect_rfcs():
    rfcs = []
    top_paths = ["concepts", "features"]

    for top_path in top_paths:
        for rfc_path in Path(top_path).iterdir():
            rfcs.append({
                'type': top_path,
                'path': rfc_path / "README.md",
                'number-title': rfc_path.name,
            })
    return rfcs

def analyze_status(rfcs):
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
            sys.exit(1)

def update(fname, tmp_fname):
    if not os.path.exists(fname):
        os.rename(tmp_fname, fname)
        print('Generated %s.' % fname)
        return
    with open(fname, 'rt') as f:
        old = f.read()
    with open(tmp_fname, 'rt') as f:
        new = f.read()
    if old == new:
        print('No change to %s.' % fname)
        return
    os.remove(fname)
    os.rename(tmp_fname, fname)
    print('Updated %s.' % fname)

def dump(rfcs, fname):
    rfcs.sort(key=itemgetter('number'))
    tmp_fname = fname + '.tmp'
    #group rfcs by status
    with open(tmp_fname, 'w', encoding='utf-8') as out:
        out.write("(This file is machine-generated; see [code/generate_index.py](code/generate_index.py).)\n\n")
        out.write("# Aries RFCs by Status\n")
        for status in status_list:
            out.write(f"\n## Status: {status}\n")
            for rfc in [rfc for rfc in rfcs if rfc['status'] == status]:
                out.write(f"* [{rfc['number']}: {rfc['title']}]({rfc['path'].as_posix()})\n")
    update(fname, tmp_fname)

def main(target_fname = None):
    root_path = Path(os.path.abspath(os.path.dirname(__file__))).parent
    # We need all paths that we walk and store to be relative to the root
    # of the repo, even if that's not where we're running the script.
    os.chdir(root_path)
    if target_fname is None:
        target_fname = 'index.md'
    rfcs = collect_rfcs()
    analyze_status(rfcs)
    dump(rfcs, target_fname)

if __name__ == '__main__':
    main()
