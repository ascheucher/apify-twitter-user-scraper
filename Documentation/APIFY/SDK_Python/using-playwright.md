# Using Playwright | SDK for Python | Apify Documentation

**Source URL**: https://docs.apify.com/sdk/python/docs/guides/playwright

[Playwright](https://playwright.dev) is a tool for web automation and testing that can also be used for web scraping. It allows you to control a web browser programmatically and interact with web pages just as a human would.

## Key Features of Playwright

- **Cross-browser support** - Supports latest versions of Chrome, Firefox, and Safari
- **Headless mode** - Can run browser without visible window
- **Powerful selectors** - Provides CSS, XPath, and text matching selectors
- **Emulation of user interactions** - Can click, scroll, fill forms, and type text

## Using Playwright in Actors

To create Actors using Playwright:
- Start from the [Playwright & Python](https://apify.com/templates/categories/python) Actor template
- On Apify platform, Playwright and browsers are pre-installed
- For local development, you'll need to set up Playwright

### Installation (Local Setup)

Linux / macOS:
```
source .venv/bin/activate
playwright install --with-deps
```

Windows:
```
.venv\Scripts\activate
playwright install --with-deps
```

## Example Actor

Here's a sample Actor that recursively scrapes website titles using Playwright:

```python
from __future__ import annotations
from urllib.parse import urljoin
from playwright.async_api import async_playwright
from apify import Actor, Request

async def main() -> None:
    async with Actor:
        # Retrieve Actor input with defaults
        actor_input = await Actor.get_input() or {}
        start_urls = actor_input.get('start_urls', [{'url': 'https://apify.com'}])
        max_depth = actor_input.get('max_depth', 1)

        # Exit if no start URLs
        if not start_urls:
            Actor.log.info('No start URLs specified in actor input, exiting...')
            await Actor.exit()

        # Open request queue and enqueue start URLs
        request_queue = await Actor.open_request_queue()
        for start_url in start_urls:
            url = start_url.get('url')
            new_request = Request.from_url(url, user_data={'depth': 0})
            await request_queue.add_request(new_request)

        # Launch Playwright browser
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=True)
            page = await browser.new_page()

            # Process URLs from request queue
            while request := await request_queue.fetch_next_request():
                url = request.url
                depth = int(request.user_data['depth'])
                Actor.log.info(f'Scraping {url} (depth={depth})...')

                try:
                    # Navigate to the page
                    await page.goto(url)
                    
                    # Extract data
                    title = await page.title()
                    h1s = await page.evaluate('() => Array.from(document.querySelectorAll("h1")).map(h1 => h1.textContent)')
                    
                    data = {
                        'url': url,
                        'title': title,
                        'h1s': h1s,
                    }
                    await Actor.push_data(data)

                    # Find and enqueue new links if depth allows
                    if depth < max_depth:
                        links = await page.evaluate('() => Array.from(document.querySelectorAll("a")).map(a => a.href)')
                        for link in links:
                            if link.startswith(('http://', 'https://')):
                                new_request = Request.from_url(link, user_data={'depth': depth + 1})
                                await request_queue.add_request(new_request)

                except Exception as e:
                    Actor.log.error(f'Failed to scrape {url}: {e}')
                
                # Mark request as handled
                await request_queue.mark_request_as_handled(request)

            await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
```

## Key Advantages

- Handles JavaScript-rendered content
- Can interact with complex web applications
- Supports multiple browser engines
- Robust automation capabilities
- Excellent for dynamic content extraction