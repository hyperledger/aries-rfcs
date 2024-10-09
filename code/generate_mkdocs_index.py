import argparse
from operator import itemgetter
import os
from pathlib import Path
import sys

import rfcs

def update(fname, tmp_fname):
    if not os.path.exists(fname):
        os.rename(tmp_fname, fname)
        # print('Generated %s.' % fname)
        return
    with open(fname, encoding='utf-8', mode='rt') as f:
        old = f.read()
    with open(tmp_fname, encoding='utf-8', mode='rt') as f:
        new = f.read()
    if old == new:
        # print('No change to %s.' % fname)
        return
    os.remove(fname)
    os.rename(tmp_fname, fname)
    # print('Updated %s.' % fname)


def main(fname = None):
    if not fname:
        fname = os.path.join(rfcs.root_folder, 'mkdocs_index.yml')
    # Load all metadata
    all = [rfc for rfc in rfcs.walk()]
    all.sort(key=lambda x: x.num)
    tmp_fname = fname + '.tmp'
    with open(tmp_fname, 'w', encoding='utf-8') as out:
        for status in rfcs.status_list:
            out.write(f"- {status}:\n")
            with_status = [rfc for rfc in all if rfc.status == status]
            for rfc in with_status:
                out.write(f"    - {rfc.num} {rfc.title}: {rfc.relpath}\n")
    update(fname, tmp_fname)


if __name__ == '__main__':
    ap = argparse.ArgumentParser('Generate index')
    ap.add_argument('altpath', metavar='PATH', nargs='?', default=None, help='override where index is generated')
    args = ap.parse_args()
    main(args.altpath)
