all: download_language_models

configure_syntaxnet:
	@echo "************************************************************" 1>&2
	@echo "                  configure syntaxnet                       " 1>&2
	@echo "************************************************************" 1>&2
	rm -rf models
	git clone --recursive https://github.com/tensorflow/models.git
	rm -rf ~/tmp_syntaxnet
	mkdir -p ~/tmp_syntaxnet
	export TEST_TMPDIR=`cd ~/tmp_syntaxnet; pwd` && \
	virtualenv ~/tmp_syntaxnet/venv && \
	~/tmp_syntaxnet/venv/bin/pip install tensorflow && \
	cd models/syntaxnet/tensorflow && \
	printf "$$TEST_TMPDIR/venv/bin/python\n\n\n\n\n\n\n\n\n\n\n\n\n\n" | ./configure

build_syntaxnet: configure_syntaxnet
	@echo "************************************************************" 1>&2
	@echo "                     build syntaxnet                        " 1>&2
	@echo "************************************************************" 1>&2
	cd models/syntaxnet && \
	export TEST_TMPDIR=`cd ~/tmp_syntaxnet; pwd` && \
	bazel --output_user_root=bazel_root test syntaxnet/... util/utf8/... && \
	bazel build -c opt //dragnn/tools:parse-to-conll && \
	bazel build -c opt //examples/dragnn:tutorial_1 && \
	bazel build -c opt //examples/dragnn:tutorial_2
	cd models/syntaxnet && \
	rm tensorflow/util/python/python_lib && \
	ln -s `python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())"` tensorflow/util/python/python_lib
	@echo "************************************************************" 1>&2
	@echo "                building syntaxnet finished                 " 1>&2
	@echo "************************************************************" 1>&2

copy_demo_scripts: build_syntaxnet
	cp models/syntaxnet/syntaxnet/models/parsey_universal/parse.sh models/syntaxnet/parse.sh
	cp models/syntaxnet/syntaxnet/models/parsey_universal/tokenize.sh models/syntaxnet/tokenize.sh
	cp models/syntaxnet/syntaxnet/models/parsey_universal/tokenize_zh.sh models/syntaxnet/tokenize_zh.sh

clear_tmp_venv: copy_demo_scripts
	#rm -rf ~/tmp_syntaxnet
	mkdir -p pids && \
	chmod 777 pids
	@echo "************************************************************" 1>&2
	@echo "                 download language models                   " 1>&2
	@echo "************************************************************" 1>&2

download_language_models: \
	models/syntaxnet/syntaxnet/models/parsey_universal/Ancient_Greek-PROIEL \
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
	models/syntaxnet/syntaxnet/models/parsey_universal/Turkish \
	download_dragnn_model

models/syntaxnet/syntaxnet/models/parsey_universal/%: clear_tmp_venv
	cd models/syntaxnet/syntaxnet/models/parsey_universal/ && \
	wget http://download.tensorflow.org/models/parsey_universal/$*.zip && \
	unzip $*.zip && \
	cd $* && \
	chmod 644 * && \
	cd .. && \
	chmod 755 $* && \
	rm $*.zip

download_dragnn_model:
	cd models/syntaxnet/dragnn && \
	wget https://gliacloud.blob.core.windows.net/nlp/conll17.tar.gz && \
	tar xvfz conll17.tar.gz && \
	rm conll17.tar.gz
