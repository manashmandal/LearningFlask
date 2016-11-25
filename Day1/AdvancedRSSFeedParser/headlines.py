from flask import Flask
import feedparser
from flask import render_template
from flask import request
from _credentials_ import keys

import requests
import json


app = Flask(__name__)


RSS_FEEDS = {
    'bbc' : 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn' : 'http://rss.cnn.com/rss/edition.rss',
    'fox' : 'http://feeds.foxnews.com/foxnews/latest',
    'iol' : 'http://www.iol.co.za/cmlink/1.640'
}


@app.route("/", methods=['GET', 'POST'])
def get_news():
    query = request.form.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()

    feed = feedparser.parse(RSS_FEEDS[publication])
    weather = get_weather("London,UK")

    return render_template("home.html", articles=feed['entries'], weather=weather)


def get_weather(query):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q=" + query + "&units=metric&appid=" + keys.OPEN_WEATHER_MAP_API_KEY

    try:
        data = requests.get(api_url).json()
        weather = {
            "description": data['weather'][0]['description'],
            "temperature": data['main']['temp'],
            "city": data['name']
        }

    except json.decoder.JSONDecodeError:
        weather = None

    return weather

if __name__ == '__main__':
    app.run(port=5000, debug=True)