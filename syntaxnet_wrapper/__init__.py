from .syntaxnet_class import SyntaxNetParser, SyntaxNetTagger

__all__ = ['parser', 'tagger', 'language_code_to_model_name', 'parse_text', 'tag_text']

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
    'en': 'English-Parsey',
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
    'it': 'Italian',
    'kk': 'Kazakh',
    'la': 'Latin',
    'lv': 'Latvian',
    'no': 'Norwegian',
    'fa': 'Persian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sl': 'Slovenian',
    'es': 'Spanish',
    'sv': 'Swedish',
    'ta': 'Tamil',
    'tr': 'Turkish',
}


class Tagger(object):
    cached = {}

    def __del__(self):
        for code in self.cached:
            tmp = self.cached[code]
            self.cached[code] = None
            del tmp

    def __getitem__(self, code):
        if code not in language_code_to_model_name:
            raise ValueError(
                'Invalid language code for tagger: {}'.format(code))
        lang = language_code_to_model_name[code]
        if code in self.cached:
            return self.cached[code]
        self.cached[code] = SyntaxNetTagger(lang)
        return self.cached[code]


tagger = Tagger()


class Parser(object):
    cached = {}

    def __del__(self):
        for code in self.cached:
            tmp = self.cached[code]
            self.cached[code] = None
            del tmp

    def __getitem__(self, code):
        if code not in language_code_to_model_name:
            raise ValueError(
                'Invalid language code for parser: {}'.format(code))
        lang = language_code_to_model_name[code]
        if code in self.cached:
            return self.cached[code]
        self.cached[code] = SyntaxNetParser(lang, tagger=tagger[code])
        return self.cached[code]


parser = Parser()


def parse_text(text, lang='en', returnRaw=True):
    lang = language_code_to_model_name[lang]
    tagger, parser = None, None
    try:
        tagger = SyntaxNetTagger(lang)
        parser = SyntaxNetParser(lang, tagger=tagger)
        result = parser.query(text, returnRaw)
        return result
    finally:
        del tagger, parser


def tag_text(text, lang='en', returnRaw=True):
    lang = language_code_to_model_name[lang]
    tagger = None
    try:
        tagger = SyntaxNetTagger(lang)
        result = tagger.query(text, returnRaw)
        return result
    finally:
        del tagger
