
#
# http://flask-restful.readthedocs.io/en/0.3.5/quickstart.html
#

import config
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import mysql.connector as mariadb

app = Flask(__name__)
api = Api(app)
cfg = config.readConfig()

ARTICLES = {
    'article1': {'url': 'http://blah.com', 'headline': 'build an API', 'article': 'blah blah'},
    'article2': {'headline': '?????'},
    'article3': {'headline': 'profit!'},
}

def query_articles():
    try:
        articles = {}
        cursor.execute("SELECT Id,URL,title,headline FROM Articles LIMIT 500", ())
        if cursor.rowcount < 1:
            return True
        print "Found {0} articles".format(cursor.rowcount)
        for (Id, URL, title, headline) in cursor:
            article = {}
            article['URL'] = URL
            article['title'] = title
            article['headline'] = headline
#            print " {0}, {1}, {2}, {3}".format(Id, URL, title, headline)
            print(article)
            articles[Id] = article
        global ARTICLES
        ARTICLES = articles
    except:
        print "Error: unable to look for URL"

def abort_if_article_doesnt_exist(article_id):
    if article_id not in ARTICLES:
        abort(404, message="Article {} doesn't exist".format(article_id))

parser = reqparse.RequestParser()
parser.add_argument('headline')


# Article
# shows a single article item and lets you delete a article item
class Article(Resource):
    def get(self, article_id):
        abort_if_article_doesnt_exist(article_id)
        return ARTICLES[article_id]

# ArticleList
# shows a list of all articles, and lets you POST to add new headlines
class ArticleList(Resource):
    def get(self):
        query_articles()
        return ARTICLES

##
## Actually setup the Api resource routing here
##
api.add_resource(ArticleList, '/articles')
api.add_resource(Article, '/articles/<article_id>')

if __name__ == '__main__':
#	cfg = config.readConfig()
	print(cfg)
	global mariadb_connection
	mariadb_connection = mariadb.connect(host=cfg['mysql']['host'], user=cfg['mysql']['user'], password=cfg['mysql']['pass'], database=cfg['mysql']['database'])
	global cursor
	cursor = mariadb_connection.cursor(buffered=True)
	app.run(debug=True)

