from flask import session, redirect
from .. import db
from ..models import User
#from ..models import Users
# we need to work on this more and make it easier.


"""
@@Class_name: AuthPerms
@@Class_Description: This class and its function isLoggedIn is used by every
				function in the application where authentication is mandated.
				This checks if the user sending certain requests 1) exists in
				2) and is marked online on the db. 
@@CODEOWNERS: Rojan Rijal
@@Last_Update_Date: April 01, 2020
"""
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
