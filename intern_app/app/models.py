from app import db

class User(db.Model):
	__tablename__ = 'users'

	user_id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(60), index=True, unique=True) # we can also search by username if needed
	name = db.Column(db.String(60))
	facebook = db.Column(db.Boolean, default=False)
	google = db.Column(db.Boolean, default=False)
	linkedin = db.Column(db.Boolean, default=False)
	online = db.Column(db.Boolean, default=False)
	image_url = db.Column(db.Text, nullable=True)


# class for intern_profile table
class InternProfile(db.Model):
	__tablename__ = 'intern_profile'
	user_id = db.Column(db.Integer, primary_key=True)
	company_name = db.Column(db.Text,nullable=False)
	company_website = db.Column(db.String(255), nullable=False)
	location = db.Column(db.Text, nullable=False)
	start_date = db.Column(db.DateTime, nullable=False)

class Friends(db.Model):
	__tablename__ = 'friends'
	status = db.Column(db.Integer, index=True, nullable=False)
	user1_id = db.Column(db.Integer, index=True, nullable=False, primary_key=True)
	user2_id = db.Column(db.Integer, index=True, nullable=False, primary_key=True)
	last_update_data = db.Column(db.DateTime, nullable=False)

class Posts(db.Model):
	__tablename__ = 'posts'
	post_id = db.Column(db.Integer, index=True, primary_key=True)
	post = db.Column(db.Text, nullable=False)
	likes_count = db.Column(db.Integer, nullable=False)
	author_id = db.Column(db.Integer, nullable=False, index=True)
	post_date = db.Column(db.DateTime, nullable=False)

class Likes(db.Model):
	__tablename__ = 'likes'
	like_id = db.Column(db.Integer, index=True, primary_key=True)
	post_id = db.Column(db.Integer, index=True, nullable=False)
	liker_id = db.Column(db.Integer, index=True, nullable=False)
	like_date = db.Column(db.DateTime, nullable=False)
