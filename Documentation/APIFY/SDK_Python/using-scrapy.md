# Using Scrapy | SDK for Python | Apify Documentation

**Source URL**: https://docs.apify.com/sdk/python/docs/guides/scrapy

## Overview
Scrapy is an open-source web scraping framework for Python that can be integrated with Apify Actors and platform services. The integration allows Scrapy projects to be converted into Apify Actors with minimal modifications.

## Key Integration Components

### Main Integration Features
- Uses Twisted's `asyncioreactor` to combine Twisted and asyncio event loops
- Provides custom Scrapy components for Apify platform integration:
  - `ApifyScheduler`: Replaces default Scrapy scheduler
  - `ActorDatasetPushPipeline`: Pushes scraped items to Apify dataset
  - `ApifyHttpProxyMiddleware`: Manages proxy configurations
  - `ApifyCacheStorage`: Provides HTTP cache storage using Apify key-value store

## Project Setup

### Project Structure Example
Typical Scrapy Actor project includes:
- `__main.py__`: Actor entry point
- `main.py`: Main Actor coroutine
- `settings.py`: Scrapy settings
- `items.py`: Define scraped item structures
- `spiders/`: Contains spider implementations

### Key Configuration Steps
1. Install Twisted's asyncio reactor
2. Set `SCRAPY_SETTINGS_MODULE` environment variable
3. Use `apify.scrapy.run_scrapy_actor()` to execute the Actor

## Example Spider Implementation

```python
class TitleSpider(Spider):
    name = 'title_spider'
    custom_settings = {'CLOSESPIDER_PAGECOUNT': 10}

    def parse(self, response):
        # Extract page title
        url = response.url
        title = response.css('title::text').extract_first()
        yield TitleItem(url=url, title=title)

        # Discover and queue new links
        for link_href in response.css('a::attr("href")'):
            link_url = urljoin(response.url, link_href.get())
            if link_url.startswith(('http://', 'https://')):
                yield Request(url=link_url, callback=self.parse)
```

## Integration Benefits

- Leverages Scrapy's robust framework
- Seamless integration with Apify platform services
- Automatic data pipeline to Apify datasets
- Built-in proxy management
- Scalable architecture for large-scale scraping projects

## Key Advantages

- Mature and feature-rich framework
- Excellent for complex scraping projects
- Built-in middleware and pipeline system
- Strong concurrent processing capabilities
- Comprehensive documentation and community support