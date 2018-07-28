from setuptools import setup

setup(
    name='escape',
    packages=['escape'],
    include_package_data=True,
    install_requires=[
        'flask',
        'gevent'
    ],
)

