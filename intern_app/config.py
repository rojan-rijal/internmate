import os
class Config(object):
	"""
	Regular Config for apis
	"""
	# any config


class DevConfig(Config): #sub class of Config
	DEBUG = True #this is for testing
	SQLALCHEMY_ECHO = True #print sql errors and result in the console
class ProdConfig(Config):
	DEBUG = False # do not do any sensitive console logging
app_config = {
	'dev': ProdConfig,
	'production': ProdConfig
}
