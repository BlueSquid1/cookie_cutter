import cv2
import numpy as np
import glob
import os

# values to adjust
threshold_margin = 5
erode_kernal_size = 2
erode_iterations = 2
dilute_kernal_size = 5
dilute_interations = 3

class cookieCutter:
    def readImage(self, imagePath):
        img_bgr = cv2.imread(imagePath)
        blue,green,red = cv2.split(img_bgr)
        img_rgb = cv2.merge((red,green,blue))
        return img_rgb

    # def max_index(self, array):
    #     max_value = max(array)
    #     for i in range(len(array)):
    #         if array[i] == max_value:
    #             return i
    #     return 0

    # def process_image(self, image_grey):
    #     # High pass filter
    #     sigma = 30
    #     image_grey = image_grey - cv2.GaussianBlur(image_grey, (0,0), sigma) + 127

    #     cv2.imshow(image_path, img_bgr)
    #     cv2.waitKey(0)

    #     # Find global background colour by finding the most frequently used background colour
    #     histogram = cv2.calcHist(image_grey, [0], None, [256], [0,255])
    #     common_grey = max_index(histogram)
        
    #     # apply threshold at the common grey
    #     result, img_bw = cv2.threshold(image_grey, common_grey - threshold_margin, 255, cv2.THRESH_BINARY_INV)

    #     # Dilate picture slightly to rejoin any loosely disconnected blobs
    #     dilue_kernal = np.ones((dilute_kernal_size, dilute_kernal_size), np.uint8)
    #     erode_kernal = np.ones((erode_kernal_size, erode_kernal_size), np.uint8)
    #     img_erosion = cv2.erode(img_bw, erode_kernal, iterations=erode_iterations)
    #     output_img_bw = cv2.dilate(img_erosion, dilue_kernal, iterations=dilute_interations)

    #     return output_img_bw

    # def reveal_blob(self, img_bw):
    #     contours, hierarchy = cv2.findContours(img_bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    #     biggest_blob = max(contours, key = cv2.contourArea)

    #     return biggest_blob

    # def save_picture(self, path, image):
    #     cv2.imwrite(path, image)

# def main():
#     # Get a list of all the .tif files to load
#     root_image_path = os.path.abspath(root_image_folder)
#     image_paths = glob.glob(root_image_path + "/*.tif")

#     # Create output folder if it doesn't already exist
#     os.makedirs(root_output_folder, exist_ok=True)

#     for image_path in image_paths:
#         # Load image as greyscale
#         img_bgr = cv2.imread(image_path)
#         img_grey = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

#         # Convert to binary image
#         img_bw = process_image(img_grey)

#         # draw blob onto a blank binary image
#         blob = reveal_blob(img_bw)
#         output_bw = np.zeros(img_bw.shape, np.uint8)
#         cv2.drawContours(output_bw, [blob], -1, (255,255,255), -1)

#         # Save blob to a file
#         save_picture(root_output_folder + "/" + os.path.basename(image_path), output_bw)

#         # Display trace overlay over original to performance can be measured
#         cv2.drawContours(img_bgr, [blob], -1, (0,255,0), 2)
#         cv2.imshow(image_path, img_bgr)
#         cv2.waitKey(0)