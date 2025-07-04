# Basic Commands | Platform | Apify Documentation

## Overview

This documentation covers essential commands for initializing, running, and exiting Actors in both JavaScript and Python using the Apify SDK. These commands provide the foundation for Actor development.

## 1. Initialize Actor

### JavaScript
```javascript
// Using Actor.main() - recommended
const { Actor } = require('apify');

Actor.main(async () => {
    // Your Actor code here
});

// Using Actor.init() - manual initialization
const { Actor } = require('apify');

async function main() {
    await Actor.init();
    
    // Your Actor code here
    
    await Actor.exit();
}

main();
```

### Python
```python
# Using async context manager - recommended
from apify import Actor

async def main():
    async with Actor:
        # Your Actor code here
        pass

# Using manual initialization
from apify import Actor

async def main():
    await Actor.init()
    
    # Your Actor code here
    
    await Actor.exit()
```

### Purpose
- Prepares Actor to receive platform events
- Configures storage and environment
- Sets up SDK functionality

## 2. Get Input

### JavaScript
```javascript
const input = await Actor.getInput();
console.log('Input:', input);

// Handle missing input
if (!input) {
    console.log('No input provided');
}
```

### Python
```python
actor_input = await Actor.get_input()
print('Input:', actor_input)

# Handle missing input
if not actor_input:
    print('No input provided')
```

### Features
- Retrieves Actor input stored as JSON
- Input conforms to predefined schema if specified
- Returns `null`/`None` if no input provided

## 3. Key-Value Store Access

### JavaScript
```javascript
// Store data
await Actor.setValue('my-key', { foo: 'bar' });

// Store with content type
await Actor.setValue('my-file.txt', 'Hello World', {
    contentType: 'text/plain'
});

// Retrieve data
const value = await Actor.getValue('my-key');
console.log('Value:', value);

// Access different store
const store = await Actor.openKeyValueStore('my-store');
await store.setValue('key', 'value');
```

### Python
```python
# Store data
await Actor.set_value('my-key', {'foo': 'bar'})

# Store with content type
await Actor.set_value('my-file.txt', 'Hello World', 
                     content_type='text/plain')

# Retrieve data
value = await Actor.get_value('my-key')
print('Value:', value)

# Access different store
store = await Actor.open_key_value_store('my-store')
await store.set_value('key', 'value')
```

### Capabilities
- Read/write arbitrary files and objects
- Support for binary files with content types
- Access to multiple key-value stores
- Automatic serialization/deserialization

## 4. Push Results to Dataset

### JavaScript
```javascript
// Push single item
await Actor.pushData({ name: 'John', age: 30 });

// Push multiple items
await Actor.pushData([
    { name: 'Alice', age: 25 },
    { name: 'Bob', age: 35 }
]);

// Push to specific dataset
const dataset = await Actor.openDataset('my-dataset');
await dataset.pushData({ custom: 'data' });
```

### Python
```python
# Push single item
await Actor.push_data({'name': 'John', 'age': 30})

# Push multiple items
await Actor.push_data([
    {'name': 'Alice', 'age': 25},
    {'name': 'Bob', 'age': 35}
])

# Push to specific dataset
dataset = await Actor.open_dataset('my-dataset')
await dataset.push_data({'custom': 'data'})
```

### Features
- Store larger result sets in append-only storage
- Optional schema validation for stored objects
- Support for structured data
- Automatic data persistence

## 5. Exit Actor

### JavaScript
```javascript
// Basic exit (success)
await Actor.exit();

// Exit with custom message
await Actor.exit('Task completed successfully');

// Exit with failure
await Actor.exit('Error occurred', { exitCode: 1 });

// Immediate exit
await Actor.exit('Emergency exit', { timeoutSecs: 0 });

// Exit with event handler
Actor.on('exit', () => {
    console.log('Actor is exiting...');
});
```

### Python
```python
# Basic exit (success)
await Actor.exit()

# Exit with custom message
await Actor.exit('Task completed successfully')

# Exit with failure
await Actor.exit('Error occurred', exit_code=1)

# Immediate exit
await Actor.exit('Emergency exit', timeout_secs=0)
```

### Exit Behavior
- **Exit code 0**: Run status = SUCCEEDED
- **Non-zero exit code**: Run status = FAILED
- **Custom status messages**: Provide context for exit
- **Timeout handling**: Graceful vs immediate shutdown

## Advanced Examples

### Complete Actor Example (JavaScript)
```javascript
const { Actor } = require('apify');

Actor.main(async () => {
    console.log('Actor starting...');
    
    // Get input
    const input = await Actor.getInput();
    if (!input) {
        await Actor.exit('No input provided', { exitCode: 1 });
        return;
    }
    
    // Process data
    const results = [];
    for (let i = 0; i < input.count; i++) {
        results.push({
            id: i,
            message: `Item ${i}`,
            timestamp: new Date().toISOString()
        });
    }
    
    // Store results
    await Actor.pushData(results);
    
    // Store summary
    await Actor.setValue('summary', {
        itemCount: results.length,
        processingTime: new Date().toISOString()
    });
    
    console.log('Actor finished successfully');
});
```

### Complete Actor Example (Python)
```python
from apify import Actor

async def main():
    async with Actor:
        print('Actor starting...')
        
        # Get input
        actor_input = await Actor.get_input()
        if not actor_input:
            await Actor.exit('No input provided', exit_code=1)
            return
        
        # Process data
        results = []
        for i in range(actor_input.get('count', 0)):
            results.append({
                'id': i,
                'message': f'Item {i}',
                'timestamp': datetime.now().isoformat()
            })
        
        # Store results
        await Actor.push_data(results)
        
        # Store summary
        await Actor.set_value('summary', {
            'item_count': len(results),
            'processing_time': datetime.now().isoformat()
        })
        
        print('Actor finished successfully')

if __name__ == '__main__':
    import asyncio
    from datetime import datetime
    asyncio.run(main())
```

## Best Practices

1. **Always initialize**: Use `Actor.main()` or `Actor.init()` at the start
2. **Handle missing input**: Check for null/None input values
3. **Use appropriate storage**: Choose between datasets and key-value stores based on data type
4. **Provide meaningful exits**: Include descriptive messages when exiting
5. **Error handling**: Implement try/catch blocks for robust error handling
6. **Resource cleanup**: Ensure proper cleanup before exit

These basic commands provide the foundation for building sophisticated Actors that can process data, interact with storage, and communicate their status effectively.