#!/bin/sh

#
# Install bazel 0.2.2b
#
wget https://github.com/bazelbuild/bazel/releases/download/0.2.2b/bazel-0.2.2b-installer-linux-x86_64.sh
chmod +x bazel-0.2.2b-installer-linux-x86_64.sh
./bazel-0.2.2b-installer-linux-x86_64.sh --user
rm bazel-0.2.2b-installer-linux-x86_64.sh

#
# SyntaxNet original version (installed as a normal user)
#
sudo apt-get -y install swig unzip
sudo pip install -U protobuf==3.0.0b2
sudo pip install asciitree
###
git clone --recursive https://github.com/tensorflow/models.git
cd models/syntaxnet/tensorflow
./configure < /dev/null  # no Google Cloud Platform support, no GPU support
cd ..
~/bin/bazel --output_user_root=bazel_root test syntaxnet/... util/utf8/...
# The --output_user_root ensures that all of the build output is
# stored within the syntaxnet directory. Otherwise bazel puts files
# in ~/.cache/bazel and makes ridiculous symlinks to it all over
# the place, making it difficult to keep all of the files together.

#
# Download pretrained models
#
cd syntaxnet/models/parsey_universal/
wget http://download.tensorflow.org/models/parsey_universal/Ancient_Greek-PROIEL.zip
wget http://download.tensorflow.org/models/parsey_universal/Ancient_Greek.zip
wget http://download.tensorflow.org/models/parsey_universal/Arabic.zip
wget http://download.tensorflow.org/models/parsey_universal/Basque.zip
wget http://download.tensorflow.org/models/parsey_universal/Bulgarian.zip
wget http://download.tensorflow.org/models/parsey_universal/Catalan.zip
wget http://download.tensorflow.org/models/parsey_universal/Chinese.zip
wget http://download.tensorflow.org/models/parsey_universal/Croatian.zip
wget http://download.tensorflow.org/models/parsey_universal/Czech-CAC.zip
wget http://download.tensorflow.org/models/parsey_universal/Czech-CLTT.zip
wget http://download.tensorflow.org/models/parsey_universal/Czech.zip
wget http://download.tensorflow.org/models/parsey_universal/Danish.zip
wget http://download.tensorflow.org/models/parsey_universal/Dutch-LassySmall.zip
wget http://download.tensorflow.org/models/parsey_universal/Dutch.zip
wget http://download.tensorflow.org/models/parsey_universal/English-LinES.zip
wget http://download.tensorflow.org/models/parsey_universal/English.zip
wget http://download.tensorflow.org/models/parsey_universal/Estonian.zip
wget http://download.tensorflow.org/models/parsey_universal/Finnish-FTB.zip
wget http://download.tensorflow.org/models/parsey_universal/Finnish.zip
wget http://download.tensorflow.org/models/parsey_universal/French.zip
wget http://download.tensorflow.org/models/parsey_universal/Galician.zip
wget http://download.tensorflow.org/models/parsey_universal/German.zip
wget http://download.tensorflow.org/models/parsey_universal/Gothic.zip
wget http://download.tensorflow.org/models/parsey_universal/Greek.zip
wget http://download.tensorflow.org/models/parsey_universal/Hebrew.zip
wget http://download.tensorflow.org/models/parsey_universal/Hindi.zip
wget http://download.tensorflow.org/models/parsey_universal/Hungarian.zip
wget http://download.tensorflow.org/models/parsey_universal/Indonesian.zip
wget http://download.tensorflow.org/models/parsey_universal/Irish.zip
wget http://download.tensorflow.org/models/parsey_universal/Italian.zip
wget http://download.tensorflow.org/models/parsey_universal/Kazakh.zip
wget http://download.tensorflow.org/models/parsey_universal/Latin-ITTB.zip
wget http://download.tensorflow.org/models/parsey_universal/Latin-PROIEL.zip
wget http://download.tensorflow.org/models/parsey_universal/Latin.zip
wget http://download.tensorflow.org/models/parsey_universal/Latvian.zip
wget http://download.tensorflow.org/models/parsey_universal/Norwegian.zip
wget http://download.tensorflow.org/models/parsey_universal/Old_Church_Slavonic.zip
wget http://download.tensorflow.org/models/parsey_universal/Persian.zip
wget http://download.tensorflow.org/models/parsey_universal/Polish.zip
wget http://download.tensorflow.org/models/parsey_universal/Portuguese-BR.zip
wget http://download.tensorflow.org/models/parsey_universal/Portuguese.zip
wget http://download.tensorflow.org/models/parsey_universal/Romanian.zip
wget http://download.tensorflow.org/models/parsey_universal/Russian-SynTagRus.zip
wget http://download.tensorflow.org/models/parsey_universal/Russian.zip
wget http://download.tensorflow.org/models/parsey_universal/Slovenian-SST.zip
wget http://download.tensorflow.org/models/parsey_universal/Slovenian.zip
wget http://download.tensorflow.org/models/parsey_universal/Spanish-AnCora.zip
wget http://download.tensorflow.org/models/parsey_universal/Spanish.zip
wget http://download.tensorflow.org/models/parsey_universal/Swedish-LinES.zip
wget http://download.tensorflow.org/models/parsey_universal/Swedish.zip
wget http://download.tensorflow.org/models/parsey_universal/Tamil.zip
wget http://download.tensorflow.org/models/parsey_universal/Turkish.zip
for file in *.zip
do
    unzip $file
done
rm *.zip
cd ../../..

#
# Test models
#
cp syntaxnet/models/parsey_universal/*.sh .
echo 'Bob brought the pizza to Alice.' | bash parse.sh syntaxnet/models/parsey_universal/English 2> /dev/null
echo '球 從 天上 掉 下來' | bash parse.sh syntaxnet/models/parsey_universal/Chinese 2> /dev/null
echo '球從天上掉下來' | bash tokenize_zh.sh syntaxnet/models/parsey_universal/Chinese 2> /dev/null
