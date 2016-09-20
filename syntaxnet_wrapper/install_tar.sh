#!/bin/sh

if [ "$EUID" -eq 0 ]
then
# install open-jdk 8
add-apt-repository -y ppa:openjdk-r/ppa
apt-get -y update
apt-get -y install openjdk-8-jdk

# install tensorflow for python 2.7
export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow-0.10.0rc0-cp27-none-linux_x86_64.whl
pip install --upgrade $TF_BINARY_URL

# install python packages
sudo apt-get -y install swig unzip
pip install -U protobuf==3.0.0b2
pip install asciitree

fi

tar xvfz models.tgz
cp *.py models/syntaxnet/bazel-bin/syntaxnet/parser_eval.runfiles/

cd models/syntaxnet/syntaxnet/models/parsey_universal/
wget http://download.tensorflow.org/models/parsey_universal/Arabic.zip
wget http://download.tensorflow.org/models/parsey_universal/Basque.zip
wget http://download.tensorflow.org/models/parsey_universal/Bulgarian.zip
wget http://download.tensorflow.org/models/parsey_universal/Catalan.zip
wget http://download.tensorflow.org/models/parsey_universal/Chinese.zip
wget http://download.tensorflow.org/models/parsey_universal/Croatian.zip
wget http://download.tensorflow.org/models/parsey_universal/Czech.zip
wget http://download.tensorflow.org/models/parsey_universal/Danish.zip
wget http://download.tensorflow.org/models/parsey_universal/Dutch.zip
wget http://download.tensorflow.org/models/parsey_universal/English.zip
wget http://download.tensorflow.org/models/parsey_universal/Estonian.zip
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
wget http://download.tensorflow.org/models/parsey_universal/Latin.zip
wget http://download.tensorflow.org/models/parsey_universal/Latvian.zip
wget http://download.tensorflow.org/models/parsey_universal/Norwegian.zip
wget http://download.tensorflow.org/models/parsey_universal/Persian.zip
wget http://download.tensorflow.org/models/parsey_universal/Polish.zip
wget http://download.tensorflow.org/models/parsey_universal/Portuguese.zip
wget http://download.tensorflow.org/models/parsey_universal/Romanian.zip
wget http://download.tensorflow.org/models/parsey_universal/Russian.zip
wget http://download.tensorflow.org/models/parsey_universal/Slovenian.zip
wget http://download.tensorflow.org/models/parsey_universal/Spanish.zip
wget http://download.tensorflow.org/models/parsey_universal/Swedish.zip
wget http://download.tensorflow.org/models/parsey_universal/Tamil.zip
wget http://download.tensorflow.org/models/parsey_universal/Turkish.zip
for file in *.zip
do
    unzip $file
done
rm *.zip
cd ../../../../..
