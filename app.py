import urllib.request as urllib2
from bs4 import BeautifulSoup

from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from string import punctuation

from nltk.probability import FreqDist
from heapq import nlargest
from collections import defaultdict

import streamlit as st

html_temp = """
<div style ="background-color:#acf07f;padding:13px">
<h1 style ="color:black;text-align:center;font-family: Garamond, serif;font-size:42px;">Washington Post Article <br> Summary Generator</h1>
</div>
"""
st.markdown(html_temp, unsafe_allow_html = True)

st.markdown("""
<h2><center>Short Summary of Long Articles of Washington Post</center></h2>
"""
,unsafe_allow_html = True)

st.markdown("""
<h3><center><i>*Note - Enter the article url, <br>ignore the error once url entered the error will dismiss</i></center></h3>
"""
,unsafe_allow_html = True)

st.sidebar.subheader("Click here to go to Washington Post official website")
link = '[Washinton Post](https://www.washingtonpost.com/)'
st.sidebar.markdown(link, unsafe_allow_html=True)

st.sidebar.subheader("About App")

st.sidebar.info("This web app is my hands-on project on NLP (Natural Language Processing) ")
st.sidebar.info("Enter the URL of the Washinton Post Article ")
st.sidebar.info("Click on the 'Summarize' button to get the summary of the article ")
st.sidebar.info('Developed By ~ TechieRushi (Rushikesh Shinde)')


def summarize(url,n):
    page = urllib2.urlopen(url).read().decode('utf-8','ignore')
    soup = BeautifulSoup(page,"lxml")
    text = " ".join(map(lambda x: x.text, soup.find_all("article")))
    text.encode('ascii',errors='replace').replace(b"?",b"")

    sents = sent_tokenize(text)

    assert n <= len(sents)

    word_sent = word_tokenize(text.lower())
    _stopwords = set(stopwords.words('english') + list(punctuation))

    word_sent = [word for word in word_sent if word not in _stopwords]

    freq = FreqDist(word_sent)

    ranking = defaultdict(int)

    for i,sent in enumerate(sents):
        for w in word_tokenize(sent.lower()):
            if w in freq:
                ranking[i] += freq[w]

    sents_idx = nlargest(n,ranking,key=ranking.get)
    return [sents[j] for j in sorted(sents_idx)]


#Article URL input from user
articleURL = st.text_input("Enter the Washington Post Article URL here below (You can use the below default URL of an article or enter your own): ",'https://www.washingtonpost.com/technology/2021/05/14/tesla-apple-tech/')
n = st.slider("Enter the no.of.sentences you want",1,5)

page = urllib2.urlopen(articleURL).read().decode('utf-8','ignore')
soup = BeautifulSoup(page,"lxml")
title = soup.title

if st.button("Summarize"):
    result = summarize(articleURL,n)
    st.write(title.string)
    st.success('Summary of the article : {}'.format(result))
