from setuptools import find_packages, setup

with open('requirements-dev.txt') as fp:
    tests_require = fp.readlines()

setup(
    name='functions',
    packages=find_packages(),
    setup_requires=['pytest-runner'],
    tests_require=tests_require
)
