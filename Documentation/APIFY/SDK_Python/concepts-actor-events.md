# Actor Events & State Persistence in Apify SDK for Python

## Event Types

The Apify platform and SDK support several key event types during Actor runtime:

### 1. SYSTEM_INFO Event
- Provides resource usage details
- Includes:
  - `created_at`: datetime
  - `cpu_current_usage`: float
  - `mem_current_bytes`: int
  - `is_cpu_overloaded`: boolean

### 2. MIGRATING Event
- Indicates the Actor will be migrated to another worker server
- Allows state preservation before migration

### 3. ABORTING Event
- Triggered when a user aborts an Actor run
- Provides opportunity for graceful shutdown and cleanup

### 4. PERSIST_STATE Event
- Emitted at regular intervals (default 60 seconds)
- Encourages state preservation
- Includes `is_migrating` flag

## Adding Event Handlers

Developers can manage event handlers using two primary methods:
- `Actor.on()`: Add an event handler
- `Actor.off()`: Remove an event handler

### Code Example

```python
import asyncio
from typing import Any
from apify import Actor, Event

async def main() -> None:
    async with Actor:
        total_items = 1000
        processed_items = 0
        
        # Load previous state if available
        actor_state = await Actor.get_value('STATE')
        if actor_state is not None:
            processed_items = actor_state
        
        # State saving handler
        async def save_state(event_data: Any) -> None:
            nonlocal processed_items
            Actor.log.info('Saving Actor state', extra=event_data)
            await Actor.set_value('STATE', processed_items)
        
        # Register event handler
        Actor.on(Event.PERSIST_STATE, save_state)
        
        # Process items
        for i in range(processed_items, total_items):
            Actor.log.info(f'Processing item {i}...')
            processed_items = i
            await asyncio.sleep(0.1)
        
        # Remove state saving handler when done
        Actor.off(Event.PERSIST_STATE, save_state)
```

## State Persistence Benefits

- Resume processing from where it left off after interruption
- Handle Actor migrations gracefully
- Provide better user experience with progress tracking
- Ensure data consistency across runs