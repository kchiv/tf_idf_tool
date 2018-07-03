# -*- coding: utf-8 -*-

import pandas as pd
import os

import web_page_parser
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

urllist = [
'https://us.norton.com/internetsecurity-malware-5-ways-you-didnt-know-you-could-get-a-virus-malware-or-your-social-account-hacked.html',
'https://us.norton.com/internetsecurity-malware-7-tips-to-prevent-ransomware.html',
'https://us.norton.com/internetsecurity-malware-android-malware.html',
'https://us.norton.com/internetsecurity-malware-apple-cyber-security-2017.html',
'https://us.norton.com/internetsecurity-malware-cybercrime-rings-gameover-zeus.html',
'https://us.norton.com/internetsecurity-malware-destructive-malware.html',
'https://us.norton.com/internetsecurity-malware-how-norton-keeps-you-shaded-from-silent-but-deadly-threats.html',
'https://us.norton.com/internetsecurity-malware-how-can-i-tell-if-i-have-malware-and-what-can-i-do-about-it.html',
'https://us.norton.com/internetsecurity-malware-how-to-remove-malware-from-android-phones.html',
'https://us.norton.com/internetsecurity-malware-macro-viruses.html',
'https://us.norton.com/internetsecurity-malware-malware-101-how-do-i-get-malware-complex-attacks.html',
'https://us.norton.com/internetsecurity-malware-malware-101-how-do-i-get-malware-simple-attacks.html',
'https://us.norton.com/internetsecurity-malware-osx-malware.html',
'https://us.norton.com/internetsecurity-malware-pc-or-mac.html',
'https://us.norton.com/internetsecurity-malware-pi-cybersecurity-numbers.html',
'https://us.norton.com/internetsecurity-malware-ransomware-and-the-importance-of-backing-up.html',
'https://us.norton.com/internetsecurity-malware-ransomware-5-dos-and-donts.html',
'https://us.norton.com/internetsecurity-malware-safely-use-memory-sticks.html',
'https://us.norton.com/internetsecurity-malware-the-worm-in-the-apple-part-1-why-mac-users-are-not-immune-from-viruses-and-malware.html',
'https://us.norton.com/internetsecurity-malware-virus-faq.html',
'https://us.norton.com/internetsecurity-malware-webcam-hacking.html',
'https://us.norton.com/internetsecurity-malware-what-is-a-computer-virus.html',
'https://us.norton.com/internetsecurity-malware-what-are-bots.html',
'https://us.norton.com/internetsecurity-malware-what-are-browser-hijackers.html',
'https://us.norton.com/internetsecurity-malware-what-are-malicious-websites.html',
'https://us.norton.com/internetsecurity-malware-what-is-a-trojan.html',
'https://us.norton.com/internetsecurity-malware-what-is-a-botnet.html',
'https://us.norton.com/internetsecurity-malware-ransomware.html',
'https://us.norton.com/internetsecurity-malware-when-were-computer-viruses-first-written-and-what-were-their-original-purposes.html',
'https://us.norton.com/internetsecurity-malware-why-mac-users-are-not-immune.html'
]
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

cw_directory = os.getcwd() + '/output_files/'

full_df.to_csv(cw_directory + 'adhoc.csv', encoding='utf-8')