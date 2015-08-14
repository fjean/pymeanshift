PYMEANSHIFT
Python Module for Mean Shift Image Segmentation
By Frederic Jean, 2012

Table of Contents:

  1. Prerequisites
  2. Install
  3. Implementation Notes

------------------------------------------------------------------------------
1. PREREQUISITES
------------------------------------------------------------------------------

  See https://github.com/fjean/pymeanshift/wiki/Install for the lastest
  prerequisites.

  You need to have the following installed on your computer:
     
  * Python development headers and Numpy.
      - On Debian-based (ex. Ubuntu) Linux distributions, this is provided by
        the package python-dev; 
      - On Redhat-based Linux distributions (ex. Fedora), this is provided by
        the package python-devel; 
      - On Windows, the Python headers can be installed during the Python
        installation process. 
        
  * (Windows only): Visual C++ 2008 Express Edition with SP1.
    (http://www.microsoft.com/visualstudio/en-us/products/2008-editions/express)


------------------------------------------------------------------------------
2. INSTALL
------------------------------------------------------------------------------

  See https://github.com/fjean/pymeanshift/wiki/Install for the lastest
  install instructions.

  * The Python extension can be compiled as follows:

    - For Linux and Mac OSX (in a terminal window):
    ./setup.py build

    - For Windows (command prompt):
    python setup.py build

  * The wrapper module and the extension can be installed as follows
    (you might need admin privileges):

    - For Linux and Mac OSX (in a terminal window):
    sudo ./setup.py install

    - For Windows (command prompt):
    python setup.py install

    Add the option "--user" if you only want to install it for
    the current user.
    
  * If everything went fine, you should be able to import the pymeanshift
    module in your Python code. The module consists in one function named
    "segment" and a class named "Segmenter".

    In your Python code:
    import pymeanshift as pms


------------------------------------------------------------------------------
3. IMPLEMENTATION NOTES
------------------------------------------------------------------------------

  See https://github.com/fjean/pymeanshift/wiki/ImplementationNotes for the
  lastest implementation notes.

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
