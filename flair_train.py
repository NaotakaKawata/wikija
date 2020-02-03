from flair.datasets import ColumnCorpus
from flair.embeddings import StackedEmbeddings, FlairEmbeddings
from flair.data import Sentence
from flair.models import SequenceTagger
from flair.trainers import ModelTrainer

columns = {0: 'text', 1: 'ner'}
data_folder = '.'
corpus = ColumnCorpus(data_folder, columns,
                      train_file='data/ja.wikipedia.conll')

tag_type = 'ner'
tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)

embedding_types = [
    FlairEmbeddings('ja-forward'),
    FlairEmbeddings('ja-backward'),
]
embeddings = StackedEmbeddings(embeddings=embedding_types)

tagger = SequenceTagger(hidden_size=256,
                        embeddings=embeddings,
                        tag_dictionary=tag_dictionary,
                        tag_type=tag_type,
                        use_crf=True)

trainer = ModelTrainer(tagger, corpus)
trainer.train("output",
              learning_rate=0.1,
              mini_batch_size=32,
              max_epochs=150,
              embeddings_storage_mode="none")
