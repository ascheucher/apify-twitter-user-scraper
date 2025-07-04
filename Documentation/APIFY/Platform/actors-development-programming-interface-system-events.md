# System Events | Platform | Apify Documentation

## Overview

System events are notifications sent to Actors about various platform conditions, helping developers manage Actor behavior and resources effectively. Events enable Actors to respond dynamically to environmental changes and platform requirements.

## Available System Events

### 1. `cpuInfo` Event
- **Purpose**: Indicates CPU resource usage
- **Payload**: `{ isCpuOverloaded: Boolean }`
- **Frequency**: Emitted approximately every second
- **Usage**: Monitor and respond to CPU load

### 2. `migrating` Event
- **Purpose**: Signals impending migration to another worker server
- **Payload**: `{ timeRemainingSecs: Float }`
- **Usage**: Prepare for container migration

### 3. `aborting` Event
- **Purpose**: Triggered when a user initiates a graceful Actor run abort
- **Payload**: No payload
- **Usage**: Perform cleanup before termination

### 4. `persistState` Event
- **Purpose**: Notifies SDK components to save their state
- **Payload**: `{ isMigrating: Boolean }`
- **Default interval**: 60 seconds
- **Usage**: Ensure data persistence

## Event Transmission

### WebSocket Connection
Events are received via WebSocket with the connection address specified by:
- **Environment variable**: `ACTOR_EVENTS_WEBSOCKET_URL`
- **Format**: JSON messages

### Event Message Format
```json
{
    "name": "String",
    "createdAt": "String",
    "data": "Object"
}
```

## Event Handling

### JavaScript Example
```javascript
import { Actor } from 'apify';

await Actor.init();

// Handle CPU overload
Actor.on('cpuInfo', (data) => {
    if (data.isCpuOverloaded) {
        console.log('CPU is overloaded, slowing down...');
        // Implement throttling logic
        setTimeout(() => {
            // Resume normal operation
        }, 1000);
    }
});

// Handle migration
Actor.on('migrating', (data) => {
    console.log(`Migration in ${data.timeRemainingSecs} seconds`);
    // Save critical state
    saveCriticalState();
});

// Handle abort
Actor.on('aborting', () => {
    console.log('Actor is being aborted, cleaning up...');
    // Perform cleanup
    cleanup();
});

// Handle state persistence
Actor.on('persistState', (data) => {
    console.log('Persisting state...');
    if (data.isMigrating) {
        console.log('Migration-triggered state persistence');
    }
    // Save current state
    saveCurrentState();
});

await Actor.exit();
```

### Python Example
```python
from apify import Actor
from apify_shared.consts import ActorEventTypes

async def handle_cpu_info(data):
    if data.get('isCpuOverloaded'):
        print('CPU is overloaded, slowing down...')
        # Implement throttling logic
        await asyncio.sleep(1)

async def handle_migrating(data):
    print(f"Migration in {data['timeRemainingSecs']} seconds")
    # Save critical state
    await save_critical_state()

async def handle_aborting(data):
    print('Actor is being aborted, cleaning up...')
    # Perform cleanup
    await cleanup()

async def handle_persist_state(data):
    print('Persisting state...')
    if data.get('isMigrating'):
        print('Migration-triggered state persistence')
    # Save current state
    await save_current_state()

async def main():
    async with Actor:
        # Register event handlers
        Actor.on(ActorEventTypes.CPU_INFO, handle_cpu_info)
        Actor.on(ActorEventTypes.MIGRATING, handle_migrating)
        Actor.on(ActorEventTypes.ABORTING, handle_aborting)
        Actor.on(ActorEventTypes.PERSIST_STATE, handle_persist_state)
        
        # Your Actor logic here
        await run_actor_logic()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

## Event Handling Patterns

### CPU Load Management
```javascript
let processingSlowdown = false;

Actor.on('cpuInfo', (data) => {
    if (data.isCpuOverloaded && !processingSlowdown) {
        processingSlowdown = true;
        console.log('Enabling CPU throttling');
        
        // Reduce concurrent operations
        reduceParallelism();
        
        // Add delays between operations
        setTimeout(() => {
            processingSlowdown = false;
            console.log('CPU load normalized, resuming normal speed');
        }, 5000);
    }
});

async function processBatch(items) {
    for (const item of items) {
        await processItem(item);
        
        // Add delay if CPU is overloaded
        if (processingSlowdown) {
            await new Promise(resolve => setTimeout(resolve, 100));
        }
    }
}
```

### Migration Handling
```javascript
let isMigrating = false;

Actor.on('migrating', async (data) => {
    isMigrating = true;
    console.log(`Migration starting in ${data.timeRemainingSecs} seconds`);
    
    // Save current progress
    await Actor.setValue('migration_checkpoint', {
        processedItems: currentProgress,
        timestamp: new Date().toISOString(),
        remainingWork: pendingItems
    });
    
    // Finish current batch if time permits
    if (data.timeRemainingSecs > 10) {
        await finishCurrentBatch();
    }
});

// Check migration status during processing
async function processWithMigrationCheck() {
    while (hasMoreWork() && !isMigrating) {
        await processNextItem();
    }
}
```

### Graceful Shutdown
```javascript
let isAborting = false;

Actor.on('aborting', async () => {
    isAborting = true;
    console.log('Graceful shutdown initiated');
    
    // Stop accepting new work
    stopNewWork();
    
    // Save current state
    await Actor.setValue('shutdown_state', {
        completedItems: completed,
        partialResults: partial,
        shutdownTime: new Date().toISOString()
    });
    
    // Clean up resources
    await cleanup();
    
    console.log('Graceful shutdown completed');
});

// Check abort status during processing
async function processWithAbortCheck() {
    while (hasMoreWork() && !isAborting) {
        await processNextItem();
    }
}
```

### State Persistence
```javascript
let lastStateUpdate = 0;

Actor.on('persistState', async (data) => {
    const now = Date.now();
    
    // Avoid too frequent state saves
    if (now - lastStateUpdate < 30000) {
        return;
    }
    
    console.log('Saving actor state...');
    
    await Actor.setValue('actor_state', {
        processedCount: processedItems,
        currentPhase: currentPhase,
        queuedItems: queuedWork,
        statistics: gatherStatistics(),
        timestamp: new Date().toISOString(),
        isMigrating: data.isMigrating
    });
    
    lastStateUpdate = now;
});
```

## Best Practices

### 1. Event Handler Registration
```javascript
// Register event handlers early
await Actor.init();

// Register all event handlers before starting main logic
Actor.on('cpuInfo', handleCpuInfo);
Actor.on('migrating', handleMigrating);
Actor.on('aborting', handleAborting);
Actor.on('persistState', handlePersistState);

// Start main Actor logic
await runMainLogic();
```

### 2. Error Handling in Event Handlers
```javascript
Actor.on('cpuInfo', async (data) => {
    try {
        if (data.isCpuOverloaded) {
            await handleCpuOverload();
        }
    } catch (error) {
        console.error('Error in cpuInfo handler:', error);
        // Don't let event handler errors crash the Actor
    }
});
```

### 3. Asynchronous Event Handling
```javascript
Actor.on('persistState', async (data) => {
    // Use async/await for asynchronous operations
    try {
        await saveStateToStorage();
        await updateProgress();
    } catch (error) {
        console.error('Failed to persist state:', error);
    }
});
```

### 4. Resource Management
```javascript
// Keep track of resources that need cleanup
const openConnections = new Set();
const runningTasks = new Set();

Actor.on('aborting', async () => {
    // Clean up all resources
    for (const connection of openConnections) {
        await connection.close();
    }
    
    for (const task of runningTasks) {
        await task.cancel();
    }
});
```

## Benefits of System Events

1. **Dynamic Resource Management**: Respond to CPU load and optimize performance
2. **Graceful Migration Handling**: Prepare for container migrations without data loss
3. **State Preservation**: Ensure critical data is saved regularly
4. **Responsive Actor Development**: Build Actors that adapt to platform conditions

System events enable the development of robust, efficient Actors that can handle the dynamic nature of cloud execution environments while maintaining data integrity and optimal performance.