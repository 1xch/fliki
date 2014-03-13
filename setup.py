"""
Flask-Fliki
-------------
A flask extension to add wiki functionality to your application
"""
from setuptools import setup

setup(
    name='Flask-Fliki',
    version='0',
    url = 'https://github.com/thrisp/fliki',
    license='MIT',
    author='hurrata/thrisp',
    author_email='blueblank@gmail.com',
    description='flask wiki extension',
    long_description=__doc__,
    packages=['flask_fliki'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask >= 0.9',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    test_suite='nose.collector',
    tests_require=[
        'nose',
        'blinker'],
)
