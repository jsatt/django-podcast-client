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

setup(name='django-podcast-client',
      version='0.1.1',
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
          'Django>=1.5',
          'django-extensions',
          'python-dateutil',
          'requests',
          'lxml',
          'djangorestframework',
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
