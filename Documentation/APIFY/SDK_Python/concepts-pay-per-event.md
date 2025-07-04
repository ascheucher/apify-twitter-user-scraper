# Pay-per-event Monetization in Apify Python SDK

## Overview

Apify offers a flexible pay-per-event monetization model that allows developers to charge users programmatically for specific events within an Actor. This pricing model enables charging for actions like API calls or returning results.

## Setup Requirements

1. Configure pay-per-event pricing in the Apify console
2. Implement charging mechanisms in your Actor's code

## Charging for Events

### Basic Charging Methods

```python
from apify import Actor

async def main() -> None:
    async with Actor:
        # Charge for a single event occurrence
        await Actor.charge(event_name='init')
        
        # Prepare results
        result = [
            {'word': 'Lorem'},
            {'word': 'Ipsum'},
            {'word': 'Dolor'},
            {'word': 'Sit'},
            {'word': 'Amet'},
        ]
        
        # Charge for each dataset item
        await Actor.push_data(result, 'result-item')
        
        # Manually charge for multiple events
        await Actor.charge(
            event_name='result-item',
            count=len(result),
        )
```

### Advanced Charging Control

Developers can use `Actor.get_charging_manager()` to access the `ChargingManager` for more detailed charging information and control.

## Transitioning Between Pricing Models

When moving from another pricing model (e.g., pay-per-result), you'll need to support both models during the transition:

```python
from apify import Actor

async def main() -> None:
    async with Actor:
        # Check existing dataset
        default_dataset = await Actor.open_dataset()
        dataset_info = await default_dataset.get_info()
        charged_items = dataset_info.item_count if dataset_info else 0
        
        # Handle different pricing models
        if Actor.get_charging_manager().get_pricing_info().is_pay_per_event:
            await Actor.push_data({'hello': 'world'}, 'dataset-item')
        elif charged_items < Actor.config.max_paid_dataset_items:
            await Actor.push_data({'hello': 'world'})
```

## Key Features

- Flexible event-based pricing
- Support for multiple event types
- Automatic charging integration
- Transition support between pricing models
- Detailed charging management controls