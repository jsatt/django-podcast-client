#!/usr/bin/env python

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup
import os
import sys

version = '0.2.3'

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    sys.exit()

if sys.argv[-1] == 'tag':
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

setup(name='django-podcast-client',
      version=version,
      description='A client for downloading and organzing podcasts.',
      author='Jeremy Satterfield',
      author_email='jsatt22@gmail.com',
      url='http://github.com/jsatt/django-podcast-client',
      license='GNU General Public License v3 (GPLv3)',
      packages=[
          'podcast_client', 'podcast_client.api', 'podcast_client.management',
          'podcast_client.management.commands', 'podcast_client.migrations',
      ],
      include_package_data=True,
      install_requires=[
          'South',
          'Django>=1.5, <1.7',
          'django-extensions',
          'python-dateutil',
          'requests',
          'lxml',
          'celery>=3.1',
          'djangorestframework<3.0',
      ],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Framework :: Django',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Utilities',],
     )
