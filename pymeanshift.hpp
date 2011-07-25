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

#include <cv.h>

#ifndef PYMEANSHIFT_HPP
#define PYMEANSHIFT_HPP

// Function declaration 
int segmentMeanShiftImpl(const CvMat* inInputImage,
                         CvMat* outMeanColorLabelImage,
                         CvMat* outLabels, int inSigmaS,
                         float inSigmaR,
                         unsigned int inMinRegion,
                         unsigned int inSpeedUpLevel);

#endif // PYMEANSHIFT_HPP
