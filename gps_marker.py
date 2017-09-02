#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import sys
import os
import datetime

import gpxpy
import pyexiv2, fractions

__author__ = 'Chen Hai'
  
class GPSMarker:
  path = ''
  _points = []

  def __init__(self, path):
    self.path = path

  @staticmethod
  def file_extension(f):
    return os.path.splitext(f)[1].lower()

  @staticmethod
  def get_point_time(point):
    return point.time

  def load_gpx(self, path):
    with open(path, 'r') as gpx_file
      gpx = gpxpy.parse(gpx_file)

    for track in gpx.tracks:
      for segment in track.segments:
        self._points.extend(segment.points)
        
  def load_all_gpxs(self):
    print 'Gpx is Loading......'
    files = os.listdir(self.path)
    for f in files:
      if GPSMarker.file_extension(f) == '.gpx':
        self.load_gpx(self.path + os.sep + f)
    self._points.sort(key = GPSMarker.get_point_time)
    self._points = tuple(self._points)

  def find_point(self, time):
    length = len(self._points)
    if length == 0:
      return -1
    start = 0
    end = length
    index = start;
    while end > start:
      index = (start + end) / 2
      point = self._points[index]
      if point.time == time:
        break
      elif point.time > time:
        end = index
      else:
        start = index + 1

    timedelta = abs(self._points[index].time - time)
    if index > 0:
      previous = self._points[index - 1]
      if (abs(previous.time - time) < timedelta):
        timedelta = abs(previous.time - time)
        index = index - 1
    if index < length - 1:
      subsequent = self._points[index + 1]
      if (abs(subsequent.time - time) < timedelta):
        timedelta = abs(subsequent.time - time)
        index = index + 1
    if timedelta.seconds > 600:  # Ten minutes
      index = -1
    return index
  
  @staticmethod  
  def float_to_rational(value):
    frac = fractions.Fraction(abs(value)).limit_denominator(99999)
    return pyexiv2.Rational(frac.numerator, frac.denominator)

  @staticmethod
  def is_photo(file_name):
    extension = GPSMarker.file_extension(file_name)
    if '.nef' == extension:
      return True
    elif '.jpeg' == extension:
      return True;
    elif '.jpg' == extension:
      return True;
    elif '.cr2' == extension or '.crw' == extension:
      return True
    elif '.arw' == extension:
      return True
    elif '.raf' == extension:
      return True
    elif '.srw' == extension:
      return True
    elif '.rw2' == extension:
      return True
    elif '.orf' == extension:
      return True
    elif '.ref' == extension:
      return True
    elif '.dng' == extension:
      return True
    return False

  def mark_photo(self, file_name):
    metadata = pyexiv2.ImageMetadata(file_name)
    metadata.read()
    print file_name
    try:
      if len(metadata['Exif.GPSInfo.GPSLongitude'].value) > 0:
        return
    except KeyError:
      pass

    timedelta = datetime.datetime.now() - datetime.datetime.utcnow()
    # To UC datetime.
    try:
      date_time_original = metadata['Exif.Photo.DateTimeOriginal'].value - timedelta
      index = self.find_point(date_time_original)
    except KeyError:
      index = -1
    print 'find:', index
    if index < 0:
      return
    point = self._points[index]
    if point.longitude > 0:
      metadata['Exif.GPSInfo.GPSLongitudeRef'] = 'E'
    else:
      metadata['Exif.GPSInfo.GPSLongitudeRef'] = 'W'
    if point.latitude > 0:
      metadata['Exif.GPSInfo.GPSLatitudeRef'] = 'N'
    else:
      metadata['Exif.GPSInfo.GPSLatitudeRef'] = 'S'
    if point.elevation > 0:
      metadata['Exif.GPSInfo.GPSAltitudeRef'] = '0';
    else:
      metadata['Exif.GPSInfo.GPSAltitudeRef'] = '1';
    gps_altitude = pyexiv2.Rational(abs(point.elevation) * 1000, 1000)
    
    gps_longitude = pyexiv2.NotifyingList()
    gps_longitude.append(pyexiv2.Rational(point.longitude, 1))
    minute = (point.longitude - int(point.longitude)) * 60
    gps_longitude.append(pyexiv2.Rational(minute, 1))
    second = (minute - int(minute)) * 60
    gps_longitude.append(pyexiv2.Rational(minute * 10000, 10000))
    
    gps_latitude = pyexiv2.NotifyingList()
    gps_latitude.append(pyexiv2.Rational(point.latitude, 1))
    minute = (point.latitude - int(point.latitude)) * 60
    gps_latitude.append(pyexiv2.Rational(minute, 1))
    second = (minute - int(minute)) * 60
    gps_latitude.append(pyexiv2.Rational(minute * 10000, 10000))
    
    gps_time_stamp = pyexiv2.NotifyingList()
    gps_time_stamp.append(pyexiv2.Rational(point.time.hour, 1))
    gps_time_stamp.append(pyexiv2.Rational(point.time.minute, 1))    
    gps_time_stamp.append(pyexiv2.Rational(
        point.time.second * 100 + point.time.microsecond / 10000,
        100))
                        
    metadata['Exif.GPSInfo.GPSLongitude'] = gps_longitude
    metadata['Exif.GPSInfo.GPSLatitude'] = gps_latitude
    metadata['Exif.GPSInfo.GPSAltitude'] = gps_altitude
    metadata['Exif.GPSInfo.GPSDateStamp'] = point.time.strftime('%Y-%m-%d')
    metadata['Exif.GPSInfo.GPSTimeStamp'] = gps_time_stamp
    print metadata['Exif.GPSInfo.GPSLongitudeRef'].value, metadata['Exif.GPSInfo.GPSLongitude'].value
    print metadata['Exif.GPSInfo.GPSLatitudeRef'].value, metadata['Exif.GPSInfo.GPSLatitude'].value
    metadata.write()

  def mark_photos(self):
    files = os.listdir(self.path)
    for f in files:
      if GPSMarker.is_photo(f):
        self.mark_photo(self.path + os.sep + f)

if __name__ == '__main__':
  path = os.path.abspath('.')
  if len(sys.argv) > 1:
    path = sys.argv[1]
  print 'path:', path
  marker = GPSMarker(path)
  marker.load_all_gpxs()
  marker.mark_photos()
