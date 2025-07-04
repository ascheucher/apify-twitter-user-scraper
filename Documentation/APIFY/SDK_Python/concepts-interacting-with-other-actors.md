# Interacting with other Actors in Apify SDK for Python

The Apify SDK for Python provides several methods to interact with other Actors and Actor tasks on the Apify platform:

## Actor Start

The `Actor.start()` method starts another Actor and immediately returns its run details:

```python
from apify import Actor

async def main() -> None:
    async with Actor:
        # Start your own Actor named 'my-fancy-actor'
        actor_run = await Actor.start(
            actor_id='~my-fancy-actor',
            run_input={'foo': 'bar'},
        )
        # Log the Actor run ID
        Actor.log.info(f'Actor run ID: {actor_run.id}')
```

## Actor Call

The `Actor.call()` method starts another Actor and waits for it to complete:

```python
from apify import Actor

async def main() -> None:
    async with Actor:
        # Start the apify/screenshot-url Actor
        actor_run = await Actor.call(
            actor_id='apify/screenshot-url',
            run_input={'url': 'http://example.com', 'delay': 10000},
        )
        if actor_run is None:
            raise RuntimeError('Actor task failed to start.')
        
        # Wait for the Actor run to finish
        run_client = Actor.apify_client.run(actor_run.id)
        await run_client.wait_for_finish()
        
        # Get the Actor output from the key-value store
        kvs_client = run_client.key_value_store()
        output = await kvs_client.get_record('OUTPUT')
        Actor.log.info(f'Actor output: {output}')
```

## Actor Call Task

The `Actor.call_task()` method starts an Actor task and waits for completion:

```python
from apify import Actor

async def main() -> None:
    async with Actor:
        # Start the Actor task by its ID
        actor_run = await Actor.call_task(task_id='Z3m6FPSj0GYZ25rQc')
        
        if actor_run is None:
            raise RuntimeError('Actor task failed to start.')
        
        # Process the results
        Actor.log.info(f'Task completed with status: {actor_run.status}')
```

## Key Methods

- `Actor.start()`: Start an Actor and return immediately
- `Actor.call()`: Start an Actor and wait for completion
- `Actor.call_task()`: Start an Actor task and wait for completion

## Use Cases

- Chain multiple Actors together
- Process results from other Actors
- Create Actor workflows
- Leverage specialized Actors for specific tasks