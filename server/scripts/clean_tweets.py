import os
import csv

import itertools
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer

script_dir = os.path.dirname(__file__)
rel_path = "../assets/sample.csv"
# rel_path = "../assets/twcs.csv"
abs_file_path = os.path.join(script_dir, rel_path)


def extract_csv_data(path):
    with open(path, newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        return [ row for row in reader ]


tweets = extract_csv_data(abs_file_path)

def build_conversation(tweets):
    all_tweets = {}
    starter_tweet_ids = []
    conversations = []

    def appendResponses(tweet, conversation):
        conversation.append(tweet)
        response_tweet_id = tweet['response_tweet_id']
        if response_tweet_id:
            response_tweet = all_tweets.get(response_tweet_id)
            if response_tweet:
                return(appendResponses(response_tweet, conversation))
        else:
            conversations.append(conversation)

    for tweet in tweets:
        if tweet['in_response_to_tweet_id'] == '':
            tweet_id = tweet['tweet_id']
            starter_tweet_ids.append(tweet_id)

        all_tweets[tweet['tweet_id']] = tweet

    for tweet_id in starter_tweet_ids:
        new_conversation = []
        starter_tweet = all_tweets.get(tweet_id)
        appendResponses(starter_tweet, new_conversation)

    # test
    conversations_ordered = [[tweet['text'] for tweet in conversation] for conversation in conversations]
    return conversations_ordered

def preprocess_text(text):
    nltk.download('stopwords')
    nltk.download('punkt')
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words('english'))

    text = text.lower()
    words = word_tokenize(text)
    words = [word for word in words if word not in stop_words]
    words = [stemmer.stem(word) for word in words]
    text = ' '.join(words)
    text = ''.join(character for character in text if character.isalpha() or character.isspace())

    return text
        
# build_conversation(tweets)