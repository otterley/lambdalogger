import logging
from contextlib import contextmanager
from structlog._frames import _find_first_app_frame_and_name


def add_app_context(logger, method_name, event_dict):
    f, _ = _find_first_app_frame_and_name(['logging', __name__])
    event_dict['file'] = f.f_code.co_filename
    event_dict['line'] = f.f_lineno
    event_dict['function'] = f.f_code.co_name
    return event_dict


@contextmanager
def lambdalogger(event={}, context={}, level=logging.INFO):
    import structlog
    import uuid

    # Reset root logger configuration
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(level=level, format='%(message)s')

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            add_app_context,
            structlog.stdlib.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.TimeStamper(fmt='iso', utc=True),
            structlog.processors.JSONRenderer(sort_keys=True, indent=None)
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    event['trace_id'] = event.get('trace_id') \
        or getattr(context, 'aws_request_id', None) \
        or str(uuid.uuid4())
    log = structlog.get_logger()
    log = log.bind(trace_id=event['trace_id'])

    lambda_context = {}

    for key in ('function_name', 'function_version', 'aws_request_id'):
        val = getattr(context, key, None)
        if val:
            lambda_context[key] = val

    if len(lambda_context) > 0:
        log = log.bind(lambda_context=lambda_context)

    yield log


if __name__ == '__main__':
    event = {}
    context = {'function_name': 'foo'}
    with lambdalogger(event, context) as log:
        log.warn('this is a test')
