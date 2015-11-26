import os

class BaseConfig(object)
  DEBUG = false
  DATABASE = 'seo.db'
  MOZSCAPE_API_ACCESS_ID = ''
  MOZSCAPE_API_SECRET_KEY = ''

class DevelopementConfig(BaseConfig):
  DEBUG = True

class ProductionConfig(BaseConfig):
  DEBUG = True
