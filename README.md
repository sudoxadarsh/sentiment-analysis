# Tweet Sentiment Analysis

This Flask app uses NLTK's VADER sentiment analyzer to classify tweets as
positive, negative, or neutral. Enter one tweet per line to see each
classification and an overall count for the submitted tweets.

## Setup

From the project directory, install the Python packages and NLTK's VADER
lexicon:

```powershell
python -m pip install -r requirement.txt
python -m nltk.downloader vader_lexicon
```

Run the app:

```powershell
python app.py
```

Open the local URL printed by Flask in your browser. The app analyzes tweet
text that you enter or paste; it does not connect to or download data from
Twitter/X.
