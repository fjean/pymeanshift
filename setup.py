#!/usr/bin/env python
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

from distutils.core import setup
from distutils.core import Extension
import re

# Check for Numpy
try:
    import numpy as np
except ImportError as exc:
    raise RuntimeError("Error: Failed to import Numpy ({}). Please check that Numpy is installed on your system.".format(exc))

# Parse package version
version_file = 'pymeanshift.py'
module_version = None
for line in open(version_file, "rt"):
    result = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", line, re.M)
    if result:
        module_version = result.group(1)
        break 
if module_version is None:
    raise RuntimeError("Error: Cannot find module version in file {}".format(version_file))

# Setup    
setup(name='pymeanshift',
      version=module_version,
      description='Python Extension for Mean Shift Image Segmentation',
      long_description='C++ extension for segmenting images with the mean shift algorithm. Segmentation can be performed on color or grayscale images represented by Numpy arrays.',
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
      
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: GNU General Public License (GPL)',
                   'Natural Language :: English',
                   'Operating System :: POSIX :: Linux',
                   'Operating System :: Microsoft :: Windows',
                   'Operating System :: MacOS :: MacOS X',
                   'Programming Language :: C++',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.2',
                   'Topic :: Scientific/Engineering :: Image Recognition'                 
                  ]                  
     )
