#! /usr/bin/python

import yaml
from lxml import html
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
			print k, "->", v
			if k == "dbpass":
				dbpass = v

def pollFox():
	url = 'http://www.foxnews.com/'
	page = requests.get(url)
	tree = html.fromstring(page.content)

	# <a href="http://www.foxnews.com/politics/2017/03/17/trump-presses-merkel-hard-on-nato-dues-during-visit.html">Trump presses Merkel 'hard' on NATO dues during visit</a>
	# 
	# http://www.foxbusiness.com/politics/2017/03/17/trump-touts-jobs-jabs-merkel-on-trade-nato.html

	atags = tree.xpath('//a')

	p = re.compile('http://(.*fox.*com)/([a-z\-]+)/(\d\d\d\d)/(\d\d)/(\d\d)/')
	for atag in atags:
		print 'atag: ', atag.text
		href = atag.get('href')
		print ' href: ', href
		m = p.search(href)
		if m and atag.text and len(atag.text)>10:
			print ' len: ', len(atag.text)
			print ' m: ', m
		else:
			print ' No match'

def connectDb():
	print 'dbpass=', dbpass
	mariadb_connection = mariadb.connect(host=dbhost, user=dbuser, password=dbpass, database=database)
	cursor = mariadb_connection.cursor()
	return cursor


readConfig()
cursor=connectDb()
print 'cursor=', cursor


