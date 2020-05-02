from .. import db
from ..models import Friends, User
from pymongo import MongoClient, DESCENDING
from datetime import datetime
import os

client = MongoClient('mongodb://chat_admin:{db_password}@{db_ip}'.format(db_password=os.environ.get('CHAT_PASS'),
                                                                        db_ip=os.environ.get('CHAT_IP')))

chat_db = client.get_database("chatdb")


"""
@@Function_Name: create_conversation
@@Function_Description: This function is called in api/views.py by add_user function.
					When a friend request is accepted via the add_user function, a 
					UUID is generated for the conversation and this function is called
					to create the first message. The first message is default to all users:
				    'XXXX added you as friend. Start a conversation'
					This function connects to the MongoDB not the main db that stores user information.
@@Input_Variables
				- conversation_id: String UUID unique to the friendship
				- sender_name: Name of the sender who initiated the first chat
				- sender_id: user_id of the sender who first sent the message
				- receiver: user_id of the receiver who received the first message
@@Output - This function does not output anything.
@@CODEOWNERS: Rojan Rijal & Brandon Nguyen 
"""
def create_conversation(conversation_id, sender_name, sender_id, receiver):
    collection = chat_db[conversation_id] # this creates a table for the conversation.
    first_message = {"text":'{sender_name} added you as friend. Start a conversation :)'.format(sender_name=sender_name),
                    'sender_id':sender_id,
                    'created_at':datetime.now(),
                    'receiver_id':receiver}
    collection.insert_one(first_message)



"""
@@Function_Name: is_friend
@@Function_Description: This function is called by multiple features throughout the application. 
					This is a helper function that helps to decide if two users are friend
					given both of their user_id's. 
@@Input_Variables
				- rec_id: user_id of the second user we are checking the relation with
				- current_id: user_id of the current logged in user. 
@@Output - Returns a boolean: True if Friends, False if not friends.
@@CODEOWNERS: Rojan Rijal
"""
def is_friend(rec_id, current_id):
	sent_by_current= Friends.query.filter_by(user1_id=current_id, user2_id=rec_id).first()
	if sent_by_current is not None:
		return True
	elif Friends.query.filter_by(user1_id=rec_id, user2_id=current_id).first() is not None:
		return True
	else:
		return False

"""
@@Function_Name: get_friends
@@Function_Description: This function is used mainly in the API calls and functions in api/views.py. 
					This function is used to query and get friends for the user_id that is passed into
					then function.
@@Input_Variables
				- current_id: user_id of the user whose friends are to be queried.
@@Output - Returns a list of User objects of all the friends that this user has. 
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
