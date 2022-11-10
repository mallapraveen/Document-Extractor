from constants import config
from yolov7.infer_single import infer_yolov7
from exception_handling import TesseractOCR, Aadhar_Extraction, PAN_Extraction, Cheque_Extraction, Classify_Document, Classify_Extract_Document
from classify_document import classify


def aadhar_pipeline(image):
    labels = {0: 'aadharNumber', 1: 'address', 2: 'dob', 3: 'gender', 5: 'name'}
    # extracted_data, conf_score = get_inference(image)
    try:
        extracted_data, conf_score = infer_yolov7(config.yolov7_aadhar_model_path, image, labels, 'aadhar', False)
        return extracted_data, conf_score
    except TesseractOCR as e:
        raise TesseractOCR(e.message)
    except Exception as e:
        raise Aadhar_Extraction(str(e))


def pan_pipeline(image):
    labels = {0: 'dob', 1: 'father_name', 2: 'name', 3: 'pan'}
    # extracted_data, conf_score = get_inference(image)
    try:
        extracted_data, conf_score = infer_yolov7(config.yolov7_pan_model_path, image, labels, 'pan', False)
        return extracted_data, conf_score
    except TesseractOCR as e:
        raise TesseractOCR(e.message)
    except Exception as e:
        raise PAN_Extraction(str(e))


def cheque_pipeline(image):
    labels = {0: 'accNumber', 1: 'bank', 2: 'ifsc', 3: 'name'}
    # extracted_data, conf_score = get_inference(image)
    try:
        extracted_data, conf_score = infer_yolov7(config.yolov7_cheque_model_path, image, labels, 'cheque', False)
        return extracted_data, conf_score
    except TesseractOCR as e:
        raise TesseractOCR(e.message)
    except Exception as e:
        raise Cheque_Extraction(str(e))


def classify_pipeline(image):
    try:
        document, conf_score = classify(image)
        return document, round(conf_score, 2)
    except Exception as e:
        raise Classify_Document(str(e))


def classify_extract_pipeline(image):
    try:
        document, conf_score = classify(image)
        extracted_data, conf_score = map_pipeline(document, image)
        return document, extracted_data, conf_score
    except Classify_Document as e:
        raise Classify_Document(str(e))
    except Exception as e:
        raise Classify_Extract_Document(str(e))


def map_pipeline(document, image):
    try:
        if document == 'aadhar':
            labels = {0: 'aadharNumber', 1: 'address', 2: 'dob', 3: 'gender', 5: 'name'}
            extracted_data, conf_score = infer_yolov7(config.yolov7_aadhar_model_path, image, labels, 'aadhar', False)
        elif document == 'cheque':
            labels = {0: 'accNumber', 1: 'bank', 2: 'ifsc', 3: 'name'}
            extracted_data, conf_score = infer_yolov7(config.yolov7_cheque_model_path, image, labels, 'cheque', False)
        elif document == 'pan':
            labels = {0: 'dob', 1: 'father_name', 2: 'name', 3: 'pan'}
            extracted_data, conf_score = infer_yolov7(config.yolov7_pan_model_path, image, labels, 'pan', False)
        else:
            raise Classify_Document("Classification of document failed.")
        return extracted_data, conf_score

    except TesseractOCR as e:
        raise TesseractOCR(e.message)
    except Aadhar_Extraction as e:
        raise Aadhar_Extraction(e.message)
    except PAN_Extraction as e:
        raise PAN_Extraction(e.message)
    except Cheque_Extraction as e:
        raise Cheque_Extraction(e.message)
    except Exception as e:
        raise Classify_Extract_Document(str(e))
