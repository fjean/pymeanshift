#!/usr/bin/env python

from distutils.core import setup
from distutils.core import Extension
import sys

try:
    import numpy as np
except ImportError as exc:
    sys.stderr.write("Error: Failed to import Numpy ({}). Please check that Numpy is installed on your system.".format(exc))

setup(name='pymeanshift',
      version='0.2.0',
      description='Python Extension for Mean Shift Image Segmentation',
      long_description='C++ extension for segmenting images with the mean shift algorithm. Segmentation can be performed on color or graysalve images represented by Numpy arrays.',
      author='Frederic Jean',
      author_email='googlecode@fredericjean.ca',
      url='http://pymeanshift.googlecode.com',
      license='GNU General Public License (GPL) version 3',
      platforms=['Linux, Windows, MacOS X'],
      keywords=['image segmentation', 'mean shift', 'numpy', 'C++'],
      ext_modules=[Extension('_pymeanshift',
                             ['ms.cpp','msImageProcessor.cpp','rlist.cpp','RAList.cpp','pymeanshift.cpp'],
                             depends=['ms.h', 'msImageProcessor.h', 'RAList.h', 'rlist.h', 'tdef.h'],
                             language='c++',
                             include_dirs=[np.get_include()]
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

