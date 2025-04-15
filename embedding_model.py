from gensim.models.fasttext import FastText
from gensim.test.utils import common_texts


combined_texts = common_texts.copy() 

f = open("./technique_text.txt", 'r')
my_text = eval(f.readline())
print(my_text)
print(type(my_text))

combined_texts.extend(my_text)  
model = FastText(vector_size=256, window=5, min_count=2, sample = 1e-2, workers=30, negative = 5)
model.build_vocab(corpus_iterable=combined_texts) 
model.train(corpus_iterable=combined_texts, total_examples=len(combined_texts), epochs=50)

model.save('./technique-embedding-256.model')