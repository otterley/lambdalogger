# LambdaLogger: An opinionated structured logger for Python AWS Lambda functions

LambdaLogger is a Python module that will help your Lambda function emit
JSON-structured logs by default.  

Structured logs provide uniformity of format to all your functions, and allow
the user to easily analyze logs using readily-available JSON parsers.  Such
logs can also be analyzed at scale using services such as Amazon CloudWatch Logs
Insights, Datadog, Splunk, and Honeycomb.

LambdaLogger does not change the destination of logs.  Logs are still sent to
Amazon CloudWatch Logs.  If you desire to have your logs sent to other
destinations, check their documentation for instructions on ingesting logs from
CloudWatch Logs.


## Supported environments

Only Python 3.6 and higher are supported.


## Typical usage

```python
from lambdalogger import lambdalogger
import logging

def handler(event, context):
    with lambdalogger(event, context) as log:
        # Your logic goes here
        log.info('message', foo='bar', baz='quux')
```

## Building and uploading

Scripts are included to build the source and package the modules for upload as
Lambda layers.  These scripts depend on your AWS CLI environment being set up
correctly.  We recommend configuring your `~/.aws/config` file and setting the
`$AWS_PROFILE` environment variable to point to the appropriate profile in the
config file.

### Microsoft Windows (PowerShell)

[Install Python 3.7](https://www.python.org/downloads/windows/) first.  Then run
`pip3 install pipenv`.  Then you can run:

* Build: run `build-layer.ps1`
* Upload: run `upload-layer.ps1`

### Linux/MacOS

TBD


## Authors

* Michael S. Fischer, fiscmi@amazon.com