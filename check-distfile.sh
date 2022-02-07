#!/bin/sh

repopath="${HOME}/git/ports"

[ ! -f "${repopath}/INDEX*" ] && make -C "${repopath}" fetchindex

[ ! -f /usr/local/bin/distilator ] && pkg install -y distilator

ports=$(make -C "${repopath}" search key="sbz@FreeBSD.org" \
    display=path|grep -v ^$|awk '{print $2}')

for origin in ${ports};
do
    (cd ${origin}; echo "Port: ${origin}"; distilator; echo) | tee -a /tmp/myport-distfile.log
done
