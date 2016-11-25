from flask import Flask
import feedparser

app = Flask(__name__)


RSS_FEEDS = {
    'bbc' : 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn' : 'http://rss.cnn.com/rss/edition.rss',
    'fox' : 'http://feeds.foxnews.com/foxnews/latest',
    'iol' : 'http://www.iol.co.za/cmlink/1.640'
}


@app.route("/")
@app.route("/<publication>")
def get_news(publication="bbc"):
    try:
        feed = feedparser.parse(RSS_FEEDS[publication])
        first_article = feed['entries'][0]
    except KeyError:
        return "<h1>Publication not found</h1>"

    return """
    <html>
        <title>
            RSS FEEDS
        </title>
        <body>
            <h1 style="color:blue;margin-left:30px;">{0} News Headlines</h1>
            <b> {1} </b> </br>
            <i> {2} </i> </br>
            <p> {3} </p> </br>
        </body>
    </html>
    """.format(
        publication.upper(),
        first_article.get('title'),
        first_article.get('published'),
        first_article.get('summary')
    )

if __name__ == '__main__':
    app.run(port=5000, debug=True)
