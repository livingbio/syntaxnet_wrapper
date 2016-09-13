# A Python Wrapper for Google SyntaxNet

## Installation

### Install tensorflow

Please refer to [Download and Setup](https://www.tensorflow.org/versions/r0.10/get_started/os_setup.html)
page in TensorFlow documents. I choose the CPU version here.

```shell-script
# SyntaxNet only support Python 2.7, install tensorflow for Python 2.7
export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.10.0rc0-cp27-none-linux_x86_64.whl
pip install --upgrade $TF_BINARY_URL
```

### Checkout this repository

```shell-script
git clone git@github.com:livingbio/syntaxnet_wrapper.git
```

### Run installation script

```shell-script
cd syntaxnet_wrapper/syntaxnet_wrapper
sh install.sh
```

If everything is installed well, you should see following outputs:

```
1       Bob     _       PROPN   NNP     Number=Sing|fPOS=PROPN++NNP     2       nsubj   _  _
2       brought _       VERB    VBD     Mood=Ind|Tense=Past|VerbForm=Fin|fPOS=VERB++VBD 0  ROOT     _       _
3       the     _       DET     DT      Definite=Def|PronType=Art|fPOS=DET++DT  4       det__
4       pizza   _       NOUN    NN      Number=Sing|fPOS=NOUN++NN       2       dobj    _  _
5       to      _       ADP     IN      fPOS=ADP++IN    6       case    _       _
6       Alice.  _       PROPN   NNP     Number=Sing|fPOS=PROPN++NNP     2       nmod    _  _

1       球      _       PROPN   NNP     fPOS=PROPN++NNP 4       nsubj   _       _
2       從      _       ADP     IN      fPOS=ADP++IN    3       case    _       _
3       天上    _       NOUN    NN      fPOS=NOUN++NN   4       nmod    _       _
4       掉      _       VERB    VV      fPOS=VERB++VV   0       ROOT    _       _
5       下來    _       VERB    VV      fPOS=VERB++VV   4       mark    _       _

球 從天 上 掉 下 來
```


## Usage

Move to `syntaxnet_wrapper/` directory. You can use `ipython` to test it.

NOTE: at the first time you execute `query`, the model will be initialized,
that's cost some time.

```python
from syntaxnet_wrapper import tagger, parser

print tagger['en'].query('this is a good day', returnRaw=True)
# 1       this    _       DET     DT      _       0       _       _       _
# 2       is      _       VERB    VBZ     _       0       _       _       _
# 3       a       _       DET     DT      _       0       _       _       _
# 4       good    _       ADJ     JJ      _       0       _       _       _
# 5       day     _       NOUN    NN      _       0       _       _       _
tagger['en'].query('this is a good day')  # in default, return splitted text

print parser['en'].query('Alice drove down the street in her car', returnRaw=True)
# 1       Alice   _       NOUN    NNP     _       2       nsubj   _       _
# 2       drove   _       VERB    VBD     _       0       ROOT    _       _
# 3       down    _       ADP     IN      _       2       prep    _       _
# 4       the     _       DET     DT      _       5       det     _       _
# 5       street  _       NOUN    NN      _       3       pobj    _       _
# 6       in      _       ADP     IN      _       2       prep    _       _
# 7       her     _       PRON    PRP$    _       8       poss    _       _
# 8       car     _       NOUN    NN      _       6       pobj    _       _

# use Chinese model
print tagger['zh'].query(u'今天 天氣 很 好', returnRaw=True)
# 1       今天    _       NOUN    NN      _       0       _       _       _
# 2       天氣    _       NOUN    NN      _       0       _       _       _
# 3       很      _       ADV     RB      _       0       _       _       _
# 4       好      _       ADJ     JJ      _       0       _       _       _

print parser['zh'].query(u'今天 天氣 很 好', returnRaw=True)
# 1       今天    _       NOUN    NN      _       4       nmod:tmod       _       _
# 2       天氣    _       NOUN    NN      _       4       nsubj   _       _
# 3       很      _       ADV     RB      _       4       advmod  _       _
# 4       好      _       ADJ     JJ      _       0       ROOT    _       _
```

### Language Selection

The default model is `'English-Parsey'`. This is
[announced by Google](https://research.googleblog.com/2016/05/announcing-syntaxnet-worlds-most.html)
on May, 2016.
Other models, includes `'English'`, are trained by [Universal Dependencies](http://universaldependencies.org/),
[announced by Google](https://research.googleblog.com/2016/08/meet-parseys-cousins-syntax-for-40.html)
on August, 2016.

```python
from syntaxnet_wrapper import language_code_to_model_name
language_code_to_model_name
# {'ar': 'Arabic',
#  'bg': 'Bulgarian',
#  'ca': 'Catalan',
#  'cs': 'Czech',
#  'da': 'Danish',
#  'de': 'German',
#  'el': 'Greek',
#  'en': 'English-Parsey',
#  'en-uni': 'English',
#  'es': 'Spanish',
#  'et': 'Estonian',
#  'eu': 'Basque',
#  'fa': 'Persian',
#  'fi': 'Finnish',
#  'fr': 'French',
#  'ga': 'Irish',
#  'gl': 'Galician',
#  'hi': 'Hindi',
#  'hr': 'Croatian',
#  'hu': 'Hungarian',
#  'id': 'Indonesian',
#  'it': 'Italian',
#  'iw': 'Hebrew',
#  'kk': 'Kazakh',
#  'la': 'Latin',
#  'lv': 'Latvian',
#  'nl': 'Dutch',
#  'no': 'Norwegian',
#  'pl': 'Polish',
#  'pt': 'Portuguese',
#  'ro': 'Romanian',
#  'ru': 'Russian',
#  'sl': 'Slovenian',
#  'sv': 'Swedish',
#  'ta': 'Tamil',
#  'tr': 'Turkish',
#  'zh': 'Chinese',
#  'zh-cn': 'Chinese',
#  'zh-tw': 'Chinese'}
```