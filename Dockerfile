from gliacloud/base_images:django

run apt-get install python-software-properties software-properties-common python-software-properties  -y

RUN echo "deb http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main" | tee -a /etc/apt/sources.list
RUN echo "deb-src http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main" | tee -a /etc/apt/sources.list
RUN echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys EEA14886 && apt-get update && apt-get install -y curl dnsutils oracle-java8-installer ca-certificates


# install latest bazel 
# run echo "deb [arch=amd64] http://storage.googleapis.com/bazel-apt stable jdk1.8" | tee /etc/apt/sources.list.d/bazel.list
# run curl https://bazel.build/bazel-release.pub.gpg | apt-key add -
# run apt-get update && apt-get install -y bazel

run pip install virtualenv

add . /work
workdir /work
run wget https://github.com/bazelbuild/bazel/releases/download/0.4.0/bazel-0.4.0-installer-linux-x86_64.sh && chmod +x bazel-0.4.0-installer-linux-x86_64.sh && ./bazel-0.4.0-installer-linux-x86_64.sh
run python setup.py install
