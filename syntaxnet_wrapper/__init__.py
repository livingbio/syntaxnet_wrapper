# from .syntaxnet_class import SyntaxNetParser as WrapParser
# from .syntaxnet_class import SyntaxNetTagger as WrapTagger
from .dragnn_class import DragnnParser as WrapParser

__all__ = ['parser', 'language_code_to_model_name', 'parse_text']

# reference: https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
language_code_to_model_name = {
    'ar': 'Arabic',
    'eu': 'Basque',
    'bg': 'Bulgarian',
    'ca': 'Catalan',
    'zh': 'Chinese',
    'zh-tw': 'Chinese',
    'zh-cn': 'Chinese',
    'hr': 'Croatian',
    'cs': 'Czech',
    'da': 'Danish',
    'nl': 'Dutch',
    'en': 'English',
    'et': 'Estonian',
    'fi': 'Finnish',
    'fr': 'French',
    'gl': 'Galician',
    'de': 'German',
    'el': 'Greek',
    'iw': 'Hebrew',
    'hi': 'Hindi',
    'hu': 'Hungarian',
    'id': 'Indonesian',
    'ga': 'Irish',
    'ja': 'Japanese',
    'it': 'Italian',
    'kk': 'Kazakh',
    'ko': 'Korean',
    'la': 'Latin',
    'lv': 'Latvian',
    'no': 'Norwegian-Bokmaal',
    'fa': 'Persian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sl': 'Slovenian',
    'es': 'Spanish',
    'sv': 'Swedish',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'vi': 'Vietnamese',
}


class Parser(object):
    cached = {}

    def __del__(self):
        for code in self.cached:
            tmp = self.cached[code]
            self.cached[code] = None
            del tmp

    def __getitem__(self, code):
        if code not in language_code_to_model_name:
            raise ValueError('Invalid language code for parser: {}'.format(code))
        lang = language_code_to_model_name[code]
        if code in self.cached:
            return self.cached[code]
        self.cached[code] = WrapParser(lang)
        return self.cached[code]


parser = Parser()


def parse_text(text, lang='en', returnRaw=True):
    lang = language_code_to_model_name[lang]
    parser = None
    try:
        parser = WrapParser(lang)
        result = parser.query(text, returnRaw)
        return result
    finally:
        del parser
