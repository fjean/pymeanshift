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
 
%module pymeanshift
%{
  #include "pymeanshift.hpp"
%}

%include exception.i
%{    
  #include <opencv/cv.h>
  #include <Python.h>  

  // *******************************************************************************
  // This code comes from the OpenCV Python binding: modules/python/src1/cv.cpp
  //
  static int failmsg(const char *fmt, ...)
  {
    char str[1000];

    va_list ap;
    va_start(ap, fmt);
    vsnprintf(str, sizeof(str), fmt, ap);
    va_end(ap);

    PyErr_SetString(PyExc_TypeError, str);
    return 0;
  }

  struct cvmat_t {
    PyObject_HEAD
    CvMat *a;
    PyObject *data;
    size_t offset;
  };

  static int is_cvmat(PyObject *o)
  {
    return (strcmp(o->ob_type->tp_name,"cv.cvmat") == 0);
  }

  static int convert_to_CvMat(PyObject *o, CvMat **dst, const char *name)
  {
    cvmat_t *m = (cvmat_t*)o;
    void *buffer;
    Py_ssize_t buffer_len;

    if (!is_cvmat(o)) {
      #if !PYTHON_USE_NUMPY
        return failmsg("Argument '%s' must be CvMat", name);
      #else
      PyObject *asmat = fromarray(o, 0);
      if (asmat == NULL)
        return failmsg("Argument '%s' must be CvMat", name);
        // now have the array obect as a cvmat, can use regular conversion
      return convert_to_CvMat(asmat, dst, name);
      #endif
    } else {
      m->a->refcount = NULL;
      if (m->data && PyString_Check(m->data)) {
        assert(cvGetErrStatus() == 0);
        char *ptr = PyString_AsString(m->data) + m->offset;
        cvSetData(m->a, ptr, m->a->step);
        assert(cvGetErrStatus() == 0);
        *dst = m->a;
        return 1;
      } else if (m->data && PyObject_AsWriteBuffer(m->data, &buffer, &buffer_len) == 0) {
        cvSetData(m->a, (void*)((char*)buffer + m->offset), m->a->step);
        assert(cvGetErrStatus() == 0);
        *dst = m->a;
        return 1;
      } else if (m->data && m->a->data.ptr){
        *dst = m->a;
        return 1;
      }
      else {
        return failmsg("CvMat argument '%s' has no data", name);
      }
    }
  }
  // *******************************************************************************
  
%}


%typemap(in) CvMat *
{
  if (!convert_to_CvMat($input, &($1), ""))
  {
    SWIG_exception( SWIG_TypeError, "%%typemap: could not convert input argument to an CvMat");
  }
}


%typemap(typecheck) CvMat *
{
  $1 = is_cvmat($input) ? 1 : 0;
}


%rename(_segmentMeanShiftImpl) segmentMeanShiftImpl;
int segmentMeanShiftImpl(const CvMat* inInputImage, CvMat* outMeanColorLabelImage, CvMat* outLabels, int inSigmaS, float inSigmaR, unsigned int inMinRegion, unsigned int inSpeedupLevel);


%pythoncode
%{

  # Exceptions definition
  class OpenCVNotFound(Exception):
    pass

  class BadParameterValue(Exception):
    pass

  class ImplementationError(Exception):
    pass

  class BadImageType(Exception):
    pass


  try:
    import cv
  except:
    raise OpenCVNotFound("Cannot import OpenCV Python module.")


  def segmentMeanShift(inputImage, sigmaS=6, sigmaR=4.5, minRegion=300, speedUpLevel=2):
    '''
    Segmentation of an image (grayscale or color) using the mean shift algorithm.
    
    Return a 3-tuple (colorLabelsImage, labelsImg, nbRegions).
      - colorLabelsImage is the segmented image with each region colored as the
        mean color value of its pixels.
      - labelsImg is an image where a pixel value represents the region it belongs to.
        This image is one channel, 32 bits per pixel.
      - nbRegions is the number of regions found in the image.

    This function can take CvMat or IplImage as an input image. Th output images will
    be of the same type than the input image. If IplImage is used, be aware that the
    output IplImage will not be aligned on memory boundary. This is not a problem
    as long as the OpenCV functions are used to read/write pixel values in these images.

    The mean shift algorithm and its implementation in C++ are by
    Chris M. Christoudias and Bogdan Georgescu. This Python module provides the "glue"
    that is necessary in order to use the C++ implementation with OpenCV in Python.

    For details on the algorithm:
    D. Comanicu, P. Meer: "Mean shift: A robust approach toward feature space analysis".
    IEEE Transactions on Pattern Analysis and Machine Intelligence, May 2002.
    
    '''
  
    if sigmaS < 0:
      raise BadParameterValue("Spatial radius must be greater or equal to zero")
    if sigmaR < 0:
      raise BadParameterValue("Range radius must be greater or equal to zero")
    if minRegion < 0:
      raise BadParameterValue("Minimum region must be greater or equal to zero")
    if speedUpLevel < 0 or speedUpLevel > 2:
      raise BadParameterValue("Speedup level must be 0 (no speedup), 1 (medium speedup), or 2 (high speedup)")

    if isinstance(inputImage, cv.cvmat):
      # If input image is a CvMat, then create outputs image as CvMat too      
      inputImageMat = inputImage
      colorImageMat = cv.CreateMat(inputImageMat.rows, inputImageMat.cols, inputImageMat.type)
      labelImageMat = cv.CreateMat(inputImageMat.rows, inputImageMat.cols, cv.CV_32SC1)
      colorImage = colorImageMat
      labelImage = labelImageMat
    elif isinstance(inputImage, cv.iplimage):
      # If input image is an IplImage, then create outputs image as IplImage too
      # Input image must be copied into a CvMat structure since IplImage
      # might be aligned on memory boundaries, which is a problem for the mean shift algorithm implementation
      inputImageMatTmp = cv.GetMat(inputImage)
      inputImageMat = cv.CreateMat(inputImageMatTmp.rows, inputImageMatTmp.cols, inputImageMatTmp.type)
      cv.Copy(inputImageMatTmp, inputImageMat)
      
      colorImageMat = cv.CreateMat(inputImageMat.rows, inputImageMat.cols, inputImageMat.type)
      labelImageMat = cv.CreateMat(inputImageMat.rows, inputImageMat.cols, cv.CV_32SC1)
      colorImage = cv.GetImage(colorImageMat)
      labelImage = cv.GetImage(labelImageMat)
    else:
      raise BadImageType("Input image must be either a CvMat or an IplImage")
    
    nbRegion = _segmentMeanShiftImpl(inputImageMat, colorImageMat, labelImageMat, sigmaS, sigmaR, minRegion, speedUpLevel)

    if nbRegion < 0:
      raise ImplementationError("An error occured in the mean shift C implementation (This should not happen)")

    return (colorImage, labelImage, nbRegion)

%}

