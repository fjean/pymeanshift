/*
 *  Python Module for Mean Shift Image Segmentation using OpenCV (PyMeanShift)
 *  Copyright (C) 2011 by Frederic Jean
 *
 *  PyMeanShift is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published
 *  by the Free Software Foundation, either version 3 of the License,
 *  or (at your option) any later version.
 *
 *  PyMeanShift is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with PyMeanShift.  If not, see <http://www.gnu.org/licenses/>.
 *
 */

#include "pymeanshift.hpp"
#include "msImageProcessor.h"

#include <cstring> // For memcpy

// Implementation of the mean shift image segmentation algorithm
//
//  - The image inInputImage can be either 8bits one channel (CV_8UC1) or 8bits 3 channels (CV_8UC3).
//  - The image outMeanColorLabelImage must be of the same type than inInputImage.
//  - The image outLabels must be 32 bits per pixel, one channel (CV_32SC1).
//
//  - The return value is the number of regions found (>=0), or -1 if the images where not properly
//    initialized or if they are of the wrong type.
//
int segmentMeanShiftImpl(const CvMat* inInputImage,
                         CvMat* outMeanColorLabelImage,
                         CvMat* outLabels, int inSigmaS,
                         float inSigmaR,
                         unsigned int inMinRegion,
                         unsigned int inSpeedUpLevel)
{
  msImageProcessor lIP;
  SpeedUpLevel lSpeedUpLevel;
  int* lLabels;
  float* lModes;
  int* lModePointCounts;
  int lNbRegions;

  if(!inInputImage || !outMeanColorLabelImage || !outLabels)
    return -1;  
   
  // Check if labels image is 32 bits per pixel, one channel
  if(CV_MAT_DEPTH(inInputImage->type) != CV_MAT_DEPTH(outMeanColorLabelImage->type) ||
     CV_MAT_CN(inInputImage->type) != CV_MAT_CN(outMeanColorLabelImage->type))
  {
    return -1;
  }
  
  // Check if labels image is 32 bits per pixel, one channel
  if(CV_MAT_DEPTH(outLabels->type) != 4 || CV_MAT_CN(outLabels->type) != 1)
    return -1;
  
  switch(inSpeedUpLevel)
  {
    case 0:
      lSpeedUpLevel = NO_SPEEDUP;
      break;
    case 1:
      lSpeedUpLevel = MED_SPEEDUP;
      break;
    case 2:
      lSpeedUpLevel = HIGH_SPEEDUP;
      break;      
    default:
      lSpeedUpLevel = HIGH_SPEEDUP;
  }

  // If input image is a color image, convert from BGR to RGB, using outMeanColorLabelImage
  // as a temp image, and define it as the image to segment.
  if(CV_MAT_CN(inInputImage->type)==3)
  {
    cvCvtColor(inInputImage, outMeanColorLabelImage, CV_BGR2RGB);     
    lIP.DefineImage(outMeanColorLabelImage->data.ptr, COLOR, inInputImage->rows, inInputImage->cols);
  }
  else
  {
    lIP.DefineImage(inInputImage->data.ptr, GRAYSCALE, inInputImage->rows, inInputImage->cols);
  }

  // Perform segmentation et get the color/grayscale labels image
  lIP.Segment(inSigmaS, inSigmaR, inMinRegion, lSpeedUpLevel);     
  lIP.GetResults(outMeanColorLabelImage->data.ptr);

  // Convert the color labels image from RGB to BGR if necessary
  if (CV_MAT_CN(inInputImage->type)==3)
    cvCvtColor(outMeanColorLabelImage, outMeanColorLabelImage, CV_RGB2BGR); 

  // Get labels image (each pixel value corrrespond to the region number it belongs to)
  lNbRegions = lIP.GetRegions( &lLabels, &lModes, &lModePointCounts);
  memcpy(outLabels->data.i, lLabels, inInputImage->rows*inInputImage->cols*sizeof(int));

  // Cleanup
  delete [] lLabels;
  delete [] lModes;
  delete [] lModePointCounts;
  
  return lNbRegions;
}
