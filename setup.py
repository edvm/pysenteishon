# -*- coding: utf-8 -*-


import sys
from setuptools import setup, find_packages
import pysenteishon


if sys.version_info[0] < 3:
    raise Exception('Python 2 version is not supported')

if sys.platform == 'darwin':
    requirements_file = 'requirements.darwin.txt'
else:
    requirements_file = 'requirements.txt'

with open(requirements_file, 'r') as fh:
    dependencies = [l.strip() for l in fh]


setup(
    name=pysenteishon.__prj__,
    version=pysenteishon.__version__,
    description='Control your presentations swiping your touchscreen!',
    long_description=open('README.rst').read(),
    url='https://github.com/edvm/pysenteishon',
    author=pysenteishon.__author__,
    author_email=pysenteishon.__email__,
    maintainer='Manuel Kaufmann',
    maintainer_email='humitos@gmail.com',
    license=pysenteishon.__license__,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Communications :: Conferencing',
    ],
    keywords='presentation touchscreen talk pycon conference',
    packages=find_packages(exclude=['samples']),
    install_requires=dependencies,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pysenteishon=pysenteishon.app:main',
        ],
    },
)
