import os
class Config(object):
	"""
	Regular Config for apis
	"""
	# any config


class DevConfig(Config): #sub class of Config
	DEBUG = True #this is for testing
	SQLALCHEMY_ECHO = True #print sql errors and result in the console
	SERVER_NAME = 'internmate.tech'
class ProdConfig(Config):
	DEBUG = False # do not do any sensitive console logging
	SESSION_COOKIE_DOMAIN = '.internmate.tech' # this is so we can use the same cookie on chat.
app_config = {
	'dev': DevConfig,
	'production': ProdConfig
}
