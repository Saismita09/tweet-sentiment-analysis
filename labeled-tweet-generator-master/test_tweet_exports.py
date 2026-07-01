import io
import unittest

from tweet_exports import find_text_column, label_csv_tweets


class TweetExportTests(unittest.TestCase):
    def test_find_text_column_accepts_common_export_names(self):
        self.assertEqual(find_text_column(["id", "full_text"]), "full_text")

    def test_label_csv_tweets_skips_blank_rows(self):
        csv_file = io.BytesIO(b"user,text\nalice,Great launch\nbob,\n")

        rows = label_csv_tweets(csv_file, lambda text: "positive")

        self.assertEqual(rows, [{"text": "Great launch", "user": "alice", "sentiment": "positive"}])


if __name__ == "__main__":
    unittest.main()
