import os
import sys
sys.path.append('~/public_html/domain1.com/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'MyTestProject.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
