import argparse
from operator import itemgetter
import os
from pathlib import Path
import sys

import rfcs


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


def main(fname = None):
    if not fname:
        fname = os.path.join(rfcs.root_folder, 'index.md')
    # Load all metadata
    all = [rfc for rfc in rfcs.walk()]
    all.sort(key=lambda x: x.num)
    tmp_fname = fname + '.tmp'
    with open(tmp_fname, 'w', encoding='utf-8') as out:
        out.write("# Aries RFCs by Status\n")
        for status in rfcs.status_list:
            out.write(f"\n## [{status}](README.md#{status.lower()})\n")
            with_status = [rfc for rfc in all if rfc.status == status]
            for rfc in with_status:
                line = f"* [{rfc.num}: {rfc.title}]({rfc.relpath})"
                tags = [f"[`{x}`](/tags.md#{x})" for x in rfc.tags]
                line += f" ({rfc.since}"
                if rfc.impl_count:
                    line += f", {rfc.impl_count} impl"
                    if rfc.impl_count > 1:
                        line += 's'
                line += ' &mdash; ' + ' '.join(tags) + ')'
                out.write(line + '\n')
        out.write("\n\n>(This file is machine-generated; see [code/generate_index.py](code/generate_index.py).)\n")
    update(fname, tmp_fname)


if __name__ == '__main__':
    ap = argparse.ArgumentParser('Genrate index')
    ap.add_argument('altpath', metavar='PATH', nargs='?', default=None, help='override where index is generated')
    args = ap.parse_args()
    main(args.altpath)
