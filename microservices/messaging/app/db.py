#Brandon Nguyen and Rojan Rijal
#April 28, 2020
from datetime import datetime
import os, requests
from bson import ObjectId
from pymongo import MongoClient, DESCENDING

client = MongoClient('mongodb://chat_admin:{db_password}@{db_ip}'.format(db_password=os.environ.get('CHAT_PASS'),
                                                                        db_ip=os.environ.get('CHAT_IP')))

chat_db = client.get_database("chatdb")




"""
This is called when they add each other as friends
"""
#Creates conversation between to users once they have added each other as friends
#Sends the users who added a "wink"
def create_conversation(conversation_id, sender_name, sender_id, receiver):
    collection = chat_db[conversation_id]
    first_message = {"text":'{sender_name} added you as friend. Start a conversation :)'.format(sender_name=sender_name),
                    'sender_id':sender_id,
                    'created_at':datetime.now()}
    collection.insert_one(first_message)

#This fucntion takes in a conversation ID, sender Id and the text of the message
#It then pulls conversation history from the database and store it in the list variable collection
#Post message then sends a message and the inserts it to the collection list
def send_message(conversation_id, sender_id, text):
    collection = chat_db[conversation_id]
    post_message = {"text":text,
                    "sender_id":sender_id,
                    "created_at":datetime.now()}
    collection.insert_one(post_message)

#Take in conversation id and page num
def get_messages(conversation_id, page=0):
    offset = page * 0
    #call the collection list and pull conversation history from DB
    collection = chat_db[conversation_id]
    #display messages in order of when they were sent 
    messages = list(
        collection.find().sort('_id', DESCENDING).limit(0).skip(offset))
    for message in messages:
        message['created_at'] = message['created_at'].strftime("%d %b, %H:%M")
        sender_info = requests.get('http://localhost:8000/api/user_exists/{id}'.format(id=message['sender_id'])).json()
        message.update({'sender_name':sender_info['name'],'sender_image':sender_info['image']})
    return messages[::-1]
