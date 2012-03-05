#
#  Python Module for Mean Shift Image Segmentation (PyMeanShift)
#  Copyright (C) 2012 by Frederic Jean
#
#  PyMeanShift is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published
#  by the Free Software Foundation, either version 3 of the License,
#  or (at your option) any later version.
# 
#  PyMeanShift is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with PyMeanShift.  If not, see <http://www.gnu.org/licenses/>.
# 

import numpy as np
import _pymeanshift

'''
Python Extension for Mean Shift Image Segmentation
     
The mean shift algorithm and its implementation in C++ are by
Chris M. Christoudias and Bogdan Georgescu. This Python module provides the "glue"
that is necessary in order to use the C++ implementation with OpenCV in Python.

For details on the algorithm:
D. Comanicu, P. Meer: "Mean shift: A robust approach toward feature space analysis".
IEEE Transactions on Pattern Analysis and Machine Intelligence, May 2002.
  
'''

# Define segment function alias from the extension
segment = _pymeanshift.segment

# Backward compatibility with PyMeanShift 0.1.x
def segmentMeanShift(inputImage, sigmaS=6, sigmaR=4.5, minRegion=300, speedUpLevel=2):
  '''
  Segmentation of an image (grayscale or color) using the mean shift algorithm.
  
  WARNING: This function might be removed from future version of PyMeanShift.
           Please use the "segment" function or the MeanShiftSegmenter class.
  
  Return a 3-tuple (colorLabelsImage, labelsImg, nbRegions).
    - colorLabelsImage is the segmented image with each region colored as the
      mean color value of its pixels.
    - labelsImg is an image where a pixel value represents the region it belongs to.
      This image is one channel, 32 bits per pixel.
    - nbRegions is the number of regions found in the image.  
  '''  
  return segment(inputImage, sigmaS, sigmaR, minRegion, speedUpLevel)





