import csv
import yaml
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import pandas as pd
import fiona
from itertools import chain
from matplotlib.collections import PatchCollection
from shapely.geometry import Point, Polygon, MultiPoint, MultiPolygon
from descartes import PolygonPatch
import geopandas as gp

#source: http://sensitivecities.com/so-youd-like-to-make-a-map-using-python-EN.html#.VZGG_VyZ65Y

class BostonMap(object):
  def __init__(self, outname):
    self.outname = outname
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
    self.ax = self.fig.add_subplot(111, axisbg='w', frame_on=False)

    self.map = Basemap(
    projection='tmerc',
    lon_0=(self.coords[0] + self.coords[2])/2, # here was where I went wrong
    lat_0=(self.coords[3] + self.coords[1])/2,
    llcrnrlon=self.coords[0] - self.extra * self.w,
    llcrnrlat=self.coords[1] - self.extra + 0.01 * self.h,
    urcrnrlon=self.coords[2] + self.extra * self.w,
    urcrnrlat=self.coords[3] + self.extra + 0.01 * self.h,
    lat_ts=0,
    resolution='i',
    suppress_ticks=True)

    self.map.readshapefile(
      'Tracts_Boston_2010_BARI',
      'boston',
      color='none',
      zorder=2)
    return

  def buildDFs(self):
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

  def plotMap(self):
    self.loadBasemap()

    self.buildDFs()

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

    # plot boroughs by adding the PatchCollection to the axes instance
    self.ax.add_collection(PatchCollection(self.df_map['patches'].values, match_original=True))

    plt.title("Boston")
    # this will set the image width to 722px at 100dpi
    #fig.set_size_inches(7.22, 5.25)
    plt.savefig(self.outname + '.png', dpi=100, alpha=True)
    plt.show()
    return

if __name__ == "__main__":
  out = raw_input("Enter name of map png: ")
  boston = BostonMap(out)
  boston.plotMap()