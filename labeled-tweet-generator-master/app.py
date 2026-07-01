import os
from flask import Flask, request, render_template, jsonify
from tweet_exports import label_csv_tweets
from twitter import TwitterClient

app = Flask(__name__)
# Setup the client <query string, retweets_only bool, with_sentiment bool>
api = TwitterClient('@Saismita17')


def strtobool(v):
    return str(v).lower() in ["yes", "true", "t", "1"]


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/tweets')
def tweets():
    retweets_only = request.args.get('retweets_only')
    api.set_retweet_checking(strtobool(retweets_only))
    with_sentiment = request.args.get('with_sentiment')
    api.set_with_sentiment(strtobool(with_sentiment))
    query = request.args.get('query')
    api.set_query(query)

    tweets = api.get_tweets()
    return jsonify({'data': tweets, 'count': len(tweets)})


@app.route('/label_csv', methods=['POST'])
def label_csv():
    uploaded_file = request.files.get('tweet_csv')
    if uploaded_file is None or uploaded_file.filename == '':
        return jsonify({'error': 'Upload a CSV file first.'}), 400
    try:
        tweets = label_csv_tweets(uploaded_file, api.get_tweet_sentiment)
    except ValueError as error:
        return jsonify({'error': str(error)}), 400
    return jsonify({'data': tweets, 'count': len(tweets)})


port = int(os.environ.get('PORT', 5000))
app.run(host="0.0.0.0", port=port, debug=True)
