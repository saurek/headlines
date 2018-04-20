from flask import Flask
import feedparser

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640',
             'wsp': 'http://feeds.washingtonpost.com/rss/politics'}


@app.route('/')
@app.route('/<publication>')
def index(publication="bbc"):
    return get_news(publication)

#
# @app.route('/cnn')
# def cnn():
#     return get_news('cnn')
#
#
# @app.route('/wsp')
# def wsp():
#     return get_news('wsp')


def get_news(publication):
    feed = feedparser.parse((RSS_FEEDS[publication]))
    first_article = feed['entries'][0]
    return """<html>
        <body>
            <h1>Headlines</h1>
            <b>{0}</b> </br>
            <i>{1}</i> </br>
            <p>{2}</p> </br>
        </body>
    </html>""".format(first_article.get("title"), first_article.get("published"),
                      first_article.get("summary"))


if __name__ == '__main__':
    app.run(port=5000, debug=True)
