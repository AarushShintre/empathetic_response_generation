# emotional-response-generation

The scraper.py file uses PRAW to get data from a specific subreddit locally. The classifier uses the data brought in by scraper.py, and sorts out conversations that meet the criteria, and also labels the overall conversation's and the last utterance's emotion. It is seen that approximately 50% of the raw data actually does meet the criteria. 

I have used the pretrained bert model and tokenizer(Here: https://www.kaggle.com/datasets/aimenbaig/savedbertmodelandtokenizer). 

Empathetic_response_generation
  |
  |=======> data
  |         |_____reddit_conversation_data_raw.bin
  |         |_____reddit_conversation_data_processed.csv
  |         |_____scraper.py
  |         |_____classifier.py
  |
  |=======> kaggle .....(save the pretrained bert model here)
  |         |_____ working
  |                 |_____tokenizer
  |                       |_____special_tokens_map.json
  |                       |_____vocab.txt
  |                       |_____tokenizer_config.json
  |                 |_____model
  |                       |_____pytorch_model.bin
  |                       |_____finetunemodel.pt
  |                       |_____config.json
  |         |_____ input
  |                 |_____ emotions-dataset-for-nlp
  |                         |_____train.txt
  |                         |_____val.txt
  |                         |_____test.txt
  |
  |___________________________________________________________
