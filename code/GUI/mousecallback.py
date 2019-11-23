import sys

master_working_path = "/Users/mymac/Desktop/Assignments/DIP-Assignments/Project/code/"
sys.path.append(master_working_path)
print(sys.path)
import numpy as np
import cv2 as cv
from common import common_cv
from logs import syslogger as logger
from config import config

config_json = config.open_config_file()


is_drawing = False # true if mouse is pressed
ix,iy = -1,-1
image_global_points = set()

def draw_freehand(event,x,y,flags,param):
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
    image_list = list()
    if 0==image_width%2:
        image_width +=1
    r = image_width//2
    for point in points_list:
        image_list.append([image_matrix[point[0]-r : point[0]+r+1,point[1]-r : point[1]+r+1],point])
    return image_list

def put_subimages(image_matrix, subimage_list, image_width):
    org_image = np.copy(image_matrix)
    r = image_width//2
    for subimages in subimage_list:
        point = subimages[1]
        subimage = subimages[0]
        image_matrix[point[0]-r : point[0]+r+1,point[1]-r : point[1]+r+1] = subimage
    #print(np.sum(image_matrix - org_image))
    return image_matrix

def process_subimage(subimage_list,kernel_width,sigma_range,sigma_domain,filter_itr):
    for element in range(len(subimage_list)):
        subimage = subimage_list[element][0]
        for i in range(filter_itr):
            subimage = common_cv.apply_bilateral_filter(subimage,kernel_width,sigma_range,sigma_domain)
        subimage_list[element][0] = subimage
    return subimage_list   

image_path = "images/lena.png"
img_mat = common_cv.read_image(image_path,"COLOR")
img = img_mat
img_for_subimages = np.copy(img)
cv.namedWindow('image')
cv.setMouseCallback('image',draw_freehand)

while(1):
    cv.imshow('image',img)
    key_val = cv.waitKey(1)
    if key_val == ord('y'):
        break
cv.destroyAllWindows()

image_width = 30
kernel_width = 5
sigma_range = 25
sigma_domain = 0.5
filter_itr = 2
subimage_list = get_subimages(img_for_subimages, image_global_points, image_width)
processed_subimage_list = process_subimage(subimage_list,kernel_width,sigma_range,sigma_domain,filter_itr)
processed_image = put_subimages(img_for_subimages, processed_subimage_list, image_width)
print('Image Processed')
cv.imshow('Image',processed_image)
cv.waitKey(0)
cv.destroyAllWindows()