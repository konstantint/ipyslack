"""
IPython magic for sending slack notifications.

Copyright 2017, Konstantin Tretyakov
Based on: https://github.com/kalaidin/ipytelegram/blob/master/ipytelegram.py
License: MIT
"""

from setuptools import setup

setup(name='ipyslack',
      version='1.1',
      description="IPython magic for sending slack notifications",
      long_description=open("README.rst").read(),
      classifiers=[  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
          'Development Status :: 4 - Beta',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Framework :: IPython'
      ],
      platforms=['Platform Independent'],
      keywords='matplotlib plotting charts venn-diagrams',
      author='Konstantin Tretyakov',
      author_email='kt@ut.ee',
      url='https://github.com/konstantint/ipyslack',
      license='MIT',
      packages=['ipyslack'],
      zip_safe=True,
      install_requires=['slacker'],
      )
