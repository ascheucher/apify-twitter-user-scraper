# Upgrading to Apify Python SDK v2

## Python Version Support

- Dropped support for Python 3.8
- Now requires Python 3.9 or later

## Storages

### Key Changes
- Now uses [crawlee](https://github.com/apify/crawlee-python) for local storage emulation
- `RequestQueue.add_request` method changes:
  - Accepts `apify.Request` object instead of dictionary
  - Migration options:
    1. Wrap dictionary with `Request.model_validate()`
    2. Use `Request.from_url()` helper
    3. Use plain URL strings
- Removed `StorageClientManager` class
  - Use `crawlee.service_container` instead

## Configuration

- Now uses `pydantic_settings` to load configuration from environment variables
- Attributes with `_millis` suffix renamed
- Attributes now use `datetime.timedelta` type

## Actor

### Breaking Changes
- Removed `Actor.main()` method
- Webhook and method calls now require specific model instances
- Return types now use typed models (e.g., `ActorRun`)
- Logging configuration added by default when entering context manager
- `config` parameter renamed to `configuration`
- Event handlers now receive Pydantic objects

## Scrapy Integration

- Removed `open_queue_with_custom_client` function

## Subpackage Visibility

The following modules are now private:
- `apify.proxy_configuration`
- `apify.config`
- `apify.actor`
- `apify.event_manager`
- `apify.consts`

(Corresponding classes remain exported from `apify`)

## Migration Recommendations

1. Update Python version to 3.9+
2. Replace dictionary-based requests with `Request` objects
3. Update event handler access to use Pydantic object attributes
4. Review and update webhook and method calls to use model instances