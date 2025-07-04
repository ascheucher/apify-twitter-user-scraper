# Storage Usage | Platform | Apify Documentation

## Overview

Apify provides three main types of storage for your data processing and automation needs. Each storage type serves specific purposes and offers different capabilities for managing your Actor data.

## Storage Types

### 1. Dataset
**Purpose**: Stores series of data objects from web scraping, crawling, or data processing

**Use Cases**:
- Scraped product information
- Extracted article content
- Processed user data
- Search results
- Social media posts

**Characteristics**:
- Append-only structure
- JSON object storage
- Schema validation support
- Export capabilities (JSON, CSV, Excel)

### 2. Key-Value Store
**Purpose**: Saves records like files, screenshots, PDFs, or Actor state

**Use Cases**:
- Screenshots and images
- PDF documents
- Actor configuration state
- Temporary files
- Logs and reports

**Characteristics**:
- Key-based access
- Binary file support
- Content type specification
- Arbitrary data storage

### 3. Request Queue
**Purpose**: Maintains a dynamic queue of URLs for recursive website crawling

**Use Cases**:
- Website crawling queues
- URL processing pipelines
- Batch request management
- Recursive site exploration

**Characteristics**:
- FIFO (First In, First Out) processing
- Duplicate URL detection
- Request prioritization
- Retry mechanisms

## Access Methods

### 1. Apify Console
Web-based interface for storage management:
- **Browse data**: View stored items directly
- **Download exports**: Get data in various formats
- **Manage permissions**: Control access rights
- **Monitor usage**: Track storage consumption

### 2. Apify API
RESTful API for programmatic access:

```bash
# Get dataset items
curl "https://api.apify.com/v2/datasets/DATASET_ID/items" \
  -H "Authorization: Bearer YOUR_API_TOKEN"

# Store key-value pair
curl -X PUT "https://api.apify.com/v2/key-value-stores/STORE_ID/records/KEY" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data": "value"}'

# Add URL to request queue
curl -X POST "https://api.apify.com/v2/request-queues/QUEUE_ID/requests" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

### 3. API Clients
Language-specific clients for easy integration:

```javascript
// JavaScript client
const { ApifyApi } = require('apify-client');
const client = new ApifyApi({ token: 'YOUR_API_TOKEN' });

// Dataset operations
const dataset = await client.dataset('DATASET_ID');
await dataset.pushItems([{ name: 'Product', price: 29.99 }]);
const { items } = await dataset.listItems();

// Key-value store operations
const kvStore = await client.keyValueStore('STORE_ID');
await kvStore.setRecord({ key: 'config', value: { setting: 'value' } });
const record = await kvStore.getRecord('config');

// Request queue operations
const requestQueue = await client.requestQueue('QUEUE_ID');
await requestQueue.addRequest({ url: 'https://example.com' });
const request = await requestQueue.getRequest();
```

```python
# Python client
from apify_client import ApifyClient

client = ApifyClient('YOUR_API_TOKEN')

# Dataset operations
dataset = client.dataset('DATASET_ID')
dataset.push_items([{'name': 'Product', 'price': 29.99}])
items = dataset.list_items()

# Key-value store operations
kv_store = client.key_value_store('STORE_ID')
kv_store.set_record('config', {'setting': 'value'})
record = kv_store.get_record('config')

# Request queue operations
request_queue = client.request_queue('QUEUE_ID')
request_queue.add_request({'url': 'https://example.com'})
request = request_queue.get_request()
```

### 4. Apify SDKs
Native SDK integration within Actors:

```javascript
// JavaScript SDK in Actor
const { Actor } = require('apify');

Actor.main(async () => {
    // Dataset usage
    await Actor.pushData({ name: 'Product', price: 29.99 });
    
    // Key-value store usage
    await Actor.setValue('config', { setting: 'value' });
    const config = await Actor.getValue('config');
    
    // Request queue usage (via RequestQueue class)
    const requestQueue = await Actor.openRequestQueue();
    await requestQueue.addRequest({ url: 'https://example.com' });
    const request = await requestQueue.fetchNextRequest();
});
```

## Key Features

### Rate Limiting
- **Standard limit**: 30 requests per second
- **High-throughput endpoints**: Some endpoints allow 200 requests per second
- **Automatic throttling**: SDKs handle rate limiting automatically
- **Burst capability**: Short bursts above limit are tolerated

### Data Retention

#### 10 Most Recent Runs
- **Indefinite storage**: Data from your 10 most recent runs stored indefinitely
- **Automatic management**: Apify automatically tracks and maintains this limit
- **All storage types**: Applies to datasets, key-value stores, and request queues

#### Unnamed Datasets
- **7-day retention**: Automatically deleted after 7 days
- **Cleanup automation**: No manual intervention required
- **Performance optimization**: Reduces storage overhead

#### Named Storages
- **Indefinite retention**: Named storages retained indefinitely
- **Manual management**: User controls deletion
- **Shared access**: Can be accessed across multiple runs

### Storage Characteristics

#### Named Storages
- **Character limit**: Up to 63 characters long
- **Cross-run sharing**: Can be shared between different runs
- **Persistent access**: Remain available beyond run completion
- **Manual deletion**: User must explicitly delete

#### Concurrent Usage
- **Datasets**: Support multiple concurrent readers and writers
- **Key-value stores**: Support concurrent access with last-write-wins semantics
- **Request queues**: Only one run can process at a time (exclusive access)

#### Storage Limits
- **Size limits**: Vary by subscription plan
- **Item limits**: Maximum number of items per storage
- **Request limits**: API call quotas and rate limits

## Deletion Options

### 1. Apify Console
Web interface deletion:
- Navigate to storage in Console
- Select items or entire storage
- Click delete button
- Confirm deletion

### 2. JavaScript SDK
```javascript
// Delete dataset
const dataset = await Actor.openDataset('my-dataset');
await dataset.drop();

// Delete key-value store
const kvStore = await Actor.openKeyValueStore('my-store');
await kvStore.drop();

// Delete request queue
const requestQueue = await Actor.openRequestQueue('my-queue');
await requestQueue.drop();
```

### 3. Python SDK
```python
# Delete dataset
dataset = await Actor.open_dataset('my-dataset')
await dataset.drop()

# Delete key-value store
kv_store = await Actor.open_key_value_store('my-store')
await kv_store.drop()

# Delete request queue
request_queue = await Actor.open_request_queue('my-queue')
await request_queue.drop()
```

### 4. API Clients
```javascript
// Using Apify client
await client.dataset('DATASET_ID').delete();
await client.keyValueStore('STORE_ID').delete();
await client.requestQueue('QUEUE_ID').delete();
```

### 5. Direct API Endpoints
```bash
# Delete via API
curl -X DELETE "https://api.apify.com/v2/datasets/DATASET_ID" \
  -H "Authorization: Bearer YOUR_API_TOKEN"

curl -X DELETE "https://api.apify.com/v2/key-value-stores/STORE_ID" \
  -H "Authorization: Bearer YOUR_API_TOKEN"

curl -X DELETE "https://api.apify.com/v2/request-queues/QUEUE_ID" \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

## Sharing and Collaboration

### Access Rights Management
Grant access to other Apify users:

```javascript
// Share dataset with read access
await client.dataset('DATASET_ID').update({
    accessRights: {
        users: [
            { userId: 'USER_ID', permission: 'READ' }
        ]
    }
});

// Share with write access
await client.keyValueStore('STORE_ID').update({
    accessRights: {
        users: [
            { userId: 'USER_ID', permission: 'WRITE' }
        ]
    }
});
```

### Permission Levels
- **READ**: View and download data
- **WRITE**: Add, modify, and delete data
- **ADMIN**: Full control including access management

### Sharing via ID or Name
```javascript
// Access by ID (always works)
const dataset = await client.dataset('abc123def456');

// Access by name (if you have access)
const dataset = await client.dataset('shared-dataset-name');
```

## Best Practices

### 1. Naming Convention
```javascript
// Use descriptive names
const dataset = await Actor.openDataset('product-catalog-2024');
const kvStore = await Actor.openKeyValueStore('session-cookies');
const requestQueue = await Actor.openRequestQueue('ecommerce-urls');
```

### 2. Data Organization
```javascript
// Organize data logically
await Actor.pushData({
    category: 'electronics',
    subcategory: 'smartphones',
    product: {
        name: 'iPhone 15',
        price: 999,
        availability: 'in-stock'
    },
    scrapedAt: new Date().toISOString(),
    source: 'example-store.com'
});
```

### 3. Error Handling
```javascript
// Handle storage errors gracefully
try {
    await Actor.pushData(data);
} catch (error) {
    console.error('Failed to save data:', error);
    // Implement retry logic or alternative storage
}
```

### 4. Memory Management
```javascript
// Process large datasets in chunks
const dataset = await Actor.openDataset('large-dataset');
let offset = 0;
const limit = 1000;

while (true) {
    const { items } = await dataset.getData({ offset, limit });
    
    if (items.length === 0) break;
    
    await processChunk(items);
    offset += limit;
}
```

### 5. Storage Cleanup
```javascript
// Clean up temporary storages
Actor.main(async () => {
    const tempStore = await Actor.openKeyValueStore('temp-data');
    
    try {
        // Use temporary storage
        await processData(tempStore);
    } finally {
        // Clean up
        await tempStore.drop();
    }
});
```

## Performance Optimization

### 1. Batch Operations
```javascript
// Batch dataset insertions
const batch = [];
for (const item of items) {
    batch.push(item);
    
    if (batch.length >= 100) {
        await Actor.pushData(batch);
        batch.length = 0; // Clear array
    }
}

// Push remaining items
if (batch.length > 0) {
    await Actor.pushData(batch);
}
```

### 2. Efficient Querying
```javascript
// Use pagination for large datasets
async function getAllItems(datasetId) {
    const items = [];
    let offset = 0;
    const limit = 1000;
    
    while (true) {
        const data = await client.dataset(datasetId).listItems({
            offset,
            limit,
            clean: true
        });
        
        items.push(...data.items);
        
        if (data.items.length < limit) break;
        offset += limit;
    }
    
    return items;
}
```

### 3. Request Queue Optimization
```javascript
// Use request queue efficiently
const requestQueue = await Actor.openRequestQueue();

// Add requests in batches
const requests = urls.map(url => ({ url, userData: { category: 'product' } }));
await requestQueue.addRequests(requests);

// Process with concurrency control
const concurrency = 5;
const promises = [];

for (let i = 0; i < concurrency; i++) {
    promises.push(processQueue(requestQueue));
}

await Promise.all(promises);
```

Apify's storage system provides robust, scalable solutions for managing data in web scraping and automation workflows, with comprehensive access methods, sharing capabilities, and optimization features.