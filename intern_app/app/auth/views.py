from flask import abort, flash, redirect, render_template, url_for, send_file, session, Markup
from random import choice
from . import auth
from .. import db
from ..authperms.authperms import AuthPerms
from ..models import User, InternProfile
from .forms import InternProfileForm


@auth.route('/complete/profile', methods=['GET','POST'])
def complete_profile():
	check_perms = AuthPerms()
	if check_perms.isLoggedIn():
		intern_profile = InternProfile.query.filter_by(user_id=session['profile']['user_id']).first()
		form = InternProfileForm()
		if form.validate_on_submit():
			try:
				add_profile = InternProfile(company_name=form.company_name.data, company_website = form.company_website.data,
								location = form.location.data, start_date = form.start_date.data, user_id = session['profile']['user_id'])
				db.session.add(add_profile)
				db.session.commit()
			except:
				update_internship = InternProfile.query.filter_by(user_id=session['profile']['user_id']).update(dict(company_name=form.company_name.data,
																company_website = form.company_website.data,
																location = form.location.data,
																start_date = form.start_date.data))
				db.session.commit()
			finally:
				return redirect('/profile/{id}'.format(id=session['profile']['user_id']))
		if intern_profile:
			form.company_name.data = intern_profile.company_name
			form.company_website.data = intern_profile.company_website
			form.location.data = intern_profile.location
			form.start_date.data = intern_profile.start_date
		return render_template('/auth/formview.html', form = form, title = 'Complete my Profile')
	else:
		return '403 Access Denied'

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
