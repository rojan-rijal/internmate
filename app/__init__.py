from flask import Flask, render_template, send_file, session, jsonify, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from authlib.flask.client import OAuth
from six.moves.urllib.parse import urlencode

# local imports
from config import app_config


def create_app():
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_object(app_config['production'])
	app.config.from_pyfile('config.py')
	Bootstrap(app)

	#migrate = Migrate(app, db)

	#from app import models

	oauth = OAuth(app)
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

	from .users import user as user_blueprint
	app.register_blueprint(user_blueprint)

	#from .admin import admin as admin_blueprint
	#app.register_blueprint(admin_blueprint)

	#from .home import home as home_blueprint
	#app.register_blueprint(home_blueprint)

	#from .api import api as api_blueprint
	#app.register_blueprint(api_blueprint)

	@app.route('/callback')
	def callback_handling():
		auth0.authorize_access_token()
		resp = auth0.get('userinfo')
		userinfo = resp.json()
		session['jwt_payload'] = userinfo
		session['profile'] = {
			'user_id': userinfo['sub'],
			'name': userinfo['name'],
			'picture': userinfo['picture'],
			'email': userinfo['email'],
			'username': userinfo['nickname'],
		}
		print(userinfo)
		return redirect('/')

	@app.route('/login')
	def login():
		return auth0.authorize_redirect(redirect_uri='http://localhost:8000/callback', audience='https://internmate-dev.auth0.com/userinfo')

	@app.route('/logout')
	def logout():
		session.clear()
		params = {'returnTo':'http://localhost:8000', 'client_id': '47qc5c1iQ4p39w7M5YtptgZQdGJR573b'}
		return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

	@app.errorhandler(403)
	def forbidden(e):
		return render_template('403.html')
	return app
