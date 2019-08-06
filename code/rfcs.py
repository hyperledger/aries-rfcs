import collections
import os
import re

RFC = collections.namedtuple('RFC', 'title abspath relpath category folder num authors status since' +
                             ' status_note start_date supersedes superseded_by tags content_idx impl_count')


status_list = ["ADOPTED", "ACCEPTED", "DEMONSTRATED", "PROPOSED", "RETIRED"]


root_folder = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

def walk_files():
    """
    Generate the full path to every RFC in the repo.
    """
    subdirs = ['concepts', 'features']
    for subdir in subdirs:
        for root, folders, files in os.walk(os.path.join(root_folder, subdir), topdown=True):
            for f in folders:
                if (not f.startswith('.')):
                    rfc_path = os.path.normpath(os.path.join(root, f, 'README.md')).replace('\\', '/')
                    if os.path.isfile(rfc_path):
                        yield rfc_path
            # Don't recurse
            folders.clear()


_field = lambda x: re.compile(r'^[ \t]*[-*][ \t]*' + x + '[ \t]*:[ \t*](.*?)$', re.I | re.M)
_title_pat = re.compile(r'\s*#[ \t]*(?:(?:Aries )?RFC )?(\d\d\d\d)[ \t]*:[ \t]*(.*?)$', re.I | re.M)
_author_pat = _field('Authors?')
_status_pat = _field('Status')
_since_pat = _field('(?:Since|Status[-_ ]?Date)')
_status_note_pat = _field('Status[-_ ]?Note')
_start_date_pat = _field('Start[-_ ]?Date')
_supersedes_pat = _field('Supersedes')
_superseded_by_pat = _field('Superseded[-_ ]?By')
_tags_pat = _field('Tags')
_status_val_pat = re.compile(r'\[[ \t]*(\w+)')

_extractors = [
    _author_pat, _status_pat, _since_pat, _status_note_pat, _start_date_pat, _supersedes_pat, _superseded_by_pat, _tags_pat
]

def walk():
    """
    Generate an RFC tuple for every RFC in the repo.
    """
    for abspath in walk_files():
        with open(abspath, 'rt', encoding='utf-8') as f:
            txt = f.read()
        m = _title_pat.search(txt)
        if m:
            num, title = m.group(1), m.group(2)
        else:
            num, title = '', ''
        fields = []
        for ex in _extractors:
            m = ex.search(txt)
            if m:
                fields.append(m.group(1))
            else:
                fields.append('')
        rpath = relpath(abspath)
        segments = rpath.split('/')
        folder = segments[-2]
        category = segments[-3]
        status = fields[1]
        m = _status_val_pat.search(status)
        if m:
            status = m.group(1)
        tags = [x.strip() for x in fields[7].split(',')]
        content_idx = txt.find('\n##')
        impl_table = get_impl_table(txt)
        impl_count = len(impl_table) if impl_table else 0
        x = RFC(title, abspath, rpath, category, folder, num, fields[0], status, fields[2],
                fields[3], fields[4], fields[5], fields[6], tags, content_idx, impl_count)
        yield x


_impl_pat = re.compile(r'^[ \t]*#+[ \t]*Implementations?[ \t]*$', re.M)
_impl_table_head_pat = re.compile(r'^[ \t]*(\|[ \t]*)?Name[ \t]*[|](.*?)[|](.*?)\n[ \t]*([|][ \t]*)?-+[ \t]*[|](.*?)[|](.*?)\n', re.M)
_impl_table_row_pat = re.compile(r'((.*?)[|](.*?)[|](.*?))\n')

def get_impl_table(txt):
    """
    Return the impl table for an RFC.
    """
    m = _impl_pat.search(txt)
    if m:
        m = _impl_table_head_pat.search(txt, m.end())
        if m:
            i = m.end()
            rows = []
            while True:
                m = _impl_table_row_pat.match(txt, i)
                if not m: break
                row = [x.strip() for x in m.group(1).split('|')]
                try:
                    if row[0] or row[1]:
                        rows.append(row)
                except:
                    pass

                i = m.end()

            return rows


def relpath(abspath):
    return os.path.relpath(abspath, root_folder).replace('\\', '/')


_header_pat = re.compile(r'^\s*#+[ \t]*(.*?)$', re.M)

def walk_headers(txt):
    """
    Generate a regex match object for each markdown header in a doc. This matcher
    can be used to find the header or to extract the text of the header.
    """
    for match in header_pat.finditer(txt):
        yield match
