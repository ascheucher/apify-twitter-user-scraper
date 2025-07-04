# Actor Lifecycle in Apify SDK for Python

## Initialization and Cleanup

The Actor lifecycle in the Apify SDK involves several key methods for managing the runtime of an Actor:

### Initialization Methods

- `Actor.init()`: Initializes the Actor, event manager, and storage client
- `Actor.exit()`: Cleanly exits the Actor
- `Actor.fail()`: Exits the Actor and marks it as failed

### Example Code (Explicit Initialization)

```python
from apify import Actor

async def main() -> None:
    await Actor.init()
    try:
        Actor.log.info('Actor input:', await Actor.get_input())
        await Actor.set_value('OUTPUT', 'Hello, world!')
        raise RuntimeError('Ouch!')
    except Exception as exc:
        Actor.log.exception('Error while running Actor')
        await Actor.fail(exit_code=91, exception=exc)
    await Actor.exit()
```

### Context Manager Approach

The recommended way to manage Actor lifecycle is using a context manager:

```python
from apify import Actor

async def main() -> None:
    async with Actor:
        actor_input = await Actor.get_input()
        Actor.log.info('Actor input: %s', actor_input)
        await Actor.set_value('OUTPUT', 'Hello, world!')
        raise RuntimeError('Ouch!')
```

## Rebooting an Actor

The `Actor.reboot()` method allows restarting an Actor:

```python
from apify import Actor

async def main() -> None:
    async with Actor:
        # ... your code here ...
        await Actor.reboot()
```

**Note:** Use rebooting carefully to avoid creating a reboot loop.

## Actor Status Message

You can set status messages to track Actor progress:

```python
from apify import Actor

async def main() -> None:
    async with Actor:
        await Actor.set_status_message('Here we go!')
        # Do some work...
        await Actor.set_status_message('So far so good...')
        # Finish the job
        await Actor.set_status_message('Phew! That was close!')