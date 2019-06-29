from contextlib import contextmanager


@contextmanager
def lambda_logger(event={}, context={}):
    import structlog
    import uuid

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.TimeStamper(fmt='iso'),
            structlog.processors.JSONRenderer(sort_keys=True)
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    event['trace_id'] = event.get('trace_id') or context.get('aws_request_id') or str(uuid.uuid4())
    log = structlog.get_logger()
    log = log.bind(trace_id=event['trace_id'])

    for key in ('function_name', 'function_version'):
        val = context.get(key)
        if val:
          log = log.bind(**{key: val})

    request_id = context.get('aws_request_id')
    if request_id:
        log = log.bind(request_id=request_id)

    yield log


if __name__ == '__main__':
    event = {}
    context = {'function_name': 'foo'}
    with lambda_logger(event, context) as log:
        log.warn('this is a test')
