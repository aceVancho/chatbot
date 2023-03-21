# set the organization and api key (you can get them from Manage Account page)
import openai
import os
import tracemalloc

def create_fine_tune_job():
    tracemalloc.start()
    # openai.organization = "Evancho Corp"
    openai.api_key = os.environ.get('OPEN_AI_KEY')
    path_to_processed_tweets = '/Users/adamevancho/VSCodeProjects/Personal/chatbot/server/assets/processed_texts/processed.jsonl'
    # upload the data to OpenAI Server
    file_meta_data = openai.File.create(
        file = open(path_to_processed_tweets, encoding='utf-8'),
        purpose='fine-tune'
        )

    # openai.FineTune.create(training_file=open(path_to_processed_tweets, encoding='utf-8'))

    

def list_fine_tune_jobs():
    tracemalloc.start()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.FineTune.list()

