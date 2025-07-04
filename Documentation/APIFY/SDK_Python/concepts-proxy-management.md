# Proxy Management in Apify SDK for Python

## Overview

Proxy management is crucial for web scraping to overcome IP address blocking. The Apify SDK provides powerful tools for managing proxies, including:

- Using Apify Proxy
- Using custom proxy servers
- IP rotation and session management

## Quick Start

### Using Apify Proxy

```python
from apify import Actor

async def main() -> None:
    async with Actor:
        proxy_configuration = await Actor.create_proxy_configuration()
        if not proxy_configuration:
            raise RuntimeError('No proxy configuration available.')
        proxy_url = await proxy_configuration.new_url()
        Actor.log.info(f'Using proxy URL: {proxy_url}')
```

### Using Custom Proxies

```python
from apify import Actor

async def main() -> None:
    async with Actor:
        proxy_configuration = await Actor.create_proxy_configuration(
            proxy_urls=[
                'http://proxy-1.com',
                'http://proxy-2.com',
            ],
        )
        if not proxy_configuration:
            raise RuntimeError('No proxy configuration available.')
        proxy_url = await proxy_configuration.new_url()
        Actor.log.info(f'Using proxy URL: {proxy_url}')
```

## Proxy Configuration

### IP Rotation and Session Management

The `new_url()` method allows for session-based proxy management:

```python
from apify import Actor

async def main() -> None:
    async with Actor:
        proxy_configuration = await Actor.create_proxy_configuration(
            proxy_urls=['http://proxy-1.com', 'http://proxy-2.com'],
        )
        
        # Round-robin proxy rotation
        proxy_url = await proxy_configuration.new_url()  # http://proxy-1.com
        proxy_url = await proxy_configuration.new_url()  # http://proxy-2.com
        
        # Session-based proxy selection
        proxy_url = await proxy_configuration.new_url(session_id='a')  # consistent proxy for session 'a'
        proxy_url = await proxy_configuration.new_url(session_id='b')  # different proxy for session 'b'
```

## Key Features

- Automatic proxy rotation
- Session-based proxy management
- Support for both Apify Proxy and custom proxy servers
- IP blocking prevention
- Enhanced scraping reliability