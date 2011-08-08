#!/usr/bin/env python

from distutils.core import setup, Extension

import platform
import os

if platform.system()=='Windows':
  if not os.environ.has_key('OPENCV_DIR'):
    raise Exception('Cannot find the environment variable OPENCV_DIR. Please set the environment variable OPENCV_DIR to the OpenCV base directory.')

  ocv_dir = os.environ['OPENCV_DIR']
  if not os.path.exists(ocv_dir):
    raise Exception('The path "%s" specified in the environment variable OPENCV_DIR does not exist.' % (ocv_dir,) )

  ocv_inc_dir = [os.path.join(ocv_dir, 'include')]
  ocv_lib_dir = [os.path.join(ocv_dir, 'lib')]

  if os.path.exists(os.path.join(ocv_lib_dir[0], 'opencv_core230.lib')) and os.path.exists(os.path.join(ocv_lib_dir[0], 'opencv_imgproc230.lib')):
    ocv_libs = ['opencv_core230', 'opencv_imgproc230']
  elif os.path.exists(os.path.join(ocv_lib_dir[0], 'opencv_core220.lib')) and os.path.exists(os.path.join(ocv_lib_dir[0], 'opencv_imgproc220.lib')):
    ocv_libs = ['opencv_core220', 'opencv_imgproc220']
  elif os.path.exists(os.path.join(ocv_lib_dir[0], 'cv210.lib')) and os.path.exists(os.path.join(ocv_lib_dir[0], 'cxcore210.lib')):
    ocv_libs = ['cv210', 'cxcore210']
  else:
    raise Exception('Cannot find OpenCV import librairies (.lib) in directory %s' % (ocv_lib_dir[0],))
else:
  ocv_inc_dir = ['/usr/local/include']
  ocv_lib_dir = ['/usr/local/lib']
  ocv_libs = ['opencv_core', 'opencv_imgproc']



setup(name='pymeanshift',
      version='0.1.1',
      description='Python Module for Mean Shift Image Segmentation using OpenCV',
      long_description='C++ extension for segmenting images with the mean shift algorithm. The supported image types are CvMat and IplImage from the official OpenCV Python interface.',
      author='Frederic Jean',
      author_email='googlecode@fredericjean.ca',
      url='http://pymeanshift.googlecode.com',
      license='GNU General Public License (GPL) version 3',
      platforms=['Linux, Windows, MacOS X'],
      keywords=['image segmentation', 'mean shift', 'opencv', 'C++'],
      ext_modules=[Extension('_pymeanshift',
                             ['ms.cpp','msImageProcessor.cpp','rlist.cpp','RAList.cpp','pymeanshift.cpp','pymeanshift_wrap.cxx'],
                             depends=['ms.h', 'msImageProcessor.h', 'pymeanshift.hpp', 'RAList.h', 'rlist.h', 'tdef.h'],
                             language='c++',
                             include_dirs=ocv_inc_dir,
                             library_dirs=ocv_lib_dir,
                             libraries=ocv_libs
                            )],
      py_modules=['pymeanshift'],
      
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Other Environment',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: GNU General Public License (GPL)',
                   'Natural Language :: English',
                   'Operating System :: POSIX :: Linux',
                   'Operating System :: Microsoft :: Windows',
                   'Operating System :: MacOS :: MacOS X',
                   'Programming Language :: C++',
                   'Programming Language :: Python :: 2.7',
                   'Topic :: Scientific/Engineering :: Image Recognition',
                   'Topic :: Scientific/Engineering :: Artificial Intelligence'                   
                  ]                  
     )

