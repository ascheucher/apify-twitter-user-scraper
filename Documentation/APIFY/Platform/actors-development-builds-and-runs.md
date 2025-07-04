# Builds and Runs | Platform | Apify Documentation

## Overview

Understanding builds and runs is crucial for effective use of the Apify platform. These concepts form the foundation of how Actors are created, deployed, and executed.

## Key Concepts

### Build
A **build** is a Docker image containing an Actor's source code and dependencies. It represents a specific version of your Actor that can be executed.

### Run
A **run** is a build started with specific input parameters. It represents an actual execution instance of your Actor.

## Build Process

### What is a Build?
- **Docker image**: Containerized version of your Actor
- **Source code**: Your Actor's source code and dependencies
- **Environment**: Pre-configured runtime environment
- **Versioning**: Each build has a unique version identifier

### Build Creation
Builds are created when:
- **Code deployment**: New code is pushed to the Actor
- **Manual trigger**: Manually triggered through console or API
- **Scheduled builds**: Automated builds via CI/CD pipelines
- **Dependency updates**: When base images or dependencies change

### Build Statuses
- **READY**: Build completed successfully and ready for execution
- **RUNNING**: Build process is currently in progress
- **FAILED**: Build process failed due to errors
- **ABORTED**: Build was manually cancelled

## Run Process

### What is a Run?
- **Execution instance**: A specific execution of an Actor build
- **Input parameters**: Configured with specific input data
- **Resource allocation**: Assigned memory, CPU, and time limits
- **Storage**: Connected to datasets, key-value stores, and request queues

### Run Creation
Runs are created when:
- **Manual execution**: Started from console or API
- **Scheduled execution**: Triggered by schedules
- **Task execution**: Executed as part of Actor tasks
- **API calls**: Initiated via API requests

## Lifecycle Statuses

### Initial Status
- **READY**: Initial state, not yet allocated to a worker

### Transitional Statuses
- **RUNNING**: Currently executing on a worker
- **TIMING-OUT**: Currently timing out due to time limit
- **ABORTING**: Being manually aborted by user

### Terminal Statuses
- **SUCCEEDED**: Finished successfully (exit code 0)
- **FAILED**: Run failed (non-zero exit code)
- **TIMED-OUT**: Timed out completely
- **ABORTED**: Manually stopped by user

## Status Lifecycle Flow

```
READY → RUNNING → SUCCEEDED
              ↓
              FAILED
              ↓
              TIMING-OUT → TIMED-OUT
              ↓
              ABORTING → ABORTED
```

## Build Management

### Creating Builds
```bash
# Using Apify CLI
apify push --build-tag=latest

# Using API
curl -X POST "https://api.apify.com/v2/acts/YOUR_ACTOR_ID/builds" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tag": "latest"}'
```

### Build Configuration
```json
{
  "tag": "latest",
  "useCache": true,
  "betaPackages": false,
  "options": {
    "memoryMbytes": 1024,
    "diskMbytes": 2048
  }
}
```

### Managing Multiple Builds
```javascript
// List all builds
const builds = await apifyClient.actor('YOUR_ACTOR_ID').builds().list();

// Get specific build
const build = await apifyClient.actor('YOUR_ACTOR_ID').build('BUILD_ID').get();

// Delete old builds
await apifyClient.actor('YOUR_ACTOR_ID').build('BUILD_ID').delete();
```

## Run Management

### Starting Runs
```bash
# Using Apify CLI
apify run --input='{"url": "https://example.com"}'

# Using API
curl -X POST "https://api.apify.com/v2/acts/YOUR_ACTOR_ID/runs" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {"url": "https://example.com"},
    "options": {
      "build": "latest",
      "memoryMbytes": 1024,
      "timeoutSecs": 3600
    }
  }'
```

### Run Configuration
```json
{
  "input": {
    "url": "https://example.com",
    "maxPages": 100
  },
  "options": {
    "build": "latest",
    "memoryMbytes": 2048,
    "timeoutSecs": 7200,
    "metamorph": false
  }
}
```

### Monitoring Runs
```javascript
// Get run status
const run = await apifyClient.actor('YOUR_ACTOR_ID').run('RUN_ID').get();

// Wait for run completion
const run = await apifyClient.actor('YOUR_ACTOR_ID').run('RUN_ID').waitForFinish();

// Get run log
const log = await apifyClient.actor('YOUR_ACTOR_ID').run('RUN_ID').log().get();
```

## Resource Management

### Memory Allocation
```javascript
// Configure memory for builds and runs
const runOptions = {
  memoryMbytes: 4096,  // 4GB memory
  timeoutSecs: 3600,   // 1 hour timeout
  build: 'latest'
};
```

### Storage Management
```javascript
// Access run storage
const dataset = await apifyClient.actor('YOUR_ACTOR_ID').run('RUN_ID').dataset().get();
const keyValueStore = await apifyClient.actor('YOUR_ACTOR_ID').run('RUN_ID').keyValueStore().get();
```

## Best Practices

### 1. Build Optimization
```dockerfile
# Optimize Docker builds
FROM apify/actor-node:20

# Copy package files first for better caching
COPY package*.json ./
RUN npm ci --only=production

# Copy source code after dependencies
COPY . ./

# Use specific base image versions
# FROM apify/actor-node:20.1.0  # Specific version
```

### 2. Run Configuration
```javascript
// Optimize run settings
const runOptions = {
  memoryMbytes: 1024,        // Start with minimal memory
  timeoutSecs: 1800,         // 30 minutes timeout
  build: 'latest',           // Use latest stable build
  maxItems: 1000             // Limit output size
};
```

### 3. Error Handling
```javascript
// Handle run failures
try {
  const run = await apifyClient.actor('YOUR_ACTOR_ID').run('RUN_ID').get();
  
  if (run.status === 'FAILED') {
    console.error('Run failed:', run.statusMessage);
    // Handle failure
  }
} catch (error) {
  console.error('Error getting run:', error);
}
```

### 4. Resource Monitoring
```javascript
// Monitor resource usage
const run = await apifyClient.actor('YOUR_ACTOR_ID').run('RUN_ID').get();

console.log('Resource usage:', {
  memoryUsed: run.stats.memoryUsageBytes,
  cpuUsage: run.stats.cpuUsagePercent,
  duration: run.stats.runTimeSecs
});
```

## Advanced Features

### Build Caching
```json
{
  "tag": "latest",
  "useCache": true,
  "options": {
    "buildTimeoutSecs": 300
  }
}
```

### Run Metamorphosis
```javascript
// Transform runs using metamorph
await Actor.metamorph('NEW_ACTOR_ID', newInput, {
  build: 'latest',
  memoryMbytes: 2048
});
```

### Scheduled Builds
```javascript
// Schedule regular builds
const schedule = await apifyClient.schedules().create({
  name: 'Nightly Build',
  cronExpression: '0 2 * * *',  // 2 AM daily
  actions: [{
    type: 'BUILD_ACTOR',
    actorId: 'YOUR_ACTOR_ID',
    options: {
      tag: 'nightly'
    }
  }]
});
```

## Troubleshooting

### Common Build Issues
```bash
# Check build logs
apify logs --build-id=BUILD_ID

# Debug build failures
docker build -t test-actor .
docker run test-actor
```

### Common Run Issues
```bash
# Check run logs
apify logs --run-id=RUN_ID

# Debug run failures
apify run --input='{"debug": true}'
```

### Performance Issues
```javascript
// Monitor performance metrics
const run = await apifyClient.actor('YOUR_ACTOR_ID').run('RUN_ID').get();

if (run.stats.memoryUsageBytes > 0.9 * run.options.memoryMbytes * 1024 * 1024) {
  console.warn('Memory usage is high, consider increasing memory allocation');
}
```

## Monitoring and Alerting

### Build Monitoring
```javascript
// Monitor build status
const build = await apifyClient.actor('YOUR_ACTOR_ID').build('BUILD_ID').get();

if (build.status === 'FAILED') {
  // Send alert
  await sendAlert(`Build ${build.id} failed: ${build.statusMessage}`);
}
```

### Run Monitoring
```javascript
// Monitor run performance
const run = await apifyClient.actor('YOUR_ACTOR_ID').run('RUN_ID').get();

const metrics = {
  duration: run.stats.runTimeSecs,
  memoryPeak: run.stats.memoryUsageBytes,
  datasetItems: run.stats.datasetItems
};

await logMetrics(metrics);
```

## API Integration

### Build API
```javascript
// Create build
const build = await apifyClient.actor('YOUR_ACTOR_ID').builds().create({
  tag: 'latest',
  useCache: true
});

// List builds
const builds = await apifyClient.actor('YOUR_ACTOR_ID').builds().list();

// Get build details
const build = await apifyClient.actor('YOUR_ACTOR_ID').build('BUILD_ID').get();
```

### Run API
```javascript
// Create run
const run = await apifyClient.actor('YOUR_ACTOR_ID').runs().create({
  input: { url: 'https://example.com' },
  options: { memoryMbytes: 1024 }
});

// List runs
const runs = await apifyClient.actor('YOUR_ACTOR_ID').runs().list();

// Get run details
const run = await apifyClient.actor('YOUR_ACTOR_ID').run('RUN_ID').get();
```

Understanding builds and runs is essential for effective Actor management, enabling you to create reliable, scalable automation solutions on the Apify platform.