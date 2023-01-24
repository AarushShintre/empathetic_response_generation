import praw
import pickle

reddit = praw.Reddit(client_id='BVBZKW8DD2xFNcJm3FfLRQ', client_secret='g34l7Pfyd29jeHnHPZFSZdqrJaQmJQ', user_agent='web-scraper')
subreddit = reddit.subreddit('CasualConversation')

with open("./data/reddit_conversation_data_raw.bin", 'ab+') as file:
    while True:
        for post in subreddit.hot():
            if post.num_comments>5:
                conversation = [post.selftext]
                submission = reddit.submission(id=post.id)
                for comment in submission.comments.list():
                    if len(conversation)<=10:
                        conversation.append(comment.body)
            pickle.dump([conversation, post.title, post.id, post.subreddit, post.url, post.created],file)

