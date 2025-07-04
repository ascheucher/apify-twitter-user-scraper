# Accessing Apify API in Python SDK

The Apify SDK provides two primary methods for interacting with the Apify API:

## Actor Client

You can access the Apify API client through `Actor.apify_client`. Here's an example of getting user details:

```python
from apify import Actor

async def main() -> None:
    async with Actor:
        # Create a new user client
        user_client = Actor.apify_client.user('me')
        
        # Get information about the current user
        me = await user_client.get()
        Actor.log.info(f'User: {me}')
```

## Creating a New Client

To create a completely new client instance with custom configuration:

```python
from apify import Actor

TOKEN = 'ANOTHER_USERS_TOKEN'

async def main() -> None:
    async with Actor:
        # Create a new user client with a custom token
        apify_client = Actor.new_client(token=TOKEN, max_retries=2)
        user_client = apify_client.user('me')
        
        # Get information about another user
        them = await user_client.get()
        Actor.log.info(f'Another user: {them}')
```

## Key Points

- The SDK does not cover all Apify API features
- Use the provided `ApifyClientAsync` for direct API interactions
- `Actor.apify_client` provides the default client instance
- `Actor.new_client()` allows creating custom client configurations

The documentation emphasizes that while the SDK offers many features, developers may need to use the Apify API Client directly for full functionality.