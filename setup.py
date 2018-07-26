import sys
from setuptools import setup

setup(
    name="googlespreadsheets",
    packages=['googlespreadsheets'],
    py_modules=['googlespreadsheets'],
    version='0.0.3',
    description="A Package for read and writing google sheets to and from Pandas dataframes",
    long_description="A Package for read and writing google sheets to and from Pandas dataframes",
    author="leon yin",
    author_email="whereisleon@gmail.com",
    url="https://github.com/yinleon/googlespeadsheets",
    keywords='google sheet spreadsheet pandas',
    license="MIT",
    install_requires=[
        'pandas',
        'oauth2client',
        'google-api-python-client',
        'httplib2'
    ]
)
