from setuptools import setup

setup(
    name='leapfrog',
    version='0.1',
    install_requires=[
        'Click',
    ],
    entry_points={'console_scripts': ["leapfrog=src.leapfrog.cli:cli"]}
)
