import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('key') or 'ductran123'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:tranduc123@habitmakr.cq4hhb9aoctr.us-east-1.rds.amazonaws.com:3306/innodb"
    UPLOADED_PHOTOS_DEST = 'uploads/photos'
    S3_BUCKET = 'mybloghost'
    S3_KEY = "ASIAR6R4OLQMPINJURP3"
    S3_SECRET = '5pceR5tqOfxtXGIDhYOwakMOqjZmsc8BpW/JcPsB'
    S3_SESSION_TOKEN = "FwoGZXIvYXdzENf//////////wEaDCC3ePaC3zufCKgw0yLNAeXTMrO7C8JF5va+RzIGy2Wn5KKjMVo1j1cmNo46S1g2cXpKo6CXxaOFpO8vTH4AivuProzePLctgLZaIyKcPbcx7dADDCD+YVOuYakujolnzJ5BKijBH4C41AdQDzavbgYCdHgos+MCtUIFURWrEkZkVi9JRvJhypXiXb5M2+DifPP4ev2Jwan+9MG+OyPrStgDIDGm668Fz/ALVFF2hB2eh3Z7r99HD5c5HtAcgR8DMIPNe91/K216Ev2cF35ZOydWCOW7xoj/7zq8HW4o4ImXkwYyLXH6z5erzJME1eTzYClpld6Zr4hM60EexLKtc9JYbag458lzD61vf64LGeA6bw=="
    S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.gif','.jpeg','.raw']
    #"mysql+pymysql://admin:tranduc123@habitmakr.cq4hhb9aoctr.us-east-1.rds.amazonaws.com:3306/innodb" #os.environ.get('DATABASE_URL') or \'sqlite:///' + os.path.join(basedir, 'myblog.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS = 3