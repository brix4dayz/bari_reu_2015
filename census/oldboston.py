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

def test():

  shp = fiona.open('Tracts_Boston_2010_BARI.shp')
  bds = shp.bounds
  shp.close()
  extra = 0.01
  ll = (bds[0], bds[1])
  ur = (bds[2], bds[3])
  coords = list(chain(ll, ur))
  w, h = coords[2] - coords[0], coords[3] - coords[1]

  fig = plt.figure()
  ax = fig.add_subplot(111, axisbg='w', frame_on=False)

  m = Basemap(
    projection='tmerc',
    lon_0=(coords[0] + coords[2])/2, # here was where I went wrong
    lat_0=(coords[3] + coords[1])/2,
    llcrnrlon=coords[0] - extra * w,
    llcrnrlat=coords[1] - extra + 0.01 * h,
    urcrnrlon=coords[2] + extra * w,
    urcrnrlat=coords[3] + extra + 0.01 * h,
    lat_ts=0,
    resolution='i',
    suppress_ticks=True)

  m.readshapefile(
    'Tracts_Boston_2010_BARI',
    'boston',
    color='none',
    zorder=2)

  # set up a map dataframe
  df_map = pd.DataFrame({
    'poly': [Polygon(xy) for xy in m.boston]})
  df_map['area_m'] = df_map['poly'].map(lambda x: x.area)
  df_map['area_km'] = df_map['area_m'] / 100000

  # draw ward patches from polygons
  df_map['patches'] = df_map['poly'].map(lambda x: PolygonPatch(
    x,
    fc='#000055',
    ec='#787878', lw=.25, alpha=.9,
    zorder=4))

  # Draw a map scale
  m.drawmapscale(
    coords[0] + w/4, coords[3],
    coords[0], coords[1],
    2.,
    barstyle='fancy', labelstyle='simple',
    fillcolor1='w', fillcolor2='#000055',
    fontcolor='#000055',
    zorder=5,
    units='mi')

  # plot boroughs by adding the PatchCollection to the axes instance
  ax.add_collection(PatchCollection(df_map['patches'].values, match_original=True))

  plt.title("Boston")
  # this will set the image width to 722px at 100dpi
  #fig.set_size_inches(7.22, 5.25)
  plt.savefig('boston2.png', dpi=100, alpha=True)
  plt.show()

  return


if __name__ == "__main__":
  test()