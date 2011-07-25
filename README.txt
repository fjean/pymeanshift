PYMEANSHIFT
Python Module for Mean Shift Image Segmentation using OpenCV
By Frederic Jean, 2011


Table of Contents:

  1. Prerequisites
  2. Install
  3. Implementation Notes

------------------------------------------------------------------------------
1. PREREQUISITES
------------------------------------------------------------------------------

  You need to have the following installed on your computer:
  
  * OpenCV libraries and headers version 2.3, with the Python module.
      See http://opencv.willowgarage.com/ 
    
  * Python development headers.
      On Ubuntu, this is the package named "python-dev"

  * (Optional) If you want to regenerate the Python wrapper, you will need
    Swig.
      In Ubuntu, this is the package named "swig"


------------------------------------------------------------------------------
2. INSTALL
------------------------------------------------------------------------------

  * First, if OpenCV is not installed in /usr or /usr/local, you have to
    modify the file setup.cfg to specify the include directory and the library
    directory as follows:

    [build_ext]
    include_dirs = /usr/local/include/opencv
    library_dirs = /usr/local/lib

  * Next, you have to compile the Python extension as follows:

    - For Linux and Mac OSX (in a terminal window):
    ./setup.py build

    - For Windows (command prompt): **NOT TESTED**
    python setup.py build

  * Finally, the extension can be installed as follows (you will need admin
    privileges):

    - For Linux and Mac OSX (in a terminal window):
    sudo ./setup.py install

    - For Windows (command prompt): **NOT TESTED**
    python setup.py install

  * If everything went fine, you should be able to import the pymeanshift
    module in your Python code. The module consists in one function named
    "segmentMeanShift".

    In your Python code:
    import pymeanshift as pms

 
------------------------------------------------------------------------------
3. IMPLEMENTATION NOTES
------------------------------------------------------------------------------

  The mean shift algorithm and its C++ implementation are by
  Chris M. Christoudias and Bogdan Georgescu. This Python module merely
  provides the "glue" that is necessary in order to use the C++ implementation
  with OpenCV in Python.

  The authors' C++ implementation is located in the following files:

    ms.h
    ms.cpp
    msImageProcessor.cpp
    msImageProcessor.h
    RAList.cpp
    RAList.h
    rlist.cpp
    rlist.h
    tdef.h

    See the file MSReadme.txt for more information. These files were obtained
    from the Blepo computer vision library.
    Blepo is available at http://www.ces.clemson.edu/~stb/blepo/

  For details on the algorithm, see the following paper:
  D. Comanicu, P. Meer: "Mean shift: A robust approach toward feature space
  analysis". IEEE Transactions on Pattern Analysis and Machine Intelligence,
  vol. 24, no. 5, May 2002.
  
  The implementation of pymeanshift also requires some code from the OpenCV
  project (code for binding the C/C++ OpenCV objects to Python Objects). This
  code is located in the Swig interface file pymeanshift.i.
  
