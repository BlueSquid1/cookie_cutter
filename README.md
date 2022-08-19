# cookie_cutter

![cookie_cutter_mac](https://user-images.githubusercontent.com/9015401/185598653-b05dc18a-2066-4aee-9734-2ebc417527ab.png)

![cookie_cutter_windows](https://user-images.githubusercontent.com/9015401/185598122-a42ee5c6-8c8d-488e-ba59-3f51636259eb.PNG)

## Description
This is a basic program that can track the shape of a blob in a photo. The traced contours can then be saved to a black and white mask image.

## Supported file formats
- png
- jpeg
- tif
- bmp

## Settings that can be modified
1. high filter pass
    - enable - sharpens corners so they are easier to detect.
    - size - lower reduce edge detection tolerance but if it's too low it will start to miss the edges of a cell.
1. brightness threshold 
    - amount - lower will include more objects but could introduce false positives.
1. errosion 
    - enable - removes pixels at threshold border. Useful to detach false positives/noise near a cell's edge.
    - kernal size - how many pixels to delete for each errosion iteration. Large values will errode more but will also reduce resolution of image.
    - iterations - how many times to perform the errosion operation. Large values will errode more but will take longer.
1. dilution 
    - enable - add pixels at threshold border. Useful to close small gaps between contours.
    - kernal size - how many pixels to add for each errosion iteration. Large values will add more but will also reduce resolution of image.
    - iterations - how many times to perform the dilution operation. Large values will dilute more but will take longer.

## Building from source

### Requirements
- pip3 install pyinstaller

### Build instructions
```
pyinstaller -F main.py -n cookie_cutter
```
