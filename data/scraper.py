import praw
import pandas as pd
import re
import nltk

reddit = praw.Reddit(client_id='BVBZKW8DD2xFNcJm3FfLRQ', client_secret='g34l7Pfyd29jeHnHPZFSZdqrJaQmJQ', user_agent='web-scraper')
ml_subreddit = reddit.subreddit('MachineLearning')

df = []

def clean_text(text):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    text = re.sub(r"[0-9]", "",text)
    text = re.sub(r"\S*https?:\S*", "", text)
    text = re.sub(r"(\(.*\))|(\[.*\])|", "",text).split()
    text = [word for word in text if not word in stop_words]
    return ' '.join(text)

for post in ml_subreddit.hot(limit=100):
    if post.num_comments>5:
        conversation = [clean_text(post.selftext)]
        submission = reddit.submission(id=post.id)
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            if len(conversation)<=10:
                conversation.append([clean_text(comment.body)])
        df.append([conversation, post.title, post.id, post.subreddit, post.url, post.created])

print("done")
conversations = pd.DataFrame(df,columns=['conversation', 'title', 'id', 'subreddit', 'url', 'created'])
conversations.to_csv("./data/reddit_conversation_data.csv", index=False)

