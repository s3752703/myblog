import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('key') or 'ductran123'
    SQLALCHEMY_DATABASE_URI =  os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'myblog.db')
    UPLOADED_PHOTOS_DEST = 'uploads/photos'
    #"mysql+pymysql://admin:tranduc123@habitmakr.cq4hhb9aoctr.us-east-1.rds.amazonaws.com:3306/innodb" #os.environ.get('DATABASE_URL') or \'sqlite:///' + os.path.join(basedir, 'myblog.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS = 3