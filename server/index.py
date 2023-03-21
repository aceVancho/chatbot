from scripts.preprocess import clean_message
from scripts.format_tweets import *
from scripts.write_tweets import write_tweets

processed_texts_path = './assets/processed_texts/processed.jsonl'

def run_app():
    tweets = extract_csv_data(abs_file_path)
    tweet_obj = build_tweets(tweets)
    conversation_pairs = build_prompt_completion_pairs(tweet_obj)
    write_tweets(conversation_pairs, processed_texts_path)

def test_app():
    print('This is a test.')

if __name__ == "__main__":
    run_app()