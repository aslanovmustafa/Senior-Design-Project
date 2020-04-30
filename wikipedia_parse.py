# -*- coding: utf-8 -*-

import string
from bs4 import BeautifulSoup
import xml.sax
import mwparserfromhell
import pandas as pd
import re
import pickle

data_path = '/Users/aliyabnnv/Desktop/SDP/azwiki.xml'


def clean_the_article(body_text):
    """
    Cleans an article body and returns cleaned text
    """
    t = re.sub(r'\n', ' ', body_text)
    t = re.sub(r'\t', '', t)
    t = re.sub(r' +', ' ', t)

    t = re.sub(r'<title>.*?</title>', '', t)
    # art_count = re.findall(r'<title>.*?</title>')

    t = re.sub(r'< .*? >', '', t)
    t = re.sub(r'=+.*?=+', '', t)
    t = (re.sub(r'<id>.*?</id>', '', t))
    t = re.sub(r'<ns>.*?</ns>', '', t)
    t = (re.sub(r'<div.*?>', '', t))
    t = re.sub(r'<parentid>.*?</parentid>', '', t)
    t = re.sub(r'<timestamp>.*?</timestamp>', '', t)
    t = re.sub(r'<username>.*?</username>', '', t)
    t = re.sub(r'<contributor>', '', t)
    t = re.sub(r'</contributor>', '', t)
    t = re.sub(r'<comment>.*?</comment>', '', t)
    t = re.sub(r'<model>.*?</model>', '', t)
    t = re.sub(r'<format>.*?</format>', '', t)
    t = re.sub(r'\[\[Şəkil:.*?\]\]', '', t)
    t = re.sub(r'&lt;.*?&gt;', '', t)

    t = re.sub(r'&lt;small&gt;.*?&lt;/small&gt;', '', t)  # İşarələr:

    t = re.sub(r'<shal.*?shal>', '', t)
    t = re.sub(r'<text.*?>', '', t)
    t = re.sub(r'(\|)+.*', '', t)  # $1 versiyası; $2$3
    t = re.sub(r'</text>', '', t)
    t = re.sub(r'\[', '', t)
    t = re.sub(r'\]', '', t)
    t = re.sub(r'\(', '', t)
    t = re.sub(r'\)', '', t)
    t = re.sub(r'<page>', '', t)
    t = re.sub(r'</page>', '', t)
    t = re.sub(r'<minor.*?>', '', t)
    t = re.sub(r'<revision>', '', t)
    t = re.sub(r'</revision>', '', t)
    t = re.sub(r'{{[^}]*}}', '', t)

    t = re.sub(r'\{\|.*\|\}', '', t)

    t = re.sub(r'(\*)+.*', '', t)
 # any asterisk
    t = re.sub(r'(\#)+.*', '', t)

    # t = re.sub(r'\[http.*?\]+', '', t)

    # t = re.sub(r'(http)+.*?', '', t)
    # t = re.sub(r'(https)+.*?', '', t)
    t = re.sub(r'https?:\/\/.*[\r\n]*', '', t)
    # t = re.sub(r'[https.*?]', '', t)
    t = re.sub(r'(\')+?', '', t)

    # t = re.sub(r'".*?"', '', t)
    t = re.sub(r'^(\*)+.*', '', t)

    t = re.sub(r'^(\d[px])+.*', '', t)  # 30px/20px at the beginning
    t = re.sub(r'(\d[px])+.*', '', t)  # 30px/20px anywhere in the sentence
    t = re.sub(r'(\s\w{2}[:])+.*', '', t)
    t = re.sub(r'^(\:)+.*', '', t)
    t = re.sub(r'^(\$)+.*', '', t)
    t = re.sub(r'^(\+)+.*', '', t)
    t = re.sub(r'^məqalə+.*', '', t)
    t = re.sub(r'^NameDefault+.*', '', t)
    t = (re.sub(r'<input.*?>', '', t))
    t = re.sub(r'<p>', '', t)
    t = re.sub(r' +', ' ', t)  # rm empty..

    t = re.sub(r'\"+', '', t)  # rm "

    t = re.sub(r'\'+', '', t)  # rm '
    t = re.sub(r'\(\)+', '', t)
    t = re.sub(r'\( \)+', '', t)
    t = re.sub(r'(\/\/)+', '', t)  # ??
    t = re.sub(r'thumb+.*', '', t)
    t = re.sub(r'(\((, )+\))', '', t)
    t = re.sub(r'(\d\d\d[px])+', '', t)

    # t = re.sub(r"\n", " ", t)
    # t = (re.sub(r'([\W\w]*\s?){1,4}', '', t))
    l = len(t.split())  # removes sentences with less than 5 words
    if l < 5:
        t = (re.sub(r'([\W\w]*\s?)', '', t))

    # t = re.sub(r'^(\"\")', '', t)
    return t


def process_article(title, text):
    """Process a wikipedia article looking for template"""

    # Create a parsing object
    wikicode = mwparserfromhell.parse(text)

    bodytext = wikicode.strip_code().strip()

    cleaned_body = clean_the_article(bodytext)

    return [cleaned_body]


class WikiXmlHandler(xml.sax.handler.ContentHandler):
    """Content handler for Wiki XML data using SAX"""

    def __init__(self):
        xml.sax.handler.ContentHandler.__init__(self)
        self._buffer = None
        self._values = {}
        self._current_tag = None
        self._pages = []
        self._article_count = 0

    def characters(self, content):
        """Characters between opening and closing tags"""
        if self._current_tag:
            self._buffer.append(content)

    def startElement(self, name, attrs):
        """Opening tag of element"""
        if name in ('title', 'text'):
            self._current_tag = name
            self._buffer = []

    def endElement(self, name):
        """Closing tag of element"""
        if name == self._current_tag:
            self._values[name] = ''.join(self._buffer)

        if name == 'page':
            self._article_count += 1
            # Send the page to the process article function
            page = process_article(**self._values)
            # If article is a book append to the list of books
            if page:
                self._pages.append(page)
        print(self._article_count)


# Object for handling xml
handler = WikiXmlHandler()
# Parsing object
parser = xml.sax.make_parser()
parser.setContentHandler(handler)

for line in open(data_path, 'r', encoding='utf8'):
    parser.feed(line)

    # # Limiting Number of articles
    # if len(handler._pages) > 2000:
    #     break


df = pd.DataFrame(handler._pages,
                  columns=["cleaned_body_text"])

df.to_csv('./wikipedia_cleaned.csv', index=False)
df.to_excel("cleaned_wikipedia.xlsx")

wiki_parse = pd.read_csv('./wikipedia_cleaned.csv')


# optioanlly putting your file as pickle
with open('/Users/aliyabnnv/Desktop/SDP/wikipedia_parsed_v2.pickle.txt', 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(handler._pages, f, pickle.HIGHEST_PROTOCOL)


with open('/Users/aliyabnnv/Desktop/SDP/wikipedia_parsed_v2.pickle.txt', 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    data = pickle.load(f)
