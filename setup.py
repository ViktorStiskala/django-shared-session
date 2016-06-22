# coding=utf-8
import os
from setuptools import setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-shared-session',
    version='0.1',
    packages=['shared_session'],
    include_package_data=True,
    license='MPL',
    description='Django session sharing across multiple domains running same application',
    author='Viktor Stískala',
    author_email='viktor@stiskala.cz',
    install_requires=['django>=1.7', 'python-dateutil>=2.5', 'PyNaCl>=1.0.0'],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
