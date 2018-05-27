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

# opens web page
html_one = urlopen('https://us.norton.com/internetsecurity-malware-what-is-a-computer-virus.html').read()
html_two = urlopen('https://www.avg.com/en/signal/what-is-a-computer-virus').read()
html_three = urlopen('https://blog.productcentral.aol.com/2012/08/14/what-are-computer-viruses').read()

# gets body text from web pages and cleans up the text
docA = remove_punc(web_page_parser.text_from_html(html_one).lower())
docB = remove_punc(web_page_parser.text_from_html(html_two).lower())
docC = remove_punc(web_page_parser.text_from_html(html_three).lower())


bowA = docA.split(' ')
bowB = docB.split(' ')
bowC = docC.split(' ')

bowA = filter(None, bowA)
bowB = filter(None, bowB)
bowC = filter(None, bowC)

wordSet = set(bowA).union(set(bowB),set(bowC))

wordDictA = dict.fromkeys(wordSet, 0)
wordDictB = dict.fromkeys(wordSet, 0)
wordDictC = dict.fromkeys(wordSet, 0)

def count_words(tokenized, word_dict):
	for word in tokenized:
		word_dict[word]+=1
	return word_dict

wordDictA = count_words(bowA, wordDictA)
wordDictB = count_words(bowB, wordDictB)
wordDictC = count_words(bowC, wordDictC)

def computeTF(wordDict, bow):
	tfDict = {}
	bowCount = len(bow)
	for word, count in wordDict.iteritems():
		tfDict[word] = count / float(bowCount)
	return tfDict

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

idfs = computeIDF([wordDictA, wordDictB, wordDictC])

def computeTFIDF(tfBow, idfs):
	tfidf = {}
	for word, val in tfBow.iteritems():
		tfidf[word] = val * idfs[word]
	return tfidf

tfidfBowA = computeTFIDF(tfBowA, idfs)
tfidfBowB = computeTFIDF(tfBowB, idfs)
tfidfBowC = computeTFIDF(tfBowC, idfs)

df_one = pd.DataFrame.from_dict(tfBowA, orient='index')
df_two = pd.DataFrame.from_dict(tfBowB, orient='index')
df_three = pd.DataFrame.from_dict(tfBowC, orient='index')

full_df = pd.concat([df_one, df_two, df_three], axis=1, join='inner')

full_df.to_csv('output.csv', encoding='utf-8')