import os
import re
import sys
import traceback

import rfcs


title_pat = re.compile(r'\s*#[ \t]*(?:RFC[ \t]*)?(0\d\d\d)[ \t]*:[ \t]*(.*?)$', re.I | re.M)
author_pat = re.compile(r'^[ \t]*(?:[-*][ \t]*)?Authors?[ \t]*:[ \t[]*(.*?)$', re.I | re.M)
status_pat = re.compile(r'^[ \t]*(?:[-*][ \t]*)?Status[ \t]*:[ \t[]*(\w+)(.*?)$', re.I | re.M)
start_date_pat = re.compile(r'^[ \t]*(?:[-*][ \t]*)?Start Date[ \t]*:[ \t]*(.*?)$', re.I | re.M)
status_date_pat = re.compile(r'^[ \t]*(?:[-*][ \t]*)?Status Date[ \t]*:[ \t]*([- 0123456789]+)', re.I | re.M)
status_note_pat = re.compile(r'^[ \t]*(?:[-*][ \t]*)?Status Note[ \t]*:[ \t]*', re.I | re.M)
header_pat = re.compile(r'^\s*#+[ \t]*(.*?)$', re.M)
named_decorator_pat = re.compile(r'\W~\w+')
decorator_as_topic_pat = re.compile(r'(^|\W)[dD]ecorators?(\W|$)')
protocol_in_title_pat = re.compile(r'\W(protocols?)(\W|$)', re.I)
version_in_title_pat = re.compile(r'\W(\d\.\d)(?=\W|$)')
summary_header_pat = re.compile(r'^([ \t]*#+[ \t]*Summary[ \t]*)$', re.I | re.M)
supersedes_pat = re.compile(r'(?:This )?[sS]uper[sc]edes.*?(\[.*?\]\(.*?\))\.?(?=\W|$)')
useless_anchor_pat = re.compile(r'^[\t ]*\[[\t ]*[-a-zA-Z0-9_]+[\t ]*\][\t ]*:[\t ]*#[-a-zA-Z0-9_]+[\t ]*$', re.M)
overly_spaced_header_pat = re.compile(r'\n[\t ]*(#+)[\t ]*(.*?)[\t ]*\n\n\n')
unspaced_after_header_pat = re.compile(r'^[\t ]*(#+)[\t ]*(.*?)\n(?=[^\n\t ])', re.M)


substitutions = [(re.compile('(?<=\W)' + x[0] + '(?=\W)'), x[1]) for x in [
    ('DID Comm', 'DIDComm'),
    ('DID Comms', 'DIDComm'),
    ('DID comm', 'DIDComm'),
    ('didcomms', 'DIDComm'),
    ('DIDComms', 'DIDComm')
]]


def all_headers(txt):
    for match in header_pat.finditer(txt):
        yield match


def needs_decorator_tag(txt):
    needs = False
    for m in all_headers(txt):
        val = m.group(1)
        if named_decorator_pat.search(val):
            return True
        if decorator_as_topic_pat.search(val):
            return True


def revise(fname):
    print(rfcs.relative_path(fname))
    try:
        def find_pat(name, txt):
            m = globals()[name + '_pat'].search(txt)
            if not m:
                msg = f"Can't find {name.replace('_', ' ')}."
                raise ValueError(msg)
            return m

        with open(fname, 'rt') as f:
            txt = f.read().strip() + '\n'

        for pair in substitutions:
            txt = re.sub(pair[0], pair[1], txt)

        txt = re.sub(r'[ \t]+\n', '\n', txt)
        txt = re.sub(useless_anchor_pat, '', txt)
        while overly_spaced_header_pat.search(txt):
            txt = re.sub(overly_spaced_header_pat, r'\1 \2\n\n', txt)
        while unspaced_after_header_pat.search(txt):
            txt = re.sub(unspaced_after_header_pat, r'\1 \2\n\n', txt)
        i = 0
        while True:
            i = txt.find('\n#', i)
            if i == -1:
                break
            if i > 0 and txt[i - 1] != '\n':
                txt = txt[:i] + '\n' + txt[i:]
            i += 2

        tags = []
        if '/features/' in fname:
            tags.append('feature')
        else:
            tags.append('concept')
        if needs_decorator_tag(txt):
            tags.append('decorator')

        m = title_pat.match(txt)
        if not m: raise ValueError("Can't find title_pat.")
        txt = txt[m.end():].lstrip()
        rfc_num = m.group(1)
        title = m.group(2)
        m = protocol_in_title_pat.search(title)
        is_protocol = 'features' in fname and (m or 'protocol' in fname)
        if is_protocol:
            tags.append('protocol')
            if m:
                title = title[:m.start()].rstrip() + ' ' + title[m.end():].lstrip()
            m = version_in_title_pat.search(title)
            if not m:
                version = '0.9'
            else:
                version = m.group(1)
                title = title[:m.start()].rstrip() + ' ' + title[m.end():].lstrip()
            title = title.strip() + ' Protocol ' + version
        m = find_pat('summary_header', txt)
        rest_of_metadata = txt[:m.start()].rstrip()
        remainder = txt[m.start():]

        m = find_pat('author', rest_of_metadata)
        authors = m.group(1)
        m = find_pat('start_date', rest_of_metadata)
        start_date = m.group(1).strip()
        m = find_pat('status', rest_of_metadata)
        status = m.group(1).upper()
        m = find_pat('status_date', rest_of_metadata)
        status_date = m.group(1).strip()
        m = status_note_pat.search(rest_of_metadata)
        if m:
            status_note = re.sub(' {2,}', ' ', rest_of_metadata[m.end():].strip().replace('\n', ' '))
        else:
            status_note = ''
        m = supersedes_pat.search(status_note)
        if m:
            supersedes = m.group(1)
            status_note = status_note[:m.start()].rstrip() + ' ' + status_note[m.end():].lstrip()
        else:
            supersedes = ''

        txt = f"""# Aries RFC {rfc_num}: {title}

- Authors: {authors}
- Status: [{status}](/README.md#{status.lower()})
- Since: {status_date}
"""
        if status_note:
            txt += '- Status Note: ' + status_note + '\n'
        if supersedes:
            txt += '- Supersedes: ' + supersedes + '\n'
        if start_date:
            txt += '- Start Date: ' + start_date + '\n'
        txt += '- Tags: ' + ', '.join(tags) + '\n'
        txt = txt + '\n' + remainder

        os.system(f"cp {fname} {fname}.bak")
        with open(fname, 'wt') as f:
            f.write(txt)

    except KeyboardInterrupt:
        sys.exit(1)
    except:
        print("File doesn't match expected format.")
        print(traceback.format_exc())
        sys.exit(1)


def revise_all():
    for rfc in rfcs.all_rfc_files():
        revise(rfc)


if __name__ == '__main__':
    revise_all()