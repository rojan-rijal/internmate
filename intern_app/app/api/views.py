from flask import abort, flash, redirect, render_template, url_for, send_file, session, request, jsonify
from . import api
from .. import db #this is to make sure we can query stuff
from .helpers import is_friend, get_friends, create_conversation
from .posts import PostClass
from ..models import Friends, User, InternProfile, Posts, Likes, Conversations, Reviews
from ..authperms.authperms import AuthPerms
from datetime import datetime
import uuid
import time




"""
Auth api for chat
"""

@api.route('/user_exists/<int:id>', methods=['GET'])
def user_exists(id):
	get_user = User.query.get(id)
	if get_user is not None and get_user.online:
		return jsonify({"status":True,"name":get_user.name,"image":get_user.image_url})
	else:
		return jsonify({"status":False})

"""
Following functions deal with friends related api calls:
recommend_friends, list_friends, add_friends, rejgect friends
"""


@api.route('/recfriends', methods=['GET'])
def recommend_friends():
	check_perms = AuthPerms()
	if check_perms.isLoggedIn():
		recommended_friends = {"recommend":[]}
		intern_profile = InternProfile.query.get_or_404(session['profile']['user_id'])
		same_company_users = InternProfile.query.filter_by(company_name=intern_profile.company_name)
		for user in same_company_users:
			if user.user_id != session['profile']['user_id']:
				user_object = User.query.get(user.user_id)
				if not is_friend(user.user_id, session['profile']['user_id']):
					recommended_friends['recommend'].append({"user_id":user.user_id,"name":user_object.name,"user_pic":user_object.image_url})
		return jsonify(recommended_friends)
	else:
		return jsonify({"error":"Unauth request is not allowed"})


@api.route('/friends/<string:id>', methods=['GET'])
def list_friends(id):
	check_perms = AuthPerms()
	if check_perms.isLoggedIn():
		friends = {"friends":[]}
		if id != "me":
			friends_1 = Friends.query.filter_by(user1_id=int(id), status=1)
			friends_2 = Friends.query.filter_by(user2_id=int(id), status=1)
		else:
			friends_1 = Friends.query.filter_by(user1_id=session['profile']['user_id'], status=1)
			friends_2 = Friends.query.filter_by(user2_id=session['profile']['user_id'], status=1)
		for friend in friends_1:
			user_data = User.query.get(friend.user2_id)
			if id != "me":
				friends['friends'].append({'user_id':user_data.user_id,
								'name':user_data.name,"user_pic":user_data.image_url})
			else:
				conversation = Conversations.query.filter_by(conversation_id=friend.conversation_id).first()
				friends['friends'].append({'user_id':user_data.user_id,
								'name':user_data.name,"user_pic":user_data.image_url,"conv_id":friend.conversation_id,
								'conv_timestamp':conversation.last_updated})
		for friend_2 in friends_2:
			user_data = User.query.get(friend_2.user1_id)
			if id != "me":
				friends['friends'].append({'user_id':user_data.user_id,
								'name':user_data.name,"user_pic":user_data.image_url})
			else:
				conversation = Conversations.query.filter_by(conversation_id=friend_2.conversation_id).first()
				friends['friends'].append({'user_id':user_data.user_id,
								'name':user_data.name,"user_pic":user_data.image_url, "conv_id":friend_2.conversation_id,
								'conv_timestamp':conversation.last_updated})
		return jsonify(friends)
	else:
		return jsonify({"error":"Unauth request is not allowed"})

@api.route('/friendrequests', methods=['GET'])
def get_requests():
	check_perms = AuthPerms()
	if check_perms.isLoggedIn():
			friend_requests = {"requests":[]}
			requests = Friends.query.filter_by(user2_id=session['profile']['user_id'],status=0)
			for request in requests:
				user_info = User.query.get(request.user1_id)
				friend_requests['requests'].append({"user_id":user_info.user_id, "name":user_info.name, "user_pic":user_info.image_url})
			return jsonify(friend_requests)
	else:
		return jsonify({"error":"Unauth request is not allowed"})


"""
Parameters: friend_id.

Function description:
This will add a user as friend with
another user. This is done by getting
friend_id from a POST request. When friend_id
is received it will check to see if they are
already friends. If it is, it will return an error, else
update database with their friendship

Coder: Rojan Rijal
"""
@api.route('/add/friend', methods=['POST'])
def add_user():
	check_perms = AuthPerms()
	if check_perms.isLoggedIn():
		friend_add_id = request.form['friend_id']
		current_user_id = session['profile']['user_id']
		received = Friends.query.filter_by(user1_id=friend_add_id, user2_id=current_user_id).first()
		sent = Friends.query.filter_by(user1_id=current_user_id, user2_id=friend_add_id).first()
		if received is not None:
			if received.status == 0:
				received.status = 1
				conversation_id = str(uuid.uuid4())
				received.conversation_id = conversation_id
				create_conversation(conversation_id, session['profile']['name'], current_user_id, friend_add_id)
				add_conversation = Conversations(conversation_id=conversation_id,
												last_updated=datetime.now())
				db.session.add(add_conversation)
				db.session.commit()
				received.last_update_data = time.strftime('%Y-%m-%d')
				db.session.add(received)
				db.session.commit()

				return jsonify({"success":"Friend request accepted"})
			elif received.status == 1:
				return jsonify({"error":"You are already friends"})
		elif sent is not None:
			if sent.status == 0:
				return jsonify({"error":"Your friend request is pending"})
			elif sent.status == 1:
				return jsonify({"error":"You are already friends"})
			else:
				return jsonify({"error":"Sorry you cannot send a friend request to this person"})
		else:
			send_friend_request = Friends(user1_id=current_user_id, user2_id=int(friend_add_id),
							status=0, last_update_data=time.strftime('%Y-%m-%d'))
			db.session.add(send_friend_request)
			db.session.commit()
			return jsonify({"success":"Friend request sent"})


@api.route('/reject/friend', methods=['POST'])
def reject_request():
	check_perms = AuthPerms()
	if check_perms.isLoggedIn():
		friend_reject_id = request.form['friend_id']
		current_user_id = session['profile']['user_id']
		received = Friends.query.filter_by(user2_id=current_user_id, user1_id=int(friend_reject_id)).first()
		if received is not None:
			if received.status == 0:
				received.status = 3
				received.last_update_data = time.strftime('%Y-%m-%d')
				db.session.add(received)
				db.session.commit()
				return jsonify({"success":"Request rejected"})
			elif received.status == 1:
				return jsonify({"error": "You cannot cancel an already accepted request"})
			else:
				return jsonify({"error": "Request is already cancelled"})
		else:
			return jsonify({"error":"This person hasn't sent you a friend request yet"})



"""
Following API calls deal with POST related calls:
add_post, like_post, comment_post
"""
#post_object = PostClass(session['profile']['user_id'])
@api.route('/post/add', methods=['POST'])
def add_post():
	check_perms = AuthPerms()
	if check_perms.isLoggedIn():
		post_content = request.form['post_body']
		author_id = session['profile']['user_id']
		add_post = Posts(post=post_content, author_id=author_id, likes_count=0, post_date=time.strftime('%Y-%m-%d'))
		db.session.add(add_post)
		db.session.commit()
		return jsonify({"success":"Post created"})
	else:
		return jsonify({"error":"Unauth posting is not allowed"})


@api.route('/post/load/<string:pageType>', methods=['GET'])
def load_posts(pageType):
	check_perms = AuthPerms()
	if check_perms.isLoggedIn():
		posts = {"posts":[]}
		current_id = session['profile']['user_id']
		my_posts = Posts.query.filter_by(author_id=current_id)
		for post in my_posts:
			user = User.query.get(post.author_id)
			posts['posts'].append({'post_id':post.post_id,
						'author_id':post.author_id,
						'author_name':user.name,
						'author_pic':user.image_url,
						'likes':post.likes_count,
						'date':post.post_date,
						'body':post.post})
		if pageType.isdigit():
			posts = {"posts":[]}
			user_posts = Posts.query.filter_by(author_id=int(pageType))
			for post in user_posts:
				user = User.query.get(post.author_id)
				posts['posts'].append({'post_id':post.post_id,
							'author_id':post.author_id,
							'author_name':user.name,
							'author_pic':user.image_url,
							'likes':post.likes_count,
							'date':post.post_date,
							'body':post.post})
			return jsonify(posts)
		if pageType == 'pp':
			return jsonify(posts)
		elif pageType == 'nf':
			friends = get_friends(current_id)
			for friend in friends:
				friend_posts = Posts.query.filter_by(author_id=friend.user_id)
				for post in friend_posts:
					user = User.query.get(post.author_id)
					posts['posts'].append({'post_id':post.post_id,
								'author_id':post.author_id,
								'author_name':user.name,
								'author_pic':user.image_url,
								'likes':post.likes_count,
								'date':post.post_date,
								'body':post.post})
			return jsonify(posts)
		else:
			return jsonify({"error":"Invalid post query. Only pp or nf is allowed"})
	else:
		return jsonify({"error":"Uanuth query is not allowed"})

@api.route('/post/like', methods=['POST'])
def like_post():
	check_perms = AuthPerms()
	if check_perms.isLoggedIn():
		current_id = session['profile']['user_id']
		post_id = request.form['post_id']
		post = Post.query.get(post_id=int(post_id))
		likedOrNot = Likes.query.filtery_by(liker_id=current_id, post_id=post_id).first()
		if likeOrNOt is not None:
			post.likes_count -= 1
			db.session.add(post)
			db.session.delete(likedOrNot)
			db.session.commit()
			return jsonify({"success":"Disliked"})
		else:
			post.likes_count += 1
			db.sesion.add(post)
			addLike = Likes(post_id=post.post_id, liker_id=current_id,
					like_date = time.strftime('%Y-%m-%d'))
			db.session.add(addLike)
			db.session.commit()
			return jsonify({"success":"Liked"})
	else:
		return jsonify({"error":"Unauth action is not allowed"})


"""
Reiew features.
Code owner: Ean McGilvery
"""

@api.route('/reviews/add', methods=['POST'])
def add_review():
	check_perms = AuthPerms()
	if check_perms.isLoggedIn():
		print(request.form['review_body'])
		current_user_id = session['profile']['user_id']
		review_title = request.form['review_title']
		num_of_stars = request.form['num_of_stars']
		review_body = request.form['review_body']
		company_title = request.form['company_title']
		position_name = request.form['position_name']
		job_location = request.form['job_location']

		add_post = Reviews(user_id = current_user_id,
					star_rating = num_of_stars,
					comment_title = review_title,
					comment_body = review_body,
					company_name = company_title,
					position_title = position_name,
					location = job_location,
					posting_date  = time.strftime('%Y-%m-%d'))
		db.session.add(add_post)
		db.session.commit()
		return jsonify({"success":"Review created"})
	else:
		return jsonify({"Error":"Unauth review is not allowed"})



@api.route('/reviews/<string:input_company_name>', methods=['GET'])
def view_company_reviews(input_company_name):
	check_perms = AuthPerms()
	if check_perms.isLoggedIn():
		review_query = Reviews.query.filter_by(company_name = input_company_name).all()
		if review_query is None:
			return jsonify({"Error":"No review available for the company"})
		else:
			review_list = {'Review':[]}
			for result in review_query:
				user = User.query.get(result.user_id)
				review_list['Review'].append({'user_name':user.name, 'image_url': user.image_url,
											'num_stars': result.star_rating, 'review_title': result.comment_title,
											'review_body': result.comment_body})
			return jsonify(review_list)
