#!/usr/bin/env python
# encoding: utf-8
"""
common.py

Created by jrk on 2010-08-22.
Copyright (c) 2010 Fluxforge. All rights reserved.
"""

import sys
import os
import html2text
import urllib
import codecs

def get_title_from_content (content):
	title_start = content.find ("<title>")
	if title_start == -1:
		return None;
	title_start += len("<title>");
	
	title_end = content.find (" [Update] | ", title_start);
	if title_end == -1:
		title_end = content.find (" | ", title_start);
		if title_end == -1:
			title_end = content.find("</title>", title_start);
			if title_end == -1:
				return None
	
	return html2text.html2text(content[title_start:title_end]).lstrip().rstrip();
	

def get_author_from_content (content):
	entry_point = content.find ('<div class="user_info">')
	if entry_point == -1:
		return None
	
	start = content.find ('<i>', entry_point);
	if start == -1:
		return None;
	start += len ('<i>')
	
	end = content.find('</i>',start);
	if end == -1:
		return None;
	
	while 1:
		i = content.rfind(',&nbsp;', 0, end)
		if i == -1:
			break
		if i <= start:
			break;
		end = i
	
	return content[start:end]


def main():
	sys.stdout = codecs.getwriter('utf8')(sys.stdout)
	sys.stderr = codecs.getwriter('utf8')(sys.stderr)
	
	urls = ["http://www.heise.de/extras/foren/S-Re-Wann-wird-es-preiswerte-Prozessoren-geben/forum-151262/msg-18870225/read/",
			"http://www.heise.de/extras/foren/S-Wann-wird-es-preiswerte-Prozessoren-geben/forum-151262/msg-18870203/read/"]
	
	for url in urls:
		fh = urllib.urlopen (url)
		data = fh.read().decode("utf-8");
	
		print "-"*40
		print "url:\t" + url
		print "title:\t" + get_title_from_content (data)
		print "author:\t" + get_author_from_content (data)
		print "-"*40
		print ""
	
	pass


if __name__ == '__main__':
	main()

