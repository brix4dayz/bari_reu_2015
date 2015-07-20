
import os
import sys

sys.path.append(os.path.realpath('../census/'))
import bostonmap as bm

import csv

import matplotlib.pyplot as plt

reports = []

with open('911_violent_2012_2013.csv') as csvfile:
  nines = csv.DictReader(csvfile)
  for n in nines:
    reports.append(n)

boston = bm.BostonDensityCT(reports)
boston.plotMap(outname='testMap', title='911 reports by Density')
plt.show()