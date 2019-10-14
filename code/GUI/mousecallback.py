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



image_path = "images/lena.png"
img_mat = common_cv.read_image(image_path,"COLOR")
img = img_mat
cv.namedWindow('image')
cv.setMouseCallback('image',draw_freehand)

while(1):
    cv.imshow('image',img)
    key_val = cv.waitKey(1)
    if key_val == ord('y'):
        break
cv.destroyAllWindows()
print("Yes")