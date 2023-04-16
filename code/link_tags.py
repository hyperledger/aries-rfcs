import sys
import re

tag_line_pat = re.compile(r'^\s*-\s*[Tt]ags\s*:\s*(.*?)$', re.M)

def link_tags(fname):
    changed = False
    with open(fname, 'rt') as f:
        txt = f.read()
    m = tag_line_pat.search(txt)
    if m:
        tags = [t.strip() for t in m.group(1).split(',')]
        for i in range(len(tags)):
            tag = tags[i]
            if tag[0] != '[':
                changed = True
                tags[i] = '[' + tag + '](/tags.md#' + tag + ')'
        if changed:
            tags = ', '.join(tags)
            txt = txt[:m.start(1)] + tags + txt[m.end(1):]
            with open(fname, 'wt') as f:
                f.write(txt)
            print('Updated ' + fname)


if __name__ == '__main__':
    for fname in sys.argv[1:]:
        link_tags(fname)
