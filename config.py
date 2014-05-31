import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
STEAM_API_KEY = 'E3486D8978BD38D19997E8E93A1B84C8'
CHARLES_STEAM_API_KEY = '58B99BF55D7419E24AABE5CCFCB2B590'
SECRET_KEY = 'you-will-never-guesss##'
