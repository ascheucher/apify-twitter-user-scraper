# Actor Configuration in Apify SDK for Python

## Overview

The Apify SDK for Python allows configuring actors through two primary methods:
1. Configuring from code
2. Configuring via environment variables

## Configuring from Code

You can configure the Actor using the `Configuration` class directly. Here's an example of setting state persistence interval:

```python
from datetime import timedelta
from apify import Actor, Configuration, Event

async def main() -> None:
    global_config = Configuration.get_global_configuration()
    global_config.persist_state_interval = timedelta(seconds=10)
    
    async with Actor:
        async def save_state() -> None:
            await Actor.set_value('STATE', 'Hello, world!')
        
        # The save_state handler will be called every 10 seconds
        Actor.on(Event.PERSIST_STATE, save_state)
```

## Configuring via Environment Variables

Configuration can be set using environment variables prefixed with `APIFY_`. For example:

```bash
APIFY_PERSIST_STORAGE=0 apify run
```

## Key Points

- If using the Apify SDK on the Apify platform or through Apify CLI, manual configuration is typically unnecessary
- Configuration can be done programmatically or through environment variables
- Full configuration options are available in the `Configuration` class reference

## Recommendations

- For most use cases, default configurations work automatically
- Customize configuration only when you have specific requirements
- Refer to the `Configuration` class documentation for comprehensive options