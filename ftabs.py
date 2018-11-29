#!/usr/bin/env python

import os
import webbrowser
import sys

username = os.environ.get('USER') or 'sbz'
g_label = "freebsd/freebsd-{}".format(username)
g_link = "https://mail.google.com/mail/u/0/?tab=wm#label/{}".format(g_label)
out_link = "http://portscout.freebsd.org/{}@freebsd.org.html".format(username)
bts_args = "?email1={}%40FreeBSD.org&order=changeddate&resolution=---"
bts_args = bts_args.format(username)
bts_link = "https://bugs.freebsd.org/bugzilla/buglist.cgi{}"
repo_link = "https://repology.org/maintainer/{}%40freebsd.org".format(username)


class URL(object):
    def __init__(self, **kwargs):
        self.link = kwargs.get("link")
        self.desc = kwargs.get("desc", "N/A")
        self.abrv = kwargs.get("abrv", "N/A")

    def link(self):
        return self.link

    def desc(self):
        return self.desc

    def abrv(self):
        return self.abrv.upper()

URLS = [
    URL(link="https://reviews.freebsd.org/", desc="code review", abrv="cr"),
    URL(link=bts_link.format(bts_args), desc="bug tracking", abrv="bts"),
    URL(link="https://github.com/freebsd/", desc="github", abrv="gh"),
    URL(link="https://svnweb.freebsd.org/", desc="code browser", abrv="cb"),
    URL(link=out_link, desc="portcout", abrv="pc"),
    URL(link=repo_link, desc="repology", abrv="rl"),
    URL(link=g_link, desc="freebsd-{}".format(username), abrv="gmail"),
    URL(link="https://wiki.freebsd.org", desc="wiki", abrv="wk"),
    URL(link="http://beefy6.nyi.freebsd.org/", desc="builder status",
        abrv="build"),
    URL(link="https://secure.freshbsd.org/search?project=freebsd",
        desc="commit stats", abrv="stats"),
    URL(link="http://grok.dragonflybsd.org/source/xref/freebsd/",
        desc="xref browser", abrv="xref"),
]


def main():
    rc = 1
    browser = webbrowser.get()
    for url in URLS:
        ret = browser.open_new_tab(url.link)
        if ret is False:  # cannot open the link, try next one
            rc = 0
            continue

    return rc

if __name__ == "__main__":
    sys.exit(main())
