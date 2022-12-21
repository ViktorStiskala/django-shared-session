# coding=utf-8
import os
from setuptools import setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md'), 'r') as f:
    long_description = f.read()

setup(
    name='django-shared-session',
    version='0.5.3',
    packages=['shared_session', 'shared_session.templatetags'],
    include_package_data=True,
    license='MPL',
    description='Django session sharing across multiple domains running same application',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ViktorStiskala/django-shared-session',
    author='Viktor Stískala',
    author_email='viktor@stiskala.cz',
    install_requires=[
        'setuptools-git',
        'django>=2.0',
        'python-dateutil>=2.5',
        'PyNaCl>=1.0.0',
        'six>=1.11'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
