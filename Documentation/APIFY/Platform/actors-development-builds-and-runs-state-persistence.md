# State Persistence | Platform | Apify Documentation

## Overview

State persistence is a critical mechanism for preventing data loss during server migrations in long-running Actors on the Apify platform. It ensures that your Actor can resume from where it left off if the server needs to migrate your container to a different machine.

## Understanding Migrations

### What are Migrations?
Migrations occur when the Apify platform moves your running Actor from one server to another. This can happen due to:
- **Server workload optimization**: Balancing load across servers
- **Server crashes**: Hardware or software failures
- **Feature releases**: Platform updates and improvements
- **Bug fixes**: Critical system patches
- **Resource reallocation**: Optimizing resource distribution

### Migration Unpredictability
- **No advance warning**: Migrations can happen without prior notice
- **Any time during execution**: Can occur at any point during Actor run
- **Platform-wide events**: May affect multiple Actors simultaneously
- **Automatic process**: Handled transparently by the platform

## Why State is Lost

### Default Behavior
By default, an Actor's state is stored in server memory (RAM). During a migration:
1. **Current container stops**: The running container is terminated
2. **Memory becomes inaccessible**: All RAM-stored data is lost
3. **New container starts**: A fresh container begins on the new server
4. **Clean slate**: The Actor starts from the beginning

### Data at Risk
Without state persistence, you lose:
- **Processing progress**: How much work has been completed
- **Queue states**: Pending URLs or tasks
- **Temporary data**: Variables and intermediate results
- **Session information**: Login states, cookies, tokens
- **Configuration state**: Dynamic settings and parameters

## Implementation Strategies

### Using Apify SDKs

The Apify SDKs provide built-in methods for state persistence that automatically handle migration events.

#### JavaScript Implementation
```javascript
import { Actor } from 'apify';

await Actor.init();

// Listen for migration events
Actor.on('migrating', async () => {
    console.log('Migration detected, saving state...');
    
    // Save your current state
    await Actor.setValue('my-crawling-state', {
        processedUrls: processedUrls,
        currentPage: currentPage,
        sessionCookies: sessionCookies,
        lastProcessedItem: lastProcessedItem,
        queueState: queueState
    });
    
    console.log('State saved successfully');
});

// Retrieve previous state on startup
const previousCrawlingState = await Actor.getValue('my-crawling-state') || {};

if (previousCrawlingState.processedUrls) {
    console.log('Resuming from previous state...');
    processedUrls = previousCrawlingState.processedUrls;
    currentPage = previousCrawlingState.currentPage;
    sessionCookies = previousCrawlingState.sessionCookies;
}

// Your Actor logic continues...
```

#### Python Implementation
```python
from apify import Actor, Event

async def actor_migrate(event_data):
    """Handle migration event by saving state"""
    print('Migration detected, saving state...')
    
    await Actor.set_value('my-crawling-state', {
        'processed_urls': processed_urls,
        'current_page': current_page,
        'session_cookies': session_cookies,
        'last_processed_item': last_processed_item,
        'queue_state': queue_state
    })
    
    print('State saved successfully')

async def main():
    async with Actor:
        # Register migration handler
        Actor.on(Event.MIGRATING, actor_migrate)
        
        # Retrieve previous state on startup
        previous_state = await Actor.get_value('my-crawling-state') or {}
        
        if previous_state.get('processed_urls'):
            print('Resuming from previous state...')
            processed_urls = previous_state['processed_urls']
            current_page = previous_state['current_page']
            session_cookies = previous_state['session_cookies']
        
        # Your Actor logic continues...
```

## Migration Speed Optimization

### Using Actor.reboot()
To expedite migrations, you can use `Actor.reboot()` after saving state:

```javascript
Actor.on('migrating', async () => {
    // Save critical state
    await Actor.setValue('migration-state', {
        progress: currentProgress,
        queue: pendingItems,
        timestamp: Date.now()
    });
    
    console.log('State saved, initiating reboot...');
    
    // Immediately reboot to speed up migration
    await Actor.reboot();
});
```

### Benefits of Actor.reboot()
- **Faster migration**: Reduces migration time
- **Immediate restart**: New container starts quickly
- **State preservation**: Saved state is available immediately
- **User experience**: Minimal disruption to Actor execution

## Advanced State Management

### Comprehensive State Saving
```javascript
// Save comprehensive state information
Actor.on('migrating', async () => {
    const completeState = {
        // Progress tracking
        totalItems: totalItemsToProcess,
        processedItems: processedItemsCount,
        failedItems: failedItemsList,
        
        // Queue management
        pendingUrls: urlQueue.getUrls(),
        completedUrls: completedUrlsList,
        
        // Session information
        loginCredentials: loginState,
        authTokens: currentTokens,
        cookies: browserCookies,
        
        // Configuration
        runtimeConfig: currentConfig,
        userAgent: currentUserAgent,
        proxySettings: proxyConfiguration,
        
        // Timestamps
        startTime: processStartTime,
        lastSaveTime: Date.now(),
        estimatedCompletion: estimatedEndTime,
        
        // Error tracking
        errorCount: totalErrors,
        lastError: lastErrorMessage,
        retryAttempts: currentRetryCount
    };
    
    await Actor.setValue('complete-state', completeState);
});
```

### State Recovery Logic
```javascript
// Comprehensive state recovery
async function recoverState() {
    const savedState = await Actor.getValue('complete-state');
    
    if (!savedState) {
        console.log('No previous state found, starting fresh');
        return initializeNewState();
    }
    
    console.log('Recovering from previous state...');
    
    // Restore progress
    totalItemsToProcess = savedState.totalItems;
    processedItemsCount = savedState.processedItems;
    failedItemsList = savedState.failedItems || [];
    
    // Restore queues
    urlQueue.addUrls(savedState.pendingUrls || []);
    completedUrlsList = savedState.completedUrls || [];
    
    // Restore session
    loginState = savedState.loginCredentials;
    currentTokens = savedState.authTokens;
    browserCookies = savedState.cookies;
    
    // Restore configuration
    currentConfig = savedState.runtimeConfig;
    currentUserAgent = savedState.userAgent;
    proxyConfiguration = savedState.proxySettings;
    
    // Calculate time elapsed
    const elapsed = Date.now() - savedState.lastSaveTime;
    console.log(`Resumed after ${Math.round(elapsed / 1000)} seconds`);
    
    return savedState;
}
```

## Periodic State Saving

### Regular Checkpoints
```javascript
// Save state periodically, not just during migrations
let lastStateSave = 0;
const STATE_SAVE_INTERVAL = 60000; // 1 minute

async function saveStateIfNeeded() {
    const now = Date.now();
    
    if (now - lastStateSave > STATE_SAVE_INTERVAL) {
        await saveCurrentState();
        lastStateSave = now;
    }
}

async function saveCurrentState() {
    const state = {
        progress: getCurrentProgress(),
        timestamp: Date.now(),
        queue: getQueueState(),
        session: getSessionState()
    };
    
    await Actor.setValue('periodic-state', state);
    console.log('State checkpoint saved');
}

// Call during processing loop
while (hasMoreWork()) {
    await processNextItem();
    await saveStateIfNeeded();
}
```

### Event-Driven State Saving
```javascript
// Save state on significant events
async function onSignificantProgress() {
    processedCount++;
    
    // Save state every 100 processed items
    if (processedCount % 100 === 0) {
        await saveCurrentState();
        console.log(`Checkpoint: ${processedCount} items processed`);
    }
}

async function onPageComplete() {
    currentPage++;
    
    // Save state after each page
    await saveCurrentState();
    console.log(`Page ${currentPage} completed, state saved`);
}
```

## Best Practices

### 1. For Short-Running Actors
For Actors that complete in under 10 minutes:
- **Minimal state management**: Usually unnecessary
- **Simple retry logic**: Restart from beginning if needed
- **Focus on speed**: Optimize for quick completion

```javascript
// Simple approach for short Actors
Actor.main(async () => {
    const input = await Actor.getInput();
    
    // Process quickly without complex state management
    const results = await processDataQuickly(input);
    
    await Actor.pushData(results);
});
```

### 2. For Long-Running Actors
For Actors running longer than 10 minutes:
- **Implement state persistence**: Essential for reliability
- **Regular checkpoints**: Save state periodically
- **Comprehensive recovery**: Handle all aspects of state

```javascript
// Comprehensive approach for long Actors
Actor.main(async () => {
    // Set up migration handling
    Actor.on('migrating', handleMigration);
    
    // Recover previous state
    await recoverPreviousState();
    
    // Process with regular state saves
    while (hasMoreWork()) {
        await processNextBatch();
        await saveStateIfNeeded();
    }
});
```

### 3. State Size Optimization
```javascript
// Optimize state size for faster saves
async function saveOptimizedState() {
    const state = {
        // Only save essential data
        processedCount: processedItems.length,
        lastProcessedId: lastItem.id,
        queueSize: remainingItems.length,
        
        // Avoid saving large objects
        // Don't save: fullItemList, completeResults, rawHtml
        
        // Compress arrays if needed
        pendingIds: remainingItems.map(item => item.id),
        
        // Save only necessary config
        essentialConfig: {
            maxPages: config.maxPages,
            outputFormat: config.outputFormat
        }
    };
    
    await Actor.setValue('optimized-state', state);
}
```

### 4. Error Handling in State Management
```javascript
// Handle state save/load errors
async function safeStateSave(state) {
    try {
        await Actor.setValue('actor-state', state);
        console.log('State saved successfully');
    } catch (error) {
        console.error('Failed to save state:', error);
        // Continue execution without failing
    }
}

async function safeStateLoad() {
    try {
        const state = await Actor.getValue('actor-state');
        return state || {};
    } catch (error) {
        console.error('Failed to load state:', error);
        return {}; // Return empty state as fallback
    }
}
```

## When to Use State Persistence

### Essential for:
- **Web crawling**: Long-running crawls with many pages
- **Data processing**: Large dataset transformations
- **API integrations**: Sequential API calls with rate limits
- **Batch operations**: Processing large numbers of items

### Optional for:
- **Quick extractions**: Single-page scraping
- **Simple API calls**: One-time data fetching
- **Fast processing**: Tasks completing in minutes

State persistence is a crucial feature for building robust, reliable Actors that can handle interruptions gracefully and provide consistent results even in the face of platform migrations and server changes.