import cv2 as cv
import os 
import numpy as np 

COLOR_SCHEME = {
	"COLOR" : cv.IMREAD_COLOR, 
	"GRAYSCALE" : cv.IMREAD_GRAYSCALE, 
	"UNCHANGED" : cv.IMREAD_UNCHANGED 	
}

def read_image(image_path = None, image_color_scheme = "COLOR"):
	return cv.imread(image_path, COLOR_SCHEME[image_color_scheme])
	"""
	if not os.path.exists(image_path):
		print("Path does not exist!!!")
	"""
	
def distance(x, y):
    '''
    x,y : calculating distances of x,y
    '''
    return np.sqrt((x-0)**2 + (y-0)**2)


def gradient(img,k,x,y):
    '''
    Input : image of size k*k
    k : kernel size/window size
    x,y : are distance matrix
    '''
    sobelx = cv.Sobel(img,cv.CV_64F,1,0,ksize=k)
    sobely = cv.Sobel(img,cv.CV_64F,0,1,ksize=k)
    return (x*sobelx) + (y*sobely)

def gaussian(x, sigma):
    '''
    Input : x
    sigma : variance(range/domain)
    Output : gaussian
    '''
    return  np.exp(-(1/2)*((x ** 2) /(sigma ** 2)))

def apply_bilateral_filter(img, diameter, sigma_intensity, sigma_domain):
    '''
    Input : Image to be filtered
    diameter : kernel size, window size
    sigma_intensity : variance for range
    sigma_domain : variance for domain
    Ouput : Filtered Image
    '''
    row = img.shape[0]
    col = img.shape[1]
    channel = img.shape[2]
    filtered_img = np.copy(img)
    r = diameter // 2
    # calculating x,y distance from center pixel locations for w1(x,y)
    x, y = np.meshgrid(np.arange(2 * r + 1) - r, np.arange(2 * r + 1) - r)
    # Applying gaussian for domain w1(x,y)
    kernel_s = gaussian((x * x + y * y),sigma_domain)
    for x in range(r,row-r):
        for y in range(r,col-r):
            
           if img.ndim == 3:
                # Identifying k*k size neighbourhood for all channels
                tmp_r = img[x - r:x + r + 1,y - r:y + r + 1,0]
                tmp_g = img[x - r:x + r + 1,y - r:y + r + 1,1]
                tmp_b = img[x - r:x + r + 1,y - r:y + r + 1,2]
            
                # calculating direction*gradient of image and applying Gaussian 
                grad = gradient(img[x - r:x + r + 1,y - r:y + r + 1],diameter,x,y)
                kernel_r = gaussian(grad,sigma_intensity)
            
                # Calculating weight = w1(x,y)*w2(x,y)
                wgt = (kernel_r[:,:,0])+(kernel_r[:,:,1])+(kernel_r[:,:,2]) * kernel_s
            
                # Changing the center pixel of neighbourhood for all channels
                filtered_img[x, y, 0] = np.sum(wgt * tmp_r) / np.sum(wgt)
                filtered_img[x, y, 1] = np.sum(wgt * tmp_g) / np.sum(wgt)
                filtered_img[x, y, 2] = np.sum(wgt * tmp_b) / np.sum(wgt)
                
            elif img.ndim == 2:
                 # Identifying k*k size neighbourhood for all channels
                tmp_r = img[x - r:x + r + 1,y - r:y + r + 1]
                
                # calculating direction*gradient of image and applying Gaussian 
                grad = gradient(img[x - r:x + r + 1,y - r:y + r + 1],diameter,x,y)
                kernel_r = gaussian(grad,sigma_intensity)
            
                # Calculating weight = w1(x,y)*w2(x,y)
                wgt = (kernel_r * kernel_s)
            
                # Changing the center pixel of neighbourhood for all channels
                filtered_img[x, y] = np.sum(wgt * tmp_r) / np.sum(wgt)
            
    return filtered_img
