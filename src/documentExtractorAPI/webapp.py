import sys, os
import streamlit as st
import streamlit.components.v1 as components
sys.path.insert(0, "./src/yolov7")
os.environ["pytesseract_path"] == st.secrets["pytesseract_path"]

from pipeline import (
    aadhar_pipeline,
    pan_pipeline,
    cheque_pipeline,
    classify_pipeline,
    classify_extract_pipeline,
)

from PIL import Image
import numpy as np

st.title("# Document Extraction")

def load_image(image_file):
    img = Image.open(image_file)
    return img

aadhar_expander = st.expander(label='For Aadhar Extraction')
with aadhar_expander:
    st.write("### Aadhar Extraction")
    st.subheader("Upload Aadhar Image Image")
    image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg"], key=0)
    if image_file is not None:
        image = load_image(image_file)
        image = np.array(image)
        extracted_data, conf_score = aadhar_pipeline(image)
        st.json(extracted_data)
        st.json(conf_score)
        
pan_expander = st.expander(label='For PAN Extraction')
with pan_expander:
    st.write("### PAN Extraction")
    st.subheader("Upload PAN Image Image")
    image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg"], key=1)
    if image_file is not None:
        image = load_image(image_file)
        image = np.array(image)
        extracted_data, conf_score = pan_pipeline(image)
        st.json(extracted_data)
        st.json(conf_score)
        
cheque_expander = st.expander(label='For Cheque Extraction')
with cheque_expander:
    st.write("### Cheque Extraction")
    st.subheader("Upload Cheque Image Image")
    image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg"], key=2)
    if image_file is not None:
        image = load_image(image_file)
        image = np.array(image)
        extracted_data, conf_score = cheque_pipeline(image)
        st.json(extracted_data)
        st.json(conf_score)
        
classify_expander = st.expander(label='For Document Classification')
with classify_expander:
    st.write("### Document Classification")
    st.subheader("Upload Image Image")
    image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg"], key=3)
    if image_file is not None:
        image = load_image(image_file)
        image = np.array(image)
        document, conf_score = classify_pipeline(image)
        st.write(f"The document uploaded is {document} and conf_score is {conf_score}.")
        
classify_extract_expander = st.expander(label='For Document Classification and Extraction')
with classify_extract_expander:
    st.write("### Document Classification and Extraction")
    st.subheader("Upload Image Image")
    image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg"], key=4)
    if image_file is not None:
        image = load_image(image_file)
        image = np.array(image)
        document, extracted_data, conf_score = classify_extract_pipeline(image)
        st.write(f"The document uploaded is {document}.")
        st.json(extracted_data)
        st.json(conf_score)
        

st.subheader("For source code please visit my git [link](https://github.com/mallapraveen/Document-Extractor)")
st.subheader("[My Profile](https://github.com/mallapraveen)")