# Using Crawlee | SDK for Python | Apify Documentation

**Source URL**: https://docs.apify.com/sdk/python/docs/guides/crawlee

## Introduction

`Crawlee` is a Python library for web scraping and browser automation that provides a robust and flexible framework for building web scraping tasks. It seamlessly integrates with the Apify platform and supports various scraping techniques, from static HTML parsing to dynamic JavaScript-rendered content handling.

Crawlee offers multiple crawlers:
- HTTP-based crawlers:
  - `HttpCrawler`
  - `BeautifulSoupCrawler`
  - `ParselCrawler`
- Browser-based crawlers:
  - `PlaywrightCrawler`

## Actor with BeautifulSoupCrawler

Here's an example of using `BeautifulSoupCrawler` in an Apify Actor:

```python
from __future__ import annotations
from crawlee.crawlers import BeautifulSoupCrawler, BeautifulSoupCrawlingContext
from apify import Actor

async def main() -> None:
    async with Actor:
        actor_input = await Actor.get_input() or {}
        start_urls = [
            url.get('url')
            for url in actor_input.get(
                'start_urls',
                [{'url': 'https://apify.com'}],
            )
        ]
        
        if not start_urls:
            Actor.log.info('No start URLs specified in Actor input, exiting...')
            await Actor.exit()
        
        crawler = BeautifulSoupCrawler(
            max_requests_per_crawl=50,
        )
        
        @crawler.router.default_handler
        async def request_handler(context: BeautifulSoupCrawlingContext) -> None:
            url = context.request.url
            Actor.log.info(f'Scraping {url}...')
            
            data = {
                'url': context.request.url,
                'title': context.soup.title.string if context.soup.title else None,
                'h1s': [h1.text for h1 in context.soup.find_all('h1')],
                'h2s': [h2.text for h2 in context.soup.find_all('h2')],
                'h3s': [h3.text for h3 in context.soup.find_all('h3')],
            }
            
            await Actor.push_data(data)
            
            # Enqueue found links
            await context.enqueue_links()
        
        await crawler.run(start_urls)

if __name__ == '__main__':
    asyncio.run(main())
```

## Key Features

- Built-in request queue management
- Automatic link discovery and enqueuing
- Multiple crawler types for different use cases
- Seamless integration with Apify platform
- Robust error handling and retry mechanisms