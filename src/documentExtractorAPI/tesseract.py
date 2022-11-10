import pytesseract
import cv2
import numpy as np
import matplotlib.pyplot as plt
import constants

pytesseract.pytesseract.tesseract_cmd = constants.pytesseract_path

from image_tools import crop_object
from exception_handling import TesseractOCR


def ocr_cropped_image(image, boxes, pred_classes, scores, labels, resize = False):
    """
    Returns the extracted data from the image based on the predictions made by the model(b_box & pred_classes)
    Pytesseract OCR is used.

    :param image: PIL image
    :param boxes: bounding boxes in the image
    :param pred_classes: predicted class by the model
    :param scores: confidence score given by the model
    :param labels: labels we use
    :return: extarcted data from image by the ocr
    
    """ 
    
    try:
        # image = cv2.imread(image_path)
        if resize:
            image = cv2.resize(image, (525, 700))

        # dic = {"name":"", "aadharNumber":"","dob":"", "gender":"", "address":"" }
        # conf_score = {"name":0, "aadharNumber":0,"dob":0, "gender":0, "address":0}
        dic, conf_score = {}, {}
        for i in labels.values():
            dic[i] = ''
            conf_score[i] = 0

        for i in range(len(boxes)):
            box = boxes[i]
            crop_img = crop_object(image, box)
            crop_img = np.array(crop_img)
            img = cv2.cvtColor(crop_img, cv2.COLOR_RGB2BGR)
            img = cv2.resize(img, (300, 100))

            text = pytesseract.image_to_string(img)  # .replace("\n", "")
            text1 = pytesseract.image_to_data(img, output_type='data.frame')
            text1 = text1[text1.conf != -1]
            lines = text1.groupby('block_num')['text'].apply(list)
            conf = text1.groupby(['block_num'])['conf'].mean()

            # print(labels[pred_classes[i]], ':' , text)
            # plt.imshow(crop_img)
            # plt.show()
            # cv2.imshow('a',img)
            # cv2.waitKey(0)

            # dic[labels[pred_classes[i]]] = text
            if labels[pred_classes[i]] == 'address':
                lis = text.replace('Address', '').replace(':', '').split('\n')
                # dic[labels[pred_classes[i]]] = [i.strip() for i in lis if i != '' and len(i) > 1]
                dic[labels[pred_classes[i]]] = ', '.join([i.strip() for i in lis if i != '' and len(i) > 1])
            elif labels[pred_classes[i]] == 'dob':
                dic[labels[pred_classes[i]]] = text.replace('DOB', '').replace(':', '').strip()
            elif labels[pred_classes[i]] == 'aadharNumber':
                dic[labels[pred_classes[i]]] = text.replace(' ', '').strip()
            else:
                dic[labels[pred_classes[i]]] = text.strip()

            conf_score[labels[pred_classes[i]]] = conf.mean() * scores[i]

            # print(labels[pred_classes[i]], text, scores[i], conf.mean())

        return dic, conf_score

    except Exception as e:
        raise TesseractOCR(str(e))
