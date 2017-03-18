
from lxml import html
import requests
from pprint import pprint
import re

url = 'http://www.foxnews.com/'
page = requests.get(url)
tree = html.fromstring(page.content)

# <a href="http://www.foxnews.com/politics/2017/03/17/trump-presses-merkel-hard-on-nato-dues-during-visit.html">Trump presses Merkel 'hard' on NATO dues during visit</a>
# 
# http://www.foxbusiness.com/politics/2017/03/17/trump-touts-jobs-jabs-merkel-on-trade-nato.html

#atags = tree.xpath('//a/text()')
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

