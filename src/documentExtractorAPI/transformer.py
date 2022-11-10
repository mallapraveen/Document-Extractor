from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from constants import config
import numpy as np
import cv2, torch
import matplotlib
import matplotlib.pyplot as plt
from image_tools import crop_object


def transformer_ocr(image, boxes, pred_classes, scores, labels, resize=True):
    """
    Returns the extracted data from the image based on the predictions made by the model(b_box & pred_classes)
    Transformer based OCR is used 

    :param image: PIL image
    :param boxes: bounding boxes in the image
    :param pred_classes: predicted class by the model
    :param scores: confidence score given by the model
    :param labels: labels we use
    :return: extarcted data from image by the ocr
    
    """

    # image = cv2.imread(image_path)
    if resize:
        image = cv2.resize(image, (525, 700))

    dic, conf_score = {}, {}
    for i in labels.values():
        dic[i] = ''
        conf_score[i] = 0

    processor = TrOCRProcessor.from_pretrained({config.tocr_model})
    model = VisionEncoderDecoderModel.from_pretrained({config.tocr_model})

    for i in range(len(boxes)):
        box = boxes[i]
        crop_img = crop_object(image, box)
        img = np.array(crop_img)
        crop_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img = cv2.resize(crop_img, (300, 100))

        pixel_values = processor(img, return_tensors="pt").pixel_values
        generated_ids = model.generate(pixel_values, output_scores=True, return_dict_in_generate=True)
        text = processor.batch_decode(generated_ids.sequences, skip_special_tokens=True)[0]

        tot_prob = 1
        probs = torch.stack(generated_ids.scores, dim=1).softmax(-1)[0].numpy()
        pos = np.argmax(probs, axis=-1).flatten()
        for j in range(len(pos)):
            tot_prob = tot_prob * probs[j][pos[j]]

        # print(labels[pred_classes[i]], ':' , text)
        # plt.imshow(crop_img)
        # plt.show()
        # cv2.imshow('a',img)
        # cv2.waitKey(0)

        if labels[pred_classes[i]] == 'address':
            lis = text.replace('Address', '').replace(':', '').split('\n')
            # dic[labels[pred_classes[i]]] = [i.strip() for i in lis if i != '' and len(i)>1]
            dic[labels[pred_classes[i]]] = ', '.join([i.strip() for i in lis if i != '' and len(i) > 1])
        elif labels[pred_classes[i]] == 'dob':
            dic[labels[pred_classes[i]]] = text.replace('DOB', '').replace(':', '').strip()
        else:
            dic[labels[pred_classes[i]]] = text.strip()

        conf_score[labels[pred_classes[i]]] = tot_prob * scores[i]

    return dic, conf_score
