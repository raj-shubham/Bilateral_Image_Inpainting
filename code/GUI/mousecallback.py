import sys
import argparse

master_working_path = "/Users/mymac/Desktop/Assignments/DIP-Assignments/Project/code/"
sys.path.append(master_working_path)
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from common import common_cv
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from logs import syslogger as logger
from config import config

config_json = config.open_config_file()


is_drawing = False # true if mouse is pressed
ix,iy = -1,-1
image_global_points = set()

def draw_freehand(event,x,y,flags,param):
    """
    input:
        event : captures every mouse event
        x,y   : x,y coordinate of pixel under curser
    action:
        adds the selected damaged pixel coordinates in a set
        set is used to avoid redundant values

    """
    global ix,iy,is_drawing
    if event == cv.EVENT_LBUTTONDOWN:
        logger.debug("down")
        is_drawing = True
        #ix,iy = x,y
    elif event == cv.EVENT_MOUSEMOVE:
        logger.debug("move")
        if is_drawing == True:
            cv.circle(img,(x,y),1,(0,0,255),-1)
    elif event == cv.EVENT_LBUTTONUP:
        is_drawing = False
    if is_drawing:
        image_global_points.add((y,x))

def get_subimages(image_matrix, points_list, image_width):
    """
    input:
        image_matrix : input image array
        points_list  : list of damaged points
        image_width  : neighbourhood to take around points
    output:
        returns area around the selected damaged pixels to be inpainted
    """
    image_list = list()
    if 0==image_width%2:
        image_width +=1
    r = image_width//2
    logger.info("Calculated neighbourhood range of chosen pixel")
    for point in points_list:
        image_list.append([image_matrix[point[0]-r : point[0]+r+1,point[1]-r : point[1]+r+1],point])
    logger.info("Subimages collected successfully")
    return image_list

def put_subimages(image_matrix, subimage_list, image_width):
    """
    input:
        image_matrix : input image array
        subimage_list: list of inpainted regions of image
        image_width  : neighbourhood to take around points
    output:
        inpainted images with restored damaged regions
    """
    org_image = np.copy(image_matrix)
    r = image_width//2
    for subimages in subimage_list:
        point = subimages[1]
        subimage = subimages[0]
        image_matrix[point[0]-r : point[0]+r+1,point[1]-r : point[1]+r+1] = subimage
    logger.info("Subimages merged successfully in the base image")
    return image_matrix

def process_subimage(subimage_list,kernel_width,sigma_range,sigma_domain,filter_itr):
    """
    input:
        kernel_width : size of kernel
        subimage_list: list of inpainted regions of image
        sigma_range  : variation across intensity
        sigma_domain : variation across distance
        filter_itr   : inpainting iterations on damaged regions
    output:
        inpainted subimages with restored damaged regions
    """
    logger.debug("processing damaged regions")
    for element in range(len(subimage_list)):
        subimage = subimage_list[element][0]
        for i in range(filter_itr):
            subimage = common_cv.apply_bilateral_filter(subimage,kernel_width,sigma_range,sigma_domain)
        subimage_list[element][0] = subimage
    logger.info("Processing done for damaged regions")
    return subimage_list   

def get_image_path():
    """
    gui to select input image
    """
    Tk().withdraw() 
    filepath = askopenfilename() 
    logger.info("Image chosen for inpainting : "+filepath)
    return filepath

my_parser = argparse.ArgumentParser(description='Performs inpainting \n \
    eg. python3 mousecallback.py 20 5 10.0 0.5 2',add_help=True)
my_parser.add_argument('image_width',metavar='image_width',type=int,help='neighbourhood range of image (type: int ; eg. 20)')
my_parser.add_argument('kernel_width',metavar='kernel_width',type=int,help='kernel size (odd number) (type: int ; eg. 5)')
my_parser.add_argument('sigma_range',metavar='sigma_range',type=float,help='variation across intensity (type: float ; eg. 10.0)')
my_parser.add_argument('sigma_domain',metavar='sigma_domain',type=float,help='variation across distance (type: float ; eg. 0.5)')
my_parser.add_argument('filter_itr',metavar='filter_itr',type=int,help='iterations over damaged regions (type: int ; eg. 2)')

# Execute the parse_args() method
args = my_parser.parse_args()

image_path = get_image_path()
img_mat = common_cv.read_image(image_path,"COLOR")
img = np.copy(img_mat)
img_for_subimages = np.copy(img)
cv.namedWindow('image')
cv.setMouseCallback('image',draw_freehand)

while(1):
    cv.imshow('image',img)
    key_val = cv.waitKey(1)
    if key_val == ord('y'):
        break
cv.destroyAllWindows()

image_width = args.image_width or  30
kernel_width = args.kernel_width or  5
sigma_range = args.sigma_range or  25.0
sigma_domain = args.sigma_domain or  0.5
filter_itr = args.filter_itr or  5
subimage_list = get_subimages(img_for_subimages, image_global_points, image_width)
processed_subimage_list = process_subimage(subimage_list,kernel_width,sigma_range,sigma_domain,filter_itr)
processed_image = put_subimages(img_for_subimages, processed_subimage_list, image_width)
print('Image Processed')
cv.imshow('Image',processed_image)
cv.waitKey(0)
cv.destroyAllWindows()
plt.subplot(121)
plt.imshow(cv.cvtColor(img_mat, cv.COLOR_BGR2RGB))
plt.subplot(122)
plt.imshow(cv.cvtColor(processed_image, cv.COLOR_BGR2RGB))
plt.show()
