#!/usr/bin/env python

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import datetime
import os
import sys
from typing import List

import bugzilla
from bugzilla.bug import Bug

"""
In order to use this script, complete the following instructions:
    1. Generate API token using https://bugs.freebsd.org/bugzilla/userprefs.cgi?tab=apikey
    2. Define environment variable FREEBSD_BZ_API_TOKEN in your shell
"""

RFC_3339_FORMAT = "%Y%m%dT%H:%M:%S"


def fetch_bugzilla_prs(user: str, status: str = "__open__") -> List[Bug]:
    api_key = os.environ.get("FREEBSD_BZ_API_TOKEN", None)
    if not api_key:
        raise ("No api token provided")

    bz = bugzilla.Bugzilla(
        url="https://bugs.freebsd.org/bugzilla/xmlrpc.cgi", api_key=api_key
    )

    query = bz.build_query(
        product=["Ports & Packages", "Base System"],
        assigned_to=user,
        status=status,
    )

    bugs = bz.query(query)

    return bugs


def print_bugzilla_prs(bugs: List[Bug]) -> None:
    for bug in sorted(bugs, key=lambda x: x.last_change_time, reverse=True):
        bug_time = datetime.datetime.strptime(
            str(bug.last_change_time), RFC_3339_FORMAT
        )
        print(
            "{} {:10} {:12} {:60}".format(
                bug_time,
                bug.id,
                bug.status,
                bug.summary[:120] + " .." if len(bug.summary) > 120 else bug.summary,
            )
        )


def main() -> int:
    user = os.environ.get("USER") or "sbz"
    bugs = fetch_bugzilla_prs(user)
    print_bugzilla_prs(bugs)

    print("{} bugs currently opened.".format(len(bugs)))

    return 0


if __name__ == "__main__":
    sys.exit(main())
