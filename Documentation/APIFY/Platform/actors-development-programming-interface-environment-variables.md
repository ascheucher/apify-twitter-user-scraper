# Environment Variables | Platform | Apify Documentation

## Overview

Environment variables provide essential context about Actor execution, including system information, configuration settings, and runtime parameters. They enable Actors to adapt their behavior based on the execution environment.

## System Environment Variables

### Core Actor Variables
- **`ACTOR_ID`**: Unique identifier for the Actor
- **`ACTOR_RUN_ID`**: Identifier for the specific Actor run
- **`APIFY_TOKEN`**: API token of the user who started the Actor
- **`ACTOR_MEMORY_MBYTES`**: Memory allocated for the Actor run (in MB)
- **`APIFY_USER_ID`**: ID of the user who started the Actor

### Additional System Variables
- **`ACTOR_WEB_SERVER_URL`**: URL for the Actor's web server (if enabled)
- **`ACTOR_WEB_SERVER_PORT`**: Port for the Actor's web server (default: 4321)
- **`ACTOR_EVENTS_WEBSOCKET_URL`**: WebSocket URL for system events
- **`APIFY_CONTAINER_URL`**: Container URL for HTTP access

## Accessing Environment Variables

### JavaScript
```javascript
// Access environment variables using process.env
console.log('Actor ID:', process.env.ACTOR_ID);
console.log('Run ID:', process.env.ACTOR_RUN_ID);
console.log('User ID:', process.env.APIFY_USER_ID);
console.log('Memory limit:', process.env.ACTOR_MEMORY_MBYTES);

// Check if variable exists
if (process.env.APIFY_TOKEN) {
    console.log('API token is available');
}
```

### Python
```python
import os

# Access environment variables using os.environ
print('Actor ID:', os.environ.get('ACTOR_ID'))
print('Run ID:', os.environ.get('ACTOR_RUN_ID'))
print('User ID:', os.environ.get('APIFY_USER_ID'))
print('Memory limit:', os.environ.get('ACTOR_MEMORY_MBYTES'))

# Check if variable exists
if 'APIFY_TOKEN' in os.environ:
    print('API token is available')
```

## Configuration Class

### JavaScript Configuration
```javascript
const { Actor } = require('apify');

// Access configuration through Actor
const config = Actor.getConfig();
console.log('Token:', config.token);
console.log('User ID:', config.userId);
console.log('Memory limit:', config.memoryMbytes);
```

### Python Configuration
```python
from apify import Actor

# Access configuration through Actor
config = Actor.get_config()
print('Token:', config.token)
print('User ID:', config.user_id)
print('Memory limit:', config.memory_mbytes)
```

## Custom Environment Variables

### Setting in Apify Console
1. Navigate to your Actor's settings
2. Go to Environment Variables section
3. Add custom variables as key-value pairs
4. Mark sensitive variables as "Secret"

### Example Custom Variables
```javascript
// Access custom environment variables
const customApiKey = process.env.CUSTOM_API_KEY;
const debugMode = process.env.DEBUG_MODE === 'true';
const maxRetries = parseInt(process.env.MAX_RETRIES || '3');

console.log('Custom API key:', customApiKey);
console.log('Debug mode:', debugMode);
console.log('Max retries:', maxRetries);
```

## Build-time Environment Variables

### Dockerfile Usage
```dockerfile
FROM apify/actor-node:20

# Define build argument
ARG BUILD_ENV=production

# Set environment variable from build argument
ENV NODE_ENV=${BUILD_ENV}

COPY package*.json ./
RUN npm install --only=prod
COPY . ./
```

### Important Notes
- Build-time variables are used as Docker build arguments
- **Not recommended for secrets** (visible in Docker layers)
- Use runtime environment variables for sensitive data

## Best Practices

### 1. Security
```javascript
// DO: Use environment variables for sensitive data
const apiKey = process.env.API_KEY;

// DON'T: Hardcode sensitive values
const apiKey = 'sk-1234567890abcdef'; // Never do this
```

### 2. Default Values
```javascript
// Provide default values for optional variables
const timeout = parseInt(process.env.TIMEOUT_MS || '30000');
const retries = parseInt(process.env.MAX_RETRIES || '3');
const debugMode = process.env.DEBUG === 'true';
```

### 3. Type Conversion
```javascript
// Convert string environment variables to appropriate types
const port = parseInt(process.env.PORT || '3000');
const enableLogging = process.env.ENABLE_LOGGING === 'true';
const thresholds = JSON.parse(process.env.THRESHOLDS || '{}');
```

### 4. Validation
```javascript
// Validate required environment variables
function validateEnvironment() {
    const required = ['ACTOR_ID', 'APIFY_TOKEN'];
    const missing = required.filter(key => !process.env[key]);
    
    if (missing.length > 0) {
        throw new Error(`Missing required environment variables: ${missing.join(', ')}`);
    }
}

validateEnvironment();
```

## Common Patterns

### Configuration Object
```javascript
// Create configuration object from environment variables
const config = {
    actorId: process.env.ACTOR_ID,
    runId: process.env.ACTOR_RUN_ID,
    token: process.env.APIFY_TOKEN,
    memoryMB: parseInt(process.env.ACTOR_MEMORY_MBYTES || '1024'),
    debug: process.env.DEBUG === 'true',
    maxRetries: parseInt(process.env.MAX_RETRIES || '3'),
    timeout: parseInt(process.env.TIMEOUT_MS || '30000')
};
```

### Environment-specific Behavior
```javascript
// Adapt behavior based on environment
const isProd = process.env.NODE_ENV === 'production';
const logLevel = isProd ? 'error' : 'debug';
const maxConcurrency = isProd ? 10 : 3;

console.log(`Running in ${process.env.NODE_ENV} mode`);
```

## Debugging Environment Variables

### List All Variables
```javascript
// Log all environment variables (be careful with sensitive data)
console.log('Environment variables:');
Object.keys(process.env)
    .filter(key => key.startsWith('ACTOR_') || key.startsWith('APIFY_'))
    .forEach(key => {
        console.log(`${key}: ${process.env[key]}`);
    });
```

### Check Variable Availability
```javascript
// Check if running on Apify platform
const isApifyPlatform = !!process.env.APIFY_TOKEN;
console.log('Running on Apify platform:', isApifyPlatform);

// Check if web server is enabled
const hasWebServer = !!process.env.ACTOR_WEB_SERVER_URL;
console.log('Web server enabled:', hasWebServer);
```

Environment variables provide a flexible and secure way to configure Actors for different execution contexts while maintaining separation between code and configuration.