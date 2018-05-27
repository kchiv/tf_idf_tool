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

import web_page_parser

def remove_punc(document_string):
	# removes punctuation from strings
	clean = re.sub(r"[!@#$%^&*()-=_+|;':\",.<>?']+", " ", document_string)
	return clean

def url_request(url):
	req = urllib2.Request(url, headers={'Accept': 'text/html,application/xhtml+xml,*/*',"user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"})
	return urllib2.urlopen(req).read()

def count_words(tokenized, word_dict):
	# counts number of times word appears in tokenized list
	# and iterates dictionary value by 1 for each count
	for word in tokenized:
		word_dict[word]+=1
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
		idfDict[word] = math.log(N/float(val))

	return idfDict

def computeTFIDF(tfBow, idfs):
	# computes TF*IDF
	tfidf = {}
	for word, val in tfBow.iteritems():
		tfidf[word] = val * idfs[word]
	return tfidf

def avg_cond(c):
	avg_list = []
	if c[urllist[0]] > 0:
		avg_list.append(c[urllist[0]])
	if c[urllist[1]] > 0:
		avg_list.append(c[urllist[1]])
	if c[urllist[2]] > 0:
		avg_list.append(c[urllist[2]])
	if c[urllist[3]] > 0:
		avg_list.append(c[urllist[3]])
	if c[urllist[4]] > 0:
		avg_list.append(c[urllist[4]])
	if c[urllist[5]] > 0:
		avg_list.append(c[urllist[5]])
	if c[urllist[6]] > 0:
		avg_list.append(c[urllist[6]])
	if c[urllist[7]] > 0:
		avg_list.append(c[urllist[7]])
	if c[urllist[8]] > 0:
		avg_list.append(c[urllist[8]])
	if c[urllist[9]] > 0:
		avg_list.append(c[urllist[9]])
	if len(avg_list) > 0:
		return sum(avg_list)/float(len(avg_list))
	else:
		return 0

def count_docs(c):
	count_list = []
	if c[urllist[0]] > 0:
		count_list.append(1)
	if c[urllist[1]] > 0:
		count_list.append(1)
	if c[urllist[2]] > 0:
		count_list.append(1)
	if c[urllist[3]] > 0:
		count_list.append(1)
	if c[urllist[4]] > 0:
		count_list.append(1)
	if c[urllist[5]] > 0:
		count_list.append(1)
	if c[urllist[6]] > 0:
		count_list.append(1)
	if c[urllist[7]] > 0:
		count_list.append(1)
	if c[urllist[8]] > 0:
		count_list.append(1)
	if c[urllist[9]] > 0:
		count_list.append(1)
	return len(count_list)

urllist = [
'https://us.norton.com/internetsecurity-malware-what-is-a-computer-virus.html',
'https://www.avg.com/en/signal/what-is-a-computer-virus',
'https://blog.productcentral.aol.com/2012/08/14/what-are-computer-viruses',
'https://en.wikipedia.org/wiki/Computer_virus',
'https://economictimes.indiatimes.com/definition/computer-virus',
'http://www.youngupstarts.com/2016/04/14/9-types-of-computer-viruses-that-you-should-know-about-and-how-to-avoid-them/',
'http://www.allaboutcookies.org/security/computer-viruses.html',
'https://www.livescience.com/32619-how-does-a-virus-infect-your-computer.html',
'https://www.britannica.com/technology/computer-virus',
'https://antivirus.comodo.com/blog/computer-safety/what-is-virus-and-its-definition/'
]

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
	bow = filter(None, bow)
	wordSet = wordSet.union(set(bow))

# gets body text from web pages and cleans up the text
docA = remove_punc(web_page_parser.text_from_html(url_request(urllist[0])).lower())
docB = remove_punc(web_page_parser.text_from_html(url_request(urllist[1])).lower())
docC = remove_punc(web_page_parser.text_from_html(url_request(urllist[2])).lower())
docD = remove_punc(web_page_parser.text_from_html(url_request(urllist[3])).lower())
docE = remove_punc(web_page_parser.text_from_html(url_request(urllist[4])).lower())
docF = remove_punc(web_page_parser.text_from_html(url_request(urllist[5])).lower())
docG = remove_punc(web_page_parser.text_from_html(url_request(urllist[6])).lower())
docH = remove_punc(web_page_parser.text_from_html(url_request(urllist[7])).lower())
docI = remove_punc(web_page_parser.text_from_html(url_request(urllist[8])).lower())
docJ = remove_punc(web_page_parser.text_from_html(url_request(urllist[9])).lower())

# tokenizes words
# removes empty strings
# 'bow' means 'bowl of words'
bowA = filter(None, docA.split(' '))
bowB = filter(None, docB.split(' '))
bowC = filter(None, docC.split(' '))
bowD = filter(None, docD.split(' '))
bowE = filter(None, docE.split(' '))
bowF = filter(None, docF.split(' '))
bowG = filter(None, docG.split(' '))
bowH = filter(None, docH.split(' '))
bowI = filter(None, docI.split(' '))
bowJ = filter(None, docJ.split(' '))

# create a dictionary containing the # of times
# a word appears in a doc, by default at first set to 0
wordDictA = dict.fromkeys(wordSet, 0)
wordDictB = dict.fromkeys(wordSet, 0)
wordDictC = dict.fromkeys(wordSet, 0)
wordDictD = dict.fromkeys(wordSet, 0)
wordDictE = dict.fromkeys(wordSet, 0)
wordDictF = dict.fromkeys(wordSet, 0)
wordDictG = dict.fromkeys(wordSet, 0)
wordDictH = dict.fromkeys(wordSet, 0)
wordDictI = dict.fromkeys(wordSet, 0)
wordDictJ = dict.fromkeys(wordSet, 0)

# runs count word function for content on each page
wordDictA = count_words(bowA, wordDictA)
wordDictB = count_words(bowB, wordDictB)
wordDictC = count_words(bowC, wordDictC)
wordDictD = count_words(bowD, wordDictD)
wordDictE = count_words(bowE, wordDictE)
wordDictF = count_words(bowF, wordDictF)
wordDictG = count_words(bowG, wordDictG)
wordDictH = count_words(bowH, wordDictH)
wordDictI = count_words(bowI, wordDictI)
wordDictJ = count_words(bowJ, wordDictJ)

# gets term frequency for each page
tfBowA = computeTF(wordDictA, bowA)
tfBowB = computeTF(wordDictB, bowB)
tfBowC = computeTF(wordDictC, bowC)
tfBowD = computeTF(wordDictD, bowD)
tfBowE = computeTF(wordDictE, bowE)
tfBowF = computeTF(wordDictF, bowF)
tfBowG = computeTF(wordDictG, bowG)
tfBowH = computeTF(wordDictH, bowH)
tfBowI = computeTF(wordDictI, bowI)
tfBowJ = computeTF(wordDictJ, bowJ)

# runs IDF on keyword count dicitonary for all pages
idfs = computeIDF([wordDictA, 
				wordDictB, 
				wordDictC, 
				wordDictD,
				wordDictE,
				wordDictF,
				wordDictG,
				wordDictH,
				wordDictI,
				wordDictJ])

# get TF*IDF for all pages 
tfidfBowA = computeTFIDF(tfBowA, idfs)
tfidfBowB = computeTFIDF(tfBowB, idfs)
tfidfBowC = computeTFIDF(tfBowC, idfs)
tfidfBowD = computeTFIDF(tfBowD, idfs)
tfidfBowE = computeTFIDF(tfBowE, idfs)
tfidfBowF = computeTFIDF(tfBowF, idfs)
tfidfBowG = computeTFIDF(tfBowG, idfs)
tfidfBowH = computeTFIDF(tfBowH, idfs)
tfidfBowI = computeTFIDF(tfBowI, idfs)
tfidfBowJ = computeTFIDF(tfBowJ, idfs)

# create dataframe for each TF*IDF for each page
df_A = pd.DataFrame.from_dict(tfidfBowA, orient='index', columns=[urllist[0]])
df_B = pd.DataFrame.from_dict(tfidfBowB, orient='index', columns=[urllist[1]])
df_C = pd.DataFrame.from_dict(tfidfBowC, orient='index', columns=[urllist[2]])
df_D = pd.DataFrame.from_dict(tfidfBowD, orient='index', columns=[urllist[3]])
df_E = pd.DataFrame.from_dict(tfidfBowE, orient='index', columns=[urllist[4]])
df_F = pd.DataFrame.from_dict(tfidfBowF, orient='index', columns=[urllist[5]])
df_G = pd.DataFrame.from_dict(tfidfBowG, orient='index', columns=[urllist[6]])
df_H = pd.DataFrame.from_dict(tfidfBowH, orient='index', columns=[urllist[7]])
df_I = pd.DataFrame.from_dict(tfidfBowI, orient='index', columns=[urllist[8]])
df_J = pd.DataFrame.from_dict(tfidfBowJ, orient='index', columns=[urllist[9]])

# join the dataframes together
full_df = pd.concat([df_A, 
					df_B, 
					df_C, 
					df_D, 
					df_E, 
					df_F, 
					df_G, 
					df_H, 
					df_I, 
					df_J], axis=1, join='inner')

full_df['tfidf avg'] = full_df.mean(axis=1)
full_df['tfidf avg used'] = full_df.apply(avg_cond, axis=1)
full_df['docs with word'] = full_df.apply(count_docs, axis=1)
full_df['tfidf max'] = full_df[[urllist[0], 
								urllist[1], 
								urllist[2],
								urllist[3],
								urllist[4],
								urllist[5],
								urllist[6],
								urllist[7],
								urllist[8],
								urllist[9]]].max(axis=1)
#full_df['tfidf avg (used)'] = full_df[].mean(axis=1)

full_df.to_csv('output2.csv', encoding='utf-8')