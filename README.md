# freebsd-maintainer-scripts

This repository contains the following files to assist me with
[FreeBSD](https://www.freebsd.org) related
tasks:

+ **disable_debug_sysctl.conf**

[sysctl(8)][1] configuration option to disable debug

+ **ftabs**

[Python][2] script to open freebsd related links as tab on browser at once

+ **gensrc**

[tcsh(1)][3] script to generate the src.conf(5) options WITH or WITHOUT

+ **[getpatch][src]**

[Python][2] script to download bug tracker attachment using the command line.
[Documentation][doc]

+ **myportlint**

[sh(1)][4] script to run [portlint(1)][5] on a bunch of ports

+ **poudriere-runner**

[poudriere(8)][6] helper to process testport action on multiple jails

+ **sss**

[Python][2] script to display [subversion][7] verbose status (committer,
message, files) updates by parsing XML log.


+ **vimport**

[sh(1)][4] script to open all the Makefile for a given a maintainer

[1]: https://www.freebsd.org/cgi/man.cgi?sysctl
[2]: https://www.python.org/
[3]: https://www.freebsd.org/cgi/man.cgi?csh
[4]: https://www.freebsd.org/cgi/man.cgi?sh
[5]: https://www.freebsd.org/cgi/man.cgi?portlint
[6]: https://github.com/freebsd/poudriere
[7]: https://subversion.apache.org

[src]: https://svn.freebsd.org/ports/head/Tools/scripts/getpatch
[doc]: https://svn.freebsd.org/ports/head/Tools/scripts/README.getpatch
