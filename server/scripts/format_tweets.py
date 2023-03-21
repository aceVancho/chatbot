from scripts.preprocess import clean_message, add_completion_end, add_prompt_separator

import os
import csv
import json

import openai
import itertools
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from openai.api_resources import Model

script_dir = os.path.dirname(__file__)
rel_path = "../assets/training_data/sample.csv" # Sample path: "../assets/twcs.csv"
# rel_path = "../assets/training_data/twcs.csv" # Actual path: "../assets/twcs.csv"
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

def build_tweets(tweets):
    tweet_obj = {}
    for tweet in tweets:
        tweet_obj[tweet['tweet_id']] = tweet
    return tweet_obj

def build_prompt_completion_pairs(tweet_obj):
    conversation_pairs = []
    for tweet_id, tweet in tweet_obj.copy().items():
        tweet_has_multiple_responses = ',' in tweet['response_tweet_id']
        prompt_message = clean_message(tweet['text'])
        prompt_message = add_prompt_separator(prompt_message)

        if not tweet_has_multiple_responses:
            response_id = tweet['response_tweet_id']
            response_tweet = tweet_obj.get(response_id)
            if response_tweet:
                completion_message = clean_message(response_tweet['text'])
                completion_message = add_completion_end(completion_message)
                pair = {
                    'prompt': prompt_message,
                    'completion': completion_message
                }

                conversation_pairs.append(pair)

        else:
            response_ids = tweet['response_tweet_id'].split(',')
            for response_id in response_ids:
                response_tweet = tweet_obj.get(response_id)
                if response_tweet:
                    completion_message = clean_message(response_tweet['text'])
                    completion_message = add_completion_end(completion_message)
                    pair = {
                    'prompt': prompt_message,
                    'completion': completion_message
                }

                conversation_pairs.append(pair)
    return conversation_pairs


#     with open(path, newline='', encoding='utf-8') as csv_file:
#         reader = csv.DictReader(csv_file)
#         return [ row for row in reader ]

# def chooseRole(role):
#     return 'user' if role.isnumeric() else 'assistant' 

# def build_conversation(tweets):
#     all_tweets = {}
#     starter_tweet_ids = []
#     conversations = []
#     complete = 0

#     def appendResponses(tweet, conversation):
#         conversation.append(tweet)
#         response_tweet_id = tweet['response_tweet_id']
#         if response_tweet_id:
#             response_tweet = all_tweets.get(response_tweet_id)
#             if response_tweet:
#                 return(appendResponses(response_tweet, conversation))
#         else:
#             conversations.append(conversation)

#     for tweet in tweets:
#         if tweet['in_response_to_tweet_id'] == '':
#             tweet_id = tweet['tweet_id']
#             starter_tweet_ids.append(tweet_id)

#         all_tweets[tweet['tweet_id']] = tweet

#     for tweet_id in starter_tweet_ids:
#         new_conversation = []
#         starter_tweet = all_tweets.get(tweet_id)
#         appendResponses(starter_tweet, new_conversation)

#     conversations_ordered = []
#     for conversation in conversations:
#         temp_conversation = []
#         for tweet in conversation:
#             # temp_conversation.append({ 'role': chooseRole(tweet['author_id']), 'content': tweet['text'] })
#             print({ 'role': chooseRole(tweet['author_id']), 'content': tweet['text'] })
#             complete += 1
#             print(f'Tweets written: {complete}\n\n')
#             # TODO: Fix Preprocess Text
#             # temp_conversation.append({ 'role': chooseRole(tweet['author_id']), 'content': preprocess_text(tweet['text']) })

#         # pairs = create_conversation_pairs(temp_conversation)
#         # # TODO: make relative
#         # path = '/Users/adamevancho/VSCodeProjects/Personal/chatbot/server/assets/processed_texts/processed2.jsonl'
#         # write_conversations(pairs, path)

#         # complete += len(temp_conversation)
#         # print(f'Tweets written: {complete} // Pairs written: {complete/2}')
#         # conversations_ordered.append(temp_conversation)
  
#     # return conversations_ordered

# def create_conversation_pairs(temp_conversation):
#     pairs = [{"prompt": temp_conversation[i]['content'], "completion": temp_conversation[i+1]['content']} for i in range(0, len(temp_conversation)-1, 2)]
#     return pairs


# def preprocess_text(text):
#     text = text.lower()
#     words = word_tokenize(text)
#     words = [word for word in words if word not in stop_words]
#     words = [stemmer.stem(word) for word in words]
#     text = ' '.join(words)
#     text = ''.join(character for character in text if character.isalpha() or character.isspace())
#     text = text.strip()
#     return text
        
# def write_conversations(pairs, path):
#     with open(path, 'a') as f:
#         for pair in pairs:
#             f.write(json.dumps(pair) + '\n')
#         # f.write('\n')

# # TODO: Train model
# def train_model(conversations_ordered):
#     model_engine = 'gpt-3.5-turbo'
#     for conversation in conversations_ordered:
#         completion = openai.ChatCompletion.create(
#             model=model_engine,
#             messages=conversation
#         )
#         response = completion.choices[0].message
#         print('RESPONSE', response)