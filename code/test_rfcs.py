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


@pytest.mark.skip(reason="using actions index generation")
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

    def warn(rfc, msg):
        sys.stderr.write('Warning: ' + rfc.relpath.replace('README.md','') + ': ' + msg + '\n')

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
        if rfc.status == 'PROPOSED':
            for impl in rfcs.test_suite_impls(rfc, False):
                e(rfc, 'should not be PROPOSED if it has a non-test-suite impl')
                break
        # Should this RFC have links to test results?
        elif rfc.status in ['ACCEPTED', 'ADOPTED'] and 'feature' in rfc.tags and (
                'protocol' in rfc.tags or 'decorator' in rfc.tags):
            found_test_suite_in_impls = False
            for row in rfcs.test_suite_impls(rfc, True):
                found_test_suite_in_impls = True
                break
            if not found_test_suite_in_impls:
                msg = 'Test suite must be an impl for any protocol- or decorator-related RFC beyond DEMONSTRATED status.'
                if 'test-anomaly' in rfc.tags:
                    warn(rfc, msg)
                else:
                    e(rfc, msg + ' Tag "test-anomaly" to temporarily override.')
            for row in rfcs.test_suite_impls(rfc, False):
                m = rfcs.get_test_results_link(row)
                # If we lack a link entirely, this is an error, period.
                # If we have tagged the RFC with "test-anomaly", then it becomes possible to link
                # the ugly text "MISSING test results" to the test-anomaly tag and have the result
                # be only a warning. This ugly text+link should only be accepted when the 'test-anomaly'
                # tag is present.
                desc = rfcs.describe_impl_row(row)
                if m is None:
                    e(rfc, 'Impl "%s" needs a link to test results in its Notes column. Format = [test results](...) or, if RFC is tagged "test-anomaly", [MISSING test results](/tags.md#test-anomaly).' % desc)
                # Are test results explicitly declared to be missing?
                elif ('MISSING' in m.group(1) and '/tags.md#test-anomaly' in m.group(2)):
                    if 'test-anomaly' in rfc.tags:
                        warn(rfc, 'Impl "%s" needs to replace missing test results with something meaningful.' % desc)
                    else:
                        e(rfc, 'Can\'t declare missing tests without the "test-anomaly" tag to make the RFC ugly, so impl "%s" needs a link to test results in its Notes column. Format = [test results](...).' % desc)

    if errors:
        msg = '\n' + '\n'.join(errors)
        raise BaseException(msg)


def test_impls():
    errors = []

    def e(rfc, msg):
        errors.append(rfc + ': ' + msg)

    pretty_for_normalized_names = {}
    normalized_for_base_uri = {}
    base_uri_for_normalized = {}
    refs = []

    def append_to_dict(dict, key, value, ref):
        if key not in dict:
            dict[key] = []
        list = dict.get(key)
        if value not in list:
            list.append(value)
        refs.append((dict, key, value, ref))

    def track(name, link, path, row_num):
        ref = path + ', impl row ' + str(row_num)
        norm_name = rfcs.normalize_impl_name(name)
        append_to_dict(pretty_for_normalized_names, norm_name, name, ref)
        base_uri = rfcs.get_impl_base(link)
        append_to_dict(base_uri_for_normalized, norm_name, base_uri, ref)
        append_to_dict(normalized_for_base_uri, base_uri, norm_name, ref)

    for abspath in rfcs.walk_files():
        try:
            with open(abspath, 'rt', encoding='utf-8') as f:
                txt = f.read()
            path = rfcs.relpath(abspath).replace('/README.md', '')
            impl_table = rfcs.get_impl_table(txt)
            bad_count = False
            n = 1
            for row in impl_table:
                if len(row) == 2:
                    cell = row[0].strip()
                    if cell.startswith('['):
                        name, link = rfcs.split_hyperlink(cell)
                        if name and link:
                            track(name, link, path, n)
                else:
                    if (not bad_count):
                        e(path, 'row %d in impl table does not have 2 columns' % n)
                        bad_count = True
                n += 1
        except:
            print('Error while processing ' + abspath)
            raise

    def find_refs(dict, key, value):
        matches = []
        for ref in refs:
            if ref[0] == dict:
                if ref[1] == key:
                    if ref[2] in value:
                        matches.append(ref[3])
        return matches

    for key, value in pretty_for_normalized_names.items():
        if len(value) > 1:
            offenders = '\n'.join(find_refs(pretty_for_normalized_names, key, value))
            e(offenders, '\n  inconsistent variants on impl name: %s' % ', '.join(['"%s"' % v for v in value]))

    for key, value in normalized_for_base_uri.items():
        if len(value) > 1:
            offenders = '\n'.join(find_refs(normalized_for_base_uri, key, value))
            e(offenders, '\n  same site maps to multiple impl names: %s' % ', '.join(['"%s"' % v for v in value]))

    for key, value in base_uri_for_normalized.items():
        if len(value) > 1:
            offenders = '\n'.join(find_refs(base_uri_for_normalized, key, value))
            e(offenders, '\n  impl name "%s" maps to multiple sites: %s' % (key, ', '.join(['"%s"' % v for v in value])))

    if errors:
        msg = '\n' + '\n'.join(errors)
        raise BaseException(msg)
