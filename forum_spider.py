#!/usr/bin/env python
# encoding: utf-8
"""
forum_spider.py

Created by jrk on 2010-08-21.
Copyright (c) 2010 Fluxforge. All rights reserved.
"""

import sys
import os
import urllib
import time
import pprint
import codecs
import html2text
import common

class ForumSpider:
	def __init__ (self, forum_url):
		self.forum_url = forum_url;
		self.page_list = list()
		self.thread_list = list()
		self.forum_title = None;

	def retieve_raw_content (self):
		fh = urllib.urlopen (self.forum_url)
		self.raw_content = fh.read().decode("utf-8");
		
		self.forum_title = common.get_title_from_content(self.raw_content);
	
	def retrieve_page_list (self):
		self.page_list = []
		entry_point = self.raw_content.find ('<li><b>Neuere</b></li');
		if entry_point == -1:
			self.page_list.append (self.forum_url)
			return False

		start = self.raw_content.rfind('<li><a href="',0,entry_point);
		if start == -1:
			self.page_list.append (self.forum_url)
			return False
		start += len('<li><a href="');

		end = self.raw_content.rfind('/hs-',0,entry_point);
		if end == -1:
			self.page_list.append (self.forum_url)
			return False
			
		end += len ('/hs-')

		baseurl = "http://www.heise.de" + self.raw_content[start:end];
		
		maxpage_start = end;
		maxpage_end = self.raw_content.find('/', maxpage_start)
		if maxpage_end == -1:
			self.page_list.append (self.forum_url)
			return False

		maxpage = self.raw_content[maxpage_start:maxpage_end];
		
		print "base url: " + baseurl
		print "maxpage: " + maxpage
		
		self.page_list = []
		heise_stepping = 16	#16 post per page
		for page_index in range (0,int(maxpage)+heise_stepping, heise_stepping):
			self.page_list.append (baseurl + str(page_index) + "/")
		

		return True;

	def retrieve_threads_from_page_content (self, page_content):
		entry_point = page_content.find('<ul class="thread_tree">')
		if entry_point == -1:
			return None
		end = page_content.find('</ul>', entry_point)
		if end == -1:
			return None;
		
		wurst = page_content[entry_point:end];
		retlist = []
		curpos = 0;
		while 1:
			curpos = wurst.find('<div class="thread_title">', curpos)
			if curpos == -1:
				break;
			curpos += len ('<div class="thread_title">')
			
			curpos = wurst.find('<a href="', curpos)
			if curpos == -1:
				break;
			curpos += len ('<a href="')
			end = wurst.find('"', curpos)
			link = "http://www.heise.de" + wurst[curpos:end]
			curpos = end
			if u"/read/" in link:	#make sure we get only valid urls
				retlist.append (link)
			
		return retlist

	def retrieve_thread_list(self):
		self.thread_list = []
		sys.stdout.write ("retrieving thread list: ")
		for page in self.page_list:
			sys.stdout.write(".")
			sys.stdout.flush()
			fh = urllib.urlopen (page)
			current_page_raw_content = fh.read().decode("utf-8");
			threads = self.retrieve_threads_from_page_content (current_page_raw_content);
			if threads:
				self.thread_list += threads

	
	def spider_forum (self):
		#print "spidering forum: " + self.forum_url
		self.retieve_raw_content ();
		self.retrieve_page_list ()
		if self.page_list:
			self.retrieve_thread_list();

def main():
	sys.stdout = codecs.getwriter('utf8')(sys.stdout)
	sys.stderr = codecs.getwriter('utf8')(sys.stderr)
	url = "http://www.heise.de/newsticker/foren/S-Haftbefehl-gegen-Wikileaks-Chef-wegen-Vergewaltigungsverdacht-Update/forum-184583/list/"
	fs = ForumSpider(url)
	fs.spider_forum ();
	print "forum title: %s" % (fs.forum_title)
	print "PAGE LIST contains %i entries:" % (len(fs.page_list))
	print fs.page_list
	print "THREAD LIST contains %i entries:" % (len(fs.thread_list))
	print fs.thread_list

if __name__ == '__main__':
	main()

