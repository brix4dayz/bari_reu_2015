import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import pandas as pd
import fiona
from itertools import chain
from matplotlib.collections import PatchCollection
from shapely.geometry import Point, Polygon, MultiPoint, MultiPolygon
from descartes import PolygonPatch

#source: http://sensitivecities.com/so-youd-like-to-make-a-map-using-python-EN.html#.VZGG_VyZ65Y

class BostonMap(object):
  def __init__(self):
    shp = fiona.open('Tracts_Boston_2010_BARI.shp')
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
    self.map.readshapefile(
      'Tracts_Boston_2010_BARI',
      'boston',
      color='none',
      zorder=2)
    return

  def mapDF(self):
    # set up a map dataframe
    self.df_map = pd.DataFrame({
      'poly': [Polygon(xy) for xy in self.map.boston]})
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
    self.leverettG()
    return

  def makePlot(self, outname, title):
    plt.title(title)
    #self.fig.set_figsize(...)
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

class BostonScatter(BostonMap):
  def __init__(self, dataPoints):
    self.dataPoints = dataPoints
    # call parent constructor
    super(BostonScatter, self).__init__()

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

    #self.map.drawcoastlines()
    return

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
  boston = BostonScatter(testData)
  boston.plotMap(outname=out, title='Scatterplot Over Boston')
  return

if __name__ == "__main__":
  testScatter()
  plt.show()