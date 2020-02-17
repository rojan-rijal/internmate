from flask import abort, flash, redirect, render_template, url_for, send_file, session, Markup
from random import choice
from string import ascii_lowercase, digits
from . import user
from ..authperms.authperms import AuthPerms


@user.route('/private', methods=['GET'])
def home():
	check_perms = AuthPerms()
	if check_perms.isLoggedIn():
		return 'Logged in'
	else:
		return redirect('/login')
