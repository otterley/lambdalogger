from setuptools import setup, find_packages
setup(
    name="lambda_logger",
    description="An opinionated structured logging decorator for Python Lambda functions",
    version="0.1",
    packages=find_packages(),
    install_requires=["structlog>=19"],
    author="ConocoPhillips"
)