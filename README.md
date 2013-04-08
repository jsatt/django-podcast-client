Django Podcast Client
=====================
Django Podcast Client implements a simple podcasting client that can be used
from both the command line and your browser. If you choose to only use as a
command line tool, there is no need to run a Django instance as a service.

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

To running tests also requires nose and mox, run
`pip install mox nose django-nose`. You can then run `fab test`.

To manually run the app and admin, you'll want to run `fab syncdb` then
`fab migrate`, then you can run `fab serve` to start the Django dev server,
or `fab shell` to open the Django shell.

Please make sure any pull requests are PEP8 compliant and pass pyflakes. It's
also preferable that an issue is opened and discussed before a pull request is
merged.
