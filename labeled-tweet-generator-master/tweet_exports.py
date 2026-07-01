import csv
from typing import Callable


TEXT_COLUMN_CANDIDATES = ("tweet", "text", "full_text", "content", "body", "message")


def find_text_column(fieldnames):
    if fieldnames is None:
        raise ValueError("CSV must include a header row.")
    normalized = {field.strip().lower(): field for field in fieldnames if field}
    for candidate in TEXT_COLUMN_CANDIDATES:
        if candidate in normalized:
            return normalized[candidate]
    available = ", ".join(sorted(normalized.values()))
    raise ValueError("CSV must include one text column. Available columns: {}".format(available))


def label_csv_tweets(file_storage, sentiment_for_text: Callable[[str], str]):
    text = file_storage.read().decode("utf-8-sig")
    reader = csv.DictReader(text.splitlines())
    text_column = find_text_column(reader.fieldnames)
    rows = []
    for row in reader:
        tweet_text = row.get(text_column)
        if tweet_text is None or not tweet_text.strip():
            continue
        rows.append({
            "text": tweet_text.strip(),
            "user": row.get("user", "csv"),
            "sentiment": sentiment_for_text(tweet_text),
        })
    if not rows:
        raise ValueError("CSV did not contain any non-empty tweet text.")
    return rows
