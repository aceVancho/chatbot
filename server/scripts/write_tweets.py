import json

def write_tweets(conversation_pairs, path):
    tweets_written = 0
    with open(path, 'a') as f:
        for pair in conversation_pairs:
            f.write(json.dumps(pair) + '\n')
            print('Tweets written:', tweets_written)
            tweets_written += 1
        # f.write('\n')