from setuptools import setup, find_packages

NAME = 'LambdaLogger'
DESCRIPTION = 'An opinionated structured logging decorator for Python Lambda functions'

setup(
    name='lambdalogger',
    description=DESCRIPTION,
    version='0.1',
    packages=find_packages(),
    install_requires=['structlog>=19'],
    setup_requires=['wheel'],
    author='ConocoPhillips'
)
