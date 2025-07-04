# Creating Webhooks in Apify SDK for Python

## Overview
Webhooks in Apify allow you to configure platform actions when specific events occur. They enable automated interactions like starting another Actor when a run finishes or fails.

## Creating Ad-Hoc Webhooks Dynamically

You can create webhooks programmatically using the `Actor.add_webhook()` method:

```python
from apify import Actor, Webhook

async def main() -> None:
    async with Actor:
        # Create a webhook triggered on Actor run failure
        webhook = Webhook(
            event_types=['ACTOR.RUN.FAILED'],
            request_url='https://example.com/run-failed',
        )
        
        # Add the webhook to the Actor
        await Actor.add_webhook(webhook)
        
        # Raise an error to simulate a failed run
        raise RuntimeError('I am an error and I know it!')
```

## Important Notes
- Webhooks only work when running on the Apify platform
- When running locally, the method will print a warning and have no effect

## Preventing Duplicate Webhooks

To prevent duplicate webhook creation, use the `idempotency_key` parameter:

```python
async def main() -> None:
    async with Actor:
        webhook = Webhook(
            event_types=['ACTOR.RUN.FAILED'],
            request_url='https://example.com/run-failed',
            idempotency_key=Actor.config.actor_run_id,
        )
        await Actor.add_webhook(webhook)
```

The `idempotency_key` ensures only one webhook is created for a given value, using the Actor run ID as a unique identifier.

## Additional Resources
- [Apify Webhooks Documentation](https://docs.apify.com/platform/integrations/webhooks)
- [Ad-hoc Webhooks Guide](https://docs.apify.com/platform/integrations/webhooks/ad-hoc-webhooks)