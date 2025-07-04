# Runs | Platform | Apify Documentation

## Overview

A run is a single execution of an Actor with specific input in a Docker container. Runs represent the actual execution instances where your Actor processes data and performs its intended automation tasks.

## Run Basics

### What is a Run?
- **Single execution**: One instance of Actor execution
- **Specific input**: Configured with particular input parameters
- **Docker container**: Runs in an isolated containerized environment
- **Resource allocation**: Assigned memory, CPU, and time limits
- **Storage access**: Connected to datasets, key-value stores, and request queues

### Run Components
- **Build**: The Docker image version being executed
- **Input**: Data and configuration passed to the Actor
- **Resources**: Memory, CPU, and time allocations
- **Environment**: Variables and configuration settings
- **Storage**: Connected datasets and storage systems

## Starting Runs

### 1. Apify Console UI
The most user-friendly method for starting runs:
1. Navigate to your Actor in the Console
2. Click "Start" or "Try for free"
3. Configure input parameters
4. Adjust run options (memory, timeout)
5. Click "Start" to begin execution

### 2. Apify API
Programmatic run creation via REST API:

```bash
curl -X POST "https://api.apify.com/v2/acts/ACTOR_ID/runs" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "url": "https://example.com",
      "maxPages": 100
    },
    "options": {
      "build": "latest",
      "memoryMbytes": 1024,
      "timeoutSecs": 3600
    }
  }'
```

### 3. Apify SDK
Using JavaScript or Python SDKs:

```javascript
// JavaScript SDK
const { ApifyApi } = require('apify-client');
const client = new ApifyApi({ token: 'YOUR_API_TOKEN' });

const run = await client.actor('ACTOR_ID').start({
  input: { url: 'https://example.com' },
  build: 'latest',
  memory: 1024,
  timeout: 3600
});
```

```python
# Python SDK
from apify_client import ApifyClient

client = ApifyClient('YOUR_API_TOKEN')

run = client.actor('ACTOR_ID').start({
    'input': {'url': 'https://example.com'},
    'build': 'latest',
    'memory': 1024,
    'timeout': 3600
})
```

### 4. Platform Scheduler
Automated runs via scheduling:
- **Cron expressions**: Schedule runs at specific times
- **Recurring schedules**: Daily, weekly, monthly executions
- **Conditional triggers**: Based on external events

### 5. Integration Triggers
Runs triggered by external systems:
- **Webhooks**: HTTP triggers from external services
- **Zapier**: Integration with thousands of apps
- **Make (Integromat)**: Advanced automation workflows
- **API integrations**: Custom trigger implementations

## Input and Environment

### Input Handling
Runs receive input via the `INPUT` record in the default key-value store:

```javascript
// In your Actor code
const { Actor } = require('apify');

Actor.main(async () => {
    const input = await Actor.getInput();
    console.log('Received input:', input);
    
    // Process input parameters
    const { url, maxPages = 10 } = input || {};
    
    // Your Actor logic here
});
```

### Input Validation
```javascript
// Validate input parameters
Actor.main(async () => {
    const input = await Actor.getInput();
    
    if (!input) {
        throw new Error('No input provided');
    }
    
    if (!input.url) {
        throw new Error('URL parameter is required');
    }
    
    if (typeof input.maxPages !== 'number') {
        throw new Error('maxPages must be a number');
    }
    
    // Continue with validated input
    await processData(input);
});
```

### Environment Variables
Runs automatically receive environment variables:

```javascript
// Access environment variables
const runId = process.env.ACTOR_RUN_ID;
const actorId = process.env.ACTOR_ID;
const memoryMB = process.env.ACTOR_MEMORY_MBYTES;
const timeoutSecs = process.env.ACTOR_TIMEOUT_AT;

console.log('Run environment:', {
    runId,
    actorId,
    memoryMB,
    timeoutSecs
});
```

## Run Duration and Timeout

### Run Duration Types
- **Short runs**: Seconds to minutes (data extraction, API calls)
- **Medium runs**: Minutes to hours (website crawling, data processing)
- **Long runs**: Hours to days (large-scale scraping, batch processing)

### Timeout Configuration
Timeout prevents infinite runs and controls resource usage:

```javascript
// Configure timeout in run options
const run = await client.actor('ACTOR_ID').start({
    input: { url: 'https://example.com' },
    timeout: 3600 // 1 hour in seconds
});
```

### Default Timeouts
- **Varies by template**: Different Actor templates have different defaults
- **Free tier limits**: Shorter timeouts for free accounts
- **Paid plans**: Longer timeouts available with paid subscriptions

### Timeout Behavior
When a run doesn't complete within the timeout:
1. **Warning phase**: Actor receives timeout warnings
2. **Graceful shutdown**: Actor has time to save state
3. **Force termination**: Container is forcefully stopped
4. **Status update**: Run marked as "TIMED-OUT"

### Handling Timeouts
```javascript
// Handle timeout gracefully
Actor.main(async () => {
    let isTimingOut = false;
    
    Actor.on('aborting', () => {
        isTimingOut = true;
        console.log('Run is timing out, saving state...');
    });
    
    while (hasMoreWork() && !isTimingOut) {
        await processNextItem();
    }
    
    if (isTimingOut) {
        await saveCurrentState();
    }
});
```

## Run Configuration

### Basic Run Options
```javascript
const runOptions = {
    build: 'latest',           // Build version to use
    memory: 1024,              // Memory in MB
    timeout: 3600,             // Timeout in seconds
    maxItems: 1000,            // Limit output items
    webhooks: [],              // Webhook notifications
    metamorph: false           // Allow metamorphosis
};
```

### Advanced Configuration
```javascript
const advancedOptions = {
    build: 'beta',
    memory: 4096,
    timeout: 7200,
    env: {
        DEBUG: 'true',
        LOG_LEVEL: 'info'
    },
    webhooks: [{
        eventTypes: ['ACTOR.RUN.SUCCEEDED'],
        requestUrl: 'https://my-webhook.com/notify'
    }]
};
```

## Run Monitoring

### Real-time Status
```javascript
// Monitor run status
const run = await client.actor('ACTOR_ID').run('RUN_ID').get();

console.log('Run status:', {
    status: run.status,
    startedAt: run.startedAt,
    finishedAt: run.finishedAt,
    statusMessage: run.statusMessage
});
```

### Waiting for Completion
```javascript
// Wait for run to finish
const finishedRun = await client.actor('ACTOR_ID').run('RUN_ID').waitForFinish();

if (finishedRun.status === 'SUCCEEDED') {
    console.log('Run completed successfully');
    
    // Get results
    const dataset = await client.dataset(finishedRun.defaultDatasetId);
    const { items } = await dataset.listItems();
    
    console.log('Retrieved items:', items.length);
} else {
    console.error('Run failed:', finishedRun.statusMessage);
}
```

### Log Monitoring
```javascript
// Get run logs
const log = await client.actor('ACTOR_ID').run('RUN_ID').log().get();
console.log('Run log:', log);

// Stream logs in real-time
const logStream = await client.actor('ACTOR_ID').run('RUN_ID').log().stream();
logStream.on('data', (logLine) => {
    console.log('Log:', logLine);
});
```

## Run Results

### Dataset Results
```javascript
// Access run results from dataset
const run = await client.actor('ACTOR_ID').run('RUN_ID').get();
const dataset = await client.dataset(run.defaultDatasetId).listItems();

console.log('Results:', dataset.items);
```

### Key-Value Store Results
```javascript
// Access stored files and data
const kvStore = await client.keyValueStore(run.defaultKeyValueStoreId);
const output = await kvStore.getRecord('OUTPUT');

console.log('Output:', output);
```

### Statistics
```javascript
// Get run statistics
const run = await client.actor('ACTOR_ID').run('RUN_ID').get();

console.log('Statistics:', {
    runTimeSecs: run.stats.runTimeSecs,
    memoryUsageBytes: run.stats.memoryUsageBytes,
    datasetItems: run.stats.datasetItems,
    requestsTotal: run.stats.requestsTotal
});
```

## Error Handling

### Run Failures
```javascript
// Handle run failures
try {
    const run = await client.actor('ACTOR_ID').run('RUN_ID').waitForFinish();
    
    if (run.status === 'FAILED') {
        console.error('Run failed:', run.statusMessage);
        
        // Get error details from log
        const log = await client.actor('ACTOR_ID').run('RUN_ID').log().get();
        console.error('Error log:', log.slice(-1000)); // Last 1000 characters
    }
} catch (error) {
    console.error('Error waiting for run:', error);
}
```

### Retry Logic
```javascript
// Implement retry logic
async function runWithRetry(actorId, input, maxRetries = 3) {
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
        try {
            const run = await client.actor(actorId).start(input);
            const finishedRun = await run.waitForFinish();
            
            if (finishedRun.status === 'SUCCEEDED') {
                return finishedRun;
            }
            
            console.log(`Attempt ${attempt} failed:`, finishedRun.statusMessage);
        } catch (error) {
            console.error(`Attempt ${attempt} error:`, error);
        }
        
        if (attempt < maxRetries) {
            console.log(`Retrying in ${attempt * 5} seconds...`);
            await new Promise(resolve => setTimeout(resolve, attempt * 5000));
        }
    }
    
    throw new Error(`Failed after ${maxRetries} attempts`);
}
```

## Best Practices

### 1. Resource Optimization
```javascript
// Start with minimal resources and scale up
const run = await client.actor('ACTOR_ID').start({
    input: { url: 'https://example.com' },
    memory: 512,  // Start small
    timeout: 1800 // 30 minutes
});
```

### 2. Input Validation
```javascript
// Always validate input
Actor.main(async () => {
    const input = await Actor.getInput();
    
    const schema = {
        url: { type: 'string', required: true },
        maxPages: { type: 'number', default: 10, min: 1, max: 1000 }
    };
    
    const validatedInput = validateInput(input, schema);
    await processData(validatedInput);
});
```

### 3. Progress Reporting
```javascript
// Report progress for long-running tasks
Actor.main(async () => {
    const input = await Actor.getInput();
    const totalPages = input.maxPages || 10;
    
    for (let i = 0; i < totalPages; i++) {
        await processPage(i);
        
        const progress = Math.round((i + 1) / totalPages * 100);
        await Actor.setStatusMessage(`Processing page ${i + 1}/${totalPages} (${progress}%)`);
    }
});
```

### 4. Error Recovery
```javascript
// Implement graceful error recovery
Actor.main(async () => {
    const input = await Actor.getInput();
    const errors = [];
    
    for (const url of input.urls) {
        try {
            const result = await processUrl(url);
            await Actor.pushData(result);
        } catch (error) {
            errors.push({ url, error: error.message });
            console.warn(`Failed to process ${url}:`, error.message);
        }
    }
    
    // Save error summary
    if (errors.length > 0) {
        await Actor.setValue('errors', errors);
    }
});
```

## Run API Reference

### Start Run
```javascript
const run = await client.actor('ACTOR_ID').start(input, options);
```

### Get Run
```javascript
const run = await client.actor('ACTOR_ID').run('RUN_ID').get();
```

### Wait for Finish
```javascript
const run = await client.actor('ACTOR_ID').run('RUN_ID').waitForFinish();
```

### Abort Run
```javascript
const run = await client.actor('ACTOR_ID').run('RUN_ID').abort();
```

### Get Log
```javascript
const log = await client.actor('ACTOR_ID').run('RUN_ID').log().get();
```

Runs are the core execution mechanism of the Apify platform, providing flexible, scalable, and monitored execution of your automation tasks with comprehensive input handling, timeout management, and result collection capabilities.