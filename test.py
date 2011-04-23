#!/usr/bin/env python
# encoding: utf-8
"""
test.py

Created by jrk on 2010-08-21.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import codecs
import time
from post_scraper import *
from thread_spider import *
from forum_spider import *
import md5

def make_filename (dirty_text):
	filename = dirty_text
	filename = filename.lower();
	filename = filename.replace(u"-","")
	filename = filename.replace(u",","")
	filename = filename.replace(u"!","")
	filename = filename.replace(u".","")
	filename = filename.replace(u"&","")
	filename = filename.replace(u"/","")
	filename = filename.replace(u"?","")
	filename = filename.replace(u"*","")
	filename = filename.replace(u"+","")
	filename = filename.replace(u"ü","u")
	filename = filename.replace(u"ö","o")	
	filename = filename.replace(u"ä","a")
	filename = filename.replace(u"ß","ss")	
	filename = filename.replace(u"\\","")
	filename = filename.replace(u'"',"")
	filename = filename.replace(u"'","")
	filename = filename.replace(u":","")
	filename = filename.replace(u";","")	
	filename = filename.replace(u"(","")	
	filename = filename.replace(u")","")	
	filename = filename.replace(u"_","")	
	filename = filename.replace(u"{","")	
	filename = filename.replace(u"}","")	
	filename = filename.replace(u"@","")
	filename = filename.replace(u"[","")
	filename = filename.replace(u"]","")	
	filename = filename.lstrip().rstrip()
	filename = filename.replace(u" ","-")
	filename = filename.replace(u"--","-")
	return filename
	

def dump_post_to_html (forum_folder, post_chain):
	forum_folder = forum_folder.rstrip('/')
	out = u'<html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"><link rel="stylesheet" type="text/css" href="../style.css" media="screen"><title>%s</title></head><body>\n' % (post_chain[0]['subject'])
	
	out += u'<p><A href="/%s">Zurueck zum Foren Index</a></p>' % (forum_folder.replace('output/',''))
	
#	adsense = u'<script type="text/javascript"><!--\ngoogle_ad_client = "ca-pub-7113189846782554";\n/* andcode */\ngoogle_ad_slot = "6247758530";\ngoogle_ad_width = 728;\ngoogle_ad_height = 90;\n//-->\n</script>\n<script type="text/javascript"\nsrc="http://pagead2.googlesyndication.com/pagead/show_ads.js">\n</script>';

	count = 1 
	mod = int(len(post_chain))/3
	if mod == 0:
		mod = 1
	
	for post in post_chain:
		content = post['content'].replace('{quote_start}', '<span class="quote">');
		content = content.replace('{quote_end}', '</span>');
		content = content.replace('{quoted_author_start}', '<i>\'');
		content = content.replace('{quoted_author_end}', '\' schrieb:</i>');
		content = content.replace('{paragraph_start}', "<p>")
		content = content.replace('{paragraph_end}', "</p>")
		content = content.replace('{newline}', "<br />\n");
		
		d = time.localtime(float(post['date']))
		post_date = time.strftime("%d.%m.%y %H:%M", d)
		
		#print content
		out += u'<div class="postwrap"><span class="postheader">%s</span>' % (post['subject'])
		out += u'<span class="author">(Verfasst von %s am %s)</span>' % (md5.md5(post['author']).hexdigest(), post_date )
		out += u'<div class="post">%s</div>\n' % (content);
		if (count % mod) == 0:
			out = out.replace(" ein ", " Expedia ")
			out = out.replace(" das ", " Gutschein ")
			out = out.replace(" der ", " Expedia Gutschein ")
			out = out.replace(" die ", " Rabatt ")
			out += u'<div style="border: 1px dashed red;"><p>Jetzt den tollen <a href="http://www.gutscheinfarm.de/gutscheine/expedia/" rel="nofollow">Gutschein fuer Expedia</a> auschecken! 70 Euro Expedia Gutschein oder wahlweise 40% Rabatt - einfach super!</p></div>'
		out += u'</div>\n'

		count += 1
	out += u"</body></html>"
	
	filename = make_filename(post_chain[0]['subject']) + ".html";
	ret_filename = filename
	filename = "%s/%s" % (forum_folder,filename)						
	
	outfile = codecs.open(filename, "w", "utf-8")
	outfile.write(out)
	outfile.close()
	
	return ret_filename

def dump_forum_index (forum_title, forum_folder, thread_chain):
	forum_folder = forum_folder.rstrip('/')
	out = u'<html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"><link rel="stylesheet" type="text/css" href="../style.css" media="screen"><title>%s</title></head><body>\n' % (forum_title)
	out += u'<p><a href="/">Gutscheinfarm Gutscheinportal</a></p>'

	for thread in thread_chain:
		out += '<a href="%s">%s</a><br>\n' % (thread['filename'],thread['title']);
	
	filename = "index.html";
	filename = "%s/%s" % (forum_folder,filename)						
	

	outfile = codecs.open(filename, "w", "utf-8")
	outfile.write(out)
	outfile.close()
	
	
def main():
	#import sys, codecs
	sys.stdout = codecs.getwriter('utf8')(sys.stdout)
	sys.stderr = codecs.getwriter('utf8')(sys.stderr)
	
	forums = [
			"http://www.heise.de/foren/S-Peripherie-Tinte-Toner-Papier/forum-42177/list/",
			"http://www.heise.de/foren/S-Betriebssysteme-andere/forum-7288/list/",
			"http://www.heise.de/foren/S-Hardware-Grafikkarten/forum-7269/list/",
			"http://www.heise.de/foren/S-Multimedia-Nutzungskontrolle/forum-35508/list/",
			"http://www.heise.de/foren/S-Betriebssysteme-Windows-7/forum-150468/list/",
			"http://www.heise.de/foren/S-Programmieren-Sonstige/forum-44548/list/",
			"http://www.heise.de/developer/foren/S-C-C/forum-44546/list/",
			"http://www.heise.de/foren/S-Mobil-Mobiles-Internet/forum-26515/list/",
			  "http://www.heise.de/foren/S-Mobil-Smartphones/forum-26520/list/",
				"http://www.heise.de/foren/S-Software-Office-Pakete/forum-7315/list/",
			"http://www.heise.de/foren/S-Hardware-Selbstbau/forum-43922/list/"];

	forums2 = ["http://www.heise.de/foren/S-Hardware-Komplettsysteme/forum-7265/list/",
			"http://www.heise.de/foren/S-Hardware-Festplatten/forum-7268/list/",
			"http://www.heise.de/foren/S-Hardware-Mainboards/forum-7267/list/",
			"http://www.heise.de/foren/S-Multimedia-Spiele/forum-7345/list/"];

	forums3 = ["http://www.heise.de/foren/S-Mobil-Handy-im-Ausland/forum-26514/list/"]

	for forum in forums3:
		try:
			fspider = ForumSpider (forum);
			fspider.spider_forum()
			threads = fspider.thread_list
			forum_title = fspider.forum_title
			
			forum_folder = "output/%s" % (make_filename (forum_title))
			if not os.path.exists (forum_folder):
				os.mkdir(forum_folder)
	
			thread_list_for_index = list()
			endfick = list()
			for thread in threads:
				try:
					thread_files = []
					tspider = ThreadSpider (thread)
					tspider.spider_thread();
					thread_title = tspider.thread_title
					posts = list (tspider.post_list)
	
					post_list = list()
					for post_url in posts:
						pscraper = PostScraper(post_url);
						pscraper.scrape_post()
						post_dict = pscraper.post_dict;
						if post_dict:
							post_list.append (post_dict.copy())
		
					prevpost = None;
					for post in post_list:
						if prevpost:
							prevpost['next_post_id'] = post['id']
						prevpost = post
	
					endfick.append (list(post_list))
					print "\t\tdump thread to html..."
					dumpfile = dump_post_to_html (forum_folder,list(post_list))
					if dumpfile:
						thread_info = {'title': thread_title,
										'filename': dumpfile
						}
						thread_list_for_index.append(thread_info)
						print "\t\tdumped to %s\n\t#" % (dumpfile)
					else:
						print "\t\tcould not dump ... :[\n\t#"
				except:
					print "[!] invalid thread url: " + thread
					pass
			print "#"
			dump_forum_index (forum_title, forum_folder, thread_list_for_index)
		except:
			print "[!] invalid forum url: " + forum
			pass


if __name__ == '__main__':
	main()

