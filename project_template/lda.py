import json
import urllib2
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from stop_words import get_stop_words
from gensim import corpora, models
import gensim
import time
import pickle
from threading import Thread
from itertools import islice

def chunks(data, size):
    it = iter(data)
    for i in xrange(0, len(data), size):
        yield {k:data[k] for k in islice(it, size)}

tokenizer = RegexpTokenizer(r'\w+')
lda_tokenizer = RegexpTokenizer(r'\b[a-z]+\b')
en_stopwords = get_stop_words('en')
stemmer = PorterStemmer()

data = {}
with open('../data/filtered_sf_reviews.json', 'r') as in_file:
	data = json.load(in_file)

def partition(data, size=500):
	partitions = []
	for item in chunks(data, size):
		partitions.append(item)
	return partitions

def lda_reviews((data, thread_id)):
	reviews_data = data
	results = {}
	start = time.time()
	counter = 0
	for k, v in reviews_data.iteritems():

		v = [[stemmer.stem(i) for i in tokenizer.tokenize(r.lower()) if not i in en_stopwords] for r in v]
		dictionary = corpora.Dictionary(v)
		corpus = [dictionary.doc2bow(r) for r in v]
		ldamodel = gensim.models.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=50)
		lda_output = ldamodel.show_topics(num_topics=5, num_words=3)
		
		topics = []
		for i in lda_output:
			topics.extend(lda_tokenizer.tokenize(i[1]))
		# print(topics)
		results[k] = topics
		counter += 1

		time.sleep(1)

	out_file = open("../pickles/review_topics_"+str(thread_id)+".pickle", 'wb')
	pickle.dump(results, out_file)
	out_file.close()
	
	# # time_elapsed = time.time() - start
	# # print("---------------Thread #" + str(thread_id)+"DONE! TIME ELAPSED:"+str(time_elapsed)+"-------------")
	# return results



# def threaded_function((data, file_id)):
# 	results = lda_reviews(file_id, data)
	

if __name__=='__main__':
	partitions = partition(data)
	
	counter = len(partitions)
	threads = []
	start = time.time()
	for i in range(counter):
		thread = Thread(target=lda_reviews, args=((partitions[i], i), ))
		thread.start()
		threads.append(thread)

	for t in threads:
		t.join()

	time_elapsed = time.time() - start
	print(str(time_elapsed))

	# start = time.time()
	# lda_reviews((partition(data, size=20)[0], 2))
	# time_elapsed = time.time() - start
	# print(str(time_elapsed))



