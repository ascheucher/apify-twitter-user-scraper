# Using BeautifulSoup with HTTPX | SDK for Python | Apify Documentation

**Source URL**: https://docs.apify.com/sdk/python/docs/guides/beautifulsoup-httpx

## Introduction

This guide demonstrates how to use the BeautifulSoup and HTTPX libraries in Apify Actors for web scraping. 

- BeautifulSoup is a Python library for extracting data from HTML and XML files
- HTTPX is a modern HTTP client library for Python supporting synchronous and asynchronous requests

## Example Actor

Here's a sample Actor that recursively scrapes website titles with a configurable maximum depth:

```python
from __future__ import annotations
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from httpx import AsyncClient
from apify import Actor, Request

async def main() -> None:
    async with Actor:
        # Retrieve Actor input with default values
        actor_input = await Actor.get_input() or {}
        start_urls = actor_input.get('start_urls', [{'url': 'https://apify.com'}])
        max_depth = actor_input.get('max_depth', 1)

        # Exit if no start URLs are provided
        if not start_urls:
            Actor.log.info('No start URLs specified in Actor input, exiting...')
            await Actor.exit()

        # Open the default request queue
        request_queue = await Actor.open_request_queue()

        # Enqueue the start URLs with initial crawl depth of 0
        for start_url in start_urls:
            url = start_url.get('url')
            Actor.log.info(f'Enqueuing {url} ...')
            new_request = Request.from_url(url, user_data={'depth': 0})
            await request_queue.add_request(new_request)

        # Create an HTTPX client to fetch HTML content
        async with AsyncClient() as client:
            # Process URLs from the request queue
            while request := await request_queue.fetch_next_request():
                url = request.url
                depth = int(request.user_data['depth'])
                Actor.log.info(f'Scraping {url} (depth={depth}) ...')

                try:
                    # Fetch HTTP response using HTTPX
                    response = await client.get(url, follow_redirects=True)
                    
                    # Parse HTML content with BeautifulSoup
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Find and enqueue nested links if depth is less than max_depth
                    if depth < max_depth:
                        for link in soup.find_all('a'):
                            link_href = link.get('href')
                            link_url = urljoin(url, link_href)
                            if link_url.startswith(('http://', 'https://')):
                                new_request = Request.from_url(link_url, user_data={'depth': depth + 1})
                                await request_queue.add_request(new_request)

                    # Extract data and save to dataset
                    data = {
                        'url': url,
                        'title': soup.title.string if soup.title else None,
                        'h1s': [h1.text for h1 in soup.find_all('h1')],
                        'h2s': [h2.text for h2 in soup.find_all('h2')],
                        'h3s': [h3.text for h3 in soup.find_all('h3')],
                    }
                    await Actor.push_data(data)

                except Exception as e:
                    Actor.log.error(f'Failed to scrape {url}: {e}')
                
                # Mark the request as handled
                await request_queue.mark_request_as_handled(request)

if __name__ == '__main__':
    asyncio.run(main())
```

## Key Features

- Uses HTTPX for modern async HTTP requests
- BeautifulSoup for HTML parsing and data extraction
- Configurable crawling depth
- Request queue management
- Error handling and logging