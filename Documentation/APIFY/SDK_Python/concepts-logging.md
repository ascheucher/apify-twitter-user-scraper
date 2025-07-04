# Logging in Apify SDK for Python

## Overview

The Apify SDK uses Python's standard `logging` module with a logger named `apify`. The logging system provides flexible configuration and formatting options for tracking Actor events and debugging.

## Automatic Configuration

When creating an Actor from an Apify template, logging is pre-configured with:
- Logger level set to `DEBUG`
- Custom log formatter (`ActorLogFormatter`)

## Manual Configuration

### Log Level Configuration

By default, only `WARNING` and higher level logs are printed. To enable `DEBUG` and `INFO` logs, use `Logger.setLevel()`:

```python
import logging
apify_logger = logging.getLogger('apify')
apify_logger.setLevel(logging.DEBUG)
```

### Log Formatting

To enhance log output with colored levels, aligned messages, and extra fields, use `ActorLogFormatter`:

```python
import logging
from apify.log import ActorLogFormatter

handler = logging.StreamHandler()
handler.setFormatter(ActorLogFormatter())
```

## Logger Usage Example

```python
import logging
from apify import Actor
from apify.log import ActorLogFormatter

async def main() -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(ActorLogFormatter())
    
    apify_logger = logging.getLogger('apify')
    apify_logger.setLevel(logging.DEBUG)
    apify_logger.addHandler(handler)

    async with Actor:
        Actor.log.debug('This is a debug message')
        Actor.log.info('This is an info message')
        Actor.log.warning('This is a warning message', extra={'reason': 'Bad Actor!'})
        Actor.log.error('This is an error message')
        
        try:
            raise RuntimeError('Ouch!')
        except RuntimeError:
            Actor.log.exception('This is an exceptional message')
```

### Key Features
- Supports all standard logging levels
- Can include extra metadata with logs
- Automatic exception context capture
- Colorful and informative log formatting