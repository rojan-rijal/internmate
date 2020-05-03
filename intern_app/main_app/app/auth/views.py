from flask import abort, flash, redirect, render_template, url_for, send_file, session, Markup
from random import choice
from . import auth
from .. import db
from ..authperms.authperms import AuthPerms
from ..models import User, InternProfile
from .forms import InternProfileForm

"""
@@Funtion_Name: complete_profile
@@Function_Description: This function will load the complete_profile page when a new user signs up.
					The GET method will load a form for the user to fill. When a POST http method request
					is sent to the server, this function will parse the data of the form to their respective
					matters. It will then create an internship profile for the user. The form used in this request
					is defined in auth/forms.py
@@Input_Variables: 
				- form.company_name.data - Name of the company current user is joining
				- form.company_website.data - Website of the company the current user is joining
				- form.city.data - City that the current user will be interning at
				- form.state.data - State that the current user will be interning at.
				- form.start_data.data - A DateTime object of when the user is starting their internship
@@HTTP_Method: GET, POST
@@Output: A HTTP redirect that sends the user to their own profile page.
@@CODEOWNERS: Rojan Rijal
@@Last_Update_Date: April 06, 2020
"""
@auth.route('/complete/profile', methods=['GET','POST'])
def complete_profile():
	check_perms = AuthPerms()
	if check_perms.isLoggedIn():
		intern_profile = InternProfile.query.filter_by(user_id=session['profile']['user_id']).first()
		form = InternProfileForm()
		if form.validate_on_submit():
			intern = InternProfile.query.filter_by(user_id=session['profile']['user_id']).first()
			if intern is None:
				add_profile = InternProfile(company_name=form.company_name.data,
								company_website = form.company_website.data,
								city = form.city.data, 
								state = form.state.data, 
								start_date = form.start_date.data, 
								user_id = session['profile']['user_id'])
				db.session.add(add_profile)
				db.session.commit()
			else:
				print('----Updating profile-----')
				intern.city = form.city.data
				intern.state = form.state.data
				db.session.add(intern)
				db.session.commit()
			return redirect('/profile/{id}'.format(id=session['profile']['user_id']))
		if intern_profile:
			form.company_name.data = intern_profile.company_name
			form.company_website.data = intern_profile.company_website
			form.city.data = intern_profile.city
			form.state.data = intern_profile.state
			form.start_date.data = intern_profile.start_date
		return render_template('/auth/formview.html', form = form, title = 'Complete my Profile')
	else:
		return redirect('/login')

"""
@auth.route('/callback')
def callback_handling():
	auth0.authorize_access_token()
	resp = auth0.get('userinfo')
	userinfo = resp.json()
	session['jwt_payload'] = userinfo
	session['profile'] = {
		'user_id': userinfo['sub'],
		'name': userinfo['name'],
		'email':userinfo['email']
	}
	return redirect('/')
"""
