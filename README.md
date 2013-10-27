Django Podcast Client
=====================
Django Podcast Client implements a simple podcasting client that can be used
from both the command line and your browser. If you choose to only use as a
command line tool, there is no need to run a Django instance as a service.

[![Build Status](https://travis-ci.org/jsatt/django-podcast-client.png?branch=master)](https://travis-ci.org/jsatt/django-podcast-client)
[![Coverage Status](https://coveralls.io/repos/jsatt/django-podcast-client/badge.png)](https://coveralls.io/r/jsatt/django-podcast-client)

Setup
-----
Install using pip:

    pip install git://github.com/jsatt/django-podcast-client.git

Create new django instance (skip this if you already have one):

    django-admin.py startproject <project name>
    cd <project name>
    python manage.py syncdb

run `chmod +x manage.py` to run as `./manage.py <command>` from here on out

Add to installed apps in `<project name>/settings.py`:

    INSTALLED_APPS = (
        ...
        django_extensions,
        south,
        podcast_client
    )

Setup the database:

    ./manage.py migrate podcast_client

Add urls in `<project name>/urls.py` (skip if only using CLI):

    urlpatterns = ('',
    ...
    (r'^podcasts/', include('podcast_client.urls')),
    )

Using in Browser
----------------
Start Django server:

    ./manage.py runserver

There are a slew of other ways to run as a service which I will leave up to you
to research.
[How to deploy with WSGI](https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/)

Browse to `http://<localhost or hostname>:8000/podcasts/`.

Using Command-line
------------------
TODO

Requirements
------------
TODO

Contibuting
-----------
Django expects a few things to be setup for development that you won't have
without a project.  I've borrowed a pattern used by
[jsocol](https://github.com/jsocol) which uses Fabric.

Be sure to install Fabric using `pip install fabric`, and use `fab` to run your
developement environment. Run `fab -l` to see all options.

Running tests also requires nose and mox. Run
`pip install mox nose django-nose` to install. You can then run `fab test`.

To manually run the app, you'll want to run `fab syncdb` then `fab migrate`,
then you can run `fab serve` to start the Django dev server, or `fab shell` to
open the Django shell.

Please make sure any pull requests are PEP8 compliant, pass pyflakes, and have
complete test coverage. It's also preferable that an issue is opened and
discussed before a pull request is merged.

License
-------

Django Podcast Client
Copyright (C) 2013 Jeremy Satterfield

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
