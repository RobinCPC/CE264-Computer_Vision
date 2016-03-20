# CE264-Computer Vision
Repository for project code of CE264 Computer Vision

## Application of Hand-gesture Recognition Technology Using OpenCV


The following is draft flow chart of porject program:

![flow chart](./program_flow.png)

Some material for each subtasks

- [x] Row Image Input

   * [GUI feature in OpenCV](http://docs.opencv.org/3.0-last-rst/doc/py_tutorials/py_gui/py_table_of_contents_gui/py_table_of_contents_gui.html#py-table-of-content-gui)

- [x] Blur, Skin Detection, Morphology, Background Subtraction

    * [Change BGR to HSV or YCrCb](http://docs.opencv.org/3.0-last-rst/doc/py_tutorials/py_imgproc/py_colorspaces/py_colorspaces.html#converting-colorspaces)
    * [Do medianBlur](http://docs.opencv.org/3.0-last-rst/doc/py_tutorials/py_imgproc/py_filtering/py_filtering.html#filtering)
    * [Do erode and dilate](http://docs.opencv.org/3.0-last-rst/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html#morphological-ops)

- [x] Hand Contour Extraction

    * [Draw Contour and Find Convex Hull or Convexity Defects](http://docs.opencv.org/3.0-last-rst/doc/py_tutorials/py_imgproc/py_contours/py_table_of_contents_contours/py_table_of_contents_contours.html#table-of-content-contours)

- [X] Gesture Recognition

    * [Find out how many fingers show up](http://docs.opencv.org/3.0-last-rst/doc/py_tutorials/py_imgproc/py_contours/py_contours_more_functions/py_contours_more_functions.html#contours-more-functions)

- [x] Hand Position Tracking

    * [Dynamically change center of ROI] (http://docs.opencv.org/3.0-last-rst/doc/py_tutorials/py_imgproc/py_contours/py_contour_features/py_contour_features.html#contour-features) 

- [x] Input Control

    * [PyAutoGUI](http://pyautogui.readthedocs.org/en/latest/cheatsheet.html)
    * [PyUserInput](https://github.com/SavinaRoja/PyUserInput)
    
    > Note: PyAutoGUI work well in Woindows system for me. Ubuntu: got issue (invisible cursor move)

    For install PyAutoGUI on Linux (for python 2.x):
    
    ``` bash
    # install x-lib and scrot (pip not work for me)
    $ sudo apt-get install  python-xlib
    $ sudo apt-get install scrot
    
    # skip install python-tk and python2.x-dev (already had)
    # instal Pyautogui
    $ sudo apt-get install python-pip # if don't have pip
    $ sudo pip install pyautogui
    ```
    
    For install PyAutoGui on Window (for python 2.x):
    Open cmd.exe
    ```
    # Install pillow first (PIL module may cause error during install)
    C:\Python27\Scripts\pip.exe install pillow  
    C:\Python27\Scripts\pip.exe install pyautogui
    ```
    Turn off Windows UAC


## Reference

* Hui-Shyong Yeo; Byung-Gook Lee; Hyotaek Lim, "Hand tracking and gesture recognition system for 
  human-computer interaction using low-cost hardware", Multimedia Tools and Applications, Vol. 74, 
  Issue 8, Apr. 2015, On page(s) 2687-2715.

* http://vipulsharma20.blogspot.com/2015/03/gesture-recognition-using-opencv-python.html

