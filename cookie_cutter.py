import cv2
import numpy as np

# values to adjust

class Settings:
    enableHighFilterPass = False
    highFilterSigma = 0
    thresholdOffset = 0
    enableErosion = False
    erosionKernel = 0
    erosionIter = 0
    enableDilation = False
    dilationKernel = 0
    dilationIter = 0

class cookieCutter:
    cachedBlob = None
    cachedImagePath = ""
    cachedImageSize = ()

    def readImage(self, imagePath):
        imgBgr = cv2.imread(imagePath)
        blue,green,red = cv2.split(imgBgr)
        imgRgb = cv2.merge((red,green,blue))
        return imgRgb

    def generatePreview(self, imagePath, settings):
        imgRgb = self.readImage(imagePath)

        imgGrey = cv2.cvtColor(imgRgb, cv2.COLOR_RGB2GRAY)

        # Convert to binary image
        imgBw = self._processImage(imgGrey, settings)

        # draw blob onto a blank binary image
        blob = self._revealBlob(imgBw)

        # Cache results
        self.cachedBlob = blob
        self.cachedImagePath = imagePath
        self.cachedImageSize = imgBw.shape

        # Display trace overlay over original to performance can be measured
        cv2.drawContours(imgRgb, [blob], -1, (0,255,0), 2)
        return imgRgb

    def generateAndSaveBinaryImage(self, inputPath, outputPath, settings):
        # Normally generate a binary image after preview. Use cached blob if imagePath matches cache
        blob = None
        imageSize = ()
        if self.cachedImagePath == inputPath:
            blob = self.cachedBlob
            imageSize = self.cachedImageSize
        else:
            # Not cached. Need to work out from first principles
            imgRgb = self.readImage(inputPath)
            imgGrey = cv2.cvtColor(imgRgb, cv2.COLOR_RGB2GRAY)
            imgBw = self._processImage(imgGrey, settings)
            imageSize = imgBw.shape
            blob = self._revealBlob(imgBw)

        # Overlay on BW image
        outputBw = np.zeros(imageSize, np.uint8)
        cv2.drawContours(outputBw, [blob], -1, (255,255,255), -1)
        self.savePicture(outputPath, outputBw)

    def _processImage(self, imageGrey, settings):
        if settings.enableHighFilterPass:
            # High pass filter
            sigma = settings.highFilterSigma
            imageGrey = imageGrey - cv2.GaussianBlur(imageGrey, (0,0), sigma) + 127

        # Find global background colour by finding the most frequently used background colour
        histogram = cv2.calcHist(imageGrey, [0], None, [256], [0,255])
        commonGrey = self._maxIndex(histogram)
        
        # apply threshold at the common grey
        thresholdMargin = settings.thresholdOffset
        result, imgBw = cv2.threshold(imageGrey, commonGrey - thresholdMargin, 255, cv2.THRESH_BINARY_INV)

        # Erode picture to remove losely attaching blobs
        if settings.enableErosion:
            erodeKernal = np.ones((settings.erosionKernel, settings.erosionKernel), np.uint8)
            imgBw = cv2.erode(imgBw, erodeKernal, iterations=settings.erosionIter)

        # Dilate picture slightly to close of all open areas
        if settings.enableDilation:
            dilueKernal = np.ones((settings.dilationKernel, settings.dilationKernel), np.uint8)
            imgBw = cv2.dilate(imgBw, dilueKernal, iterations=settings.dilationIter)

        return imgBw

    def _maxIndex(self, array):
        maxValue = max(array)
        for i in range(len(array)):
            if array[i] == maxValue:
                return i
        return 0

    def _revealBlob(self, imgBw):
        contours, hierarchy = cv2.findContours(imgBw, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        biggestBlob = max(contours, key = cv2.contourArea)

        return biggestBlob

    def savePicture(self, path, image):
        cv2.imwrite(path, image)