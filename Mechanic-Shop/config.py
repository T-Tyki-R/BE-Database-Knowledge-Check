class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Saiouma2018@localhost/mechanic_shop'
    DEBUG = True
    # Redis configuration for Flask-Limiter
    RATELIMIT_STORAGE_URI = 'redis://localhost:6379/0'

class TestingConfig:
    SQLALCHEMY_DATABASE_URL = 'sql:///testing.db'
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'

class ProductionConfig:
    pass