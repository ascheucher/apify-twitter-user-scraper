# Apify SDK for Python Documentation

## Overview
The Apify SDK for Python is a toolkit for building Actors, providing features like:
- Actor lifecycle management
- Local storage emulation
- Actor event handling

## Key Features
- Easy input retrieval with `Actor.get_input()`
- Simple data pushing with `Actor.push_data()`

## Example Code
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
            'title': soup.title.string if soup.title else None
        }
        await Actor.push_data(data)
```

## Navigation Sections
### Learn
- Academy
- Platform

### API
- Reference
- Client for JavaScript
- Client for Python

### SDK
- SDK for JavaScript
- SDK for Python

### Other
- CLI
- Open Source

### More
- Crawlee
- GitHub
- Trust Center

## Quick Start Command
```
apify create my-python-actor
```

## Links
- [GitHub Repository](https://github.com/apify/apify-sdk-python)
- [Documentation](https://docs.apify.com/sdk/python/)
- [Discord Community](https://discord.com/invite/jyEM2PRvMU)