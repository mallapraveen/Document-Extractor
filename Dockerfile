FROM python:3.9

WORKDIR /flaskapp

COPY . . 

ENV pytesseract_path=../../../usr/bin/tesseract
RUN apt-get update
RUN apt-get -y install tesseract-ocr
RUN apt-get -y install ffmpeg libsm6 libxext6
  
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /flaskapp/src/documentExtractorAPI/

EXPOSE 8000

CMD [ "python", "main.py"]