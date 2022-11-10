import numpy as np
from flask import Flask
from PIL import Image

from pipeline import aadhar_pipeline, pan_pipeline, cheque_pipeline, classify_pipeline, classify_extract_pipeline
from exception_handling import BearerAccessToken, GetFileId

from flask import Blueprint
from flask_restx import Namespace, Resource, fields

from werkzeug.datastructures import FileStorage
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app)
upload_parser = api.parser()
upload_parser.add_argument('image', location='files', type=FileStorage)

flask_app = Blueprint("product", __name__)

document_extraction = Namespace('extractor', 'Main APIS')
classification = Namespace('classify', 'Main APIS')
classify_extract = Namespace('classify_extract', 'Main APIS')

@api.route('/upload/')
@api.expect(upload_parser)
@document_extraction.route("/aadhar")
class Aadhar(Resource):

    def post(self):
        try:
            #file = request.files['image']
            args = upload_parser.parse_args()
            file = args.get('image')
            image = Image.open(file)
            image = np.asarray(image)
            extracted_data, conf_score = aadhar_pipeline(image)

            pay_load = {
                "documentType": "AADHAR",
                "metaData": extracted_data,
                "confidenceScore": conf_score,
            }

            return pay_load, 200
        except BearerAccessToken as e:
            return {"message": e.message}, e.status_code
        except GetFileId as e:
            return {"message": e.message}, e.status_code
        except Exception as e:
            return {"message": str(e)}, 400

@api.route('/upload/')
@api.expect(upload_parser)
@document_extraction.route("/pan")
class PAN(Resource):

    def post(self):
        try:
            #file = request.files['image']
            args = upload_parser.parse_args()
            file = args.get('image')
            image = Image.open(file)
            image = np.asarray(image)
            extracted_data, conf_score = pan_pipeline(image)

            pay_load = {
                "documentType": "PAN",
                "metaData": extracted_data,
                "confidenceScore": conf_score,
            }

            return pay_load, 200
        except BearerAccessToken as e:
            return {"message": e.message}, e.status_code
        except GetFileId as e:
            return {"message": e.message}, e.status_code
        except Exception as e:
            return {"message": str(e)}, 400

@api.route('/upload/')
@api.expect(upload_parser)
@document_extraction.route("/cheque")
class Cheque(Resource):
    def post(self):
        try:
            args = upload_parser.parse_args()
            file = args.get('image')
            image = Image.open(file)
            image = np.asarray(image)

            extracted_data, conf_score = cheque_pipeline(image)

            pay_load = {
                "documentType": "Cheque",
                "metaData": extracted_data,
                "confidenceScore": conf_score,
            }

            return pay_load, 200
        except BearerAccessToken as e:
            return {"message": e.message}, e.status_code
        except GetFileId as e:
            return {"message": e.message}, e.status_code
        except Exception as e:
            return {"message": str(e)}, 400

@api.route('/upload/')
@api.expect(upload_parser)
@classification.route("")
class ClassifyImage(Resource):
    def post(self):
        try:
            args = upload_parser.parse_args()
            file = args.get('image')
            image = Image.open(file)
            image = np.asarray(image)

            document, conf_score = classify_pipeline(image)

            pay_load = {
                "documentType": document,
                "confidenceScore": conf_score
            }

            return pay_load, 200
        except BearerAccessToken as e:
            return {"message": e.message}, e.status_code
        except GetFileId as e:
            return {"message": e.message}, e.status_code
        except Exception as e:
            return {"message": str(e)}, 400

@api.route('/upload/')
@api.expect(upload_parser)
@classify_extract.route("")
class ClassifyExtract(Resource):
    def post(self):
        try:
            args = upload_parser.parse_args()
            file = args.get('image')
            image = Image.open(file)
            image = np.asarray(image)

            document, extracted_data, conf_score = classify_extract_pipeline(image)
            pay_load = {
                "documentType": document,
                "metaData": extracted_data,
                "confidenceScore": conf_score,
            }

            return pay_load, 200
        except BearerAccessToken as e:
            return {"message": e.message}, e.status_code
        except GetFileId as e:
            return {"message": e.message}, e.status_code
        except Exception as e:
            return {"message": str(e)}, 400




#
# @flask_app.route("/extractor/api/aadhar", methods=["POST"])
# def aadhar():
#     try:
#         file = request.files['image']
#         image = Image.open(file.stream)
#         image = np.asarray(image)
#         extracted_data, conf_score = aadhar_pipeline(image)
#
#         pay_load = {
#             "documentType": "AADHAR",
#             "metaData": extracted_data,
#             "confidenceScore": conf_score,
#         }
#
#         return jsonify(pay_load), 200
#     except BearerAccessToken as e:
#         return jsonify({"message": e.message}), e.status_code
#     except GetFileId as e:
#         return jsonify({"message": e.message}), e.status_code
#     except Exception as e:
#         return jsonify({"message": str(e)}), 400
#
#
# @flask_app.route("/extractor/api/pan", methods=["POST"])
# def pan():
#     try:
#         file = request.files['image']
#         image = Image.open(file.stream)
#         image = np.asarray(image)
#         extracted_data, conf_score = pan_pipeline(image)
#
#         pay_load = {
#             "documentType": "PAN",
#             "metaData": extracted_data,
#             "confidenceScore": conf_score,
#         }
#
#         return jsonify(pay_load), 200
#     except BearerAccessToken as e:
#         return jsonify({"message": e.message}), e.status_code
#     except GetFileId as e:
#         return jsonify({"message": e.message}), e.status_code
#     except Exception as e:
#         return jsonify({"message": str(e)}), 400
#
#
# @flask_app.route("/extractor/api/cheque", methods=["POST"])
# def cheque():
#     try:
#         file = request.files['image']
#         image = Image.open(file.stream)
#         image = np.asarray(image)
#
#         extracted_data, conf_score = cheque_pipeline(image)
#
#         pay_load = {
#             "documentType": "Cheque",
#             "metaData": extracted_data,
#             "confidenceScore": conf_score,
#         }
#
#         return jsonify(pay_load), 200
#     except BearerAccessToken as e:
#         return jsonify({"message": e.message}), e.status_code
#     except GetFileId as e:
#         return jsonify({"message": e.message}), e.status_code
#     except Exception as e:
#         return jsonify({"message": str(e)}), 400
#
#
# @flask_app.route("/extractor/api/classify", methods=["POST"])
# def classify_image():
#     try:
#         file = request.files['image']
#         image = Image.open(file.stream)
#         image = np.asarray(image)
#
#         document, conf_score = classify_pipeline(image)
#
#         pay_load = {
#             "documentType": document,
#             "confidenceScore": conf_score
#         }
#
#         return jsonify(pay_load), 200
#     except BearerAccessToken as e:
#         return jsonify({"message": e.message}), e.status_code
#     except GetFileId as e:
#         return jsonify({"message": e.message}), e.status_code
#     except Exception as e:
#         return jsonify({"message": str(e)}), 400
#
#
# @flask_app.route("/extractor/api/classify_extract", methods=['POST'])
# def classify_extract():
#     try:
#         file = request.files['image']
#         image = Image.open(file.stream)
#         image = np.asarray(image)
#
#         document, extracted_data, conf_score = classify_extract_pipeline(image)
#         pay_load = {
#             "documentType": document,
#             "metaData": extracted_data,
#             "confidenceScore": conf_score,
#         }
#
#         return jsonify(pay_load), 200
#     except BearerAccessToken as e:
#         return jsonify({"message": e.message}), e.status_code
#     except GetFileId as e:
#         return jsonify({"message": e.message}), e.status_code
#     except Exception as e:
#         return jsonify({"message": str(e)}), 400
