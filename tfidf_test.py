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
from urllib2 import urlopen

import web_page_parser

def remove_punc(document_string):
	# removes punctuation from strings
	clean = re.sub(r"[!@#$%^&*()-=_+|;':\",.<>?']+", " ", document_string)
	return clean

urllist = [
'https://us.norton.com/internetsecurity-malware-what-is-a-computer-virus.html',
'https://www.avg.com/en/signal/what-is-a-computer-virus',
'https://blog.productcentral.aol.com/2012/08/14/what-are-computer-viruses'
]

# creates set containing one instance of every word that appears across the docs
wordSet = set()

for url in urllist:
	# opens web page
	html = urlopen(url).read()
	# gets body text from web pages and cleans up the text
	doc = remove_punc(web_page_parser.text_from_html(html).lower())
	# tokenizes words
	# 'bow' means 'bowl of words'
	bow = doc.split(' ')
	# removes empty strings
	bow = filter(None, bow)
	wordSet = wordSet.union(set(bow))

# gets body text from web pages and cleans up the text
docA = remove_punc(web_page_parser.text_from_html(urlopen(urllist[0]).read()).lower())
docB = remove_punc(web_page_parser.text_from_html(urlopen(urllist[1]).read()).lower())
docC = remove_punc(web_page_parser.text_from_html(urlopen(urllist[2]).read()).lower())

# tokenizes words
# 'bow' means 'bowl of words'
bowA = docA.split(' ')
bowB = docB.split(' ')
bowC = docC.split(' ')

# removes empty strings
bowA = filter(None, bowA)
bowB = filter(None, bowB)
bowC = filter(None, bowC)

# joins all the words together from each doc
# wordSet = set(bowA).union(set(bowB),set(bowC))

# create a dictionary containing the # of times
# a word appears in a doc, by default at first set to 0
wordDictA = dict.fromkeys(wordSet, 0)
wordDictB = dict.fromkeys(wordSet, 0)
wordDictC = dict.fromkeys(wordSet, 0)

def count_words(tokenized, word_dict):
	# counts number of times word appears in tokenized list
	# and iterates dictionary value by 1 for each count
	for word in tokenized:
		word_dict[word]+=1
	return word_dict

# runs count word function for content on each page
wordDictA = count_words(bowA, wordDictA)
wordDictB = count_words(bowB, wordDictB)
wordDictC = count_words(bowC, wordDictC)

def computeTF(wordDict, bow):
	# computes term frequency
	tfDict = {}
	bowCount = len(bow)
	for word, count in wordDict.iteritems():
		tfDict[word] = count / float(bowCount)
	return tfDict

# gets term frequency for each page
tfBowA = computeTF(wordDictA, bowA)
tfBowB = computeTF(wordDictB, bowB)
tfBowC = computeTF(wordDictC, bowC)

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
		idfDict[word] = math.log(N/float(val))

	return idfDict

# runs IDF on keyword count dicitonary for all pages
idfs = computeIDF([wordDictA, wordDictB, wordDictC])

def computeTFIDF(tfBow, idfs):
	# computes TF*IDF
	tfidf = {}
	for word, val in tfBow.iteritems():
		tfidf[word] = val * idfs[word]
	return tfidf

# get TF*IDF for all pages 
tfidfBowA = computeTFIDF(tfBowA, idfs)
tfidfBowB = computeTFIDF(tfBowB, idfs)
tfidfBowC = computeTFIDF(tfBowC, idfs)

# create dataframe for each TF*IDF for each page
df_one = pd.DataFrame.from_dict(tfidfBowA, orient='index', columns=[urllist[0]])
df_two = pd.DataFrame.from_dict(tfidfBowB, orient='index', columns=[urllist[1]])
df_three = pd.DataFrame.from_dict(tfidfBowC, orient='index', columns=[urllist[2]])

# join the dataframes together
full_df = pd.concat([df_one, df_two, df_three], axis=1, join='inner')
full_df['tfidf avg'] = full_df.mean(axis=1)
full_df['tfidf max'] = full_df[[urllist[0], urllist[1], urllist[2]]].max(axis=1)
#full_df['tfidf avg (used)'] = full_df[].mean(axis=1)

full_df.to_csv('output.csv', encoding='utf-8')