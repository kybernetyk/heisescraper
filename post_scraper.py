#!/usr/bin/env python
# encoding: utf-8
"""
post_scraper.py

Created by jrk on 2010-08-19.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import urllib
import time
import pprint
import codecs
import html2text
import common

class PostScraper:
	"""
		c'tor takes the url of the post to scrape
		call scrape_post() afterwards to do the work
	"""
	def __init__ (self, post_url):
		''' post_url = url of the post to scrape '''
		self.post_url = post_url;
		self.post_dict = dict()
	#
	
	def retrieve_raw_content (self):
		''' get raw html page from server '''
		fh = urllib.urlopen (self.post_url)
		self.raw_content = fh.read().decode("utf-8");
	#
	
	def retrieve_post_author (self):
		self.post_author = common.get_author_from_content(self.raw_content)
		return True
	
	def retrieve_post_subject (self):
		self.post_subject = common.get_title_from_content (self.raw_content)
		"""		start = self.raw_content.find('posting_subject">')
		if start == -1:
			return False
		start += len('posting_subject">')
		
		end = self.raw_content.find('</h3>', start)
		if end == -1:
			return False
		
		self.post_subject = html2text.html2text(self.raw_content[start:end].lstrip().rstrip()).lstrip().rstrip()
		
		edit_start = self.post_subject.lower().find(" (editiert vom");
		if edit_start != -1:
			self.post_subject = self.post_subject[:edit_start]
				
		return True"""
	#
	
	def num_for_month_name (self, strdate):
		''' returns num of month for german month name '''
		strdate = strdate.lower()
		strdate = strdate.replace(u'januar','1')
		strdate = strdate.replace(u'februar','2')
		strdate = strdate.replace(u'm\xe4rz','3')
		strdate = strdate.replace(u'april','4')
		strdate = strdate.replace(u'mai','5')
		strdate = strdate.replace(u'juni','6')
		strdate = strdate.replace(u'juli','7')
		strdate = strdate.replace(u'august','8')
		strdate = strdate.replace(u'september','9')
		strdate = strdate.replace(u'oktober','10')
		strdate = strdate.replace(u'november','11')
		strdate = strdate.replace(u'dezember','12')
		
		return strdate
	
	def retrieve_post_date (self):
		start = self.raw_content.find('posting_date">')
		if start == -1:
			return False
		start += len('posting_date">')
		
		end = self.raw_content.find('</div>', start)
		if end == -1:
			return False
		
		self.post_date = self.raw_content[start:end].lstrip().rstrip()
		dstr = self.num_for_month_name(self.post_date)
		dstrct = time.strptime(dstr, u"%d. %m %Y %H:%M")
		timestamp = time.strftime(u"%s", dstrct)
		self.post_date = timestamp;
		
		return True;
	
	
	def encode_quotes (self, text):
		""" encodes html quote markup to non html so it can survive processing """
		text = text.replace('<span class="quote">', "{quote_start}")
		text = text.replace('</span>', "{quote_end}")
		return text
	

	def decode_quotes (self, text):
		''' invert encode quotes '''
		text = text.replace("{quote_end} {quote_start}", " ") #make 2 consecutive quotes into one
		text = text.replace("{quote_start}{quote_end}", "");
		text = text.replace("{quote_end}{newline}{quote_start}", "{newline}");
		
		
		#text = text.replace("$$$",'<span class="quote">')
		#text = text.replace("###",'</span>')
		return text
	

	def retrieve_post_content (self):
		start = self.raw_content.find('<p class="posting_text">')
		if start == -1:
			return False
		start += len('<p class="posting_text">')
		
		end = self.raw_content.find('</p>', start)
		if end == -1:
			return False
		
		ctnt = self.raw_content[start:end];

		#encode html quotes to non html so they survive the following procedure
		clean = self.encode_quotes(ctnt);
		
		#get quote author name
		quoted_author = None
		#remove the "Op schrieb am ..."
		orig_autor_quote_name = clean.find ('schrieb&nbsp;am')
		if orig_autor_quote_name != -1:
			start = clean.rfind('>',0,orig_autor_quote_name)
			start += len('>')
			
			stop = orig_autor_quote_name
			author_name = html2text.html2text(clean[start:stop]).lstrip().rstrip()
			quoted_author = author_name[:]
			stop = clean.find('<br />',orig_autor_quote_name)
			clean = clean.replace(clean[start:stop],"")
		
		#remove ugly html and whitespace holocaust
		wurst = html2text.html2text(clean).lstrip().rstrip().replace("\n","{newline}").replace("  "," ")
		wurst = "{paragraph_start}" + wurst
		wurst = wurst.replace(" {newline}", "{newline}")
		wurst = wurst.replace("{newline}{newline}", "{paragraph_end}{paragraph_start}")
		#wurst = wurst.replace("{newline}{newline}", " ")
		
		#test
		#wurst = wurst.replace("{paragraph_end}{paragraph_start}", "\n\n");
		
		#remove old quotemarks from heise
		wurst = wurst.replace('> ','')
		
		#remove ugly subquote author names
		cont = 1
		while cont:
			entry = wurst.find ('schrieb am')
			if entry == -1:
				break;
			
			start = wurst.rfind('{quote_start}', 0, entry)
			if start == -1:
				break;
			
			end = entry;
			author_name = wurst[start+len('{quote_start}'):end].lstrip().rstrip()
			#print author_name
			
			end = wurst.find('{quote_end}', entry)
			if end == -1:
				break;
			end += len('{quote_end}')
			wurst = wurst.replace(wurst[start:end],'')
			#print "penil: %i %i:%i" % (entry, start, end)
		

		
		#put html markup around quotes
		wurst = self.decode_quotes(wurst).lstrip().rstrip()
		
		#add quoted source
		if quoted_author:
			wurst = wurst.replace('{quote_start}','{quoted_author_start}%s{quoted_author_end}{quote_start}' %(quoted_author), 1)
		wurst = wurst.replace("{newline}{newline}", " ")
		self.post_content = wurst.lstrip().rstrip()
	#
	

	def remove_quotes (self, text):
		''' removes heise quote content (deprecated) '''
		quote_start = text.find('<span class="quote">')
		if quote_start == -1:
			return text;
		quote_end = text.find('</span>', quote_start);
		if quote_end == -1:
			return text;
		quote_end += len('</span>');
		
		text = text.replace(text[quote_start:quote_end],"")
		return self.remove_quotes(text)
	
	def retrieve_post_id (self):
		#http://www.heise.de/newsticker/foren/S-Ich-mag-keine-PDF/forum-184556/msg-19019896/read/
		start = self.post_url.find('/msg-')
		if start == -1:
			return False
		start += len ('/msg-')
		stop = self.post_url.find('/',start)
		self.post_id = self.post_url[start:stop]
		
		return True
	
	def scrape_post(self):
		"""
			scrapes a post
			scrape_post() fills self.post_dict with content and returns it
		"""
		
		print "\t\tscraping post: %s" % (self.post_url)
		
		self.retrieve_raw_content();
		if u"Dieser Beitrag wird aus einem der folgenden Gründe nicht angezeigt:" in self.raw_content:
			#print "\t\t\tbeitrag gesperrt :["
			self.post_dict = None
			return None
		
		self.retrieve_post_id();
		self.retrieve_post_author();
		self.retrieve_post_subject()
		self.retrieve_post_date();
		self.retrieve_post_content();

		self.post_dict['author'] = self.post_author
		self.post_dict['subject'] = self.post_subject
		self.post_dict['date'] = self.post_date
		self.post_dict['content'] = self.post_content
		self.post_dict['id'] = self.post_id
		#print "\t\t\tok"
		return self.post_dict
	
	

def main():
	url = "http://www.heise.de/extras/foren/S-Wann-wird-es-preiswerte-Prozessoren-geben/forum-151262/msg-18870203/read/"
	scraper = PostScraper(url);
	scraper.scrape_post();
	
	pp = pprint.PrettyPrinter(indent=2)
	#pp.pprint (scraper.post_dict);
	print ("author: " + scraper.post_dict['author'])
	print ("subject: " + scraper.post_dict['subject'])
	print ("content: " + scraper.post_dict['content'])
	#date timetamp:
	# dstr = scraper.post_date.replace("August","8")
	# dstrct = time.strptime(dstr, "%d. %m %Y %H:%M")
	# timestamp = time.strftime("%s", dstrct)
	# localtiem = time.localtime(float(timestamp))
	# ostr = time.strftime("%H:%M (%d.%m.%y)", ltiem)

	"""f_out = codecs.open ("penis.txt", "w", "utf-8");
	f_out.write(scraper.post_dict['content'])
	f_out.close()"""
	pass


if __name__ == '__main__':
	main()

