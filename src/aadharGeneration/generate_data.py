import randominfo
import pandas as pd
import tqdm
from ensure import ensure_annotations
from constants import config
from pathlib import Path


@ensure_annotations
def generate_data(num: int = 5):
    """
    Genrate fake data for aadhar card like name, dob, address etc.
    :param num: to generate those many numbers of fake data

    """
    name = []
    dob = []
    gender = []
    father_name = []

    for i in tqdm.tqdm(range(num), total=num, unit="Image"):
        name.append(randominfo.get_full_name())
        dob.append(
            randominfo.get_birthdate(startAge=None, endAge=None, _format="%d/%m/%Y")
        )
        gender.append(randominfo.get_gender(randominfo.get_first_name()))
        father_name.append(randominfo.get_full_name())

    pd.DataFrame(
        {
            "Name": name,
            "DOB": dob,
            "Gender": list(map(lambda x: x.capitalize(), gender)),
            "Father_Name": father_name,
        }
    ).to_csv(Path(f"{config.data_path}/random_data.csv"))
