import csv
import yaml
import math
import re

grid = None

cutoff = 1.0

bostonXMIN = 0.0

bostonXMAX = 0.0

bostonYMIN = 0.0

bostonYMAX = 0.0

binsize = 10.0

def initGrid():
  return 

def loadParcels():
  return

def test():
  return

def distance(parcel, datum):
  return 

class ParcelGrid(object):
  def __init__(self, xmin, xmax, ymin, ymax, binsize):
    self.grid = {}
    for i in range(xmin, xmax, binsize):
      self.grid[i] = {}
      for j in range(ymin, ymax, binsize):
        self.grid[i][j] = []
    return

  def addParcel(self, parcel):
    i = int(float(parcel['X']))/binsize
    j = int(float(parcel['Y']))/binsize
    self.grid[i][j].append(parcel)
    return

  def addData(self, datum):
    global cutoff
    i = int(float(datum['lon']))/binsize
    j = int(float(datum['lat']))/binsize
    for p in self.grid[i][j]:
      if distance(p, datum) <= cutoff:
        p.append(datum)
        return


if __name__ == "__main__":
  test()