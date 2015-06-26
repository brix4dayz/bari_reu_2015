#!/usr/bin/python2.7

# author: Hayden Fuss

import csv

filtered = []

fields = []

with open('CRM 2010-2014 No IDs.csv') as csvfile:
    reports = csv.DictReader(csvfile)
    fields = reports.fieldnames
    for r in reports:
        if "2012" in r['OPEN_DT'] or "2013" in r['OPEN_DT']:
            filtered.append(r)

with open('CRM_2012_2013_no_ids.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)

    writer.writeheader()
    for f in filtered:
        writer.writerow(f)
