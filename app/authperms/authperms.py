from flask import session, redirect
#from ..models import Users
# we need to work on this more and make it easier.
class AuthPerms:
	def __init__(self):
		self.set = 'ok'

	def isLoggedIn(self):
		if 'profile' in session:
			return True

