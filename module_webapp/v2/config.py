import os

CWD = os.getcwd()
"""
-1  all
0   disable
1.. debug level
"""
DEBUG = 0

WEB_BACK_PORT = 3000
WEB_FRONT_PORT = 8080
WEB_DB_PORT = 5432

WEB_HOME_PAGE = "templates/index.html"
WEB_FRONT_LSTN_HOST = "0.0.0.0"
WEB_BACK_LSTN_HOST = "0.0.0.0"
WEB_DB_LSTN_HOST = "0.0.0.0"
