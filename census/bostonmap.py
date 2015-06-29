import csv
import yaml
import math
import re
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np

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

def distance(parcel, datum):
  return 

def convertCoord(coordinate):
  return float(coordinate)*1000.0

class BostonMap(object):
  def __init__(self):
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
    parcel['X'] = convertCoord(parcel['X'])
    parcel['Y'] = convertCoord(parcel['Y'])
    i = int(parcel['X'])/binsize
    j = int(parcel['Y'])/binsize
    self.grid[i][j].append(parcel)
    return

  def addData(self, datum):
    global cutoff
    datum['lon'] = convertCoord(datum['lon'])
    datum['lat'] = convertCoord(datum['lat'])
    i = int(datum['lon'])/binsize
    j = int(datum['lat'])/binsize
    for p in self.grid[i][j]:
      if distance(p, datum) <= cutoff:
        p.append(datum)
        return

def test():
  
  return

if __name__ == "__main__":
  test()