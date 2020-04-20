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




@user.route('/feed', methods=['GET'])
def newsfeed():
	check_perms = AuthPerms()
	if check_perms.isLoggedIn():
		intern = InternProfile.query.get_or_404(session['profile']['user_id'])
		return render_template('/users/nf.html', title='News Feed', intern=intern)
	else:
		return redirect('/login')
