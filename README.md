# A Python Wrapper for Google SyntaxNet

## Installation

### Prerequisites

#### Minimum Disk Space Requirement

1. SyntaxNet sources: <100M
2. SyntaxNet/DRAGNN binaries: 1.5G
3. SyntaxNet models: 1.7G
4. DRAGNN models: 2.1G

#### Install OpenJDK8.

```shell-script
add-apt-repository -y ppa:openjdk-r/ppa
apt-get -y update
apt-get -y install openjdk-8-jdk
```

#### Install `bazel` and include `bazel` in `$PATH`.

**Note:** Only bazel 0.4.3 is runnable. bazel 0.4.4 may cause errors.

```shell-script
wget https://github.com/bazelbuild/bazel/releases/download/0.4.3/bazel-0.4.3-installer-linux-x86_64.sh
chmod +x bazel-0.4.3-installer-linux-x86_64.sh
./bazel-0.4.3-installer-linux-x86_64.sh --user
rm bazel-0.4.3-installer-linux-x86_64.sh
export PATH="$PATH:$HOME/bin"
```

#### Install system package dependencies.

```shell-script
apt-get -y install swig unzip
```

#### Install Python packages

**Note:** Current version of syntaxnet must be used with tensorflow r1.0.

```shell-script
pip install tensorflow protobuf asciitree mock
```

**Note:** Current version of DRAGNN must be used with tensorflow r1.1.0. Since r1.1.0 is not released yet, you can install [nightly binaries](https://github.com/tensorflow/tensorflow#installation).

Let's take linux version for Python 2.7 as an example:

```shell-script
wget https://ci.tensorflow.org/view/Nightly/job/nightly-matrix-cpu/TF_BUILD_IS_OPT=OPT,TF_BUILD_IS_PIP=PIP,TF_BUILD_PYTHON_VERSION=PYTHON2,label=cpu-slave/lastSuccessfulBuild/artifact/pip_test/whl/tensorflow-1.1.0rc1-cp27-none-linux_x86_64.whl
pip install tensorflow-1.1.0rc1-cp27-none-linux_x86_64.whl
```


#### Start Installing

```shell-script
pip install git+ssh://git@github.com/livingbio/syntaxnet_wrapper.git#egg=syntaxnet_wrapper
```

#### If installation failed...

Execute [test.sh](https://github.com/livingbio/syntaxnet_wrapper/blob/master/syntaxnet_wrapper/test.sh), you should see following outputs:

```
1       Bob     _       PROPN   NNP     Number=Sing|fPOS=PROPN++NNP     2       nsubj   _       _
2       brought _       VERB    VBD     Mood=Ind|Tense=Past|VerbForm=Fin|fPOS=VERB++VBD 0       ROOT    _ _
3       the     _       DET     DT      Definite=Def|PronType=Art|fPOS=DET++DT  4       det     _       _
4       pizza   _       NOUN    NN      Number=Sing|fPOS=NOUN++NN       2       dobj    _       _
5       to      _       ADP     IN      fPOS=ADP++IN    6       case    _       _
6       Alice.  _       PROPN   NNP     Number=Sing|fPOS=PROPN++NNP     2       nmod    _       _

1       球      _       PROPN   NNP     fPOS=PROPN++NNP 4       nsubj   _       _
2       從      _       ADP     IN      fPOS=ADP++IN    3       case    _       _
3       天上    _       NOUN    NN      fPOS=NOUN++NN   4       nmod    _       _
4       掉      _       VERB    VV      fPOS=VERB++VV   0       ROOT    _       _
5       下來    _       VERB    VV      fPOS=VERB++VV   4       mark    _       _

球 從天 上 掉 下 來
```

If the outputs are correct, problems are caused by the wrapper. If the outputs are wrong, compilation of syntaxnet may be failed.

## Usage

```python
from syntaxnet_wrapper import parser

print parser['en'].query('Alice drove down the street in her car', returnRaw=True)
# 1       Alice   _       ADV     RB      _       2       nsubj   _       _
# 2       drove   _       VERB    VB      _       0       root    _       _
# 3       down    _       ADP     RP      _       2       compound:prt    _       _
# 4       the     _       DET     DT      _       5       det     _       _
# 5       street  _       NOUN    NN      _       2       obj     _       _
# 6       in      _       ADP     IN      _       8       case    _       _
# 7       her     _       PRON    PRP$    _       8       nmod:poss       _       _
# 8       car     _       NOUN    NN      _       5       nmod    _       _

# use Chinese model
print parser['zh'].query(u'今天 天氣 很 好', returnRaw=True)
# 1       今天    _       NOUN    NN      fPOS=NOUN++NN   4       nmod:tmod       _       _
# 2       天氣    _       NOUN    NN      fPOS=NOUN++NN   4       nsubj   _       _
# 3       很      _       ADV     RB      fPOS=ADV++RB    4       advmod  _       _
# 4       好      _       ADJ     JJ      fPOS=ADJ++JJ    0       ROOT    _       _
```

### Language Selection

DRAGNN framework was [announced by Google](https://research.googleblog.com/2017/03/an-upgrade-to-syntaxnet-new-models-and.html) on March, 2017. These models were downloaded form [here](https://drive.google.com/file/d/0BxpbZGYVZsEeSFdrUnBNMUp1YzQ/view?usp=sharing).

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
#  'en': 'English',
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
#  'ja': 'Japanese',
#  'kk': 'Kazakh',
#  'ko': 'Korean',
#  'la': 'Latin',
#  'lv': 'Latvian',
#  'nl': 'Dutch',
#  'no': 'Norwegian-Bokmaal',
#  'pl': 'Polish',
#  'pt': 'Portuguese',
#  'ro': 'Romanian',
#  'ru': 'Russian',
#  'sl': 'Slovenian',
#  'sv': 'Swedish',
#  'tr': 'Turkish',
#  'uk': 'Ukrainian',
#  'vi': 'Vietnamese',
#  'zh': 'Chinese',
#  'zh-cn': 'Chinese',
#  'zh-tw': 'Chinese'}
```
