import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('key') or 'ductran123'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:tranduc123@habitmakr.cq4hhb9aoctr.us-east-1.rds.amazonaws.com:3306/innodb"
    UPLOADED_PHOTOS_DEST = 'uploads/photos'
    S3_BUCKET = 'mybloghost'
    S3_KEY = "ASIAR6R4OLQMJ5DDNO4Y"
    S3_SECRET = '4jWTuPUnJVgBT/qtuJZedgv2OyRPUIAN/u8L00C5'
    S3_SESSION_TOKEN = "FwoGZXIvYXdzENv//////////wEaDPcpDayX1VwlYUtRbyLNAQB9uLNKnagCuURF2qW55yntUc49993QlWDUlrLyxsSwRo9ipxuD69QTX15j+yHLUJGsjn4hvjksPxY7+qC95IsXQqXSy2B/woYuIUXW9f3k+ed3n9q7wK8dY6oGZA1HkouhRYJU/AN2JjOfPimT6JN7ZzMVkpj5JSjZCX7CJ0jkcfYuSRqIdKeZZavf6QR3+FfSGJYCrQMpweIaOCWaza515UkeYR7l4ingF42JHjl+z0gzBYS40S9DWCU1lnubPUYWXMGMbYBUIoubZtQo8vqXkwYyLX9J3a5+En3s+FwX0Sqv0FsWAweSqXjd1VZNWi7Nwm5pb30pXHqYp/v12XXl9w=="
    S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.gif','.jpeg','.raw']
    #"mysql+pymysql://admin:tranduc123@habitmakr.cq4hhb9aoctr.us-east-1.rds.amazonaws.com:3306/innodb" #os.environ.get('DATABASE_URL') or \'sqlite:///' + os.path.join(basedir, 'myblog.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS = 3