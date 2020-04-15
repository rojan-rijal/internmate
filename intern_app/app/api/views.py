from flask import abort, flash, redirect, render_template, url_for, send_file, session, request, jsonify
from . import api
from .. import db #this is to make sure we can query stuff
from .helpers import is_friend, get_friends
from .posts import PostClass
from ..models import Friends, User, InternProfile, Posts, Likes
from ..authperms.authperms import AuthPerms
import time





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
					recommended_friends['recommend'].append({"user_id":user.user_id,"name":user_object.name})
		return jsonify(recommended_friends)
	else:
		return jsonify({"error":"Unauth request is not allowed"})


@api.route('/friends/<int:id>', methods=['GET'])
def list_friends(id):
	check_perms = AuthPerms()
	if check_perms.isLoggedIn():
		friends = {"friends":[]}
		friends_1 = Friends.query.filter_by(user1_id=id, status=1)
		friends_2 = Friends.query.filter_by(user2_id=id, status=1)
		for friend in friends_1:
			user_data = User.query.get(friend.user2_id)
			friends['friends'].append({'user_id':user_data.user_id,
							'name':user_data.name})
		for friend_2 in friends_2:
			user_data = User.query.get(friend_2.user1_id)
			friends['friends'].append({'user_id':user_data.user_id,
							'name':user_data.name})
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
				friend_requests['requests'].append({"user_id":user_info.user_id, "name":user_info.name})
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
						'likes':post.likes_count,
						'date':post.post_date,
						'body':post.post})
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
