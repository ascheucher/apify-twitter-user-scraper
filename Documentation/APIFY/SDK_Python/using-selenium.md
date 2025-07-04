# Using Selenium | SDK for Python | Apify Documentation

**Source URL**: https://docs.apify.com/sdk/python/docs/guides/selenium

[Selenium](https://www.selenium.dev/) is a tool for web automation and testing that can also be used for web scraping. It allows you to control a web browser programmatically and interact with web pages just as a human would.

## Key Features of Selenium for Web Scraping

- **Cross-browser support** - Supports latest versions of major browsers like Chrome, Firefox, and Safari
- **Headless mode** - Can run browsers without visible window
- **Powerful selectors** - Provides CSS selectors, XPath, and text matching
- **Emulation of user interactions** - Can click, scroll, fill forms, and type text

## Using Selenium in Actors

To create Actors using Selenium:
- Start from the [Selenium & Python](https://apify.com/templates/categories/python) Actor template
- On Apify platform, Selenium and browsers are pre-installed in Docker image
- For local development, install Selenium browser drivers manually

## Example Actor

Here's a complete example of a Selenium-based web scraping Actor that recursively extracts website titles:

```python
from __future__ import annotations
import asyncio
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from apify import Actor, Request

async def main() -> None:
    async with Actor:
        # Actor input and configuration
        actor_input = await Actor.get_input() or {}
        start_urls = actor_input.get('start_urls', [{'url': 'https://apify.com'}])
        max_depth = actor_input.get('max_depth', 1)

        # Setup request queue
        request_queue = await Actor.open_request_queue()
        for start_url in start_urls:
            url = start_url.get('url')
            new_request = Request.from_url(url, user_data={'depth': 0})
            await request_queue.add_request(new_request)

        # Configure Selenium WebDriver
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(options=chrome_options)

        try:
            # Process URLs from request queue
            while request := await request_queue.fetch_next_request():
                url = request.url
                depth = int(request.user_data['depth'])
                Actor.log.info(f'Scraping {url} (depth={depth})...')

                try:
                    # Navigate to the page
                    driver.get(url)
                    
                    # Extract data
                    title = driver.title
                    h1_elements = driver.find_elements(By.TAG_NAME, 'h1')
                    h1s = [h1.text for h1 in h1_elements]
                    
                    data = {
                        'url': url,
                        'title': title,
                        'h1s': h1s,
                    }
                    await Actor.push_data(data)

                    # Find and enqueue new links if depth allows
                    if depth < max_depth:
                        link_elements = driver.find_elements(By.TAG_NAME, 'a')
                        for link_element in link_elements:
                            link_href = link_element.get_attribute('href')
                            if link_href and link_href.startswith(('http://', 'https://')):
                                new_request = Request.from_url(link_href, user_data={'depth': depth + 1})
                                await request_queue.add_request(new_request)

                except Exception as e:
                    Actor.log.error(f'Failed to scrape {url}: {e}')
                
                # Mark request as handled
                await request_queue.mark_request_as_handled(request)

        finally:
            driver.quit()

if __name__ == '__main__':
    asyncio.run(main())
```

## Key Advantages

- Mature and well-established framework
- Excellent browser automation capabilities
- Strong community support
- Handles JavaScript-rendered content
- Supports complex user interactions