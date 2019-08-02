#!/usr/bin/env python

import bugzilla
import os

"""
In order to use this script, complete the following instructions:
    1. Generate API token using https://bugs.freebsd.org/bugzilla/userprefs.cgi?tab=apikey
    2. Define environment variable FREEBSD_BZ_API_TOKEN in your shell
"""

api_key = os.environ.get("FREEBSD_BZ_API_TOKEN")
user = os.environ.get("USER") or "sbz"

bz = bugzilla.Bugzilla(
    url="https://bugs.freebsd.org/bugzilla/xmlrpc.cgi",
    api_key=api_key
)

query = bz.build_query(
    product=["Ports & Packages","Base System"],
    assigned_to=user,
    status="__open__"
)

bugs = bz.query(query)
for bug in sorted(bugs, key=lambda x:x.last_change_time, reverse=True):
    print("{:10} {:10} {:8} {:60}".format(bug.last_change_time, bug.id,
                                          bug.status, bug.summary))

print("{} bugs currently opened.".format(len(bugs)))
