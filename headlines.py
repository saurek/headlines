from flask import Flask, render_template, request
import feedparser
import json
import urllib.parse
import urllib.request

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640',
             'wsp': 'http://feeds.washingtonpost.com/rss/politics',
             'tbt': 'http://feeds.feedburner.com/TheBalticTimesNews'}

DEFAULTS = {'publication': 'tbt',
            'city': 'Vilnius, LT',
            'currency_from': 'EUR',
            'currency_to': 'USD'
            }
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=47258b3b6592bb72b736e9746e9148d7"
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=ba548b6f2c3a4fec80baa69a364f2e0b"


@app.route("/")
def home():
    # get customized headlines, based on user input or default
    publiction = request.args.get('publication')
    if not publiction:
        publiction = DEFAULTS['publication']
    articles = get_news(publiction)
    # get customized weather based on user input or default
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    # get customized currency based on user input or default
    currency_from = request.args.get("currency_from")
    if not currency_from:
        currency_from = DEFAULTS['currency_from']
    currency_to = request.args.get('currency_to')
    if not currency_to:
        currency_to = DEFAULTS['currency_to']
    rate, currencies = get_rate(currency_from, currency_to)
    return render_template("home.html", articles=articles,
                           weather=weather, currency_from=currency_from,
                           currency_to=currency_to, rate=rate,
                           currencies=sorted(currencies))


def get_news(query):
    query = request.args.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()
    feed = feedparser.parse((RSS_FEEDS[publication]))
    return feed['entries']


def get_weather(query):
    query = urllib.parse.quote(query)
    url = WEATHER_URL.format(query)
    data = urllib.request.urlopen(url).read()
    parsed = json.loads(data.decode('utf-8'))
    weather = None
    if parsed.get("weather"):
        weather = {"description":
                       parsed["weather"][0]["description"],
                   "temperature": parsed["main"]["temp"],
                   "city": parsed["name"],
                   'country': parsed['sys']['country']
                   }
    return weather


def get_rate(frm, to):
    all_currency = urllib.request.urlopen(CURRENCY_URL).read()
    parsed = json.loads(all_currency.decode('utf-8')).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return (to_rate / frm_rate, parsed.keys())


if __name__ == '__main__':
    app.run(port=5000, debug=True)
