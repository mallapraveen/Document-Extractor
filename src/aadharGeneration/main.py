from aadhar_generation import create_small_aadhar, create_big_aadhar
from generate_data import generate_data
from address_generation import address_generation
from get_image_coordinates import get_coordinates
import random, warnings
from constants import config
from aadharGeneration import logger
from language_translation import convert_to_lang

warnings.filterwarnings("ignore")

if __name__ == "__main__":

    logger.info("Script Started")

    # generate_data(5)
    # address_generation(5)
    # get_coordinates('../input/templates/Aadhar/Front_Long.png')

    # dest_lang = random.choice(list(config.languages.keys()))
    # name_in_lang = convert_to_lang('malla praveen', src='en', dest='hi')
    # print(name_in_lang)

    create_big_aadhar(10, config.template_path, config.images_path)
    create_small_aadhar(10, config.template_path, config.images_path)

    logger.info("Script Ended")
