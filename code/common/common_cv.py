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
	
def distance(x, y, i, j):
    return np.sqrt((x-i)**2 + (y-j)**2)

def gaussian(x, sigma):
    return  (1/(2*math.pi*(sigma**2)))*np.exp(-(1/2)*((x ** 2) /(sigma ** 2)))

def bilateral_filter(img, diameter, sigma_intensity, sigma_domain):
    row = img.shape[0]
    col = img.shape[1]
    channel = img.shape[2]
    filtered_img = np.copy(img)
    r = diameter // 2
    for x in range(r,row-r):
        for y in range(r,col-r):
            filtered1,filtered2,filtered3 = 0,0,0
            w1,w2,w3 = 0,0,0
            center_x = x
            center_y = y
            tmp_r = img[x - r:x + r + 1,y - r:y + r + 1,0]
            tmp_g = img[x - r:x + r + 1,y - r:y + r + 1,1]
            tmp_b = img[x - r:x + r + 1,y - r:y + r + 1,2]
            for p in range(-r,r+1):
                for q in range(-r,r+1):
                    n_x = center_x + p
                    n_y = center_y + q
                    g_i_1 = gaussian(tmp_r[p, q]-img[n_x, n_y,0], sigma_intensity)
                    g_i_2 = gaussian(tmp_g[p, q]-img[n_x, n_y,1], sigma_intensity)
                    g_i_3 = gaussian(tmp_b[p, q]-img[n_x, n_y,2], sigma_intensity)
                    g_s = gaussian(distance(n_x, n_y, center_x, center_y), sigma_domain)
                    wt1 = g_i_1 * g_s
                    wt2 = g_i_2 * g_s
                    wt3 = g_i_3 * g_s
                    filtered1 += (tmp_r[p, q] * wt1)
                    filtered2 += (tmp_g[p, q] * wt2)
                    filtered3 += (tmp_b[p, q] * wt3)
                    w1+=wt1
                    w2+=wt2
                    w3+=wt3
            
            if w1!=0 and w2!=0 and w3!=0:
                f1 = filtered1 / w1
                f2 = filtered2 / w2
                f3 = filtered3 / w3

            filtered_img[x, y,0] = f1
            filtered_img[x, y,1] = f2
            filtered_img[x, y,2] = f3
            
    return filtered_img
