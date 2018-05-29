# -*- coding: utf-8 -*-

import pandas as pd

import web_page_parser
import google_parser
import stop_words
from tf_func import remove_punc, url_request, count_words, computeTF, computeIDF, computeTFIDF

def avg_cond(c):
	avg_list = []
	for url in urllist_two:
		if c[url] > 0:
			avg_list.append(c[url])
	if len(avg_list) > 0:
		return sum(avg_list)/float(len(avg_list))
	else:
		return 0

def count_docs(c):
	count_list = []
	for url in urllist_two:
		if c[url] > 0:
			count_list.append(1)
	return len(count_list)

kywd = raw_input('What would you like to search?')
result_num = int(raw_input('How many results would you like?'))

urllist = google_parser.generate_links(kywd, result_num)
print urllist
print len(urllist)

# creates set containing one instance of every word that appears across the docs
wordSet = set()
urllist_two = []

for url in urllist:
	# opens web page
	html = url_request(url)
	# gets body text from web pages and cleans up the text
	doc = remove_punc(web_page_parser.text_from_html(html).lower())
	# tokenizes words
	# 'bow' means 'bowl of words'
	bow = doc.split(' ')
	# removes empty strings
	bow = filter(None, [bow[i]+' '+bow[i+1] for i in range(len(bow)-1)])
	print url, len(bow)
	if len(bow) > 50:
		urllist_two.append(url)
	wordSet = wordSet.union(set(bow))

print urllist_two

wordDictList = []
for url in urllist_two:
	bowOne = remove_punc(web_page_parser.text_from_html(url_request(url)).lower()).split()
	bowOne = filter(None, [bowOne[i]+' '+bowOne[i+1] for i in range(len(bowOne)-1)])
	wordSetOne = dict.fromkeys(wordSet, 0)
	wordDict = count_words(bowOne, wordSetOne)
	wordDictList.append(wordDict)

idfs = computeIDF(wordDictList)

df_list = []
# gets body text from web pages and cleans up the text
for url in urllist_two:
	bowTwo = remove_punc(web_page_parser.text_from_html(url_request(url)).lower()).split()
	bowTwo = filter(None, [bowTwo[i]+' '+bowTwo[i+1] for i in range(len(bowTwo)-1)])
	wordSetTwo = dict.fromkeys(wordSet, 0)
	wordDictTwo = count_words(bowTwo, wordSetTwo)
	tfBow = computeTF(wordDictTwo, bowTwo)
	tfidfBow = computeTFIDF(tfBow, idfs)
	df = pd.DataFrame.from_dict(tfidfBow, orient='index', columns=[url])
	df_list.append(df)


# join the dataframes together
full_df = pd.concat(df_list, axis=1, join='inner')

full_df['tfidf avg'] = full_df.mean(axis=1)
full_df['tfidf avg used'] = full_df.apply(avg_cond, axis=1)
full_df['docs with word'] = full_df.apply(count_docs, axis=1)
full_df['tfidf max'] = full_df[urllist_two].max(axis=1)

# removes additional stop words
for start_word in stop_words.begins:
	full_df.drop(full_df[full_df.index.str.startswith(start_word)].index, axis=0, inplace=True)

for end_word in stop_words.ends:
	full_df.drop(full_df[full_df.index.str.endswith(end_word)].index, axis=0, inplace=True)

file_name = kywd.replace(' ', '_')

full_df.to_csv(file_name + '2.csv', encoding='utf-8')