from __future__ import with_statement
from fabric.api import local


def clean_pyc(settings='groupware_project.settings.development'):
    local('python manage.py clean_pyc --settings={}'.format(settings))


def collectstatic(settings='groupware_project.settings.development'):
    clean_pyc(settings)
    local('python manage.py collectstatic --settings={}'.format(settings))


def runserver(settings='groupware_project.settings.development'):
    clean_pyc(settings)
    local('python manage.py runserver --settings={}'.format(settings))


def migrate(settings='groupware_project.settings.development'):
    clean_pyc(settings)
    local('python manage.py makemigrations --settings={}'.format(settings))
    local('python manage.py migrate --settings={}'.format(settings))


def test(settings='groupware_project.settings.testing'):
    clean_pyc(settings)
    local('python manage.py test --failfast --settings={}'.format(settings))


def deploy(settings='groupware_project.settings.production'):
    pass
