import os
import pytest
import re
import sys
import tempfile

# We're not using python packages, so we have to solve the path problem the old way.
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))
import rfcs

@pytest.fixture
def scratch_space():
    x = tempfile.TemporaryDirectory()
    yield x
    x.cleanup()

def test_index(scratch_space):
    temp_idx = os.path.join(scratch_space.name, 'index.md')
    import generate_index
    generate_index.main(temp_idx)
    perm_idx = os.path.join(os.path.dirname(__file__), '../index.md')
    if os.system('diff %s %s' % (perm_idx, temp_idx)):
        pytest.fail("/index.md needs to be updated. Run python code/generate_index.py.")
    
def test_links():
    import check_links
    assert check_links.main() == 0

def test_rfc_metadata():
    errors = []
    def e(rfc, msg):
        errors.append(rfc.relpath.replace('README.md','') + ': ' + msg)
    for rfc in rfcs.walk():
        if not bool(rfc.title): e(rfc, 'no title found')
        if rfc.category not in rfc.relpath: e(rfc, 'category does not match path')
        if rfc.category[:-1] not in rfc.tags: e(rfc, 'category not in tags')
        opposite_category = 'feature' if rfc.category == 'concepts' else 'concept'
        if opposite_category in rfc.tags: e(rfc, 'opposite category in tags')
        if rfc.status not in rfcs.status_list: e(rfc, 'status is not canonical')
        if not re.match(r'\d{4}$', rfc.num): e(rfc, 'num is not 4 digits')
        if not re.search(r'\d{4}-\d{2}-\d{2}', rfc.since): e(rfc, 'since does not contain yyyy-mm-dd')
        if rfc.start_date:
            if not re.search(r'\d{4}-\d{2}-\d{2}', rfc.start_date): e(rfc, 'start_date does not contain yyyy-mm-dd')
        if bool(rfc.authors):
            if '@' in rfc.authors:
                if not re.search(r'\[.*?\]\([^)]+@.*?\)', rfc.authors): e(rfc, 'email is not clickable')
        else:
            e(rfc, 'no authors found')
        if ','.join(rfc.tags) != ','.join(rfc.tags).lower(): e(rfc, 'tags are case-sensitive')
        if rfc.supersedes:
            if not re.search(r'\[.*?\]\(.*?\)', rfc.supersedes): e(rfc, 'supersedes does not contain hyperlink')
        if rfc.superseded_by:
            if not re.search(r'\[.*?\]\(.*?\)', rfc.superseded_by): e(rfc, 'superseded_by does not contain hyperlink')
        if rfc.impl_count > 0:
            if rfc.status == 'PROPOSED': e(rfc, 'should not be PROPOSED if it has an impl')
    if errors:
        msg = '\n' + '\n'.join(errors)
        raise BaseException(msg)