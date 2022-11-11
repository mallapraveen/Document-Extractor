from pathlib import Path
from utilities import read_yaml

# constants

date_regex = r"[\d]{1,4}[/-][\d]{1,4}[/-][\d]{1,4}"
aadhar_regex = r"[0-9]{4} [0-9]{4} [0-9]{4}"
gender_regex = r"MALE|FEMALE|Female|Male"

CONFIG_FILE_PATH = Path("./configs/aadharGeneration.yml")

config = read_yaml(CONFIG_FILE_PATH)
