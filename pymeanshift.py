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

import _pymeanshift

__version__ = '0.2.2'
__version_info__ = tuple([ int(num) for num in __version__.split('.')])

'''
Python Extension for Mean Shift Image Segmentation (PyMeanShift)
     
The mean shift algorithm and its implementation in C++ are by
Chris M. Christoudias and Bogdan Georgescu. The PyMeanShift extension
provides a Python interface  to the meanshift C++ implementation
using Numpy arrays.
    
For details on the algorithm:
D. Comanicu, P. Meer: "Mean shift: A robust approach toward feature space analysis".
IEEE Transactions on Pattern Analysis and Machine Intelligence, May 2002.  
'''

SPEEDUP_NO = _pymeanshift.SPEEDUP_NO
SPEEDUP_MEDIUM = _pymeanshift.SPEEDUP_MEDIUM
SPEEDUP_HIGH = _pymeanshift.SPEEDUP_HIGH    


def segment(image, spatial_radius, range_radius, min_density, speedup_level=SPEEDUP_HIGH):
    '''
    Segment the input image (color or grayscale).
    
    Keyword arguments:
    image -- Input image (2-D or 3-D numpy array or compatible).
    spatial_radius -- Spatial radius of the search window (integer).
    range_radius -- Range radius of the search window (float).
    min_density -- The minimum point density of a region in the segmented
                   image (integer).    
    speedup_level -- Filtering optimization level for fast execution
                     (default: high). See SpeedUpLevel.
    
    Return value: tuple (segmented, labels, nb_regions)
    segmented -- Image (Numpy array) where the color (or grayscale) of the
                 regions is the mean value of the pixels belonging to a region.
    labels -- Image (2-D Numpy array, 32 unsigned bits per element) where a
              pixel value correspond to the region number the pixel belongs to.
    nb_regions -- The number of regions found by the mean shift algorithm.
    
    NOTES: To avoid unnecessary image conversions when the function is called,
    make sure the input image array is 8 unsigned bits per pixel and is
    contiguous in memory.    
    
    '''        
    return _pymeanshift.segment(image, spatial_radius, range_radius, min_density, speedup_level)
    

class Segmenter(object):
    '''
    Segmenter class using the mean shift algorithm to segment image
    '''
    
    def __init__(self, spatial_radius=None, range_radius=None, min_density=None, speedup_level=SPEEDUP_HIGH):
        '''
        Segmenter init function. See function segment for keywords description.
        '''
        self._spatial_radius = None
        self._range_radius = None
        self._min_density = None
        self._speedup_level = None
        
        if spatial_radius is not None:
            self.spatial_radius = spatial_radius
        if range_radius is not None:
            self.range_radius = range_radius
        if min_density is not None:            
            self.min_density = min_density
        self.speedup_level = speedup_level
        
    def __call__(self, image):
        '''
        Segment the input image (color or grayscale).
        
        Keyword arguments:
            image -- Input image (2-D or 3-D numpy array or compatible).
            
        Return value: tuple (segmented, labels, nb_regions)
        segmented -- Image (Numpy array) where the color (or grayscale) of the
                     regions is the mean value of the pixels belonging to a region.
        labels -- Image (2-D Numpy array, 32 unsigned bits per element) where a
                  pixel value correspond to the region number the pixel belongs to.
        nb_regions -- The number of regions found by the mean shift algorithm.
    
        NOTES: To avoid unnecessary image conversions when the function is called,
        make sure the input image array is 8 unsigned bits per pixel and is
        contiguous in memory.    
            
        '''
        if self._spatial_radius is None:
            raise ValueError("Spatial radius has not been set")
        if self._range_radius is None:
            raise ValueError("Range radius has not been set")
        if self._min_density is None:
            raise ValueError("Minimum density has not been set")        
        
        return _pymeanshift.segment(image, self._spatial_radius, self._range_radius, self._min_density, self._speedup_level)
                
    def __str__(self):
        return "<Segmenter: spatial_radius={}, range_radius={}, min_density={}, speedup_level={}>".format(
                self._spatial_radius,
                self._range_radius,
                self._min_density,
                self._speedup_level)

    def __repr__(self):
        return "Segmenter(spatial_radius={}, range_radius={}, min_density={}, speedup_level={})".format(
                self._spatial_radius,
                self._range_radius,
                self._min_density,
                self._speedup_level)

    @property
    def spatial_radius(self):
        '''
        Spatial radius of the search window
        '''
        return self._spatial_radius
        
    @spatial_radius.setter
    def spatial_radius(self, value):
        if value < 0:
            raise AttributeError("Spatial radius must be greater or equal to zero")
        self._spatial_radius = value
        
    @property
    def range_radius(self):
        '''
        Range radius of the search window
        '''
        return self._range_radius
            
    @range_radius.setter
    def range_radius(self, value):
        if value < 0:
            raise AttributeError("Range radius must be greater or equal to zero")
        self._range_radius = value

    @property
    def min_density(self):
        '''
        The minimum point density of a region in the segmented image
        '''
        return self._min_density
        
    @min_density.setter
    def min_density(self, value):
        if value < 0:
            raise AttributeError("Minimum density must be greater or equal to zero")
        self._min_density = value

    @property
    def speedup_level(self):
        '''
        Filtering optimization level for fast execution
        '''
        return self._speedup_level
        
    @speedup_level.setter
    def speedup_level(self, value):
        if value != SPEEDUP_NO and value != SPEEDUP_MEDIUM and value != SPEEDUP_HIGH:
            raise AttributeError("Speedup level must be 0 (no speedup), 1 (medium speedup), or 2 (high speedup)")
        self._speedup_level = value
