pwpz13_conferences
==================


Installing Python 2.7.6 @ Windows
------------------------
1. Install:

        http://www.python.org/ftp/python/2.7.6/python-2.7.6.msi
        
2. Prepend PATH with:

        C:\Python27\Scripts;C:\Python27\; ...

3. Download & install Visual Studio 2008 Express Edition (must be 2008!):

        http://go.microsoft.com/?linkid=7729279
        
Installing PIP
--------------
Follow instructions http://www.pip-installer.org/en/latest/installing.html


Installing requirements.txt
---------------------------

        pip install -r requirements.txt
        

Local settings
----------------
For local development settings create 'local_settings.py' in same folder as 'settings.py' and put modifications there.

Synchronizing database & executing South migrations
----------------------

        manage.py syncdb --all
		manage.py migrate --fake

Starting development server
------------------------

        python manage.py runserver_plus

