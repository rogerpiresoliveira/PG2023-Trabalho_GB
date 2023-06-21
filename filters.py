import cv2
import numpy as np

def only_channel(image, channel_idx):
    channels = list(cv2.split(image))
    for i in range(len(channels)):
        if i != channel_idx:
            channels[i] = np.zeros_like(channels[i])
    return cv2.merge(channels)

def grayscale_average(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray
    
def invert(image):
    inverted_image = cv2.bitwise_not(image)
    return inverted_image

def add_color_overlay(image, blue, green, red):
    BGR = [blue, green, red]
    result = cv2.add(image, np.full(image.shape, BGR, dtype=np.uint8).astype(image.dtype))
    result[result > 255] = 255
    return result

def binarize(image, threshold):
    _, filtered_img = cv2.threshold(grayscale_average(image), threshold, 255, cv2.THRESH_BINARY)
    return filtered_img

def apply_saturation(image, saturation_factor):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv_image)
    s = np.clip(s * saturation_factor, 0, 255).astype(np.uint8)
    saturated_hsv_image = cv2.merge([h, s, v])
    output_image = cv2.cvtColor(saturated_hsv_image, cv2.COLOR_HSV2BGR)
    return output_image

def crop(image, x, y, width, height):
    cropped_image = image[y:y+height, x:x+width]
    return cropped_image

def apply_gaussian_blur(image, radius):
    blurred_image = cv2.GaussianBlur(image, (0, 0), radius)
    return blurred_image

def apply_canny_edge_detection(image, min_threshold, max_threshold):
    edges = cv2.Canny(image, min_threshold, max_threshold)
    return edges

def apply_sobel_edge_detection(image, ksize):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)
    edges = cv2.bitwise_or(cv2.convertScaleAbs(sobel_x), cv2.convertScaleAbs(sobel_y))
    return edges

def apply_dilation(image, kernel_size, iterations):
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    dilated_image = cv2.dilate(image, kernel, iterations=iterations)
    return dilated_image

def apply_erosion(image, kernel_size, iterations):
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    eroded_image = cv2.erode(image, kernel, iterations=iterations)
    return eroded_image