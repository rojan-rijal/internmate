from .. import db
from ..models import Friends, User


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
