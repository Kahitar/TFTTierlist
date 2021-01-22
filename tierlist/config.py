

class Config:
	# TODO (for production): Move all secret variables to environment variables: os.environ.get('EMAIL_USER')
	SECRET_KEY = '1e8e9af8178e72a84fd40773555a02cf'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
	MAIL_SERVER = 'mail.gmx.net'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = 'weight-assist@gmx.de'
	MAIL_PASSWORD = 'aKiR2TLMfKR9BDB' 