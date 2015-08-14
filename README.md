**PyMeanShift** is a Python module/extension for segmenting images using the mean shift algorithm. The PyMeanShift module/extension has been designed to use Numpy arrays, which makes it compatible with the OpenCV module "cv2" and the PIL module.

The mean shift algorithm and its C++ implementation are by Chris M. Christoudias and Bogdan Georgescu. The PyMeanShift extension provides a Python interface  to the meanshift C++ implementation using Numpy arrays.  For more information, see the wiki page on [implementation notes](ImplementationNotes.md).

Installation instructions can be found on the [Install](Install.md) wiki page. Examples of mean shift image segmentation with different parameters values are presented on the [Examples](Examples.md) wiki page. Bugs report can be submitted using the [Issues](http://code.google.com/p/pymeanshift/issues/list) page.


Code example with OpenCV:
```
import cv2
import pymeanshift as pms

original_image = cv2.imread("example.png")

(segmented_image, labels_image, number_regions) = pms.segment(original_image, spatial_radius=6, 
                                                              range_radius=4.5, min_density=50)
```

Code example with PIL:
```
from PIL import Image
import pymeanshift as pms

original_image = Image.open("example.png")

(segmented_image, labels_image, number_regions) = pms.segment(original_image, spatial_radius=6, 
                                                              range_radius=4.5, min_density=50)
```

Code example using the Segmenter class:
```
import pymeanshift as pms

# [...]
# load image in "original_image"
# [...]

my_segmenter = pms.Segmenter()

my_segmenter.spatial_radius = 6
my_segmenter.range_radius = 4.5
my_segmenter.min_density = 50

(segmented_image, labels_image, number_regions) = my_segmenter(original_image)
```

<table cellpadding='0' border='0' align='left' cellspacing='0' width='75%'>
<blockquote><tr cellpadding='0' cellspacing='0'>
<blockquote><td cellpadding='0' align='center' cellspacing='0'><b>Original image</b></td>
<td cellpadding='0' align='center' cellspacing='0'><b>Segmented image</b></td>
</blockquote></tr>
<tr cellpadding='0' cellspacing='0'>
<blockquote><td cellpadding='0' align='center' cellspacing='0' valign='top'>
<blockquote><img src='http://wiki.pymeanshift.googlecode.com/hg/Examples.img/example-orig.jpg' border='0' width='360px' />
</blockquote></td>
<td cellpadding='0' align='center' cellspacing='0'>
<blockquote><img src='http://wiki.pymeanshift.googlecode.com/hg/Examples.img/example-6-4_5-50.png' border='0' width='360px' />
</blockquote></td>
</blockquote></tr>
</table>