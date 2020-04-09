from flask import abort, flash, redirect, render_template, url_for, send_file, session, request, jsonify
from . import api
from .. import db #this is to make sure we can query stuff
from .helpers import is_friend
from ..models import Friends, User, InternProfile
from ..authperms.authperms import AuthPerms
import time

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
