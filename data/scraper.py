import praw
import json
import time
# from classifier import classify
print("Setup done!")

def scrape_subreddit():
    print("Scraping started!")
    
    reddit = praw.Reddit(client_id='BVBZKW8DD2xFNcJm3FfLRQ',
                            client_secret='g34l7Pfyd29jeHnHPZFSZdqrJaQmJQ', user_agent='web-g34l7Pfyd29jeHnHPZFSZdqrJaQmJQ')

    subreddits=[]
    for subreddit in reddit.subreddits.popular(limit=100):
        subreddits.append(subreddit.display_name)
    
    for subreddit_name in subreddits:
        conversations={}
        choice=input("Press 'y' key to skip scraping subreddit: {} ".format(subreddit_name))
        time.sleep(3)
        if choice=='y':
            pass
            print("Skipped.")
        else:
            print("Scraping!")
            file_name=subreddit_name + '.json'
            file = open(file_name, 'a+', encoding='utf-8')
            subreddit = reddit.subreddit(subreddit_name)
            counter=0
            # Scrape the comments from the subreddit
            for submission in subreddit.hot(limit=None):
                new_convo = []
                submission.comments.replace_more(limit=None)
                for comments in submission.comments.list():
                    if comments.author is not None:
                        new_convo.append(
                            {'author': comments.author.name, 'body': comments.body})
                if len(new_convo) > 0:
                    new_convo = extract_conversations(new_convo)
                    if new_convo != []:
                        conversations.update({counter:new_convo})
                        counter+=1
            json.dump(conversations, file, indent=2)

def extract_conversations(data, conversations=None, current_conversation=None):
    try:
        # base case: return the conversations when there are no more messages to process
        if len(data) == 0:
            if len(current_conversation) >= 4:
                return current_conversation
            else:
                return []

        # initialize the conversations list and the current conversation if they are not provided
        if conversations is None:
            conversations = []
        if current_conversation is None:
            current_conversation = []

        # get the current message and the previous message (if there is one)
        current_message = data[0]
        previous_message = current_conversation[-1] if len(
            current_conversation) > 0 else None
        unique_authors = []
        # check if the current message is part of the current conversation
        if current_message['author'] is not None:
            for convo in current_conversation:
                unique_authors.append(convo['author'])

            participants = len(unique_authors) <= 2

            if previous_message is None or current_message['author'] == previous_message['author']:
                # add the current message to the current conversation
                current_conversation.append(current_message)

            elif current_message['author'] != previous_message['author'] and participants:
                if len(current_conversation) >= 2:
                    if current_message['author'] != current_conversation[-2]['author']:
                        del current_conversation[-2]
                    # add the current message to the current conversation
                current_conversation.append(current_message)

            elif current_message['author'] in unique_authors:
                current_conversation.append(current_message)

            else:
                # add the current conversation to the list of conversations and start a new conversation
                conversations.append(current_conversation)
                current_conversation = [current_message]

        # recursive call to process the rest of the data
        return extract_conversations(data[1:], conversations, current_conversation)
    except:
        return []

# write a function to check if emotion of last != previous ones, should return True/False

# def emotion_differs(conversation):
#     conversation_emotion = classify(' '.join(conversation[0:-1]['body']))
#     conversation_emotion = max(
#         conversation_emotion, key=conversation_emotion.get)
#     last_utterance_emotion = classify(conversation[-1]['body'])
#     last_utterance_emotion = max(
#         last_utterance_emotion, key=last_utterance_emotion.get)
#     if conversation_emotion != last_utterance_emotion:
#         conversation[0:-1]['emotion'] = conversation_emotion
#         conversation[-1]['emotion'] = last_utterance_emotion
#         print(conversation)
#         return (True, conversation)
#     return (False, ())

scrape_subreddit()
