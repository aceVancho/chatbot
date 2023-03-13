import os
import csv

import openai
import itertools
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from openai.api_resources import Model

script_dir = os.path.dirname(__file__)
rel_path = "../assets/sample.csv" # Actual path: "../assets/twcs.csv"
abs_file_path = os.path.join(script_dir, rel_path)
nltk.download('stopwords')
nltk.download('punkt')
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))
openai.api_key = os.environ.get('OPEN_AI_KEY')

def extract_csv_data(path):
    with open(path, newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        return [ row for row in reader ]

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

    # TODO: consider preprocessing text elsewhere
    conversations_ordered = [[(preprocess_text(tweet['text'])) for tweet in conversation] for conversation in conversations]
    return conversations_ordered

def preprocess_text(text):
    text = text.lower()
    words = word_tokenize(text)
    words = [word for word in words if word not in stop_words]
    words = [stemmer.stem(word) for word in words]
    text = ' '.join(words)
    text = ''.join(character for character in text if character.isalpha() or character.isspace())
    text = text.strip()
    return text
        
def write_conversations(conversations_ordered, path):
    with open(path, 'w') as f:
        for conversation in conversations_ordered:
            f.write('\n'.join(conversation))
            f.write('\n\n')  # add two newlines to separate conversations

# TODO: Train model

tweets = extract_csv_data(abs_file_path)
conversations_ordered = build_conversation(tweets)
write_conversations(conversations_ordered, 'preprocessed_conversations.text')