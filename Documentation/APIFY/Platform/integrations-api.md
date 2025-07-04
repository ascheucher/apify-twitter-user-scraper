# API Integration | Platform | Apify Documentation

## Overview

Apify provides a comprehensive REST API for programmatic access to the platform, enabling automation of Actor runs, data management, scheduling, and integration with external systems. The API supports full account management and resource manipulation capabilities.

## Authentication

### API Token Management

#### Obtaining API Token
1. **Navigate to Apify Console**: Go to your account settings
2. **Find API tokens section**: Located in account preferences
3. **Generate new token**: Click "Create new token"
4. **Configure permissions**: Set appropriate scope and expiration
5. **Copy token**: Save securely for use in applications

#### Authentication Methods

##### HTTP Header (Recommended)
```bash
curl "https://api.apify.com/v2/acts" \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

```javascript
// JavaScript with fetch
const response = await fetch('https://api.apify.com/v2/acts', {
    headers: {
        'Authorization': 'Bearer YOUR_API_TOKEN',
        'Content-Type': 'application/json'
    }
});
```

##### URL Query Parameter
```bash
curl "https://api.apify.com/v2/acts?token=YOUR_API_TOKEN"
```

```javascript
// JavaScript with query parameter
const apiUrl = `https://api.apify.com/v2/acts?token=${API_TOKEN}`;
const response = await fetch(apiUrl);
```

### Token Security Best Practices

#### Environment Variables
```javascript
// Store token in environment variables
const API_TOKEN = process.env.APIFY_API_TOKEN;

if (!API_TOKEN) {
    throw new Error('APIFY_API_TOKEN environment variable is required');
}

const apiClient = new ApifyApi({ token: API_TOKEN });
```

#### Token Rotation
```javascript
// Implement token rotation for security
class TokenManager {
    constructor(tokens) {
        this.tokens = tokens;
        this.currentIndex = 0;
        this.failedTokens = new Set();
    }
    
    getCurrentToken() {
        const availableTokens = this.tokens.filter(
            (_, index) => !this.failedTokens.has(index)
        );
        
        if (availableTokens.length === 0) {
            throw new Error('No valid API tokens available');
        }
        
        const token = availableTokens[this.currentIndex % availableTokens.length];
        this.currentIndex++;
        
        return token;
    }
    
    markTokenAsFailed(token) {
        const index = this.tokens.indexOf(token);
        if (index !== -1) {
            this.failedTokens.add(index);
        }
    }
}
```

## API Clients

### JavaScript Client
```bash
npm install apify-client
```

```javascript
const { ApifyApi } = require('apify-client');

// Initialize client
const client = new ApifyApi({
    token: 'YOUR_API_TOKEN',
    baseUrl: 'https://api.apify.com', // Optional, defaults to this
    maxRetries: 3, // Optional, defaults to 3
    minDelayBetweenRetriesMillis: 500 // Optional, defaults to 500
});

// Basic usage examples
const main = async () => {
    try {
        // List actors
        const actors = await client.actors().list();
        console.log('Found actors:', actors.items.length);
        
        // Run actor
        const run = await client.actor('ACTOR_ID').start({
            input: { url: 'https://example.com' }
        });
        
        // Wait for completion
        const finishedRun = await client.actor('ACTOR_ID').run(run.id).waitForFinish();
        console.log('Run status:', finishedRun.status);
        
        // Get results
        const dataset = await client.dataset(finishedRun.defaultDatasetId);
        const { items } = await dataset.listItems();
        console.log('Results:', items.length);
        
    } catch (error) {
        console.error('API Error:', error);
    }
};

main();
```

### Python Client
```bash
pip install apify-client
```

```python
from apify_client import ApifyClient

# Initialize client
client = ApifyClient('YOUR_API_TOKEN')

async def main():
    try:
        # List actors
        actors = client.actors().list()
        print(f'Found actors: {len(actors.items)}')
        
        # Run actor
        run = client.actor('ACTOR_ID').start({
            'input': {'url': 'https://example.com'}
        })
        
        # Wait for completion
        finished_run = client.actor('ACTOR_ID').run(run['id']).wait_for_finish()
        print(f'Run status: {finished_run["status"]}')
        
        # Get results
        dataset = client.dataset(finished_run['defaultDatasetId'])
        items = dataset.list_items()
        print(f'Results: {len(items.items)}')
        
    except Exception as error:
        print(f'API Error: {error}')

if __name__ == '__main__':
    main()
```

## Token Permissions

### Scoped Token Permissions

#### Account-Level Permissions
- **Full access**: Complete account data access
- **Read-only access**: View-only permissions
- **Actor management**: Create, modify, and delete Actors
- **Run management**: Start, stop, and monitor runs
- **Storage access**: Datasets, key-value stores, request queues
- **Schedule management**: Create and manage schedules

#### Resource-Specific Permissions
```javascript
// Create scoped token via API
const scopedToken = await client.user().createToken({
    name: 'Limited Access Token',
    scopes: [
        'actors:read',
        'runs:write',
        'datasets:read'
    ],
    expiresAt: '2024-12-31T23:59:59.000Z'
});
```

### Permission Examples

#### Read-Only Access
```javascript
// Token with read-only permissions
const readOnlyClient = new ApifyApi({
    token: 'READ_ONLY_TOKEN'
});

// Can read data
const actors = await readOnlyClient.actors().list();
const runs = await readOnlyClient.actor('ACTOR_ID').runs().list();

// Cannot create or modify
try {
    await readOnlyClient.actor('ACTOR_ID').start({}); // Will fail
} catch (error) {
    console.log('Access denied:', error.message);
}
```

#### Limited Resource Access
```javascript
// Token limited to specific resources
const limitedClient = new ApifyApi({
    token: 'LIMITED_TOKEN'
});

// Access specific actor only
const allowedActorId = 'ALLOWED_ACTOR_ID';
const forbiddenActorId = 'FORBIDDEN_ACTOR_ID';

// This works
const run1 = await limitedClient.actor(allowedActorId).start({});

// This fails
try {
    const run2 = await limitedClient.actor(forbiddenActorId).start({});
} catch (error) {
    console.log('Resource access denied:', error.message);
}
```

## Common Integration Patterns

### 1. Actor Orchestration
```javascript
// Orchestrate multiple actors in sequence
const orchestrateActors = async (workflow) => {
    const results = [];
    
    for (const step of workflow) {
        console.log(`Starting step: ${step.name}`);
        
        const run = await client.actor(step.actorId).start({
            input: {
                ...step.input,
                // Pass results from previous step
                previousResults: results[results.length - 1]
            }
        });
        
        const finishedRun = await run.waitForFinish();
        
        if (finishedRun.status !== 'SUCCEEDED') {
            throw new Error(`Step ${step.name} failed: ${finishedRun.statusMessage}`);
        }
        
        // Get results for next step
        const dataset = await client.dataset(finishedRun.defaultDatasetId);
        const { items } = await dataset.listItems();
        results.push(items);
        
        console.log(`Step ${step.name} completed with ${items.length} results`);
    }
    
    return results;
};

// Example workflow
const workflow = [
    {
        name: 'Extract URLs',
        actorId: 'url-extractor',
        input: { startUrl: 'https://example.com' }
    },
    {
        name: 'Scrape Details',
        actorId: 'detail-scraper',
        input: { concurrency: 5 }
    },
    {
        name: 'Process Data',
        actorId: 'data-processor',
        input: { format: 'json' }
    }
];

const results = await orchestrateActors(workflow);
```

### 2. Real-time Monitoring
```javascript
// Monitor actor runs in real-time
class ActorMonitor {
    constructor(apiClient, actorId) {
        this.client = apiClient;
        this.actorId = actorId;
        this.activeRuns = new Map();
    }
    
    async startMonitoring() {
        console.log(`Starting monitoring for actor ${this.actorId}`);
        
        // Poll for new runs every 30 seconds
        setInterval(async () => {
            await this.checkForNewRuns();
            await this.updateActiveRuns();
        }, 30000);
    }
    
    async checkForNewRuns() {
        const runs = await this.client.actor(this.actorId).runs().list({
            limit: 10,
            desc: true
        });
        
        for (const run of runs.items) {
            if (!this.activeRuns.has(run.id) && run.status === 'RUNNING') {
                this.activeRuns.set(run.id, {
                    id: run.id,
                    startedAt: run.startedAt,
                    status: run.status
                });
                
                console.log(`New run detected: ${run.id}`);
                await this.onRunStarted(run);
            }
        }
    }
    
    async updateActiveRuns() {
        for (const [runId, runInfo] of this.activeRuns) {
            const run = await this.client.actor(this.actorId).run(runId).get();
            
            if (run.status !== runInfo.status) {
                console.log(`Run ${runId} status changed: ${runInfo.status} -> ${run.status}`);
                
                if (['SUCCEEDED', 'FAILED', 'ABORTED', 'TIMED-OUT'].includes(run.status)) {
                    await this.onRunFinished(run);
                    this.activeRuns.delete(runId);
                } else {
                    runInfo.status = run.status;
                }
            }
        }
    }
    
    async onRunStarted(run) {
        // Send notification about new run
        await this.sendNotification({
            type: 'RUN_STARTED',
            runId: run.id,
            actorId: this.actorId,
            startedAt: run.startedAt
        });
    }
    
    async onRunFinished(run) {
        // Process finished run
        if (run.status === 'SUCCEEDED') {
            const dataset = await this.client.dataset(run.defaultDatasetId);
            const { items } = await dataset.listItems();
            
            await this.sendNotification({
                type: 'RUN_SUCCEEDED',
                runId: run.id,
                actorId: this.actorId,
                itemCount: items.length,
                duration: new Date(run.finishedAt) - new Date(run.startedAt)
            });
        } else {
            await this.sendNotification({
                type: 'RUN_FAILED',
                runId: run.id,
                actorId: this.actorId,
                status: run.status,
                statusMessage: run.statusMessage
            });
        }
    }
    
    async sendNotification(data) {
        // Implement your notification logic
        console.log('Notification:', JSON.stringify(data, null, 2));
    }
}

// Usage
const monitor = new ActorMonitor(client, 'MY_ACTOR_ID');
await monitor.startMonitoring();
```

### 3. Data Processing Pipeline
```javascript
// Automated data processing pipeline
class DataPipeline {
    constructor(apiClient) {
        this.client = apiClient;
        this.processingQueue = [];
        this.isProcessing = false;
    }
    
    async addToQueue(actorId, input, priority = 'normal') {
        this.processingQueue.push({
            actorId,
            input,
            priority,
            timestamp: Date.now()
        });
        
        // Sort by priority
        this.processingQueue.sort((a, b) => {
            const priorityOrder = { high: 3, normal: 2, low: 1 };
            return priorityOrder[b.priority] - priorityOrder[a.priority];
        });
        
        if (!this.isProcessing) {
            await this.processQueue();
        }
    }
    
    async processQueue() {
        this.isProcessing = true;
        
        while (this.processingQueue.length > 0) {
            const task = this.processingQueue.shift();
            
            try {
                console.log(`Processing task for actor ${task.actorId}`);
                
                const run = await this.client.actor(task.actorId).start({
                    input: task.input
                });
                
                const finishedRun = await run.waitForFinish();
                
                if (finishedRun.status === 'SUCCEEDED') {
                    await this.onTaskCompleted(task, finishedRun);
                } else {
                    await this.onTaskFailed(task, finishedRun);
                }
                
            } catch (error) {
                console.error(`Task failed for actor ${task.actorId}:`, error);
                await this.onTaskError(task, error);
            }
        }
        
        this.isProcessing = false;
    }
    
    async onTaskCompleted(task, run) {
        console.log(`Task completed for actor ${task.actorId}`);
        
        // Process results
        const dataset = await this.client.dataset(run.defaultDatasetId);
        const { items } = await dataset.listItems();
        
        // Store processed data
        await this.storeResults(task.actorId, items);
    }
    
    async onTaskFailed(task, run) {
        console.error(`Task failed for actor ${task.actorId}: ${run.statusMessage}`);
        
        // Implement retry logic if needed
        if (task.retryCount < 3) {
            task.retryCount = (task.retryCount || 0) + 1;
            this.processingQueue.unshift(task); // Add back to front
        }
    }
    
    async onTaskError(task, error) {
        console.error(`Task error for actor ${task.actorId}:`, error.message);
        // Handle unexpected errors
    }
    
    async storeResults(actorId, data) {
        // Store results in external system
        console.log(`Storing ${data.length} results from ${actorId}`);
        // Implementation depends on your storage system
    }
}

// Usage
const pipeline = new DataPipeline(client);

// Add tasks to pipeline
await pipeline.addToQueue('web-scraper', { url: 'https://example1.com' }, 'high');
await pipeline.addToQueue('data-processor', { format: 'json' }, 'normal');
await pipeline.addToQueue('report-generator', { template: 'summary' }, 'low');
```

## Error Handling

### API Error Types
```javascript
// Comprehensive error handling
const handleApiError = (error) => {
    if (error.type === 'RATE_LIMIT_EXCEEDED') {
        console.log('Rate limit exceeded, waiting before retry...');
        return { retry: true, delay: 60000 };
    }
    
    if (error.type === 'ACTOR_NOT_FOUND') {
        console.error('Actor not found:', error.message);
        return { retry: false, fatal: true };
    }
    
    if (error.type === 'INSUFFICIENT_BALANCE') {
        console.error('Insufficient account balance');
        return { retry: false, fatal: true };
    }
    
    if (error.type === 'INVALID_INPUT') {
        console.error('Invalid input provided:', error.message);
        return { retry: false, fatal: true };
    }
    
    if (error.statusCode >= 500) {
        console.log('Server error, retrying...', error.message);
        return { retry: true, delay: 5000 };
    }
    
    console.error('Unknown API error:', error);
    return { retry: false, fatal: false };
};

// Retry wrapper
const withRetry = async (operation, maxRetries = 3) => {
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
        try {
            return await operation();
        } catch (error) {
            const errorInfo = handleApiError(error);
            
            if (errorInfo.fatal) {
                throw error;
            }
            
            if (!errorInfo.retry || attempt === maxRetries) {
                throw error;
            }
            
            console.log(`Attempt ${attempt} failed, retrying in ${errorInfo.delay}ms...`);
            await new Promise(resolve => setTimeout(resolve, errorInfo.delay));
        }
    }
};
```

## Best Practices

### 1. Efficient Polling
```javascript
// Implement exponential backoff for polling
class EfficientPoller {
    constructor(operation, options = {}) {
        this.operation = operation;
        this.initialDelay = options.initialDelay || 1000;
        this.maxDelay = options.maxDelay || 30000;
        this.backoffFactor = options.backoffFactor || 1.5;
        this.maxAttempts = options.maxAttempts || 100;
    }
    
    async poll() {
        let delay = this.initialDelay;
        
        for (let attempt = 1; attempt <= this.maxAttempts; attempt++) {
            try {
                const result = await this.operation();
                
                if (result.completed) {
                    return result.data;
                }
                
                // Reset delay on successful check
                delay = this.initialDelay;
                
            } catch (error) {
                console.warn(`Polling attempt ${attempt} failed:`, error.message);
                
                // Increase delay on error
                delay = Math.min(delay * this.backoffFactor, this.maxDelay);
            }
            
            await new Promise(resolve => setTimeout(resolve, delay));
            delay = Math.min(delay * this.backoffFactor, this.maxDelay);
        }
        
        throw new Error('Polling exceeded maximum attempts');
    }
}
```

### 2. Batch Operations
```javascript
// Process operations in batches
const batchProcess = async (items, processor, batchSize = 10) => {
    const results = [];
    
    for (let i = 0; i < items.length; i += batchSize) {
        const batch = items.slice(i, i + batchSize);
        console.log(`Processing batch ${Math.floor(i / batchSize) + 1}/${Math.ceil(items.length / batchSize)}`);
        
        const batchResults = await Promise.all(
            batch.map(item => processor(item))
        );
        
        results.push(...batchResults);
        
        // Add delay between batches to avoid rate limiting
        if (i + batchSize < items.length) {
            await new Promise(resolve => setTimeout(resolve, 1000));
        }
    }
    
    return results;
};
```

Apify's API integration capabilities provide powerful automation and integration possibilities, enabling sophisticated workflows, monitoring systems, and data processing pipelines that can scale with your business needs.