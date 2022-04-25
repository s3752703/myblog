import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('key') or 'ductran123'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:tranduc123@habitmakr.cq4hhb9aoctr.us-east-1.rds.amazonaws.com:3306/innodb"
    UPLOADED_PHOTOS_DEST = 'uploads/photos'
    S3_BUCKET = 'mybloghost'
    S3_KEY = "DgZTg0tpvhD1fPQD6haIuOs0Ptcrm6YAo7SuuVZA"
    S3_SECRET = '4jWTuPUnJVgBT/qtuJZedgv2OyRPUIAN/u8L00C5'
    S3_SESSION_TOKEN = "FwoGZXIvYXdzEOT//////////wEaDKbFUSNLJGBvN04UZCLNAa/wECUOBXX4dcLiMbZURriuOwLgniaHGyjwxk/0o4I5GrOrwz4uE7lDGd4K0P085uI6yntnhjYN7SnNusxE+U+5qsYxXk1RrhIVbmAdR1Wrrbfj0dpqCiznjunCsIOR1mk0jfrsrf9J/2rzUz4pcubJ+mGnJaaE2H61sovXWBBq8DKRNCikH5kiyTdlP3mRhB9rmMVSA3Htezxzkyuy0wPns0eFVbMj36YPhGVC/KzfWLjl3gdqXVHhE1jH/cW8X7elvL13W3/ixuzFl2co3vmZkwYyLUDqdduqeWbsQfmpgAvZGYQdMtEJc5rjw5m7oBQmXHADWKCDZvv310OYBNC+dQ=="
    S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.gif','.jpeg','.raw']
    #"mysql+pymysql://admin:tranduc123@habitmakr.cq4hhb9aoctr.us-east-1.rds.amazonaws.com:3306/innodb" #os.environ.get('DATABASE_URL') or \'sqlite:///' + os.path.join(basedir, 'myblog.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS = 3