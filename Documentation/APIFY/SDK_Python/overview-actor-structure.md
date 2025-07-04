# Actor Structure in Apify Python SDK

## Overview

The Apify Python SDK follows a standardized actor structure with specific directory and file organization:

### Directory Structure

1. `.actor/` Directory
   - Contains Actor configuration
   - Includes Actor definition and input schema
   - Contains Dockerfile for Apify platform deployment

2. `requirements.txt`
   - Specifies runtime dependencies
   - Follows standard Python requirements file format

3. `src/` Folder
   - Contains main Actor source code
   - Two critical files:
     - `main.py`: Contains the main Actor function
     - `__main__.py`: Package entrypoint

## Code Examples

### `__main__.py`
```python
import asyncio
from .main import main

if __name__ == '__main__':
    asyncio.run(main())
```

### `main.py`
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
- Leverages Apify's `Actor` context manager for input/output handling

The structure ensures consistent, modular, and platform-compatible Actor development.