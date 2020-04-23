from .. import db
from ..models import Friends, User
from pymongo import MongoClient, DESCENDING
from datetime import datetime
import os

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
                    'created_at':datetime.now(),
                    'receiver_id':receiver}
    collection.insert_one(first_message)

def is_friend(rec_id, current_id):
	sent_by_current= Friends.query.filter_by(user1_id=current_id, user2_id=rec_id).first()
	if sent_by_current is not None:
		return True
	elif Friends.query.filter_by(user1_id=rec_id, user2_id=current_id).first() is not None:
		return True
	else:
		return False

"""
@@Name: get_friends
@@Paremeters: current_id 
@@Description: Given a user id, return
a list of User objects for each of their friend.
"""
def get_friends(current_id):
	friends = []
	received = Friends.query.filter_by(user2_id=current_id, status=1)
	sent = Friends.query.filter_by(user1_id=current_id, status=1)
	for rec in received:
		friends.append(User.query.get(rec.user1_id))
	for sen in sent:
		friends.append(User.query.get(sen.user2_id))
	return friends
