import os
import csv

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
    conversations_ordered = [[tweet for tweet in conversation] for conversation in conversations]
    print(conversations_ordered)
    return conversations_ordered
    # for conversation in conversations:
    #     for tweet in conversation:
    #         print(tweet['text'])
    # print(conversations)


        
                
                

    
build_conversation(tweets)