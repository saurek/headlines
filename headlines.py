from flask import Flask, render_template, request
import feedparser
import json
import urllib.parse
import urllib.request
import urllib3

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640',
             'wsp': 'http://feeds.washingtonpost.com/rss/politics'}


@app.route("/")
def get_news():
    query = request.args.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()
    feed = feedparser.parse((RSS_FEEDS[publication]))
    weather = get_weather("London,UK")
    return render_template("home.html", articles=feed['entries'],
                           weather=weather)


def get_weather(query):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=47258b3b6592bb72b736e9746e9148d7"
    query = urllib.parse.quote(query)
    url = api_url.format(query)
    data = urllib.request.urlopen(url).read()
    parsed = json.loads(data.decode('utf-8'))
    weather = None
    if parsed.get("weather"):
        weather = {"description":
                       parsed["weather"][0]["description"],
                   "temperature": parsed["main"]["temp"],
                   "city": parsed["name"]
                   }
    return weather


if __name__ == '__main__':
    app.run(port=5000, debug=True)
