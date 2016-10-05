
all: models/syntaxnet/syntaxnet/models/parsey_universal/Ancient_Greek-PROIEL \
	models/syntaxnet/syntaxnet/models/parsey_universal/Ancient_Greek \
	models/syntaxnet/syntaxnet/models/parsey_universal/Arabic \
	models/syntaxnet/syntaxnet/models/parsey_universal/Basque \
	models/syntaxnet/syntaxnet/models/parsey_universal/Bulgarian \
	models/syntaxnet/syntaxnet/models/parsey_universal/Catalan \
	models/syntaxnet/syntaxnet/models/parsey_universal/Chinese \
	models/syntaxnet/syntaxnet/models/parsey_universal/Croatian \
	models/syntaxnet/syntaxnet/models/parsey_universal/Czech-CAC \
	models/syntaxnet/syntaxnet/models/parsey_universal/Czech-CLTT \
	models/syntaxnet/syntaxnet/models/parsey_universal/Czech \
	models/syntaxnet/syntaxnet/models/parsey_universal/Danish \
	models/syntaxnet/syntaxnet/models/parsey_universal/Dutch-LassySmall \
	models/syntaxnet/syntaxnet/models/parsey_universal/Dutch \
	models/syntaxnet/syntaxnet/models/parsey_universal/English-LinES \
	models/syntaxnet/syntaxnet/models/parsey_universal/English \
	models/syntaxnet/syntaxnet/models/parsey_universal/Estonian \
	models/syntaxnet/syntaxnet/models/parsey_universal/Finnish-FTB \
	models/syntaxnet/syntaxnet/models/parsey_universal/Finnish \
	models/syntaxnet/syntaxnet/models/parsey_universal/French \
	models/syntaxnet/syntaxnet/models/parsey_universal/Galician \
	models/syntaxnet/syntaxnet/models/parsey_universal/German \
	models/syntaxnet/syntaxnet/models/parsey_universal/Gothic \
	models/syntaxnet/syntaxnet/models/parsey_universal/Greek \
	models/syntaxnet/syntaxnet/models/parsey_universal/Hebrew \
	models/syntaxnet/syntaxnet/models/parsey_universal/Hindi \
	models/syntaxnet/syntaxnet/models/parsey_universal/Hungarian \
	models/syntaxnet/syntaxnet/models/parsey_universal/Indonesian \
	models/syntaxnet/syntaxnet/models/parsey_universal/Irish \
	models/syntaxnet/syntaxnet/models/parsey_universal/Italian \
	models/syntaxnet/syntaxnet/models/parsey_universal/Kazakh \
	models/syntaxnet/syntaxnet/models/parsey_universal/Latin-ITTB \
	models/syntaxnet/syntaxnet/models/parsey_universal/Latin-PROIEL \
	models/syntaxnet/syntaxnet/models/parsey_universal/Latin \
	models/syntaxnet/syntaxnet/models/parsey_universal/Latvian \
	models/syntaxnet/syntaxnet/models/parsey_universal/Norwegian \
	models/syntaxnet/syntaxnet/models/parsey_universal/Old_Church_Slavonic \
	models/syntaxnet/syntaxnet/models/parsey_universal/Persian \
	models/syntaxnet/syntaxnet/models/parsey_universal/Polish \
	models/syntaxnet/syntaxnet/models/parsey_universal/Portuguese-BR \
	models/syntaxnet/syntaxnet/models/parsey_universal/Portuguese \
	models/syntaxnet/syntaxnet/models/parsey_universal/Romanian \
	models/syntaxnet/syntaxnet/models/parsey_universal/Russian-SynTagRus \
	models/syntaxnet/syntaxnet/models/parsey_universal/Russian \
	models/syntaxnet/syntaxnet/models/parsey_universal/Slovenian-SST \
	models/syntaxnet/syntaxnet/models/parsey_universal/Slovenian \
	models/syntaxnet/syntaxnet/models/parsey_universal/Spanish-AnCora \
	models/syntaxnet/syntaxnet/models/parsey_universal/Spanish \
	models/syntaxnet/syntaxnet/models/parsey_universal/Swedish-LinES \
	models/syntaxnet/syntaxnet/models/parsey_universal/Swedish \
	models/syntaxnet/syntaxnet/models/parsey_universal/Tamil \
	models/syntaxnet/syntaxnet/models/parsey_universal/Turkish

models: 
	git clone --recursive https://github.com/tensorflow/models.git && \
	cd models && \
	git checkout f98c5ded31d7da0c2d127c28b2c16f0307a368f0 && \
	git submodule update && \
	cd models/syntaxnet/tensorflow && \
	git clean -fd && \
	./configure < /dev/null 

models/syntaxnet/bazel_root: models
	cd models/syntaxnet && \
    	~/bin/bazel --output_user_root=bazel_root test syntaxnet/... util/utf8/... || \
	rm -rf bazel_root

models/syntaxnet/parse.sh: models
	cp models/syntaxnet/syntaxnet/models/parsey_universal/parse.sh models/syntaxnet/parse.sh

models/syntaxnet/tokenize.sh: models
	cp models/syntaxnet/syntaxnet/models/parsey_universal/tokenize.sh models/syntaxnet/tokenize.sh

models/syntaxnet/tokenize_zh.sh: models
	cp models/syntaxnet/syntaxnet/models/parsey_universal/tokenize_zh.sh models/syntaxnet/tokenize_zh.sh

models/syntaxnet/syntaxnet/models/parsey_universal/%: models/syntaxnet/bazel_root models/syntaxnet/parse.sh models/syntaxnet/tokenize.sh models/syntaxnet/tokenize_zh.sh
	cd models/syntaxnet/syntaxnet/models/parsey_universal/ && \
    	wget http://download.tensorflow.org/models/parsey_universal/$*.zip && \
    	unzip $*.zip && \
    	rm $*.zip


