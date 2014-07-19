# This file contains the WSGI configuration required to serve up your
# web application at http://byrenx.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#
# The below has been auto-generated for your Django project

activate_this = '/home/byrenx/.virtualenvs/django16/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))


import os
import sys

# add your project directory to the sys.path
project_home = u'/home/byrenx/rbmo'
if project_home not in sys.path:
    sys.path.append(project_home)

# set environment variable to tell django where your settings.py is
os.environ['DJANGO_SETTINGS_MODULE'] = 'rbmo.settings'

# serve django via WSGI
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
