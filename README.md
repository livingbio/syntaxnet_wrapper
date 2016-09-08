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

```python
from syntaxnet_wrapper import SyntaxNetTagger, SyntaxNetParser

tag = SyntaxNetTagger()  # 'English' is the default model
print tag.query('this is a good day', returnRaw=True)
# 1       this    _       DET     DT      _       0       _       _       _
# 2       is      _       VERB    VBZ     _       0       _       _       _
# 3       a       _       DET     DT      _       0       _       _       _
# 4       good    _       ADJ     JJ      _       0       _       _       _
# 5       day     _       NOUN    NN      _       0       _       _       _
tag.query('this is a good day')  # in default, return splitted text

par = SyntaxNetParser(tagger=tag)  # use existing tagger object
par = SyntaxNetParser()     # or create a new tagger object inside
print par.query('Alice drove down the street in her car', returnRaw=True)
# 1       Alice   _       NOUN    NNP     _       2       nsubj   _       _
# 2       drove   _       VERB    VBD     _       0       ROOT    _       _
# 3       down    _       ADP     IN      _       2       prep    _       _
# 4       the     _       DET     DT      _       5       det     _       _
# 5       street  _       NOUN    NN      _       3       pobj    _       _
# 6       in      _       ADP     IN      _       2       prep    _       _
# 7       her     _       PRON    PRP$    _       8       poss    _       _
# 8       car     _       NOUN    NN      _       6       pobj    _       _

# use Chinese model
tag = SyntaxNetTagger('Chinese')
par = SyntaxNetParser('Chinese', tagger=tag)

print tag.query(u'今天 天氣 很 好', returnRaw=True)
# 1       今天    _       NOUN    NN      _       0       _       _       _
# 2       天氣    _       NOUN    NN      _       0       _       _       _
# 3       很      _       ADV     RB      _       0       _       _       _
# 4       好      _       ADJ     JJ      _       0       _       _       _

print par.query(u'今天 天氣 很 好', returnRaw=True)
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
tag.list_models()
# ['Ancient_Greek',
#  'Ancient_Greek-PROIEL',
#  'Arabic',
#  'Basque',
#  'Bulgarian',
#  'Catalan',
#  'Chinese',
#  'Croatian',
#  'Czech',
#  'Czech-CAC',
#  'Czech-CLTT',
#  'Danish',
#  'Dutch',
#  'Dutch-LassySmall',
#  'English',
#  'English-LinES',
#  'English-Parsey',
#  'Estonian',
#  'Finnish',
#  'Finnish-FTB',
#  'French',
#  'Galician',
#  'German',
#  'Gothic',
#  'Greek',
#  'Hebrew',
#  'Hindi',
#  'Hungarian',
#  'Indonesian',
#  'Irish',
#  'Italian',
#  'Kazakh',
#  'Latin',
#  'Latin-ITTB',
#  'Latin-PROIEL',
#  'Latvian',
#  'Norwegian',
#  'Old_Church_Slavonic',
#  'Persian',
#  'Polish',
#  'Portuguese',
#  'Portuguese-BR',
#  'Romanian',
#  'Russian',
#  'Russian-SynTagRus',
#  'Slovenian',
#  'Slovenian-SST',
#  'Spanish',
#  'Spanish-AnCora',
#  'Swedish',
#  'Swedish-LinES',
#  'Tamil',
#  'Turkish']
```
