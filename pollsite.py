#! /usr/bin/python

import urllib2
from urlparse import urlparse
import yaml
from lxml import html
from lxml import etree
import requests
from pprint import pprint
import re
import mysql.connector as mariadb

configFile="config.yaml"
dbhost='simpletest.chbfek7f5zas.us-west-2.rds.amazonaws.com'
dbuser='simple'
dbpass=""
database='simpledb'

def readConfig():
	global dbpass
	print "Reading config"
	stream = open(configFile, "r")
	docs = yaml.load_all(stream)
	for doc in docs:
		for k,v in doc.items():
#			print k, "->", v
			if k == "dbpass":
				dbpass = v

def IsURLKnown(url):
	try:
		cursor.execute("SELECT Id,URL,title FROM Articles WHERE URL=%s", (url,))
		if cursor.rowcount > 0:
			return True
	except:
		print "Error: unable to look for URL"
	return False


def saveURL(url, title):
	try:
		print "Fetching {0}".format(url)

		test = urllib2.urlopen(url)
		page = test.read()
		tree = etree.HTML(page)

		headline = ''
		# <div id="content">
		#     <h1>A headline</h1>
		h1s = tree.xpath("//div[@id='content']//h1")
		if h1s:
			for h1 in h1s:
				headline += h1.text

		#<header class="article-header">
		#    <h1>Costco Sues Titleist In Battle Over Golf Balls</h1>
		h1s = tree.xpath("//header[@class='article-header']//h1")
		if h1s:
			for h1 in h1s:
				headline += h1.text

		headline = headline[:128]	# make sure only 128 characters or less
		print " headline={0}".format(headline)

		article_html = ''
		# <div class="article-text">
		articles = tree.xpath("//div[@class='article-text']")
		if articles:
			for article in articles:
				article_html += etree.tostring(article, pretty_print=True)
#			print "article={0}".format(article_html)
		if len(headline)<3:
			print " headline is too short"
			return
		if len(article_html)<20:
			print " article is too short"
			return

		cursor.execute("INSERT INTO Articles (URL,title,headline,article) VALUES (%s,%s,%s,%s)", (url, title,headline,article_html))
	except mariadb.Error as error:
		print("Error: {}".format(error))
		return

def pollFox():
	url = 'http://www.foxnews.com/'
	page = requests.get(url)
	tree = html.fromstring(page.content)

	# <a href="http://www.foxnews.com/politics/2017/03/17/trump-presses-merkel-hard-on-nato-dues-during-visit.html">Trump presses Merkel 'hard' on NATO dues during visit</a>
	# 
	# http://www.foxbusiness.com/politics/2017/03/17/trump-touts-jobs-jabs-merkel-on-trade-nato.html

	atags = tree.xpath('//a')

	p = re.compile('http://(.*fox.*com)/([a-z\-]+)/(\d\d\d\d)/(\d\d)/(\d\d)/')
	found = 0
	for atag in atags:
#		print 'atag: ', atag.text
		href = atag.get('href')
#		print ' href: ', href
		m = p.search(href)
		if m and atag.text and len(atag.text)>10:
#			print ' len: ', len(atag.text)
#			print ' m: ', m

			if IsURLKnown(href):
				print "Known: {0}".format(href)
			else:
				saveURL(href, atag.text)
				found += 1
#		else:
#			print ' No match'
		mariadb_connection.commit()
	print "Found {0}".format(found)

def connectDb():
#	print 'dbpass=', dbpass
	global mariadb_connection
	mariadb_connection = mariadb.connect(host=dbhost, user=dbuser, password=dbpass, database=database)
	cursor = mariadb_connection.cursor(buffered=True)
	return cursor


readConfig()
cursor=connectDb()
#print 'cursor=', cursor
pollFox()


