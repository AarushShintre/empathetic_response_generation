import torch
from transformers import BertTokenizer, BertConfig, BertForSequenceClassification,BertConfig
import pickle
import csv
from itertools import chain
import os
# import re
# import nltk

MODEL_NAME = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME,local_files_only=True,use_differentiable_head=True)
config = BertConfig.from_pretrained(MODEL_NAME, num_labels=6,output_hidden_states=True)

model = BertForSequenceClassification.from_pretrained(MODEL_NAME,num_labels=6,)
model.eval()
model.load_state_dict(torch.load("/Users/aarush/emotional_response_generation/kaggle/working/model/pytorch_model.bin",map_location=torch.device('cpu')) ,strict=False)
 
def classify(txt):
  encodings = tokenizer.encode_plus(
      txt,
      None,
      add_special_tokens=True,
      max_length= 256,
      padding='max_length',
      return_token_type_ids=True,
      truncation=True,
      return_attention_mask=True,
      return_tensors='pt')  

  labels= ['anger', 'fear', 'joy', 'love', 'sadness' ,'surprise'] 

  model.eval()
  with torch.no_grad():
      input_ids=encodings.input_ids
      attention_mask=encodings.attention_mask
      token_type_ids=encodings.token_type_ids
      output=model(input_ids,attention_mask,token_type_ids)
      final_output = torch.sigmoid(output.logits).cpu().detach().numpy().tolist()

  probabilities=list(chain.from_iterable(final_output))
  predictions = dict(zip(labels,probabilities))
  return max(predictions, key = predictions.get)

# def clean_text(txt):
#     stop_words = set(nltk.corpus.stopwords.words('english'))
#     txt = re.sub(r"[0-9]", "",txt)
#     txt = re.sub(r"\S*https?:\S*", "", txt)
#     txt = re.sub(r"(\(.*\))|(\[.*\])|", "",txt).split()
#     txt = [word for word in txt if not word in stop_words]
#     return ' '.join(txt)
bin_path='./data/reddit_conversation_data_raw.bin'
csv_path='./data/reddit_conversation_data_processed.csv'

with open(bin_path, 'rb') as bin_file, open(csv_path,'a+') as csv_file:
  write_csv=csv.writer(csv_file,quoting=csv.QUOTE_NONE,escapechar='\\')
  read_csv=csv.reader(csv_file)
  add_counter=0
  counter=0
  if os.stat(csv_path).st_size == 0:
    write_csv.writerow(['conversation','title','id','subreddit','url','created', 'conversation_label','last_utterance_label'])
  while True:
    try:
      line=pickle.load(bin_file)
      counter+=1
      #check wether conditions of the emotion are met
      conversation_emotion=classify(' '.join(line[0][0:-1]))
      last_utterance_emotion=classify(line[0][-1])
      if conversation_emotion!=last_utterance_emotion:#if met add that conversation to the csv file
        add_counter+=1
        write_csv.writerow([line[0],line[1],line[2],line[3],line[4],line[5],conversation_emotion,last_utterance_emotion])
    except EOFError:
      print((add_counter/counter)*100)
      break

