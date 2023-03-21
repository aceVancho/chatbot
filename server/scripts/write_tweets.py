import json

def write_tweets(conversation_pairs, path):
    with open(path, 'a') as f:
        for pair in conversation_pairs:
            f.write(json.dumps(pair) + '\n')
        # f.write('\n')