"""
This page is under deployment and not currently
used in any part of the application. This can be
ignored for now. It will most likely be used
when code is refactored in future when we 
go for public deployment to the world.
""""

from flask import session
from .. import db
from ..models import Posts
import time

class PostClass:
	def __init__(self, user_id):
		self.__user_id = user_id

	def add_post(self, post_body):
		try:
			add_post_db = Posts(post=post_body,
					likes_count=0,
					author_id=self.__user_id,
					post_date=time.strftime('%Y-%m-%d'))
			db.session.add(add_post_db)
			db.session.commit()
			return True
		except:
			return False
