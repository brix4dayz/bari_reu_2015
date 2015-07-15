
# coding: utf-8

# Imports for the program (Original program by Josh Lozjim and edited by Hayden Fuss, this version by Jeremy McKenzie)

import matplotlib
import time                      # time/date parsing
import csv                       # data parsing
import numpy as np               # arrays for plotting
import matplotlib.pyplot as plt  # Plotting
import math                      # ceiling for y-max in plots
import sys

import os
sys.path.append(os.path.realpath('../census'))
import bostonmap as bm


# time_fmt declares the format for the time data
# year_data declares an empty hash, and the for loop creates further hashes (think: vectors) assigned to the keys of '2012' and '2013'

time_fmt = "%m/%d/%Y"

years = ('2012', '2013')

year_data = {}
filename = raw_input("Enter the file name to read data from: ")
#filename = sys.stdin.readline()
print filename
filename = filename.rstrip("\n")
prefix = raw_input("Enter prefix for maps: ")
prefix = prefix.rstrip("\n")


# This portion of the program builds the data list, organized by month, in a list called emergency. It runs through the list, pulling dates from the csv file, and then counts the number of times any particular month (and thereby the amount of calls in that month) comes up. If a month has not previously been encountered, it is added to the list and given a count of one. Otherwise, it's incremented by one.

reports = []
currentDay = 12

with open(filename) as csvfile:
    threeOne = csv.DictReader(csvfile)
        # for all the 311 calls the reader finds
    for e in threeOne:
        date = time.strptime(e['OPEN_DT'], time_fmt) # converts string version of date into a date object
        y = date.tm_year
        d = date.tm_mday
        if not y in year_data.keys():
            year_data[y] = {}
        if y == 2013 and date.tm_mon == 4 and d in range (12,23):
            e['lon'] = e['X']
            e['lat'] = e['Y']
            if e['lat'] != 'NA':
                if d == currentDay:
                    reports.append(e)
                elif d == currentDay + 1:                    
                    boston = bm.BostonScatter(reports)
                    boston.plotMap(outname=prefix + '_bombday_scatter_311_' + str(currentDay),
                        title='Locations of 311 Reports on 4-' + str(currentDay) + '-13')
                    boston = bm.BostonDensity(reports)
                    boston.plotMap(outname=prefix + '_bombday_density_311_' + str(currentDay),
                        title='Locations of 311 Reports in 4-' + str(currentDay) + '-13')
                    reports = [e]  # clears list of previous day and adds first of this day
                    f = open(prefix + "_most_dense_311_4-" + str(currentDay) + "-13.csv", "w")
                    currentDay += 1
                    f.write(boston.highest)
                    f.close()
                 
boston = bm.BostonScatter(reports)
boston.plotMap(outname=prefix + '_bombday_scatter_311_' + str(currentDay),
    title='Locations of 311 Reports on 4-' + str(currentDay) + '-13')
boston = bm.BostonDensity(reports)
boston.plotMap(outname=prefix + '_bombday_density_311_' + str(currentDay),
    title='Locations of 311 Reports in 4-' + str(currentDay) + '-13')
f = open(prefix + "_most_dense_311_4-" + str(currentDay) + "-13.csv", "w")
currentDay += 1
f.write(boston.highest)
f.close()
