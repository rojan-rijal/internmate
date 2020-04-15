from flask import session, redirect
from .. import db
from ..models import User
#from ..models import Users
# we need to work on this more and make it easier.
class AuthPerms:
	def __init__(self):
		self.set = 'ok'

	def isLoggedIn(self):
		if 'profile' in session:
			get_user = User.query.get(session['profile']['user_id'])
			if get_user is not None and get_user.online:
				return True
			else:
				return False
