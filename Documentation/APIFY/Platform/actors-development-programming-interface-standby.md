# Standby Mode | Platform | Apify Documentation

## Overview

Standby mode allows Actors to function like an API server, providing fast response times by keeping the Actor ready in the background to handle incoming HTTP requests. This feature transforms Actors from batch processing tools into persistent, responsive services.

## Key Features

### API-like Behavior
- **Persistent execution**: Actors remain active and waiting for requests
- **Fast response times**: No cold start delays
- **HTTP support**: Supports all HTTP request methods (GET, POST, PUT, DELETE)
- **Flexible input**: Can pass input via query string or request body

### Request Handling
- **Multiple concurrent requests**: Handle multiple requests simultaneously
- **Session persistence**: Maintain state between requests
- **Resource efficiency**: Share resources across multiple requests

## Development Approach

### Getting Started
Developers can create Standby Actors using:
- **Predefined templates**: Available in Apify Console or CLI
- **Configurable settings**: Configure in the Actor's Settings tab
- **Custom implementation**: Build from scratch using HTTP server libraries

### Basic Requirements
- **HTTP server**: Must run an HTTP server listening on a specific port
- **Port configuration**: Use `ACTOR_WEB_SERVER_PORT` to specify port
- **Readiness probe**: Implement a readiness probe endpoint for health checks

## Implementation Examples

### JavaScript with HTTP Module
```javascript
import http from 'http';
import { Actor } from 'apify';

await Actor.init();

const server = http.createServer(async (req, res) => {
    try {
        // Parse request
        const url = new URL(req.url, `http://${req.headers.host}`);
        const method = req.method;
        
        // Handle different endpoints
        if (url.pathname === '/health') {
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ status: 'healthy' }));
            return;
        }
        
        if (url.pathname === '/process' && method === 'POST') {
            // Get request body
            let body = '';
            req.on('data', chunk => {
                body += chunk.toString();
            });
            
            req.on('end', async () => {
                try {
                    const input = JSON.parse(body);
                    const result = await processData(input);
                    
                    res.writeHead(200, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify(result));
                } catch (error) {
                    res.writeHead(500, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ error: error.message }));
                }
            });
            return;
        }
        
        // Default response
        res.writeHead(200, { 'Content-Type': 'text/plain' });
        res.end('Hello from Actor Standby!\n');
        
    } catch (error) {
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: error.message }));
    }
});

const port = Actor.config.get('containerPort') || process.env.ACTOR_WEB_SERVER_PORT || 4321;
server.listen(port, () => {
    console.log(`Standby Actor listening on port ${port}`);
});

async function processData(input) {
    // Your processing logic here
    return {
        processed: true,
        data: input,
        timestamp: new Date().toISOString()
    };
}
```

### JavaScript with Express.js
```javascript
import express from 'express';
import { Actor } from 'apify';

await Actor.init();

const app = express();
app.use(express.json());

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ 
        status: 'healthy',
        mode: process.env.APIFY_META_ORIGIN || 'unknown',
        uptime: process.uptime()
    });
});

// Main processing endpoint
app.post('/process', async (req, res) => {
    try {
        const input = req.body;
        const result = await processData(input);
        
        res.json({
            success: true,
            result: result,
            processedAt: new Date().toISOString()
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Get data endpoint
app.get('/data/:id', async (req, res) => {
    try {
        const id = req.params.id;
        const data = await Actor.getValue(id);
        
        if (!data) {
            return res.status(404).json({ error: 'Data not found' });
        }
        
        res.json(data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

const port = Actor.config.get('containerPort') || process.env.ACTOR_WEB_SERVER_PORT || 4321;
app.listen(port, () => {
    console.log(`Standby Actor listening on port ${port}`);
});
```

### Python with Flask
```python
from flask import Flask, request, jsonify
import asyncio
import os
from apify import Actor

app = Flask(__name__)

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'mode': os.environ.get('APIFY_META_ORIGIN', 'unknown'),
        'uptime': time.time()
    })

@app.route('/process', methods=['POST'])
def process_data():
    try:
        input_data = request.get_json()
        
        # Run async processing
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(process_data_async(input_data))
        
        return jsonify({
            'success': True,
            'result': result,
            'processed_at': time.time()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

async def process_data_async(input_data):
    # Your async processing logic here
    return {
        'processed': True,
        'data': input_data,
        'timestamp': time.time()
    }

if __name__ == '__main__':
    port = int(os.environ.get('ACTOR_WEB_SERVER_PORT', 4321))
    app.run(host='0.0.0.0', port=port, debug=False)
```

## Mode Detection

### Checking Standby vs Standard Mode
```javascript
// Check if running in Standby mode
const isStandbyMode = process.env.APIFY_META_ORIGIN === 'STANDBY';

if (isStandbyMode) {
    console.log('Running in Standby mode');
    // Start HTTP server
    startStandbyServer();
} else {
    console.log('Running in standard mode');
    // Run normal Actor logic
    await runStandardLogic();
}
```

### Environment Variables
```javascript
// Detect execution context
const metaOrigin = process.env.APIFY_META_ORIGIN;
const isStandby = metaOrigin === 'STANDBY';
const isWeb = metaOrigin === 'WEB';
const isAPI = metaOrigin === 'API';

console.log('Execution context:', {
    isStandby,
    isWeb,
    isAPI,
    metaOrigin
});
```

## Advanced Patterns

### Request Queuing
```javascript
const requestQueue = [];
let isProcessing = false;

app.post('/queue', async (req, res) => {
    const requestId = Math.random().toString(36).substring(7);
    
    requestQueue.push({
        id: requestId,
        data: req.body,
        timestamp: Date.now()
    });
    
    res.json({ requestId, queued: true });
    
    if (!isProcessing) {
        processQueue();
    }
});

async function processQueue() {
    isProcessing = true;
    
    while (requestQueue.length > 0) {
        const request = requestQueue.shift();
        
        try {
            const result = await processData(request.data);
            await Actor.setValue(`result_${request.id}`, result);
        } catch (error) {
            await Actor.setValue(`error_${request.id}`, { error: error.message });
        }
    }
    
    isProcessing = false;
}
```

### Session Management
```javascript
const sessions = new Map();

app.post('/session/:sessionId', async (req, res) => {
    const sessionId = req.params.sessionId;
    const input = req.body;
    
    // Get or create session
    if (!sessions.has(sessionId)) {
        sessions.set(sessionId, {
            id: sessionId,
            created: Date.now(),
            data: {},
            requestCount: 0
        });
    }
    
    const session = sessions.get(sessionId);
    session.requestCount++;
    session.lastAccessed = Date.now();
    
    // Process with session context
    const result = await processWithSession(input, session);
    
    res.json({
        result,
        sessionId,
        requestCount: session.requestCount
    });
});
```

## Important Considerations

### Timeouts
- **Total response timeout**: 5 minutes maximum
- **Run selection process timeout**: 2 minutes
- **Keep-alive**: Implement appropriate keep-alive mechanisms

### Resource Management
```javascript
// Monitor memory usage
setInterval(() => {
    const memUsage = process.memoryUsage();
    console.log('Memory usage:', {
        rss: Math.round(memUsage.rss / 1024 / 1024) + 'MB',
        heapUsed: Math.round(memUsage.heapUsed / 1024 / 1024) + 'MB',
        external: Math.round(memUsage.external / 1024 / 1024) + 'MB'
    });
    
    // Implement memory cleanup if needed
    if (memUsage.heapUsed > 100 * 1024 * 1024) { // 100MB
        console.log('High memory usage detected, cleaning up...');
        // Cleanup logic
    }
}, 60000); // Check every minute
```

### Error Handling
```javascript
// Global error handler
process.on('uncaughtException', (error) => {
    console.error('Uncaught exception:', error);
    // Don't exit in Standby mode
});

process.on('unhandledRejection', (reason, promise) => {
    console.error('Unhandled rejection at:', promise, 'reason:', reason);
    // Don't exit in Standby mode
});
```

## Monetization

### Pay-per-event Model
```javascript
app.post('/process', async (req, res) => {
    try {
        // Track usage for billing
        await Actor.setValue('usage_count', 
            (await Actor.getValue('usage_count') || 0) + 1
        );
        
        const result = await processData(req.body);
        res.json(result);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});
```

### Usage Tracking
```javascript
const usageStats = {
    totalRequests: 0,
    successfulRequests: 0,
    failedRequests: 0,
    startTime: Date.now()
};

app.use((req, res, next) => {
    usageStats.totalRequests++;
    
    res.on('finish', () => {
        if (res.statusCode < 400) {
            usageStats.successfulRequests++;
        } else {
            usageStats.failedRequests++;
        }
    });
    
    next();
});
```

## Best Practices

1. **Health Checks**: Always implement health check endpoints
2. **Error Handling**: Implement comprehensive error handling
3. **Resource Monitoring**: Monitor memory and CPU usage
4. **Session Management**: Implement proper session handling for stateful operations
5. **Logging**: Provide detailed logging for debugging
6. **Graceful Shutdown**: Handle shutdown signals properly (though less relevant in Standby mode)

## Use Cases

- **Real-time APIs**: Provide instant data processing capabilities
- **Webhook Handlers**: Process incoming webhook requests
- **Interactive Services**: Create responsive user interfaces
- **Data Processing APIs**: Offer on-demand data transformation
- **Integration Endpoints**: Connect with external services

Standby mode transforms Actors from batch processing tools into responsive, persistent services that can handle real-time requests efficiently.