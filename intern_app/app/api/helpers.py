from .. import db
from ..models import Friends


def is_friend(rec_id, current_id):
	sent_by_current= Friends.query.filter_by(user1_id=current_id, user2_id=rec_id).first()
	if sent_by_current is not None:
		return True
	elif Friends.query.filter_by(user1_id=rec_id, user2_id=current_id).first() is not None:
		return True
	else:
		return False
