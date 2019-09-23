#!/usr/bin/python2.7
# -*- coding: cp936 -*-

import pyexiv2
import os

path = 'E:\\Photos\\101D300S\\CHE_2850.NEF';
metadata = pyexiv2.ImageMetadata(path)
metadata.read()

print path
print metadata.mime_type
for key in metadata.exif_keys :
  if key == 'Exif.NikonSi02xx.0x027a' or key == 'Exif.NikonCb2b.0x0095':
    continue
  print metadata[key]

   
