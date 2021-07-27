"""
Local settings

- Run in Debug mode

- Use console backend for emails

- Add Django Debug Toolbar
- Add django-extensions as app
"""
from .base import *  # noqa

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = False
# TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# django-debug-toolbar
# ------------------------------------------------------------------------------
# MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
# INSTALLED_APPS += ['debug_toolbar', ]

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = '2gmA=c.l,^O9;%9ea0&?F=z@cjq1eg$XPi+`0Gb*1P3xH6%}},'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', ]

import socket
import os
# tricks to have debug toolbar when developing with docker
if os.environ.get('USE_DOCKER') == 'yes':
    ip = socket.gethostbyname(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + '1']

# DEBUG_TOOLBAR_CONFIG = {
#     'DISABLE_PANELS': [
#         'debug_toolbar.panels.redirects.RedirectsPanel',
#     ],
#     'SHOW_TEMPLATE_CONTEXT': True,
# }

# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ['django_extensions', ]

