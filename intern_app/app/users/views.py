from flask import abort, flash, redirect, render_template, url_for, send_file, session, request, jsonify
from . import user
from .. import db #this is to make sure we can query stuff
from ..models import Friends, User, InternProfile
from ..authperms.authperms import AuthPerms
import time

@user.route('/profile/<int:id>', methods=['GET'])
def home(id):
	check_perms = AuthPerms()
	if check_perms.isLoggedIn():
		user_info = User.query.get_or_404(id)
		intern_profile = InternProfile.query.get_or_404(id)
		return render_template('/users/profile.html', title='My Feed',
					intern=intern_profile, user=user_info,
					loading_my_profile=(id==session['profile']['user_id']))
	else:
		return redirect('/login')



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
@user.route('/add/friend', methods=['POST'])
def add_user():
	check_perms = AuthPerms()
	if check_perms.isLoggedIn():
		friend_add_id = request.form['friend_id']
		current_user_id = session['profile']['user_id']
		try:
			send_friend_request = Friends(user1_id=current_user_id,
							user2_id=int(friend_add_id),
							status=0, last_update_data=time.strftime('%Y-%m-%d'))
			db.session.add(send_friend_request)
			db.session.commit()
			return jsonify({"success":"Friend request sent"})
		#if we get an error, this means that a friend request at the least was sent. Lets check the relationship status next
		except:
			relationship_check = None
			if Friends.query.filter_by(user1_id=current_user_id, user2_id=friend_add_id).first() is None:
				relationship_check = Friends.query.filter_by(user1_id=friend_add_id, user2_id=current_user_id).first()
			else:
				relationship_check = Friends.query.filter_by(user1_id=current_user_id, user2_id=friend_add_id).first()
			if relationship_check.status == 2:
				return jsonify({"error":"Sorry you cannot send friend request to this user"})
			elif relationship_check.status == 1: # already friends
				return jsonify({"error":"You are already friends"})
			else:
				if relationship_check.user1_id == curent_user_id:
					return jsonify({"error":"Friend request is pending"})
				else:
					relationship_check.status = 1
					db.session.add(relationship_check)
					db.session.commit()
					return jsonify({"success":"You are now friends!. Make sure to say hi to them."})
