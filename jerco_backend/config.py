import os

class Config:
    SECRET_KEY = os.environ.get('170503') or 'anda-harus-mengganti-ini-dengan-string-yang-lebih-kuat'
    # Konfigurasi Database MySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'mysql+pymysql://root:Qwerty1717@localhost/jerco_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('171717') or 'super-secret-jwt-key'
    JWT_ACCESS_TOKEN_EXPIRES = 3600 # 1 jam

    # Konfigurasi Mail (opsional, jika nanti ada fitur email)
    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # ADMINS = ['your-email@example.com']

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Qwerty1717@localhost/jerco_db' # Database terpisah untuk testing

class ProductionConfig(Config):
    DEBUG = False
    # Di produksi, Anda harus memiliki variabel lingkungan yang lebih kuat
    SECRET_KEY = os.environ.get('171717')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    JWT_SECRET_KEY = os.environ.get('170503')