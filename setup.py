from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md')) as f:
    longDescription = f.read()

# with open(path.join(here, 'requirements.txt')) as f:
#     requirements = f.read().split('\n')

setup(
    name="tmdbAPI",
    version="0.1.3",
    author="Kevin Riehl",
    author_email="kevinriehl@gmail.com",
    description="Python Module for accessing the TVDB API",
    long_description=longDescription,
    long_description_content_type="text/markdown",
    py_modules=['tmdbAPI'],
    install_requires=['requests >= 2.22.0', 'sanction >= 0.4.1'],
    license="MIT",
    url="https://github.com/TehRiehlDeal/tmdbAPI",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    
)