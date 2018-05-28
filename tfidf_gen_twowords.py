# -*- coding: utf-8 -*-

# Dataframe column headers:
# - Keywords - all columns below should be grouped by the keywords in this column
# - Documents - # of documents the keyword appears across
# - TF Total - Total term frequency for each keyword
# - TF*IDF avg (Used) - The average TFIDF for the keyword across all documents ONLY where that keyword is used
# - TF*IDF avg (All) - The average TFIDF for the keyword across all documents
# - TF*IDF max - The max TFIDF that appears in a single document

import math
import re
import pandas as pd
import urllib2
import requests

import web_page_parser
import google_parser

def remove_punc(document_string):
	# removes punctuation from strings
	clean = re.sub(r"[!@#$%^&*()-=_+|;':\",.<>?']+", " ", document_string)
	return clean

def url_request(url):
	req = requests.get(url, headers={'Accept': 'text/html,application/xhtml+xml,*/*',
										'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'})
	return req.text

def count_words(tokenized, word_dict):
	# counts number of times word appears in tokenized list
	# and iterates dictionary value by 1 for each count
	for word in tokenized:
		try:
			word_dict[word]+=1
		except KeyError:
			pass
	return word_dict

def computeTF(wordDict, bow):
	# computes term frequency
	tfDict = {}
	bowCount = len(bow)
	for word, count in wordDict.iteritems():
		tfDict[word] = count / float(bowCount)
	return tfDict

def computeIDF(docList):
	idfDict = {}
	N = len(docList)

	# counts the number of documents that contain a word w
	idfDict = dict.fromkeys(docList[0].keys(),0)
	for doc in docList:
		for word, val in doc.iteritems():
			if val > 0:
				idfDict[word] += 1

	# divide N by denominator above, take the log of that
	for word, val in idfDict.iteritems():
		if val > 0:
			idfDict[word] = math.log(N/float(val))
		else:
			idfDict[word] = 0

	return idfDict

def computeTFIDF(tfBow, idfs):
	# computes TF*IDF
	tfidf = {}
	for word, val in tfBow.iteritems():
		tfidf[word] = val * idfs[word]
	return tfidf

def avg_cond(c):
	avg_list = []
	for url in urllist:
		if c[url] > 0:
			avg_list.append(c[url])
	if len(avg_list) > 0:
		return sum(avg_list)/float(len(avg_list))
	else:
		return 0

def count_docs(c):
	count_list = []
	for url in urllist:
		if c[url] > 0:
			count_list.append(1)
	return len(count_list)

kywd = raw_input('What would you like to search?')

urllist = google_parser.generate_links(kywd)
print urllist

# creates set containing one instance of every word that appears across the docs
wordSet = set()

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
	wordSet = wordSet.union(set(bow))

wordDictList = []
for url in urllist:
	bowOne = remove_punc(web_page_parser.text_from_html(url_request(url)).lower()).split()
	bowOne = filter(None, [bowOne[i]+' '+bowOne[i+1] for i in range(len(bowOne)-1)])
	wordSetOne = dict.fromkeys(wordSet, 0)
	wordDict = count_words(bowOne, wordSetOne)
	wordDictList.append(wordDict)

idfs = computeIDF(wordDictList)

df_list = []
# gets body text from web pages and cleans up the text
for url in urllist:
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
full_df['tfidf max'] = full_df[urllist].max(axis=1)

file_name = kywd.replace(' ', '_')

full_df.to_csv(file_name + '.csv', encoding='utf-8')