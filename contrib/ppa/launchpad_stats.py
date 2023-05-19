#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from launchpadlib.launchpad import Launchpad
import os

PPA_OWNER='sea5kg'
PPA='wsjcpp'
PACKAGE='wsjcpp'

cachedir = os.environ['HOME'] + '/.launchpadlib/cache/'
launchpad = Launchpad.login_anonymously('just testing', 'production', cachedir)

ppa = launchpad.people[PPA_OWNER].getPPAByName(name=PPA)
bins = ppa.getPublishedBinaries(binary_name=PACKAGE)
builds = []
total = 0
for bin in bins:
    count = bin.getDownloadCount()
    total += count
    if (count > 0):
        builds.append(
            [count, f'{bin.binary_package_name} {bin.binary_package_version}']
        )

builds_sorted = sorted(builds,key=lambda count: count[0],reverse=True)
for build in builds_sorted:
    print(f"{str(build[0])}:{str(build[1])}")