# Actor Input in Apify SDK for Python

## Overview

The Actor input is retrieved from the default key-value store, which can be accessed using the `Actor.get_input()` method. This method automatically handles reading the input record and decrypting any secret input fields.

## Example Usage

```python
from apify import Actor

async def main() -> None:
    async with Actor:
        actor_input = await Actor.get_input() or {}
        first_number = actor_input.get('firstNumber', 0)
        second_number = actor_input.get('secondNumber', 0)
        Actor.log.info('Sum: %s', first_number + second_number)
```

## Key Features

- Input is stored in the default key-value store
- `Actor.get_input()` method provides convenient access to input
- Supports JSON input with multiple fields
- Allows setting default values when accessing input fields
- Automatically handles decryption of secret input fields

## Input Handling

- Use `.get()` method to safely retrieve input values
- Provide default values to prevent errors if input is missing
- Can handle various input types and structures
- Supports optional input by using `or {}` to provide an empty dictionary if no input is found

## Best Practices

- Always check for input existence
- Use default values to handle potential missing inputs
- Log input processing for debugging
- Use type-safe methods to extract input values