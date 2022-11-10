import os
from pathlib import Path
from utilities import read_yaml

# Tesseract Executable path
pytesseract_path = os.getenv('pytesseract_path', r'C:\Program Files\Tesseract-OCR\tesseract.exe')
CONFIG_FILE_PATH = Path("./configs/documentExtractorAPI.yml")

config = read_yaml(CONFIG_FILE_PATH)