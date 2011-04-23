#!/usr/bin/env python
# encoding: utf-8
"""
forum_job.py

spiders a forum and saves the thread to databasw

Created by jrk on 2010-08-23.
Copyright (c) 2010 Fluxforge. All rights reserved.
"""

import sys
import os
import codecs
import forum_spider
import DataBase

class ThreadExtractJob:
	def __init__(self, forum_url):
		self.forum_url = forum_url
		self.thread_list = None

	def store_thread_list(self):
		print "\t\t\tstoring list to db ..."
		# open thread db
		# store threads
		for thread in self.thread_list:
			print "\t\t\t\tstoring thread: %s" %(thread)
		print "\t\t\t#"
		
	def do_job (self):
		print "\t\tspidering %s" %(self.forum_url)
		fs = forum_spider.ForumSpider(self.forum_url)
		fs.spider_forum ();
		self.thread_list = fs.thread_list
		print "\t\t\tforum title: %s" % (fs.forum_title)
		print "\t\t\tTHREAD LIST contains %i entries:" % (len(fs.thread_list))
		self.store_thread_list();
		print "\t\t#"

def main():
	sys.stdout = codecs.getwriter('utf8')(sys.stdout)
	sys.stderr = codecs.getwriter('utf8')(sys.stderr)
	
	print "-"*80
	print "ThreadExtractJob - extracts links to threads from forum urls"
	print "-"*80
	print ""
			
	forum_database = DataBase.ForumDB();
	
	max_forums_to_spider = 10;
	counter = 1
	while 1:
		if counter > max_forums_to_spider:
			break;
		print "\tjob %i/%i ..." % (counter, max_forums_to_spider);
		url = forum_database.get_random_forum_url()
		if not url:
			print "\t\t" + "*"*80
			print "\t\tERROR:"
			print "\t\t\tcould not get url from database. aborting job!"
			print "\t\t" + "*"*80
			break;
		
		job = ThreadExtractJob (url);
		job.do_job();
		counter += 1
	
	print ""
	print "-"*80
	print "ThreadExtractJob done"
	print "-"*80
	
if __name__ == '__main__':
	main()

