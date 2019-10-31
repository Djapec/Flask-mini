from config.__init__ import  Config


class Development(Config):
    ENV_TYPE = "Dev"

    DB_NAME = 'praksa_baza'
    DB_USER = 'pedja.radovanovic'
    DB_PASSWD = 'pedja'
    DB_HOST = '127.0.0.1'
    DB_PORT = 5432

    SQLALCHEMY_DATABASE_URI = "postgres://qhyxtfjdfwgsct:61662661e35384237c67f5445ae6e5c4481be0004505b15754d9b39a2387365d@ec2-54-228-252-67.eu-west-1.compute.amazonaws.com:5432/d2sv19p29av74o"

