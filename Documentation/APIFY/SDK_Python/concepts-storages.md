# Working with Storages in Apify SDK for Python

## Types of Storages

The Apify SDK provides three primary types of storages:

1. **Datasets**
   - Append-only tables for storing Actor results
   - Opened via `Actor.open_dataset()`
   - Used for storing structured result data

2. **Key-Value Stores**
   - Read/write storage for file-like objects
   - Opened via `Actor.open_key_value_store()`
   - Typically used for storing Actor state or binary results

3. **Request Queues**
   - Queues for storing URLs to scrape
   - Opened via `Actor.open_request_queue()`
   - Used for managing and processing scraping requests

## Local Storage Emulation

When developing locally, storages are emulated on the local filesystem:
- Stored in a `storage` folder
- Each storage type has its own subfolder
- Default storages are stored in `default` folders
- Storage contents are persisted across Actor runs

### Opening Storages Example

```python
from apify import Actor

async def main() -> None:
    async with Actor:
        # Open default dataset
        dataset = await Actor.open_dataset()
        
        # Open specific key-value store by ID
        key_value_store = await Actor.open_key_value_store(id='mIJVZsRQrDQf4rUAf')
        
        # Open request queue by name
        request_queue = await Actor.open_request_queue(name='my-queue')
```

## Working with Datasets

### Writing and Reading Data

```python
async def main() -> None:
    async with Actor:
        dataset = await Actor.open_dataset(name='my-dataset')
        
        # Push data to dataset
        await dataset.push_data([{'itemNo': i} for i in range(1000)])
        
        # Read dataset data
        first_half = await dataset.get_data(limit=500)
        
        # Iterate over items
        second_half = [item async for item in dataset.iterate_items(offset=500)]
```

## Convenience Methods

- `Actor.get_value()`: Read from default key-value store
- `Actor.set_value()`: Save value to default key-value store
- `Actor.push_data()`: Save results to default dataset

## Key Features

- Each Actor run has default dataset, key-value store, and request queue
- Local storage is emulated on filesystem in a `storage` folder
- Can work with named or unnamed storages
- Supports local and remote storage options