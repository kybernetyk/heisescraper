#!/usr/bin/env python
# encoding: utf-8
"""
DataBase.py

Created by jrk on 2010-08-23.
Copyright (c) 2010 Fluxforge. All rights reserved.
"""

import sys
import os
import codecs

DB_SERVER = "fluxforge.com"
DB_USER = "root"
DB_PASS = ""
DB_NAMES = {'forum_db' : 'forums',
			'thread_db' : 'threads',
			'post_db' : 'posts'
			}

class ForumDB:
	counter = 0
	urls = ["http://www.heise.de/newsticker/foren/S-Gamescom-Heldenmaester-und-Zombie-Comic-Originelles-aus-deutschen-Landen/forum-184654/list/",
			"http://www.heise.de/tp/blogs/foren/S-CIA-und-ISI-Partner-mit-voellig-unterschiedlichen-Zielen/forum-184648/list/"
	]
	
	def __init__ (self):
		self.connection_is_open = 0
	
	def connect_to_db (self):
		self.connection_is_open = 1
		return self.connection_is_open

	def disconnect_from_db (self):
		self.connection_is_open = 0;

	def get_random_forum_url (self):
		if not self.connection_is_open:
			if not self.connect_to_db():
				return None;
		try:
			retval =  self.urls[self.counter]
		except IndexError:
			self.counter = 0;
			return None
			
		self.counter += 1
		return retval
	
	def store_forum_url (self, forum_url):
		self.urls.append (forum_url)
	
		
def main():
	sys.stdout = codecs.getwriter('utf8')(sys.stdout)
	sys.stderr = codecs.getwriter('utf8')(sys.stderr)

	forum_db = ForumDB();
	forum_db.connect_to_db();

	print "*"*80
	print "testing forum db input ..."	
	print "*"*80
	url = "http://www.heise.de/newsticker/foren/S-Apple-Patent-fuer-Notabschaltung-von-iPhone-Co/forum-184599/list/"
	print "storing %s ..." % (url)
	forum_db.store_forum_url(url)
	print "#"*80
	print ""
	
	print "*"*80
	print "testing forum db output ..."	
	print "*"*80

	max_forums_to_spider = 10;
	counter = 1
	while 1:
		if counter > max_forums_to_spider:
			break;
		print "\tcounter: %i/%i ..." % (counter, max_forums_to_spider);
		url = forum_db.get_random_forum_url()
		if not url:
			print "\t\tgot no url ..."
			break
		print "\t\turl: " + url
		counter += 1
	forum_db.disconnect_from_db()
	print "#"*80
	print ""

if __name__ == '__main__':
	main()

