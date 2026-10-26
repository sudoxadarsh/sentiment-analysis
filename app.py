from flask import Flask, render_template, request
from nltk.sentiment.vader import SentimentIntensityAnalyzer

app = Flask(__name__)


def classify_tweet(tweet: str, analyzer: SentimentIntensityAnalyzer) -> dict[str, str]:
    compound = analyzer.polarity_scores(tweet)["compound"]
    if compound >= 0.05:
        sentiment = "positive"
    elif compound <= -0.05:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {
        "text": tweet,
        "sentiment": sentiment,
        "score": f"{compound:.2f}",
    }


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    submitted_tweets = request.form.get("tweets", "")
    tweets = [line.strip() for line in submitted_tweets.splitlines() if line.strip()]
    if not tweets:
        return render_template(
            "index.html",
            submitted_tweets=submitted_tweets,
            error="Please enter at least one tweet to analyze.",
        )

    try:
        analyzer = SentimentIntensityAnalyzer()
    except LookupError:
        return render_template(
            "index.html",
            submitted_tweets=submitted_tweets,
            error=(
                "The NLTK VADER lexicon is missing. Install it by running "
                "'python -m nltk.downloader vader_lexicon' and try again."
            ),
        )

    results = [classify_tweet(tweet, analyzer) for tweet in tweets]
    summary = {
        sentiment: sum(result["sentiment"] == sentiment for result in results)
        for sentiment in ("positive", "negative", "neutral")
    }
    return render_template(
        "index.html",
        submitted_tweets=submitted_tweets,
        results=results,
        summary=summary,
    )


if __name__ == "__main__":
    app.run(debug=True)
