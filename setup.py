#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='privsim',
      version='0.0.1',
      description='Differential Privacy Simulator',
      author='Rafal Furmanski',
      author_email='r.furmanski@gmail.com',
      url='https://github.com/r4fek/Differential-Privacy',
      packages=find_packages(),
      package_dir={'privsim': 'privsim'},
      install_requires=[
        'click',
      ],
      entry_points='''
          [console_scripts]
          privsim=privsim.main:main
      ''')
