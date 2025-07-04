# Container Web Server | Platform | Apify Documentation

## Overview

The container web server feature enables HTTP access to a web server running inside the Actor's Docker container. This allows Actors to function as APIs or provide web interfaces for interaction during execution.

## Container URL

Each Actor run receives a unique URL for HTTP access:
- **Example**: `kmdo7wpzlshygi.runs.apify.net`
- **Format**: `{run-id}.runs.apify.net`

### Finding the Container URL

The container URL can be found in:
1. **Web application**: Run details page
2. **API**: Run object response
3. **Environment variable**: `ACTOR_WEB_SERVER_URL`

## Web Server Configuration

### Port Configuration
- **Default port**: 4321
- **Environment variable**: `ACTOR_WEB_SERVER_PORT`
- **Custom port**: Can be set in Actor version configuration

### Server Requirements
- Must listen on the port specified by `ACTOR_WEB_SERVER_PORT`
- Must bind to all interfaces (`0.0.0.0`) for external access
- Should handle HTTP requests appropriately

## Implementation Examples

### JavaScript with Express.js

```javascript
import express from 'express';
import { Actor } from 'apify';

const app = express();
const port = process.env.ACTOR_WEB_SERVER_PORT || 4321;

// Middleware for JSON parsing
app.use(express.json());

// Basic route
app.get('/', (req, res) => {
    res.json({
        message: 'Hello world from Express app!',
        timestamp: new Date().toISOString(),
        url: process.env.ACTOR_WEB_SERVER_URL
    });
});

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        uptime: process.uptime(),
        memory: process.memoryUsage()
    });
});

// API endpoint for Actor functionality
app.post('/process', async (req, res) => {
    try {
        const { data } = req.body;
        
        // Process data using Actor SDK
        const result = await processData(data);
        
        res.json({
            success: true,
            result: result
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Start server
app.listen(port, '0.0.0.0', () => {
    console.log(`Web server is listening at ${process.env.ACTOR_WEB_SERVER_URL}!`);
});

// Actor main logic
Actor.main(async () => {
    console.log('Actor started with web server');
    
    // Keep Actor running while server is active
    process.on('SIGINT', () => {
        console.log('Shutting down gracefully...');
        process.exit(0);
    });
});
```

### Python with Flask

```python
from flask import Flask, request, jsonify
import os
from apify import Actor
import threading
import time

app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify({
        'message': 'Hello world from Flask app!',
        'timestamp': time.time(),
        'url': os.environ.get('ACTOR_WEB_SERVER_URL')
    })

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'uptime': time.time()
    })

@app.route('/process', methods=['POST'])
def process_data():
    try:
        data = request.get_json()
        
        # Process data using Actor SDK
        result = process_data_function(data)
        
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def run_flask_server():
    port = int(os.environ.get('ACTOR_WEB_SERVER_PORT', 4321))
    app.run(host='0.0.0.0', port=port, debug=False)

async def main():
    async with Actor:
        print('Actor started with web server')
        
        # Start Flask server in a separate thread
        server_thread = threading.Thread(target=run_flask_server)
        server_thread.daemon = True
        server_thread.start()
        
        # Keep Actor running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print('Shutting down gracefully...')

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

## Advanced Use Cases

### API Gateway Pattern
```javascript
const express = require('express');
const { Actor } = require('apify');

const app = express();
app.use(express.json());

// Queue for handling requests
const requestQueue = [];
let isProcessing = false;

// API endpoint that queues requests
app.post('/api/scrape', async (req, res) => {
    const requestId = Math.random().toString(36).substring(7);
    
    requestQueue.push({
        id: requestId,
        data: req.body,
        resolve: (result) => res.json(result),
        reject: (error) => res.status(500).json({ error: error.message })
    });
    
    // Process queue if not already processing
    if (!isProcessing) {
        processQueue();
    }
});

async function processQueue() {
    isProcessing = true;
    
    while (requestQueue.length > 0) {
        const request = requestQueue.shift();
        
        try {
            const result = await scrapeData(request.data);
            request.resolve(result);
        } catch (error) {
            request.reject(error);
        }
    }
    
    isProcessing = false;
}

app.listen(process.env.ACTOR_WEB_SERVER_PORT, '0.0.0.0');
```

### Real-time Progress Updates
```javascript
const express = require('express');
const { Actor } = require('apify');

const app = express();
let currentProgress = { status: 'idle', progress: 0 };

// Get current progress
app.get('/progress', (req, res) => {
    res.json(currentProgress);
});

// Start processing
app.post('/start', async (req, res) => {
    res.json({ message: 'Processing started' });
    
    // Update progress during processing
    for (let i = 0; i <= 100; i++) {
        currentProgress = {
            status: 'processing',
            progress: i,
            message: `Processing item ${i}/100`
        };
        
        await new Promise(resolve => setTimeout(resolve, 100));
    }
    
    currentProgress = { status: 'completed', progress: 100 };
});

app.listen(process.env.ACTOR_WEB_SERVER_PORT, '0.0.0.0');
```

## Integration with Actor Storage

### Accessing Actor Data
```javascript
app.get('/results', async (req, res) => {
    try {
        // Get data from Actor's default dataset
        const dataset = await Actor.openDataset();
        const { items } = await dataset.getData();
        
        res.json({
            count: items.length,
            data: items
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.get('/logs', async (req, res) => {
    try {
        // Get log data from key-value store
        const logs = await Actor.getValue('logs');
        res.json(logs || []);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});
```

## Best Practices

### 1. Error Handling
```javascript
// Global error handler
app.use((error, req, res, next) => {
    console.error('Server error:', error);
    res.status(500).json({
        error: 'Internal server error',
        timestamp: new Date().toISOString()
    });
});

// Async error wrapper
const asyncHandler = (fn) => (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next);
};

app.get('/data', asyncHandler(async (req, res) => {
    const data = await fetchData();
    res.json(data);
}));
```

### 2. Security Considerations
```javascript
// Basic security headers
app.use((req, res, next) => {
    res.header('X-Content-Type-Options', 'nosniff');
    res.header('X-Frame-Options', 'DENY');
    res.header('X-XSS-Protection', '1; mode=block');
    next();
});

// Rate limiting (simple implementation)
const requestCounts = new Map();

app.use((req, res, next) => {
    const ip = req.ip || req.connection.remoteAddress;
    const count = requestCounts.get(ip) || 0;
    
    if (count > 100) {
        return res.status(429).json({ error: 'Rate limit exceeded' });
    }
    
    requestCounts.set(ip, count + 1);
    setTimeout(() => requestCounts.delete(ip), 60000); // Reset after 1 minute
    
    next();
});
```

### 3. Graceful Shutdown
```javascript
let server;

Actor.main(async () => {
    server = app.listen(process.env.ACTOR_WEB_SERVER_PORT, '0.0.0.0', () => {
        console.log(`Server running at ${process.env.ACTOR_WEB_SERVER_URL}`);
    });
    
    // Graceful shutdown
    process.on('SIGINT', () => {
        console.log('Shutting down server...');
        server.close(() => {
            console.log('Server closed');
            process.exit(0);
        });
    });
});
```

## Use Cases

1. **API Endpoints**: Create REST APIs for data processing
2. **Interactive Dashboards**: Provide web interfaces for monitoring
3. **Webhook Handlers**: Receive and process webhook requests
4. **Real-time Updates**: Stream progress and status updates
5. **Data Visualization**: Display results in web formats

## Important Notes

- **Persistent API Access**: For consistent API access, consider using [Actor Standby mode](/platform/actors/development/programming-interface/standby)
- **Resource Management**: Web servers consume additional memory and CPU
- **Security**: Implement appropriate security measures for public endpoints
- **Monitoring**: Include health checks and monitoring endpoints

The container web server feature transforms Actors from simple batch processors into interactive, API-driven applications that can handle real-time requests and provide dynamic responses.