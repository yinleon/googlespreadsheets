import sys
from setuptools import setup

long_description = """This package makes working with link data from social media and webpages easier. It not only expands links, but catches errors, and makes parallel link expansion quick and efficient.
```
import urlexpander as ux
ux.expand('https://trib.al/xXI5ruM')
```
returns
```
{'original_url': 'https://trib.al/xXI5ruM',
 'resolved_domain': 'breitbart.com',
 'resolved_url': 'https://www.breitbart.com/video/2017/12/31/lindsey-graham-trump-just-cant-tweet-iran/'}
 ```
 
 Please take a look at the [quickstart](http://nbviewer.jupyter.org/github/SMAPPNYU/urlExpander/blob/master/examples/quickstart.ipynb?flush=true).
    """

setup(
    name="googlespeadsheets",
    packages=['googlespreadsheets'],
    py_modules=['googlespreadsheets'],
    version='0.0.1',
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
        'apiclient',
    ]
)