#!/usr/bin/python3

import collections
import os
import re
import subprocess
import argparse
 
# create parser
parser = argparse.ArgumentParser(
    description='List the RFCs set in an Aries Interop Profile (AIP) that have subsequently evolved. ' +
    'By default, the AIPs in the local version of the file are processed. A specific version can be ' +
    'specified, and then only that AIP version is processed. The AIP version can be a previous (not current) ' +
    'AIP.  Optionally, the diffs between RFCs set in processed AIP and the "main" branch can be included.')
 
# add arguments to the parser
parser.add_argument('--version', '-v', help='The AIP version to display. Defaults to the current version(s) in the local file')
parser.add_argument('--diffs', '-d', dest='diffs', action='store_true',
                    help='Display the diffs of any updated RFCs found')
parser.add_argument('--list', '-l', help='List the RFCs and commits in the AIP with a prefixed by the name of a (for example) shell script')
 
# parse the arguments
args = parser.parse_args()

aip_path = './concepts/0302-aries-interop-profile/README.md'

# Regular expressions to find an AIP header and an entry in the AIP RFC list
_aip_pat = re.compile(r'^[ \t]*#+[ \t]*Aries Interop Profile Version: ([1-9]*.[0-9]*.[0-9]*)?[ \t]*$')
_aip_commit_and_file = '(.*?)(tree/)([0-9a-f]*)(/)(.*?)(\).*$)'

def readAIP( aip_path, version ):
    # Open the local file and see if there is a version in it or in a previous file.
    lines = open(aip_path, "r").readlines()
    if not(version):
        # No version wanted - use local file, all versions
        return lines
    for line in lines:
        # version specified
        aip_version = re.search(_aip_pat, line)
        if aip_version:
            if aip_version.group(1) == version:
                # Version is defined in the local file
                return lines
        # Check the list of previous versions
        aip_link = re.search('^- \[([1-9]*.[0-9]*.[0-9]*)\]\((.*)\)', line)
        if aip_link:
            if aip_link.group(1) == version:
                # Found it - read in the raw version of the file from github and we'll use that
                lines = subprocess.run(['curl', '-L', '--silent', aip_link.group(2).replace('tree', 'raw')], stdout=subprocess.PIPE).stdout.decode('utf-8')
                return lines
    # Uh-oh - all the way through the file and no version found. Error and out...
    print('Error: AIP version %s not found' % (version))
    exit(1)

# Read the local file and if necessary a previous version of the local file
txt = readAIP( aip_path, args.version )

# Tracks if the changed RFCs for this AIP version should be listted
ListVersionRFCs = True

# Iterate through the file
for line in txt:
    # Version line?
    aip_version = re.search(_aip_pat, line)
    if aip_version:
        # Check if we want all the AIPs in the file or this one
        if ( not(args.version) or aip_version.group(1) == args.version ):
            print("# Aries Interop Profile: %s" % (aip_version.group(1)))
            ListVersionRFCs = True
        else:
            # Not this one...don't list the changed version
            ListVersionRFCs = False
    
    rfc = re.search(_aip_commit_and_file, line)
    # Is this an AIP RFC line? Is it in an RFC we want to list?
    if ( rfc and ListVersionRFCs ):
        # From the RFC line, get the commit ID and protocol file
        commit = rfc.group(3)
        protocol = rfc.group(5)
        changed = re.search(protocol, subprocess.run(['git', 'diff', '--name-only', commit, 'main'], stdout=subprocess.PIPE).stdout.decode('utf-8'))
        # Has this RFC changed since it was set in the RFC?
        if args.list:
            print('%s %s %s' % (args.list, protocol, commit))
        elif changed:
            # Yes - list it.
            print('>>>>>>>> Changed protocol: %s, latest commit to protocol: %s' % (protocol, 
                subprocess.run(['git', 'log', '-n', '1', '--pretty=format:%H', '--', protocol], stdout=subprocess.PIPE).stdout.decode('utf-8')))
            if args.diffs:
                # If we're showing diffs, then show the diffs
                print('')
                print(subprocess.run(['git', 'diff', commit, 'main', protocol], stdout=subprocess.PIPE).stdout.decode('utf-8'))
exit()
