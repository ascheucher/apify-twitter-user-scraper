# Actor structure | SDK for Python | Apify Documentation

**Source URL**: https://docs.apify.com/sdk/python/docs/overview/actor-structure

## Overview

The Apify Python SDK follows a specific actor structure with key components:

### Directory Structure

1. `.actor/` directory
   - Contains Actor configuration
   - Includes Actor definition and input schema
   - Contains Dockerfile for Apify platform deployment

2. `requirements.txt`
   - Specifies runtime dependencies
   - Follows standard Python requirements file format

3. `src/` folder
   - Contains main Actor source code
   - Two critical files:
     - `main.py`: Contains the main Actor function
     - `__main__.py`: Package entrypoint

### Example `__main__.py`

```python
import asyncio
from .main import main

if __name__ == '__main__':
    asyncio.run(main())
```

### Example `main.py`

```python
from apify import Actor

async def main() -> None:
    async with Actor:
        actor_input = await Actor.get_input()
        Actor.log.info('Actor input: %s', actor_input)
        await Actor.set_value('OUTPUT', 'Hello, world!')
```

## Key Considerations

- Actor must be executable as a module via `python -m src`
- Recommended to keep entrypoint in `src/__main__.py`
- Uses `asyncio` for asynchronous execution
- Integrates with Apify's Actor lifecycle and logging mechanisms