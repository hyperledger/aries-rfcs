import os
import re
import requests
import sys
import traceback
import urllib

ROOT_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
LINK_PAT = re.compile(r'\[([^[(]+)\][(]([^)]+)\)', re.S)
RFC_NAME_PAT = re.compile(r'\d{4}-[-_.a-z0-9]+', re.I)
HTML_ANCHOR_PAT_TXT = r'<a[ \t\r\n]+[^>]*name=[\'"]X[\'"]'
MD_ANCHOR_PAT = re.compile(r'^[ \t]*(?:\[[^]]+\][ \t]*:[ \t]*)?#+[ \t]*(.*)$', re.MULTILINE)
COMMON_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
# The following URI patterns give errors even when we http HEAD them.
SKIP_PATS = [
    '://www.learningmachine.com',
    '://agilemodeling.com',
    '://nvlpubs.nist.gov',
    '://crates.io'
]
COMMIT_HASH_URI_PAT = re.compile('.*://github.com/hyperledger/[a-zA-Z-_]+/blob/[a-f0-9]+/text/([a-zA-Z0-9_-]+)(/.*)?$')
SHORTENER_PAT = re.compile('http://(bit.ly|t.co|goo.gl|youtu.be)')


def make_md_anchor(txt):
    anchor = ''
    txt = txt.strip()
    for c in txt.lower():
        if c.isalpha() or c.isdigit() or c in '_-':
            anchor += c
        elif c == ' ':
            anchor += '-'
    if 'elapsed' in anchor:
        pass
    return anchor


def fragment_in_content(fragment, content, ct):
    if "html" in ct:
        pat = re.compile(HTML_ANCHOR_PAT_TXT.replace('X', fragment), re.I or re.S)
        if pat.search(content):
            return True
    else:
        found = False
        for anchor_match in MD_ANCHOR_PAT.finditer(content):
            if make_md_anchor(anchor_match.group(1)) == fragment:
                found = True
                break
        return found


def should_skip_website(uri):
    for pat in SKIP_PATS:
        if pat in uri:
            return True


def handle_local_file(relative_to_fname, uri, cache):
    error = None
    content = None
    if uri.startswith('/'):
        path = ROOT_FOLDER + uri
    else:
        path = os.path.join(os.path.dirname(relative_to_fname), uri)
    path = os.path.normpath(path)
    if path in cache:
        error, content = cache[path]
    else:
        if not os.path.exists(path):
            error = "does not exist"
        else:
            if os.path.isdir(path):
                error = "should link to README.md rather than folder"
            elif path.endswith('.md'):
                with open(path, 'rt') as f:
                    content = f.read()
        cache[path] = (error, content)
    return error, content, path


def find_matching_rfc(rfcs, which):
    def norm_name(x):
        return re.sub('[^a-z]', '', x).lower()
    n_which = norm_name(which)
    for rfc in rfcs:
        n_rfc = norm_name(rfc)
        if n_which == n_rfc:
            return rfc


def handle_web_resource(uri, rfcs, cache):
    error = None
    ct = None
    # Do we have the uri cached?
    if uri in cache:
        error, content = cache[uri]
    else:
        m = SHORTENER_PAT.match(uri)
        if m:
            return error, ct
        m = COMMIT_HASH_URI_PAT.match(uri)
        if m:
            rfc = find_matching_rfc(rfcs, m.group(1))
            if rfc:
                error = 'should reference RFC %s' % rfc
        if not error:
            r = requests.head(uri, headers={'User-Agent': COMMON_USER_AGENT}, timeout=10)
            if r.status_code < 200 or r.status_code > 299:
                error = "returns HTTP status code " + str(r.status_code)
            else:
                ct = r.headers['content-type']
                i = ct.find(';')
                if i > -1:
                    ct = ct[:i]
        cache[uri] = (error, None)
    return error, ct


def check_link(fname, short_fname, txt, match, rfcs, cache, problem_count_in_file_thus_far, full_check):
    """Look at a link and return an error string about it, if any."""
    error = None
    # What's exactly the uri as it appears in the markdown link?
    full_uri = match.group(2).strip()
    uri = full_uri
    try:
        if uri in cache:
            error, content = cache[uri]
        else:
            content = None
            ct = "text/markdown"
            # Split into most-of-uri + fragment
            fragment = None
            i = uri.find('#')
            if i > -1:
                fragment = uri[i + 1:]
                uri = uri[:i]
            # Now look at what type of URI it is.
            if uri.startswith('http'):
                if not full_check:
                    return None
                else:
                    if should_skip_website(uri):
                        return None
                    error, ct = handle_web_resource(uri, rfcs, cache)
            elif uri.startswith('mailto:'):
                return None
            # If URI is empty, then the URI is relative to the open file, so it was probably a pure fragment
            elif uri == '':
                content = txt
            else:
                error, content, uri = handle_local_file(fname, uri, cache)
            # If we got this far without an error, the only other thing to check is whether the fragment
            # is valid.
            if (not error) and fragment:
                cacheable = '%s#%s' % (uri, fragment)
                if cacheable in cache:
                    error, content = cache[cacheable]
                else:
                    if ct and content and (not fragment_in_content(fragment, content, ct)):
                        error = "#%s not in %s content" % (fragment, ct)
                    # Cache what we learned about the specific URI+fragment
                    cache[cacheable] = (error, None)
    except KeyboardInterrupt:
        sys.exit(1)
    except BaseException:
        error = traceback.format_exc()
    if error:
        alt = match.group(1).strip()
        if len(alt) > 20:
            alt = alt[:20] + '...'
        if problem_count_in_file_thus_far == 0:
            print(short_fname + ':')
        print("    [%s](%s) %s" % (alt, full_uri, error))
    return error


def check_links(fname, rfcs, cache, full_check):
    relative_fname = os.path.relpath(fname, ROOT_FOLDER)
    sys.stdout.write(relative_fname.ljust(80, ' ') + '\r')
    error_count = 0
    if fname not in cache:
        with open(fname, "rt") as f:
            txt = f.read()
        cache[fname] = (None, txt)
    else:
        txt = cache[fname][1]
    for match in LINK_PAT.finditer(txt):
        if check_link(fname, relative_fname, txt, match, rfcs, cache, error_count, full_check):
            error_count += 1
    return error_count


def get_rfcs(folder):
    return [x for x in os.listdir(folder) if RFC_NAME_PAT.match(x) and os.path.isdir(os.path.join(folder, x))]


def main(full_check = False):
    error_count = 0
    folders = [x for x in map(lambda x: os.path.join(ROOT_FOLDER, x), ["concepts", "features"]) if os.path.isdir(x)]
    rfcs = []
    for starting_point in folders:
        rfcs += get_rfcs(starting_point)
    cache = {}
    for starting_point in folders:
        for root, dirs, files in os.walk(starting_point):
            for file in files:
                if file.endswith('.md'):
                    error_count += check_links(os.path.join(root, file), rfcs, cache, full_check)
    print('%s\n%d errors.' % (''.rjust(80), error_count))
    return error_count


if __name__ == '__main__':
    full_check = (len(sys.argv) > 1 and sys.argv[1] == '--full')
    error_count = main(full_check)
    sys.exit(error_count)