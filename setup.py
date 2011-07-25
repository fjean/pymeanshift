#!/usr/bin/env python

from distutils.core import setup, Extension

setup(name='pymeanshift',
      version='0.1.0',
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
                             language='c++',
                             include_dirs=['/usr/local/include/opencv'],
                             library_dirs=['/usr/local/lib'],
                             libraries=['opencv_core', 'opencv_imgproc']                             
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

