/*
 *  Python Module for Mean Shift Image Segmentation (PyMeanShift)
 *  Copyright (C) 2012 by Frederic Jean
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

#include <Python.h>
#include <numpy/arrayobject.h>
#include <cstring>

#include "msImageProcessor.h"


// ***************************************************************************
// PyMeanShift related functions
// ***************************************************************************

// Segment image function (the only function provided by the extension)
static PyObject* segment(PyObject* self, PyObject* args)
{
  PyObject* array = NULL;
  PyObject* inputImage = NULL;
  PyArrayObject* segmentedImage = NULL;
  PyArrayObject* labelImage = NULL;
  int radiusS[1];
  double radiusR[1];
  unsigned int minDensity[1];
  unsigned int speedUp[1] = { HIGH_SPEEDUP };

  msImageProcessor imageSegmenter;
  SpeedUpLevel speedUpLevel;    
  int* tmpLabels = NULL;
  float* tmpModes = NULL;
  int* tmpModePointCounts = NULL;
  int nbRegions;
  npy_intp dimensions[3];
  int nbDimensions;
  
  if (!PyArg_ParseTuple(args, "OidI|I", &array, &radiusS, &radiusR, &minDensity, &speedUp))
    return NULL;
  
  if(radiusS[0] < 0)
  {
    PyErr_SetString(PyExc_ValueError, "Spatial radius must be greater or equal to zero");
    return NULL;
  }

  if(radiusR[0] < 0.)
  {
    PyErr_SetString(PyExc_ValueError, "Range radius must be greater or equal to zero");
    return NULL;
  }

  if(minDensity[0] < 0)
  {
      PyErr_SetString(PyExc_ValueError, "Minimum density must be greater or equal to zero");
      return NULL;
  }
    
  if(speedUp[0] > 2)
  {
    PyErr_SetString(PyExc_ValueError, "Speedup level must be 0 (no speedup), 1 (medium speedup), or 2 (high speedup)");
    return NULL;
  }
    
  // Get ndarray object having 8 unsigned bits per element (uchar) and 
  inputImage = PyArray_FROM_OTF(array, NPY_UBYTE, NPY_IN_ARRAY);
  if(inputImage == NULL)
    return NULL;
    
  // Check that the array is 2 dimentional (gray scale image) or 3 dimensional (RGB color image),
  // and initialize segmenter
  if(PyArray_NDIM(inputImage) == 2)
  {
    nbDimensions = 2;
    dimensions[0] = PyArray_DIM(inputImage, 0);
    dimensions[1] = PyArray_DIM(inputImage, 1);
    imageSegmenter.DefineImage((unsigned char*)PyArray_DATA(inputImage), GRAYSCALE, dimensions[0], dimensions[1]);
  }
  else if(PyArray_NDIM(inputImage) == 3)
  {
    nbDimensions = 3;
    dimensions[0] = PyArray_DIM(inputImage, 0);
    dimensions[1] = PyArray_DIM(inputImage, 1);      
    dimensions[2] = 3;
    imageSegmenter.DefineImage((unsigned char*)PyArray_DATA(inputImage), COLOR, dimensions[0], dimensions[1]);
  }
  else
  {
    Py_DECREF(inputImage);
    PyErr_SetString(PyExc_ValueError, "Array must be 2 dimentional (gray scale image) or 3 dimensional (RGB color image)");
    return NULL;
  }
    
  // Create output images
  segmentedImage = (PyArrayObject *) PyArray_SimpleNew(nbDimensions, dimensions, PyArray_UBYTE);
  if(!segmentedImage)
  {
    Py_DECREF(inputImage);
    return NULL;  
  }

  labelImage = (PyArrayObject *) PyArray_SimpleNew(2, dimensions, PyArray_INT);
  if(!labelImage)
    return NULL;  
    
  // Set speedup level
  switch(speedUp[0])
  {
    case 0:
      speedUpLevel = NO_SPEEDUP;
      break;
    case 1:
      speedUpLevel = MED_SPEEDUP;
      break;
    case 2:
      speedUpLevel = HIGH_SPEEDUP;
      break;      
    default:
      speedUpLevel = HIGH_SPEEDUP;
  }
    
  // Segment image and get segmented image
  imageSegmenter.Segment(radiusS[0], radiusR[0], minDensity[0], speedUpLevel);
  imageSegmenter.GetResults((unsigned char*)PyArray_DATA(segmentedImage));
    
  // Get labels images and number of regions
  nbRegions = imageSegmenter.GetRegions( &tmpLabels, &tmpModes, &tmpModePointCounts);
  memcpy((int*)PyArray_DATA(labelImage), tmpLabels, dimensions[0]*dimensions[1]*sizeof(int));
        
  // Cleanup
  Py_DECREF(inputImage);
  delete [] tmpLabels;
  delete [] tmpModes;
  delete [] tmpModePointCounts;    
    
  // Return a tuple with the segmented image, the label image, and the number of regions
  return Py_BuildValue("(NNi)", PyArray_Return(segmentedImage), PyArray_Return(labelImage), nbRegions) ;    
}


// ***************************************************************************
// Doc strings for Python module and functions
// ***************************************************************************

// Module doc
static char pmsDoc[] = \
  "Python Extension for Mean Shift Image Segmentation (PyMeanShift)\n\
  \n\
  The mean shift algorithm and its implementation in C++ are by \n\
  Chris M. Christoudias and Bogdan Georgescu. The PyMeanShift extension \n\
  provides a Python interface  to the meanshift C++ implementation \n\
  using Numpy arrays.\n\
  \n\
  For details on the algorithm: \n\
  D. Comanicu, P. Meer. Mean shift: A robust approach toward feature space analysis.\n\
  IEEE Transactions on Pattern Analysis and Machine Intelligence, May 2002.\n\
  \n\
  ";

// Segment image function doc
static char pmsSegmentDoc[] = \
  "Segment a color and gray scale image using the mean shift algorithm.\n\
   \n\
   NOTE: This function is not intended to be used directly; use the segment \n\
   function in the PyMeanShift wrapper module instead. \n\
   \n\
   Arguments:\n\
   Argument 1 -- The image to segment as a Numpy array (or compatible)\n\
   Argument 2 -- The spatial radius of the search window (integer)\n\
   Argument 3 -- The range radius of the search window (double)\n\
   Argument 4 -- The minimum point density of a region in the segmented image (integer)\n\
   Argument 5 -- The speed up level (integer, 0: NO; 1: MEDIUM; 2: HIGH)\n\
   \n\
   Return value: 3-tuple\n\
   Element 1 -- Image (Numpy array) where the color (or grayscale) of the\n\
                regions is the mean value of the pixels belonging to a region.\n\
   Element 2 -- Image (2-D Numpy array, 32 unsigned bits per element) where a\n\
                pixel value correspond to the region number the pixel belongs to.\n\
   Element 3 -- The number of regions found by the mean shift algorithm.\n\
   \n\
   ";


// ***************************************************************************
// Declaration of Python module functions
// ***************************************************************************

// Module methods definition
static PyMethodDef pmsMethods[] = {
  {"segment", segment, METH_VARARGS, pmsSegmentDoc},
  {NULL, NULL}
};


// ***************************************************************************
// Python Module initialization function(s)
// ***************************************************************************

#if PY_MAJOR_VERSION < 3

// Module initialization function for Python 2.x
PyMODINIT_FUNC init_pymeanshift()
{
  PyObject* modulePMS = Py_InitModule3("_pymeanshift", pmsMethods, pmsDoc);
  PyModule_AddIntConstant(modulePMS, "SPEEDUP_NO", NO_SPEEDUP);
  PyModule_AddIntConstant(modulePMS, "SPEEDUP_MEDIUM", MED_SPEEDUP);
  PyModule_AddIntConstant(modulePMS, "SPEEDUP_HIGH", HIGH_SPEEDUP);
  import_array();
}  

#else

// Module definition structure for Python 3.x

struct PyModuleDef moduleDef =
{
  PyModuleDef_HEAD_INIT,
  "_pymeanshift",
  pmsDoc,
  -1,
  pmsMethods,
  NULL,
  NULL,
  NULL,
  NULL
};

// Module initialization function for Python 3.x
PyMODINIT_FUNC PyInit__pymeanshift()
{
  import_array();

  PyObject* modulePMS = PyModule_Create(&moduleDef);
  PyModule_AddIntConstant(modulePMS, "SPEEDUP_NO", NO_SPEEDUP);
  PyModule_AddIntConstant(modulePMS, "SPEEDUP_MEDIUM", MED_SPEEDUP);
  PyModule_AddIntConstant(modulePMS, "SPEEDUP_HIGH", HIGH_SPEEDUP);

  return modulePMS;
}

#endif // PY_MAJOR_VERSION < 3
