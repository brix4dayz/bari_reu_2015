import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import pandas as pd
import fiona
from itertools import chain
from matplotlib.collections import PatchCollection
from shapely.geometry import Point, Polygon, MultiPoint, MultiPolygon
from descartes import PolygonPatch

# author: Hayden Fuss
# last edited: Monday, July 6, 2015

#source: http://sensitivecities.com/so-youd-like-to-make-a-map-using-python-EN.html#.VZGG_VyZ65Y
# mass. census source: http://catalog.data.gov/dataset/tiger-line-shapefile-2014-state-massachusetts-current-census-tract-state-based-shapefile

# uses os and inspect to determine path to module
import os
import inspect
myDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

bostonTracts = '/boston/Tracts_Boston_2010_BARI'
stateTracts = '/mass/tl_2014_25_tract'

#####################################################################################################################
class BostonMap(object):
  def __init__(self):
    shp = fiona.open(myDir + bostonTracts + '.shp')
    bds = shp.bounds
    shp.close()
    self.extra = 0.01
    self.ll = (bds[0], bds[1])
    self.ur = (bds[2], bds[3])
    self.coords = list(chain(self.ll, self.ur))
    self.w, self.h = self.coords[2] - self.coords[0], self.coords[3] - self.coords[1]
    return

  def loadBasemap(self):
    self.fig = plt.figure()
    self.ax = self.fig.add_subplot(111)
    self.map = Basemap(
      projection='tmerc',
      lon_0=(self.coords[0] + self.coords[2])/2, # here was where I went wrong
      lat_0=(self.coords[3] + self.coords[1])/2,
      llcrnrlon=self.coords[0] - self.extra * self.w,
      llcrnrlat=self.coords[1] - self.extra + 0.01 * self.h,
      urcrnrlon=self.coords[2] + self.extra * self.w,
      urcrnrlat=self.coords[3] + self.extra + 0.01 * self.h,
      lat_ts=0,
      resolution='h',
      area_thresh=0.01,
      suppress_ticks=True)
    self.loadShapeFile()
    return

  def loadShapeFile(self):
    self.map.readshapefile(
      myDir + stateTracts,
      'boston',
      color='none',
      zorder=2)
    return

  def mapDF(self):
    # set up a map dataframe
    indices = []
    self.df_map = pd.DataFrame({
      'poly': [Polygon(xy) for xy in self.map.boston],
      'land_info': [info['ALAND'] for info in self.map.boston_info]})
    for i,row in self.df_map.iterrows():
      if row['land_info'] == 0:
        print 'yes'
        indices.append(i)
    self.df_map.drop(indices)
    self.df_map['area_m'] = self.df_map['poly'].map(lambda x: x.area)
    self.df_map['area_km'] = self.df_map['area_m'] / 100000
    # draw ward patches from polygons
    self.df_map['patches'] = self.df_map['poly'].map(lambda x: PolygonPatch(
      x,
      fc='#000055',
      ec='#787878', lw=.25, alpha=.9,
      zorder=4))
    return

  # virtual function to be overridden
  def dataDF(self):
    return

  def buildDFs(self):
    self.mapDF()
    self.dataDF()
    return

  def leverettG(self):
    # plot leverett g tower for fun
    x,y = self.map(-71.1161, 42.3692)
    self.map.plot(x, y, 'go', markersize=5)
    return

  def mapScale(self):
    # Draw a map scale
    self.map.drawmapscale(
      self.coords[0] + self.w/4, self.coords[3],
      self.coords[0], self.coords[1],
      2.,
      barstyle='fancy', labelstyle='simple',
      fillcolor1='w', fillcolor2='#000055',
      fontcolor='#000055',
      zorder=5,
      units='mi')
    return

  def tracts(self):
    # plot tracts by adding the PatchCollection to the axes instance
    self.ax.add_collection(PatchCollection(self.df_map['patches'].values, match_original=True))
    return

  # virtual function to be overridden
  def data(self):
    #self.leverettG()
    return

  def makePlot(self, outname, title):
    plt.title(title)
    self.fig.set_size_inches(10, (self.h/self.w)*10)
    plt.savefig(outname + '.png', dpi=100, alpha=True)
    return

  def plotMap(self, outname='boston', title='Boston'):
    self.loadBasemap()
    self.buildDFs()
    self.mapScale()
    self.tracts()
    self.data()
    self.makePlot(outname, title)
    return

#####################################################################################################################
class BostonScatter(BostonMap):
  def __init__(self, dataPoints):
    self.dataPoints = dataPoints
    # call parent constructor
    super(BostonScatter, self).__init__()
    return

  def dataDF(self):
    output = {'lon':[], 'lat':[]}
    for d in self.dataPoints:
      for each in ('lon', 'lat'):
        output[each].append(d[each])

    df = pd.DataFrame(output)
    df[['lon', 'lat']] = df[['lon', 'lat']].astype(float)

    self.dataPoints = pd.Series(
      [Point(self.map(mapped_x, mapped_y)) for mapped_x, mapped_y in zip(df['lon'], df['lat'])])
    return

  def data(self):
    self.map.scatter(
      [geom.x for geom in self.dataPoints],
      [geom.y for geom in self.dataPoints],
      10, marker='o', lw=.25,
      facecolor='#33ccff', edgecolor='w',
      alpha=0.9, antialiased=True, zorder=3)
    return

#####################################################################################################################
class GreaterBostonScatter(BostonScatter):
  def __init__(self, dataPoints):
    super(GreaterBostonScatter, self).__init__(dataPoints)
    return

  # override so polygon patches arent added
  def tracts(self):
    return

  # override so dataframe of map isnt made, instead draw boundaries and fill in colors
  def mapDF(self):
    self.map.drawmapboundary(color='w', fill_color='aqua')
    self.map.drawcoastlines()
    self.map.fillcontinents(color='coral', lake_color='aqua')
    return

  def loadShapeFile(self):
    self.map.readshapefile(
      myDir + stateTracts,
      'boston',
      zorder=2)
    return

#####################################################################################################################
def testMap():
  out = raw_input("Enter name of output png: ")
  boston = BostonMap()
  boston.plotMap(outname=out)

def testScatter():
  out = raw_input("Enter name of output png: ")
  testData = [
    {'lon':'-71.0120751', 'lat':'42.27090738'},
    {'lon':'-71.1864942', 'lat':'42.36610796'},
    {'lon':'-71.0530936', 'lat':'42.35931187'}
  ]
  boston = GreaterBostonScatter(testData)
  boston.plotMap(outname=out, title='Scatterplot Over Boston')
  return

#####################################################################################################################
if __name__ == "__main__":
  testMap()
  plt.show()