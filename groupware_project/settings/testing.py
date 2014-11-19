from groupware_project.settings.base import *

DATABASES['default'] =  {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
}

DEBUG=False
DEBUG_TOOLBAR_CONFIG = {}
