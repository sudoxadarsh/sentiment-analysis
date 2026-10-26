import unittest
from unittest.mock import patch

from app import app


class FakeSentimentAnalyzer:
    def polarity_scores(self, tweet: str) -> dict[str, float]:
        scores = {
            "I love this!": 0.8,
            "This is awful.": -0.8,
            "The meeting starts at 3.": 0.0,
        }
        return {"compound": scores[tweet]}


class SentimentAnalysisTests(unittest.TestCase):
    def setUp(self) -> None:
        app.config["TESTING"] = True
        self.client = app.test_client()

    @patch("app.SentimentIntensityAnalyzer", return_value=FakeSentimentAnalyzer())
    def test_classifies_multiple_tweets_and_returns_summary(self, _analyzer) -> None:
        response = self.client.post(
            "/",
            data={
                "tweets": (
                    "I love this!\n"
                    "This is awful.\n"
                    "The meeting starts at 3."
                )
            },
        )

        self.assertEqual(response.status_code, 200)
        page = response.get_data(as_text=True)
        self.assertIn("Positive:</strong> 1", page)
        self.assertIn("Negative:</strong> 1", page)
        self.assertIn("Neutral:</strong> 1", page)
        self.assertIn("Compound score:</strong> 0.80", page)
        self.assertIn("Compound score:</strong> -0.80", page)

    @patch("app.SentimentIntensityAnalyzer", side_effect=LookupError)
    def test_shows_setup_help_if_vader_lexicon_is_missing(self, _analyzer) -> None:
        response = self.client.post("/", data={"tweets": "A tweet"})

        self.assertEqual(response.status_code, 200)
        self.assertIn("python -m nltk.downloader vader_lexicon", response.get_data(as_text=True))

    def test_rejects_empty_tweet_input(self) -> None:
        response = self.client.post("/", data={"tweets": " \n "})

        self.assertEqual(response.status_code, 200)
        self.assertIn("Please enter at least one tweet", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
