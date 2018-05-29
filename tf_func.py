import math
import re
import requests

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
		tfDict[word] = count / (1 + float(bowCount))
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
		idfDict[word] = math.log(N/(1+float(val)))

	return idfDict

def computeTFIDF(tfBow, idfs):
	# computes TF*IDF
	tfidf = {}
	for word, val in tfBow.iteritems():
		tfidf[word] = val * idfs[word]
	return tfidf
