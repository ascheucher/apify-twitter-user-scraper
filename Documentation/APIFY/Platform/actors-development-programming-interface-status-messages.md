# Status Messages | Platform | Apify Documentation

## Overview

Status messages provide real-time feedback about an Actor's progress and current state. They help users understand what the Actor is doing and inform them about the execution status.

## Actor Status Types

### Core Status Values
- **`READY`**: Initial state, not yet allocated to a worker
- **`RUNNING`**: Currently executing
- **`SUCCEEDED`**: Finished successfully
- **`FAILED`**: Run failed
- **`TIMING-OUT`**: Currently timing out
- **`TIMED-OUT`**: Timed out completely
- **`ABORTING`**: Being manually aborted
- **`ABORTED`**: Manually stopped

## Status Message Features

### Automatic Messages
- Generated automatically by the platform
- Examples: "Actor finished with exit code 1", "Actor started"
- Provide basic information about Actor lifecycle

### Manual Messages
- Set by developers during Actor execution
- Provide specific, contextual information
- Help users understand current progress

## Updating Status Messages

### JavaScript Example
```javascript
const { Actor } = require('apify');

Actor.main(async () => {
    // Set initial status
    await Actor.setStatusMessage('Starting data collection...');
    
    // Update progress during execution
    for (let i = 0; i < 100; i++) {
        // Process data
        await processItem(i);
        
        // Update status every 10 items
        if (i % 10 === 0) {
            await Actor.setStatusMessage(`Processed ${i + 1} of 100 items`);
        }
    }
    
    // Final status update
    await Actor.setStatusMessage('Data collection completed successfully');
});
```

### Python Example
```python
from apify import Actor

async def main():
    async with Actor:
        # Set initial status
        await Actor.set_status_message('Starting data collection...')
        
        # Update progress during execution
        for i in range(100):
            # Process data
            await process_item(i)
            
            # Update status every 10 items
            if i % 10 == 0:
                await Actor.set_status_message(f'Processed {i + 1} of 100 items')
        
        # Final status update
        await Actor.set_status_message('Data collection completed successfully')
```

## Best Practices

### 1. Meaningful Messages
```javascript
// Good: Specific and informative
await Actor.setStatusMessage('Crawling product pages: 45 of 100 completed');

// Better: Include percentage and context
await Actor.setStatusMessage('Crawling product pages: 45/100 (45%) - Processing electronics category');

// Avoid: Too generic
await Actor.setStatusMessage('Processing...');
```

### 2. Progress Tracking
```javascript
// Track progress with detailed information
const totalItems = 1000;
let processedItems = 0;

for (const item of items) {
    await processItem(item);
    processedItems++;
    
    // Update status every 5%
    if (processedItems % Math.floor(totalItems / 20) === 0) {
        const percentage = Math.round((processedItems / totalItems) * 100);
        await Actor.setStatusMessage(
            `Processing items: ${processedItems}/${totalItems} (${percentage}%)`
        );
    }
}
```

### 3. Error Context
```javascript
try {
    await Actor.setStatusMessage('Connecting to API...');
    const data = await fetchFromAPI();
    
    await Actor.setStatusMessage('Processing API response...');
    const results = await processData(data);
    
    await Actor.setStatusMessage('Saving results...');
    await Actor.pushData(results);
    
} catch (error) {
    await Actor.setStatusMessage(`Error: ${error.message}`);
    throw error;
}
```

## Advanced Status Patterns

### Time-based Updates
```javascript
// Update status periodically
const startTime = Date.now();
let lastUpdate = 0;

async function updateStatusIfNeeded(currentCount, totalCount) {
    const now = Date.now();
    
    // Update every 30 seconds
    if (now - lastUpdate > 30000) {
        const elapsed = Math.round((now - startTime) / 1000);
        const rate = currentCount / elapsed;
        const estimated = Math.round((totalCount - currentCount) / rate);
        
        await Actor.setStatusMessage(
            `Processed ${currentCount}/${totalCount} items. ` +
            `Rate: ${rate.toFixed(1)}/sec. ETA: ${estimated}s`
        );
        
        lastUpdate = now;
    }
}
```

### Phase-based Status
```javascript
const phases = [
    'Initializing crawler',
    'Discovering pages',
    'Extracting data',
    'Processing results',
    'Saving data'
];

for (let i = 0; i < phases.length; i++) {
    await Actor.setStatusMessage(`Phase ${i + 1}/${phases.length}: ${phases[i]}`);
    await executePhase(i);
}
```

### Conditional Status Updates
```javascript
// Only update status when something meaningful happens
let lastStatusMessage = '';

async function updateStatus(message) {
    if (message !== lastStatusMessage) {
        await Actor.setStatusMessage(message);
        lastStatusMessage = message;
    }
}

// Usage
await updateStatus('Starting data extraction...');
await updateStatus('Starting data extraction...'); // Won't update (same message)
await updateStatus('Data extraction completed');   // Will update (different message)
```

## Performance Considerations

### SDK Optimization
- The SDK automatically optimizes API calls
- Status messages are only sent when the message changes
- Frequent updates with the same message don't cause additional API calls

### Update Frequency
```javascript
// Good: Reasonable update frequency
if (processedCount % 100 === 0) {
    await Actor.setStatusMessage(`Processed ${processedCount} items`);
}

// Avoid: Too frequent updates
await Actor.setStatusMessage(`Processing item ${i}`); // Called for every item
```

## Integration with Logging

### Combined Status and Logging
```javascript
async function logAndUpdateStatus(message, level = 'info') {
    console.log(`[${level.toUpperCase()}] ${message}`);
    await Actor.setStatusMessage(message);
}

// Usage
await logAndUpdateStatus('Starting web scraping process');
await logAndUpdateStatus('Failed to load page', 'error');
```

### Error Handling
```javascript
async function handleError(error, context) {
    const errorMessage = `Error in ${context}: ${error.message}`;
    
    // Log detailed error
    console.error('Detailed error:', error);
    
    // Set user-friendly status
    await Actor.setStatusMessage(errorMessage);
    
    // Optionally store error details
    await Actor.setValue('last_error', {
        message: error.message,
        stack: error.stack,
        context: context,
        timestamp: new Date().toISOString()
    });
}
```

## Common Status Message Patterns

### Web Scraping
```javascript
await Actor.setStatusMessage('Loading target website...');
await Actor.setStatusMessage('Extracting product links...');
await Actor.setStatusMessage('Scraping product details: 15/50 products');
await Actor.setStatusMessage('Saving scraped data...');
await Actor.setStatusMessage('Scraping completed successfully');
```

### Data Processing
```javascript
await Actor.setStatusMessage('Reading input data...');
await Actor.setStatusMessage('Validating data format...');
await Actor.setStatusMessage('Transforming data: 300/1000 records');
await Actor.setStatusMessage('Applying filters and sorting...');
await Actor.setStatusMessage('Exporting processed data...');
```

Status messages are essential for providing transparency and building trust with users by keeping them informed about Actor progress and current activities.