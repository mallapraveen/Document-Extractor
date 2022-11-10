import cv2
import numpy as np
import urllib
from PIL import Image


def url_to_image(url):
    """
    download the image, convert it to a NumPy array, and then read it into OpenCV format

    :param url: url of the image
    :return: image from the url
    
    """
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    
    return image

def crop_object(image, box):
    """
    Crops the image based on given bounding box and return cropped image

    :param image: PIL image
    :param box: one box from Detectron2 pred_boxes
    :return: cropped image
    
    """ 

    color_coverted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image=Image.fromarray(color_coverted)

    x_top_left = box[0]
    y_top_left = box[1]
    x_bottom_right = box[2]
    y_bottom_right = box[3]

    crop_img = pil_image.crop((int(x_top_left), int(y_top_left), int(x_bottom_right), int(y_bottom_right)))
    
    return crop_img