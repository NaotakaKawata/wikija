# wikija

「wikija」は日本語wikification(Entity Linking)ツールである。入力された文章に対して固有表現認識(NER)を行い、抽出された固有表現に対してwikipediaのリンクを付与することができる。



# 必要条件

本ソフトウェアは以下の環境で動作確認を行った。

- Ubuntu==16.04

- Ruby==1.9.3

- Python==3.6



環境構築にはRubyは[rbenv](https://github.com/rbenv/rbenv)、Pythonは[Anaconda3](https://www.anaconda.com/distribution/)を用いている。kyotocabinetのように古いツールを使っている関係で、バージョンの依存関係が非常に強く、環境構築に失敗する可能性を考慮して、仮想環境での実行を強く薦める。



# 仮想環境の構築



## Ruby

```ruby
$ git clone https://github.com/sstephenson/rbenv.git ~/.rbenv
$ git clone https://github.com/sstephenson/ruby-build.git ~/.rbenv/plugins/ruby-build
$ echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.bashrc
$ echo 'eval "$(rbenv init -)"' >> ~/.bashrc
$ source ~/.bashrc

#仮想環境の作成
$ rbenv install 1.9.3-p551
$ rbenv rehash

#仮想環境の立ち上げ
$ rbenv global 1.9.3-p551
```



## Python

```shell
$ wget https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh
$ bash Anaconda3-2019.03-Linux-x86_64.sh
$ source ~/.bashrc

#仮想環境の作成
$ conda create -n wikification python=3.6

#仮想環境の立ち上げ
$ source activate wikification
```



# インストール

```shell
#Kyotocabinetのインストール
$ wget http://fallabs.com/kyotocabinet/pkg/kyotocabinet-1.2.76.tar.gz
$ tar zxvf kyotocabinet-1.2.76.tar.gz
$ cd kyotocabinet-1.2.76
$ ./configure
$ make
$ sudo make install

#Kyotocabinet-rubyのインストール
$ gem install kyotocabinet-ruby-reanimated
$ gem install mecab
$ gem install oj
$ gem install levenshtein

#flairのインストール
pip install flair

#インストールに失敗する場合
pip install --upgrade git+https://github.com/zalandoresearch/flair.git

#形態素解析ツールMecabのインストール
$ pip install mecab

#ブラウザ操作用ツールFlaskのインストール
$ pip install flask

$ bash download_data.sh
```



# 学習

```shell
$ python flair_train.py
```



# テスト

```bash
#任意の文章をinput.txtに入力して保存
$ bash wikification_flair.sh
```

実行後、[localhost:5000](localhost:5000)で出力結果の確認ができる。



# ライセンス

MIT



# 著者

Naotaka Kawata



# 参考文献

- [flair](https://github.com/flairNLP/flair)
- [jawikify](https://github.com/conditional/jawikify)

