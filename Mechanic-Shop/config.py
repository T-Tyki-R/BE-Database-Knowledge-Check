class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Coconut1@localhost/mechanic_shop'
    DEBUG = True
    # Redis configuration for Flask-Limiter
    RATELIMIT_STORAGE_URI = 'redis://localhost:6379/0'

class TestingConfig:
    pass

class ProductionConfig:
    pass