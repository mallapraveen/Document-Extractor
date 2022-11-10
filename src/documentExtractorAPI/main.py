import sys, os
from pathlib import Path
sys.path.insert(0, './src/yolov7')
import cv2
import warnings
from constants import config
warnings.filterwarnings('ignore')

from constants import config
from flask import Flask
from api import flask_app, document_extraction, classification, classify_extract
from flask_restx import Api, Resource
from infer_single import infer_yolov7
from pipeline import aadhar_pipeline
from pipeline import aadhar_pipeline, pan_pipeline, cheque_pipeline, classify_pipeline, classify_extract_pipeline

if __name__ == '__main__':

    # image_url = './sample images/Aadhar/Back_0.JPG'
    # image = cv2.imread(image_url)
    # labels = {0: 'aadharNumber', 1: 'address', 2: 'dob', 3: 'gender', 5: 'name'}
    # print(aadhar_pipeline(image))
    # print(infer_yolov7(config.yolov7_aadhar_model_path, image, labels, 'aadhar', False))

    # image_url = '../../sample images/PAN/Compress-and-Resize-Your-Digital-Photos_jpg.rf.3e9a76b6ac850cfae0f38be6a1da5b99.jpg'
    # image = cv2.imread(image_url)
    # labels = {0: 'dob', 1: 'father_name', 2: 'name', 3: 'pan'}
    # print(pan_pipeline(image))
    # print(infer_yolov7(config.yolov7_pan_model_path, image, labels, 'pan', False))

    # image_url = '../../sample images/Cheque/16.jpg'
    # image = cv2.imread(image_url)
    # labels = {0: 'accNumber', 1: 'bank', 2: 'ifsc', 3: 'name'}
    # print(infer_yolov7(config.yolov7_cheque_model_path, image, labels, 'cheque', False))
    # print(cheque_pipeline(image))

    # image_url = '../../sample images/Aadhar/Back_0.JPG'
    # image = cv2.imread(image_url)
    # print(classify_pipeline(image))
    # print(classify_extract_pipeline(image))

    port = os.getenv('PORT', default=8000)
    flask_end = Flask(__name__)
    flask_end.register_blueprint(flask_app)
    app = Api(app=flask_end, version='1.0', title='Document Extraction API', description='Main APIS')
    app.add_namespace(document_extraction)
    app.add_namespace(classification)
    app.add_namespace(classify_extract)
    flask_end.run(host="0.0.0.0", port=port, debug=True)