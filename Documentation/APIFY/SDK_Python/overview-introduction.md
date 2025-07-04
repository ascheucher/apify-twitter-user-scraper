# Introduction to Apify SDK for Python

## What are Actors?

Actors are serverless cloud programs capable of performing web-based tasks, ranging from simple operations like filling out forms to complex jobs such as web scraping and data processing. They can be executed locally or on the Apify platform, which provides features for scaling, monitoring, scheduling, and potentially monetizing them.

## Quick Start

### Creating an Example Actor

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

## Guides for Integration

The SDK offers integration guides for popular web scraping libraries:
- BeautifulSoup with HTTPX
- Crawlee
- Playwright
- Selenium
- Scrapy

## Key Concepts to Explore

Important usage concepts include:
- Actor lifecycle
- Working with storages
- Handling Actor events
- Proxy management

## Installation

To install the Apify SDK independently:

```bash
pip install apify
```

## Additional Information

For those primarily interested in API interactions, the documentation recommends using the [Apify API client for Python](https://docs.apify.com/api/client/python) directly.

The SDK is designed to help developers create Actors on the Apify platform, providing a comprehensive toolkit for web automation and data extraction tasks.