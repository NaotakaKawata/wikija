# wikija

"wikija" is a Japanese wikification (Entity Linking) tool. Named Entity Recognition (NER) is performed on the input text, and wikipedia links can be added to the extracted named entities.



# Prerequisites

The operation of this software was confirmed under the following environment.

- Ubuntu==16.04

- Ruby==1.9.3

- Python==3.6

Used tool of virtual environment are [rbenv](https://github.com/rbenv/rbenv) and [Anaconda3](https://www.anaconda.com/distribution/). Author recommends to make virtual environment. Because the old tool like kyotocabinet is used. Therefore, the version dependencies are strong and you easy to fail to make virtual environment.



# Construction of Virtual Environment



## Ruby

```ruby
$ git clone https://github.com/sstephenson/rbenv.git ~/.rbenv

$ git clone https://github.com/sstephenson/ruby-build.git ~/.rbenv/plugins/ruby-build

$ echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.bashrc

$ echo 'eval "$(rbenv init -)"' >> ~/.bashrc

$ source ~/.bashrc

# make virtual environment
$ rbenv install 1.9.3-p551

$ rbenv rehash

# start virtual environment
$ rbenv global 1.9.3-p551
```



## Python

```shell
$ wget https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh

$ bash Anaconda3-2019.03-Linux-x86_64.sh

$ source ~/.bashrc

# make virtual environment
$ conda create -n wikification python=3.6

# start virtual environment
$ source activate wikification
```



# Installing

```shell
# Kyotocabinet
$ wget http://fallabs.com/kyotocabinet/pkg/kyotocabinet-1.2.76.tar.gz

$ tar zxvf kyotocabinet-1.2.76.tar.gz

$ cd kyotocabinet-1.2.76

$ ./configure

$ make

$ sudo make install

# Kyotocabinet-ruby
$ gem install kyotocabinet-ruby-reanimated

$ gem install mecab

$ gem install oj -v "2.12"

$ gem install levenshtein

# flair
$ pip install flair

# Mecab
$ pip install mecab

# Flask
$ pip install flask

#download model and dataset
$ bash download_data.sh
```

 # Train

```shell
$ python flair_train.py
```



# Test

```bash
# input sentences in "input.txt" and save
$ bash wikification_flair.sh
```

Also, You can confirm output in [localhost:5000](localhost:5000)



# License

MIT



# Author

Naotaka Kawata



# Reference

- [flair](https://github.com/flairNLP/flair)
- [jawikify](https://github.com/conditional/jawikify)

