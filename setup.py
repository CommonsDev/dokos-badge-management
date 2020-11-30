# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in badge_management/__init__.py
from badge_management import __version__ as version

setup(
	name='badge_management',
	version=version,
	description='Badge management',
	author='Guerbadot Alexandre',
	author_email='guerbadot.alexandre@free.fr',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
