#!/usr/bin/env python
# Copyright 2011 The greplin-twisted-utils Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Setup script for greplin-twisted-utils."""

try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

setup(name='greplin-twisted-utils',
      version='0.1',
      description='Utilities for Twisted',
      license='Apache',
      author='Greplin, Inc.',
      author_email='opensource@greplin.com',
      url='http://www.github.com/Greplin/greplin-twisted-utilities',
      package_dir = {'':'src'},
      packages = [
        'greplin',
        'greplin.database',
        'greplin.defer',
        'greplin.net',
        'greplin.testing',
      ],
      namespace_packages = [
        'greplin',
        'greplin.database',
        'greplin.defer',
        'greplin.net',
        'greplin.testing',
      ],
      test_suite = 'nose.collector',
      zip_safe = True
)