import cv2
import os  

COLOR_SCHEME = {
	"COLOR" : cv2.IMREAD_COLOR, 
	"GRAYSCALE" : cv2.IMREAD_GRAYSCALE, 
	"UNCHANGED" : cv2.IMREAD_UNCHANGED 	
}

def read_image(image_path = None, image_color_scheme = "COLOR"):
	return cv2.imread(image_path, COLOR_SCHEME[image_color_scheme])
	"""
	if not os.path.exists(image_path):
		print("Path does not exist!!!")
	"""