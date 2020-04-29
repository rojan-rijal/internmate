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
def create_conversation(conversation_id, sender_name, sender_id, receiver):
    collection = chat_db[conversation_id]
    first_message = {"text":'{sender_name} added you as friend. Start a conversation :)'.format(sender_name=sender_name),
                    'sender_id':sender_id,
                    'created_at':datetime.now()}
    collection.insert_one(first_message)

def send_message(conversation_id, sender_id, text):
    collection = chat_db[conversation_id]
    post_message = {"text":text,
                    "sender_id":sender_id,
                    "created_at":datetime.now()}
    collection.insert_one(post_message)


def get_messages(conversation_id, page=0):
    offset = page * 0
    collection = chat_db[conversation_id]
    messages = list(
        collection.find().sort('_id', DESCENDING).limit(0).skip(offset))
    for message in messages:
        message['created_at'] = message['created_at'].strftime("%d %b, %H:%M")
        sender_info = requests.get('http://localhost:8000/api/user_exists/{id}'.format(id=message['sender_id'])).json()
        message.update({'sender_name':sender_info['name'],'sender_image':sender_info['image']})
    return messages[::-1]
