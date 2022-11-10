import googletrans
from googletrans import Translator
from ensure import ensure_annotations

@ensure_annotations
def convert_to_lang(text: str, src: str='en', dest: str='hi') -> str:
    '''
    Using google translation for translating to different indian languages

    :param text: text to be translated
    :param src: src language
    :param text: dest language
    :return: translated language

    '''
    translator = Translator()
    result = translator.translate(text, src=src, dest=dest)
    return result.text