#!/usr/bin/env python
# encoding: utf-8
"""
thread_spider.py

Created by jrk on 2010-08-20.
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

class ThreadSpider:
	def __init__ (self, thread_url):
		self.post_list = list()
		thread_url = thread_url.rstrip('showthread-1')
		self.thread_url = thread_url
		self.thread_title = None
		self.thread_author = None
		self.post_list.append (thread_url) #append self as the root
		
		if "showthread-1" not in thread_url:
			self.thread_url = thread_url.rstrip('/') + "/showthread-1";
		
	def retieve_raw_content (self):
		fh = urllib.urlopen (self.thread_url)
		self.raw_content = fh.read().decode("utf-8");

		self.thread_title = common.get_title_from_content(self.raw_content);
		self.thread_author = common.get_author_from_content(self.raw_content)

		#set entry point for list parsing
		entry_point = self.raw_content.find ('<span class="active_post">');
		if entry_point == -1:
			self.raw_content = None
			return False;
		entry_point += len ('<span class="active_post">');
		
		stop = self.raw_content.find ('<ul class="forum_navi">', entry_point)
		if stop == -1:
			self.raw_content = None;
			return False;
		
		self.raw_content = self.raw_content[entry_point:stop];
		
		return True;

	def retrieve_post_list (self, from_content):
		''' will fill self.post_list with links to each post in thread '''
		if not from_content:
			return False

		start = from_content.find('<div class="thread_title">')
		if start == -1:
			return False;
		start += len ('<div class="thread_title">')
		
		start = from_content.find ('<a href="', start);
		if start == -1:
			return False;
		start += len ('<a href="');
		
		end = from_content.find ('"', start);
		if end == -1:
			return False;
		
		new_content = from_content[end:]
		if u"/read/" in from_content[start:end]:	#let's make sure it's a readable post and not some fucked up error
			self.post_list.append ("http://www.heise.de" + from_content[start:end])
		
		return self.retrieve_post_list(new_content)
		
	
	def spider_thread (self):
		print "\tspidering thread: " + self.thread_url
		self.retieve_raw_content ();
		self.retrieve_post_list (self.raw_content);
		return self.post_list

def main():
	spider = ThreadSpider ("http://www.heise.de/extras/foren/S-Wann-wird-es-preiswerte-Prozessoren-geben/forum-151262/msg-18870203/read/showthread-1");
	print "spidering thread %s ..." % (spider.thread_url)
	spider.spider_thread();
	
	print "author: %s" % (spider.thread_author)
	print "title: %s" % (spider.thread_title)
	print "thread spidered. retrieved %i post links" % (len (spider.post_list))
	print spider.post_list

if __name__ == '__main__':
	main()

