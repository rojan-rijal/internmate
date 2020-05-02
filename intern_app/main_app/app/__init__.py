"""

This script creates the main app and runs it from here.
CODEOWNERS: Rojan Rijal, Brittany Kraemer, Brandon Nguyen, Janeen Yamak, Ean McGilvery
"""

from flask import Flask, render_template, send_file, session, jsonify, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from authlib.flask.client import OAuth
from six.moves.urllib.parse import urlencode
from flask_wtf.csrf import CSRFProtect
# local imports
from config import app_config
db = SQLAlchemy()
csrf = CSRFProtect()
def create_app():
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_object(app_config['production'])
	app.config.from_pyfile('config.py')
	app.config['SERVER_DOMAIN'] = '.internmate.tech'
	app.config['SESSION_COOKIE_DOMAIN'] = '.internmate.tech'
	Bootstrap(app)
	csrf.init_app(app)
	oauth = OAuth(app)
	db.init_app(app)
	auth0 = oauth.register(
		'auth0',
		client_id='b8IJ3nS40w2Hvetco79z5NChA6NLJOel',
		client_secret='tfIxeIut3gBZI_7Hwrwbd5vpxzFQRzIhrBqfbxHt-ArShk6GTyX_woPgQV1Hl_d8',
		api_base_url='https://internmate-dev.auth0.com',
		access_token_url='https://internmate-dev.auth0.com/oauth/token',
		authorize_url='https://internmate-dev.auth0.com/authorize',
		client_kwargs={
			'scope': 'openid profile email',
		},
	)
	from app import models
	from app.models import User

	from .users import user as user_blueprint
	app.register_blueprint(user_blueprint)

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint)

	from .api import api as api_blueprint
	app.register_blueprint(api_blueprint, url_prefix='/api')

	def add_user(user_info): #used when a new user signs in. We add them to db
		loginType = user_info['sub']
		google = 'google' in loginType
		facebook = 'facebook' in loginType
		linkedin = 'linkedin' in loginType
		user = User(email=user_info['email'],name=user_info['name'],online=True,
				google = google, facebook = facebook, linkedin=linkedin, image_url=user_info['picture'])
		db.session.add(user)
		db.session.commit()


	"""
	After successful login from Auth0, we take a callback to verify
	the login mechanism
	""""
	@app.route('/callback')
	def callback_handling():
		auth0.authorize_access_token()
		resp = auth0.get('userinfo')
		userinfo = resp.json()
		user = User.query.filter_by(email=userinfo['email']).first()
		# following can  be improved
		loginType = userinfo['sub']
		google = 'google' in loginType
		facebook = 'facebook' in loginType
		linkedin = 'linkedin' in loginType

		# add the new login flow on setup if there is any
		if user is not None: # user has already registered before
			# for the following if check, i am thinking of storing mode of login as an array instead of boolean to make it easier.
			if not user.google:
				user.google = google
			if not user.facebook:
				user.facebook = facebook
			if not user.linkedin:
				user.linkedin = linkedin
			update_login_mode = User.query.filter_by(user_id=user.user_id).update(dict(google=user.google, linkedin=user.linkedin,
											facebook = user.facebook, online=True))
			db.session.commit()
			session['jwt_payload'] = userinfo
			session['profile'] = {
				'user_id': user.user_id,
				'name': userinfo['name'],
				'picture': userinfo['picture'],
				'email': userinfo['email'],
				'username': userinfo['nickname']
			}
			return redirect('/feed')
		else:
			add_user(userinfo)
			user = User.query.filter_by(email=userinfo['email']).first()
			session['jwt_payload'] = userinfo
			session['profile'] = {
				'user_id': user.user_id,
				'name': userinfo['name'],
				'picture': userinfo['picture'],
				'email': userinfo['email'],
				'username': userinfo['nickname']
			}
			return redirect('/complete/profile')

	@app.route('/login')
	def login():
		print(session)
		if 'profile' in session:
			get_user = User.query.get(session['profile']['user_id'])
			if get_user is not None and get_user.online:
				return redirect('/feed')
			else:
				return auth0.authorize_redirect(redirect_uri='https://internmate.tech/callback', audience='https://internmate-dev.auth0.com/userinfo')
		return auth0.authorize_redirect(redirect_uri='https://internmate.tech/callback', audience='https://internmate-dev.auth0.com/userinfo')

	@app.route('/logout')
	def logout():
		user_notonline = User.query.filter_by(email=session['profile']['email']).update(dict(online=False))
		db.session.commit()
		session.clear()
		params = {'returnTo':'https://internmate.tech', 'client_id': '47qc5c1iQ4p39w7M5YtptgZQdGJR573b'}
		#return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))
		return redirect('/')

	@app.route('/')
	def home():
		return render_template('home/index.html')

	@app.errorhandler(403)
	def forbidden(e):
		return render_template('403.html')
	return app
