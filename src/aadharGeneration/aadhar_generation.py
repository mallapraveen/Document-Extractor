import numpy as np
import pandas as pd

from PIL import Image, ImageFont, ImageDraw
import tqdm
from language_translation import convert_to_lang
import random
from constants import config
from pathlib import Path
from ensure import ensure_annotations


def print_front_layout(img: Image, data: dict, fonts: dict, dest_lang: str):
    """
    Generates the front layout of Big aadhar
    :param img: The front layout of aadahr
    :param data: aadhar data needs to be printed on
    :param fonts: fonts required for different languages
    :param dest_lang: destination language to be converted to

    """
    image_editable = ImageDraw.Draw(img)

    name_in_lang = convert_to_lang(data["Name"], src="en", dest=dest_lang)

    image_editable.text((183, 1193), name_in_lang, (0, 0, 0), font=fonts["fnt"])
    image_editable.text((183, 1216), data["Name"], (0, 0, 0), font=fonts["fnt"])
    image_editable.text(
        (183, 1239),
        data["dob_lang"] + " / " + "DOB:" + data["DOB"],
        (0, 0, 0),
        font=fonts["fnt"],
    )
    image_editable.text(
        (193, 1425), str(data["Aadhar_No"]), (0, 0, 0), font=fonts["fnt2"]
    )
    image_editable.text(
        (180, 990), str(data["Aadhar_No"]), (0, 0, 0), font=fonts["fnt2"]
    )

    image_editable.text(
        (255, 1470), str(data["Aadhar_No"]), (0, 0, 0), font=fonts["vid"]
    )
    image_editable.text(
        (245, 1031), str(data["Aadhar_No"]), (0, 0, 0), font=fonts["vid2"]
    )

    if data["Gender"] == "Male":
        image_editable.text(
            (183, 1262),
            data["gender_male_lang"] + " / " + data["Gender"],
            (0, 0, 0),
            font=fonts["fnt"],
        )
    else:
        image_editable.text(
            (183, 1262),
            data["gender_female_lang"] + " / " + data["Gender"],
            (0, 0, 0),
            font=fonts["fnt"],
        )

    # image_editable.text((112, 420), 'Address: S/O ' + data['Father_Name'] + ",", (0, 0, 0), font=fonts['fnt'])

    image_editable.text((112, 420), name_in_lang, (0, 0, 0), font=fonts["fnt"])
    image_editable.text(
        (112, 445), "S/O " + data["Father_Name"], (0, 0, 0), font=fonts["fnt"]
    )

    image_editable.text((112, 470), str(data["Address1"]), (0, 0, 0), font=fonts["fnt"])

    if data["Address2"] is not np.nan and data["Address3"] is not np.nan:
        image_editable.text(
            (112, 495), str(data["Address2"]), (0, 0, 0), font=fonts["fnt"]
        )
    elif data["Address2"] is not np.nan:
        image_editable.text(
            (112, 495), str(data["Address2"]), (0, 0, 0), font=fonts["fnt"]
        )

    if data["Address3"] is not np.nan and data["Address4"] is not np.nan:
        image_editable.text(
            (112, 520), str(data["Address3"]), (0, 0, 0), font=fonts["fnt"]
        )
    elif data["Address3"] is not np.nan:
        image_editable.text(
            (112, 520), str(data["Address3"]), (0, 0, 0), font=fonts["fnt"]
        )

    if data["Address4"] is not np.nan and data["Address5"] is not np.nan:
        image_editable.text(
            (112, 545), str(data["Address4"]), (0, 0, 0), font=fonts["fnt"]
        )
    elif data["Address4"] is not np.nan:
        image_editable.text(
            (112, 545), str(data["Address4"]), (0, 0, 0), font=fonts["fnt"]
        )

    if data["Address5"] is not np.nan:
        image_editable.text(
            (112, 570), str(data["Address5"]), (0, 0, 0), font=fonts["fnt"]
        )


def print_back_layout(img: Image, data: dict, fonts: dict):

    """
    Generates the back layout of Big aadhar
    :param img: The front layout of aadahr
    :param data: aadhar data needs to be printed on
    :param fonts: fonts required for different languages

    """

    image_editable = ImageDraw.Draw(img)

    image_editable.text(
        (200, 1431), str(data["Aadhar_No"]), (0, 0, 0), font=fonts["fnt2"]
    )
    image_editable.text(
        (260, 1468), str(data["Aadhar_No"]), (0, 0, 0), font=fonts["vid2"]
    )

    image_editable.text(
        (29, 1258),
        "Address: S/O " + data["Father_Name"] + ",",
        (0, 0, 0),
        font=fonts["fnt"],
    )
    image_editable.text(
        (29, 1278), str(data["Address1"]) + ", ", (0, 0, 0), font=fonts["fnt"]
    )

    if data["Address2"] is not np.nan and data["Address3"] is not np.nan:
        image_editable.text(
            (29, 1298), str(data["Address2"]) + ", ", (0, 0, 0), font=fonts["fnt"]
        )
    elif data["Address2"] is not np.nan:
        image_editable.text(
            (29, 1298), str(data["Address2"]), (0, 0, 0), font=fonts["fnt"]
        )

    if data["Address3"] is not np.nan and data["Address4"] is not np.nan:
        image_editable.text(
            (29, 1318), str(data["Address3"]) + ", ", (0, 0, 0), font=fonts["fnt"]
        )
    elif data["Address3"] is not np.nan:
        image_editable.text(
            (29, 1318), str(data["Address3"]), (0, 0, 0), font=fonts["fnt"]
        )

    if data["Address4"] is not np.nan and data["Address5"] is not np.nan:
        image_editable.text(
            (29, 1338), str(data["Address4"]) + ", ", (0, 0, 0), font=fonts["fnt"]
        )
    elif data["Address4"] is not np.nan:
        image_editable.text(
            (29, 1338), str(data["Address4"]), (0, 0, 0), font=fonts["fnt"]
        )

    if data["Address5"] is not np.nan:
        image_editable.text(
            (29, 1358), str(data["Address5"]), (0, 0, 0), font=fonts["fnt"]
        )


@ensure_annotations
def create_big_aadhar(no_of_images: int, template_path: str, save_path: str):
    """
    Generates the front and back of big aadhar layout
    :param no_of_images: Total no. of images to be generated for both front and back of aadhar
    :param template_path: The template path for front and back of aadhar
    :param save_path: Path of images to be saved to

    """

    data = pd.read_csv(Path(f"{config.data_path}/aadhar_data.csv"))
    data = data.sample(frac=1)

    for i in tqdm.tqdm(range(no_of_images), total=no_of_images, unit="Image"):
        aadhar_data = {}

        fonts = {}

        dest_lang = random.choice(list(config.languages.keys()))
        fonts["fnt"] = ImageFont.truetype(f"{config.fonts_path}/{dest_lang}.ttf", 22)
        fonts["fnt2"] = ImageFont.truetype(f"{config.fonts_path}/arial.ttf", 34)
        fonts["fnt3"] = ImageFont.truetype(f"{config.fonts_path}/arial.ttf", 11)
        fonts["fnt4"] = ImageFont.truetype(f"{config.fonts_path}/arial.ttf", 24)
        fonts["vid"] = ImageFont.truetype(f"{config.fonts_path}/arial.ttf", 12)
        fonts["vid2"] = ImageFont.truetype(f"{config.fonts_path}/arial.ttf", 15)
        dob = ""

        if dest_lang in ["te", "ta", "mr", "pa", "ur"]:
            dob = "dateofbirth"
        else:
            dob = "dob"

        dob_lang = convert_to_lang(dob, src="en", dest=dest_lang)
        gender_male_lang = convert_to_lang("Male", src="en", dest=dest_lang)
        gender_female_lang = convert_to_lang("Female", src="en", dest=dest_lang)

        aadhar_data["Name"] = data.iloc[i]["Name"]
        aadhar_data["DOB"] = data.iloc[i]["DOB"]
        aadhar_data["Gender"] = data.iloc[i]["Gender"]
        aadhar_data["Aadhar_No"] = data.iloc[i]["Aadhar_No"]
        aadhar_data["Father_Name"] = data.iloc[i]["Father_Name"]
        aadhar_data["Address1"] = data.iloc[i]["Address1"]
        aadhar_data["Address2"] = data.iloc[i]["Address2"]
        aadhar_data["Address3"] = data.iloc[i]["Address3"]
        aadhar_data["Address4"] = data.iloc[i]["Address4"]
        aadhar_data["Address5"] = data.iloc[i]["Address5"]

        aadhar_data["dob_lang"] = dob_lang
        aadhar_data["gender_male_lang"] = gender_male_lang
        aadhar_data["gender_female_lang"] = gender_female_lang

        img1 = Image.open(Path(template_path + "/Front_Long.png"))
        img2 = Image.open(Path(template_path + "/Back_Long.jpg"))

        print_front_layout(img1, aadhar_data, fonts, dest_lang)

        print_back_layout(img2, aadhar_data, fonts)

        rgb_im1 = img1.convert("RGB")
        rgb_im1.save(save_path + "\\Front_Long\\" + "Front_Long_" + str(i) + ".JPG")

        rgb_im2 = img2.convert("RGB")
        rgb_im2.save(save_path + "\\Back_Long\\" + "Back_Long_" + str(i) + ".JPG")


@ensure_annotations
def create_small_aadhar(no_of_images: int, template_path: str, save_path: str):
    """
    Generates the front and back of small aadhar layout
    :param no_of_images: Total no. of images to be generated for both front and back of aadhar
    :param template_path: The template path for front and back of aadhar
    :param save_path: Path of images to be saved to

    """

    data = pd.read_csv(Path(f"{config.data_path}/aadhar_data.csv"))
    data = data.sample(frac=1)

    for i in tqdm.tqdm(range(no_of_images), total=no_of_images, unit="Image"):

        dest_lang = random.choice(list(config.languages.keys()))

        fnt = ImageFont.truetype(f"{config.fonts_path}/{dest_lang}.ttf", 12)
        fnt2 = ImageFont.truetype(f"{config.fonts_path}/arial.ttf", 20)
        fnt3 = ImageFont.truetype(f"{config.fonts_path}/arial.ttf", 12)

        dob = ""

        if dest_lang in ["te", "ta", "mr", "pa", "ur"]:
            dob = "dateofbirth"
        else:
            dob = "dob"

        dob_lang = convert_to_lang(dob, src="en", dest=dest_lang)
        gender_male_lang = convert_to_lang("Male", src="en", dest=dest_lang)
        gender_female_lang = convert_to_lang("Female", src="en", dest=dest_lang)

        aadhar_data = {}

        aadhar_data["Name"] = data.iloc[i]["Name"]
        aadhar_data["DOB"] = data.iloc[i]["DOB"]
        aadhar_data["Gender"] = data.iloc[i]["Gender"]
        aadhar_data["Aadhar_No"] = data.iloc[i]["Aadhar_No"]
        aadhar_data["Father_Name"] = data.iloc[i]["Father_Name"]
        aadhar_data["Address1"] = data.iloc[i]["Address1"]
        aadhar_data["Address2"] = data.iloc[i]["Address2"]
        aadhar_data["Address3"] = data.iloc[i]["Address3"]
        aadhar_data["Address4"] = data.iloc[i]["Address4"]
        aadhar_data["Address5"] = data.iloc[i]["Address5"]

        aadhar_data["dob_lang"] = dob_lang
        aadhar_data["gender_male_lang"] = gender_male_lang
        aadhar_data["gender_female_lang"] = gender_female_lang

        img1 = Image.open(Path(template_path + "/Front.PNG"))
        img2 = Image.open(Path(template_path + "/Back.PNG"))

        image_editable = ImageDraw.Draw(img1)
        image_editable.text(
            (99, 50),
            convert_to_lang(aadhar_data["Name"], src="en", dest=dest_lang),
            (0, 0, 0),
            font=fnt,
        )
        image_editable.text((99, 65), aadhar_data["Name"], (0, 0, 0), font=fnt)
        image_editable.text(
            (99, 80),
            dob_lang + " /" + " DOB:" + aadhar_data["DOB"],
            (0, 0, 0),
            font=fnt,
        )
        image_editable.text(
            (99, 158), str(aadhar_data["Aadhar_No"]), (0, 0, 0), font=fnt2
        )

        if aadhar_data["Gender"] == "Male":
            image_editable.text(
                (99, 95),
                gender_male_lang + " / " + aadhar_data["Gender"],
                (0, 0, 0),
                font=fnt,
            )
        else:
            image_editable.text(
                (99, 95),
                gender_female_lang + " / " + aadhar_data["Gender"],
                (0, 0, 0),
                font=fnt,
            )

        image_editable = ImageDraw.Draw(img2)
        image_editable.text(
            (99, 158), str(aadhar_data["Aadhar_No"]), (0, 0, 0), font=fnt2
        )
        image_editable.text(
            (26, 54),
            "Address: S/O " + aadhar_data["Father_Name"] + ",",
            (0, 0, 0),
            font=fnt3,
        )

        image_editable.text(
            (26, 66), aadhar_data["Address1"] + ", ", (0, 0, 0), font=fnt3
        )
        # image_editable.text((26, 85),  str(aadhar_data['Address2']), (0, 0, 0), font=fnt3)

        if (
            aadhar_data["Address2"] is not np.nan
            and aadhar_data["Address3"] is not np.nan
        ):
            image_editable.text(
                (26, 78), str(aadhar_data["Address2"]) + ", ", (0, 0, 0), font=fnt3
            )
        elif aadhar_data["Address2"] is not np.nan:
            image_editable.text(
                (26, 78), str(aadhar_data["Address2"]), (0, 0, 0), font=fnt3
            )

        if (
            aadhar_data["Address3"] is not np.nan
            and aadhar_data["Address4"] is not np.nan
        ):
            image_editable.text(
                (26, 90), str(aadhar_data["Address3"]) + ", ", (0, 0, 0), font=fnt3
            )
        elif aadhar_data["Address3"] is not np.nan:
            image_editable.text(
                (26, 90), str(aadhar_data["Address3"]), (0, 0, 0), font=fnt3
            )

        if (
            aadhar_data["Address4"] is not np.nan
            and aadhar_data["Address5"] is not np.nan
        ):
            image_editable.text(
                (26, 102), str(aadhar_data["Address4"]) + ", ", (0, 0, 0), font=fnt3
            )
        elif aadhar_data["Address4"] is not np.nan:
            image_editable.text(
                (26, 102), str(aadhar_data["Address4"]), (0, 0, 0), font=fnt3
            )

        if aadhar_data["Address5"] is not np.nan:
            image_editable.text(
                (26, 114), str(aadhar_data["Address5"]), (0, 0, 0), font=fnt3
            )

        rgb_im1 = img1.convert("RGB")
        rgb_im1.save(save_path + "\\Front\\" + "Front_" + str(i) + ".JPG")

        rgb_im2 = img2.convert("RGB")
        rgb_im2.save(save_path + "\\Back\\" + "Back_" + str(i) + ".JPG")
