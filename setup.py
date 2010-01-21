#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys

from setuptools import setup, find_packages

from distutils.command.install_data import install_data
from distutils.command.install import INSTALL_SCHEMES

def read(*path):
	return open(os.path.join(os.path.abspath(os.path.dirname(__file__)), *path)).read()

events = __import__('events', {}, {}, [''])

packages, data_files = [], []

root_dir = os.path.dirname(__file__)
if root_dir != '':
	os.chdir(root_dir)

events_dir = "events"

def osx_install_data(install_data):
	def finalize_options(self):
		self.set_undefined_options("install", ("install_lib", "install_dir"))
		install_data.finalize_options(self)

def fullsplit(path, result=None):
	if result is None:
		result = []
	head, tail = os.path.split(path)
	if head == '':
		return [tail] + result
	if head == path:
		return result
	return fullsplit(head, [tail] + result)

for scheme in INSTALL_SCHEMES.values():
	scheme['data'] = scheme['purelib']


for dirpath, dirnames, filenames in os.walk(events_dir):
	# Ignore dirnames that start with '.'
	for i, dirname in enumerate(dirnames):
		if dirname.startswith("."): del dirnames[i]
	for filename in filenames:
		if filename.endswith(".py"):
			packages.append('.'.join(fullsplit(dirpath)))
		else:
			data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])

setup(
	name = 'asgard-events',
	version = events.__version__,
	url = 'http://asgardproject.org/apps/events.html',
	
	author = 'Myles Braithwaite',
	author_email = 'me@mylesbraithwaite.com',
	
	description = 'A simple Bookmarking application for the Asgard CMS system.',
	long_description = read('docs', 'intro.rst'),
	
	license = 'BSD License',
	
	packages = packages,
	data_files = data_files,
	zip_safe = False,
	
	install_requires = [
		'distribute',
	],
	
	classifiers = [
		'Development Status :: 4 - Beta',
		'Environment :: Web Environment',
		'Intended Audience :: Developers',
		'Operating System :: OS Independent',
		'Framework :: Django',
		'License :: OSI Approved :: BSD License',
		'Programming Language :: Python',
		'Topic :: Internet :: WWW/HTTP',
	],
)