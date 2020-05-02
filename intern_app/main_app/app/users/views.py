from flask import abort, flash, redirect, render_template, url_for, send_file, session, request, jsonify
from . import user
from .. import db #this is to make sure we can query stuff
from ..models import Friends, User, InternProfile
from ..authperms.authperms import AuthPerms
from ..api.helpers import is_friend
import time


"""
@@Funtion_Name: home
@@Function_Description: This is used to load profile feed of any user that exists on the system. 
					The HTML of this function (profile.html) calls JS functions from friends.js and 
					posts.js
@@Input_Variables: 
				- id - user_id of the user whose profile is being viewed.
@@HTTP_Method: GET
@@Output: A HTML rendering of the profile page of the user. The rendering will consist of friends the user has,
		any posts they have made, their name, their intership location and the company they are doing their internship at.
@@CODEOWNERS: Rojan Rijal
@@Last_Update_Date: April 05, 2020
"""
@user.route('/profile/<int:id>', methods=['GET'])
def home(id):
	check_perms = AuthPerms()
	if check_perms.isLoggedIn():
		user_info = User.query.get_or_404(id)
		intern_profile = InternProfile.query.get_or_404(id)
		is_friend_boolean = is_friend(id, session['profile']['user_id'])
		return render_template('/users/profile.html',
								title='My Feed',
								intern=intern_profile,
								user=user_info,
								loading_my_profile=(id==session['profile']['user_id']),
								is_friend=is_friend_boolean)
	else:
		return redirect('/login')


"""
@@Funtion_Name: newsfeed
@@Function_Description: This is used to load regular news feed for the user. It will return posts
					by their friends and them. This calls JS functions from friends.js, posts.js and microservices.js. 
@@Input_Variables: N/A
@@HTTP_Method: GET
@@Output: A HTML rendering of the newsfeed containing posts they and their friends have posted. It will also use foursquare and
		airbnb microservice to list places around the user's internship location and airbnb's around their place.
@@CODEOWNERS: Rojan Rijal
@@Last_Update_Date: April 05, 2020
"""
@user.route('/feed', methods=['GET'])
def newsfeed():
	check_perms = AuthPerms()
	if check_perms.isLoggedIn():
		intern = InternProfile.query.get(session['profile']['user_id'])
		if intern is not None:
			return render_template('/users/nf.html',
							title='News Feed',
							intern=intern)
		else:
			return redirect('/complete/profile')
	else:
		return redirect('/login')


"""
@@Funtion_Name: chat
@@Function_Description: This loads the chat ui for the user to message their friends. It uses JS functions from static/js/chat.js script.
@@Input_Variables: N/A
@@HTTP_Method: GET
@@Output: A HTML rendering of the chat UI. This will include list of their friends they have. chat.js then handles rest of the work along with the chat.html.
@@CODEOWNERS: Rojan Rijal
@@Last_Update_Date: April 22, 2020
"""
@user.route('/chat', methods=['GET'])
def chat():
	check_perms = AuthPerms()
	if check_perms.isLoggedIn():
		return render_template('/chat/chats.html', title="Chat")
	else:
		return redirect('/login')

"""
@@Funtion_Name: review_page
@@Function_Description: This loads a UI that allows interns to submit review about places they interned at. This feature is relatively new and is not polished yet.
@@Input_Variables: N/A
@@HTTP_Method: GET
@@Output: A HTML rendering of the review UI. 
@@CODEOWNERS: Rojan Rijal & Ean McGilvery
@@Last_Update_Date: April 25, 2020
"""
@user.route('/review', methods=['GET'])
def review_page():
	check_perms = AuthPerms()
	if check_perms.isLoggedIn():
		return render_template('/reviews/formview.html', title="Review Forms")
	else:
		return redirect('/login')


"""
@@Funtion_Name: view_review
@@Function_Description: This will load a page of all the reviews a particular company has received.
@@Input_Variables: 
				- company_name - Name of the company whose review is being viewed.
@@HTTP_Method: GET
@@Output: A HTML rendering of the reviews that the company has received. This will return a 404 if the company does not exist. 
@@CODEOWNERS: Rojan Rijal & Ean McGilvery
@@Last_Update_Date: April 25, 2020
"""
@user.route('/reviews/<string:company_name>', methods=['GET'])
def view_review(company_name):
	check_perms = AuthPerms()
	if check_perms.isLoggedIn():
		return render_template('/reviews/listrev.html', title='Review', company=company_name)
