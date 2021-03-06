#!/usr/bin/env python3

"""
sss - sbz svn status verbose on one line
"""

import os
import shlex
import subprocess
import sys
import xml.etree.ElementTree as ET

"""
Algorithm:

line = Parse output of svn up
foreach path in lines
    xml data = svn log -rHEAD path --xml
    author, shortmsg, status, path = parse xml data
    print status, path, shortmsg, status, author
"""

def valid_line(line):
    if line.startswith('U ') or \
       line.startswith('A ') or \
       line.startswith('D '):
        return True
    else:
        return False


def main():
    src_path = os.path.expanduser('~/svn/src/')
    ports_path = os.path.expanduser('~/svn/ports/')
    svn_path = sys.argv[1] if len(sys.argv) == 2 else src_path
    out = {}
    data = subprocess.run(shlex.split('svn up {0}'.format(svn_path)),
                          stdout=subprocess.PIPE).stdout
    data = data.decode("utf-8")
    for line in data.split('\n'):
        if not valid_line(line):
            continue
        status, path = line.split()
        out['status'] = status
        out['path'] = path
        xml = subprocess.run(
            shlex.split('svn log -l 1 {path} --xml'.format(path=path)),
            stdout=subprocess.PIPE
        )
        xml_data = xml.stdout
        xml_data = xml_data.decode("utf-8")
        try:
            root = ET.fromstring(xml_data)
            for commit in root.findall('logentry'):
                author = commit.find('author').text
                date = commit.find('date').text
                shortmsg = commit.find('msg').text.split('\n')[0]
                out['author'] = author
                out['shortmsg'] = shortmsg
                out['rev'] = commit.attrib.get('revision', 'norev')
                out['date'] = date.split('.')[0]
                svnmsg = "{status} {path}\t {shortmsg} | {rev} | {author} | {date}"
                print(svnmsg.format(**out))
        except:
            pass


if __name__ == '__main__':
    sys.exit(main())
