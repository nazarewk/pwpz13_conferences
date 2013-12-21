pwpz13_conferences
==================


Installing Python 2.7.6 @ Windows
------------------------
1. Install:

        http://www.python.org/ftp/python/2.7.6/python-2.7.6.msi
        
2. Prepend PATH with:

        C:\Python27\Scripts;C:\Python27\; ...

3. Download & install compiler for some plugins:

        http://go.microsoft.com/?linkid=7729279


Installing Django CMS 3 beta
----------------------------

        git clone https://github.com/divio/django-cms.git
        python django-cms/setup.py install
        
        
Installing requirements.txt
---------------------------

        pip install -r requirements.txt
        

Local settings
----------------
For local development settings create 'local_settings.py' in same folder as 'settings.py' and put modifications there.

Synchronizing database
----------------------

        manage.py syncdb

Starting development server
------------------------

        python manage.py runserver_plus

