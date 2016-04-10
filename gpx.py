#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import gpxpy
import gpxpy.gpx

path = 'E:\\Photos\\101D300S\\test.gpx';

gpx_file = open(path, 'r')

gpx = gpxpy.parse(gpx_file)

for track in gpx.tracks:
  for segment in track.segments:
    for point in segment.points:
      print 'Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.time)
