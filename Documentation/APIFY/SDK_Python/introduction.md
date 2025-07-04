# Introduction | SDK for Python | Apify Documentation

**Source URL**: https://docs.apify.com/sdk/python/docs/overview/introduction

## What are Actors?

Actors are serverless cloud programs capable of performing web-based tasks, ranging from simple operations like filling out forms to complex jobs such as web scraping and data processing. They can be executed locally or on the Apify platform, which provides features for scaling, monitoring, scheduling, and potentially monetizing them.

## Quick Start

### Creating Actors

Developers can create and run Actors using:
- Apify Console
- Local development (refer to [running Actors locally](/sdk/python/docs/overview/running-actors-locally))

### Integration Guides

The SDK offers integration guides for popular web scraping libraries:
- BeautifulSoup with HTTPX
- Crawlee
- Playwright
- Selenium
- Scrapy

### Example Code

```python
import httpx
from bs4 import BeautifulSoup
from apify import Actor

async def main() -> None:
    async with Actor:
        actor_input = await Actor.get_input()
        async with httpx.AsyncClient() as client:
            response = await client.get(actor_input['url'])
        soup = BeautifulSoup(response.content, 'html.parser')
        data = {
            'url': actor_input['url'],
            'title': soup.title.string if soup.title else None,
        }
        await Actor.push_data(data)
```

## Installation

Install the Apify SDK using pip:

```bash
pip install apify
```

## Key Concepts

Developers are encouraged to explore:
- Actor lifecycle
- Storage management
- Event handling
- Proxy management

## Additional Resources

- [Apify Platform Documentation](https://docs.apify.com/platform/about)
- [Apify API Client for Python](https://docs.apify.com/api/client/python)