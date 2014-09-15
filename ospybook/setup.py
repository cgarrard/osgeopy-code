from distutils.core import setup

setup(
    name='ospybook',
    version='0.11',
    author='Chris Garrard',
    author_email='garrard.chris@gmail.com',
    packages=['ospybook'],
    url='https://github.com/cgarrard/osgeopy-code/',
    license='LICENSE.txt',
    description='Module for the book Geoprocessing with Python.',
    long_description=open('README.txt').read(),
    install_requires=[
        "numpy",
        "matplotlib",
        # "osgeo",
    ],
)
