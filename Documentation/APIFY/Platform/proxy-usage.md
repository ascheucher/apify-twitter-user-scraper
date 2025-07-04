# Proxy Usage | Platform | Apify Documentation

## Overview

Apify Proxy provides rotating IP addresses for web scraping and automation, helping you avoid rate limiting and IP blocking. The proxy supports both datacenter and residential IP addresses with advanced features for session management and geographic targeting.

## Connection Methods

### 1. External Connection
For connecting from outside the Apify platform:

**Connection Details**:
- **Hostname**: `proxy.apify.com`
- **Port**: `8000`
- **Protocol**: HTTP proxy protocol
- **Requirements**: Paid Apify plan

**Connection String Format**:
```
http://<username>:<password>@proxy.apify.com:8000
```

### 2. Connection from Actors
For Actors running on the Apify platform:

**Environment Variables**:
- `APIFY_PROXY_HOSTNAME`: Proxy server hostname
- `APIFY_PROXY_PORT`: Proxy server port
- `APIFY_PROXY_PASSWORD`: Authentication password

**Recommended Approach**: Use built-in proxy configuration tools in Apify SDK

## Username Parameters

The username field supports multiple parameters for controlling proxy behavior:

### Basic Format
```
groups-<GROUP_NAME>,session-<SESSION_ID>,country-<COUNTRY_CODE>
```

### Groups Parameter
Specify proxy server groups:
- **`SHADER`**: Datacenter proxies (default)
- **`RESIDENTIAL`**: Residential proxies
- **`GOOGLE_SERP`**: Google SERP proxies

```javascript
// Example usernames
const username = 'groups-RESIDENTIAL';
const username = 'groups-SHADER,session-my-session';
const username = 'groups-GOOGLE_SERP,country-US';
```

### Session Parameter
Control IP address persistence:
- **Session ID**: Custom identifier for IP persistence
- **Behavior**: Same IP returned for same session
- **Duration**: Varies by proxy type

```javascript
// Consistent IP for a session
const username = 'session-user123-crawler';
const username = 'groups-RESIDENTIAL,session-mobile-scraper';
```

### Country Parameter
Filter proxy servers by geographic location:
- **ISO country codes**: 2-letter country codes (US, GB, DE, etc.)
- **Geographic targeting**: Access geo-restricted content
- **Compliance**: Meet data locality requirements

```javascript
// US-based proxies
const username = 'country-US';
const username = 'groups-RESIDENTIAL,country-GB,session-uk-session';
```

## IP Address Rotation

### Rotation Behavior
IP rotation differs between connection types:

#### Browser Requests
- **Automatic rotation**: New IP for each request by default
- **Session control**: Use sessions to maintain same IP
- **Smart rotation**: Optimized for browser-like behavior

#### HTTP Requests
- **Per-request rotation**: Different IP for each HTTP request
- **Session persistence**: Maintain IP within session
- **Load balancing**: Distributed across available IPs

### Session Persistence Duration

#### Datacenter Proxies
- **Duration**: 26 hours maximum
- **Stability**: Highly stable connections
- **Performance**: Fast response times

#### Residential Proxies
- **Duration**: 1 minute maximum
- **Refresh**: Frequent IP changes
- **Authenticity**: Real residential IPs

## SDK Integration

### JavaScript SDK
```javascript
const { Actor } = require('apify');
const { PuppeteerCrawler } = require('crawlee');

Actor.main(async () => {
    const proxyConfiguration = await Actor.createProxyConfiguration({
        groups: ['RESIDENTIAL'],
        countryCode: 'US'
    });
    
    const crawler = new PuppeteerCrawler({
        proxyConfiguration,
        requestHandler: async ({ page, request }) => {
            // Your scraping logic here
            const content = await page.content();
            await Actor.pushData({
                url: request.url,
                content: content.length
            });
        }
    });
    
    await crawler.run(['https://example.com']);
});
```

### Python SDK
```python
from apify import Actor
from apify_client import ApifyClient

async def main():
    async with Actor:
        proxy_config = await Actor.create_proxy_configuration(
            groups=['RESIDENTIAL'],
            country_code='US'
        )
        
        # Use proxy with your scraping logic
        async with aiohttp.ClientSession() as session:
            proxy_url = proxy_config.new_url()
            async with session.get(
                'https://example.com',
                proxy=proxy_url
            ) as response:
                content = await response.text()
                await Actor.push_data({
                    'url': str(response.url),
                    'status': response.status
                })
```

### Manual Proxy Configuration
```javascript
// Manual proxy setup
const proxyUrl = `http://groups-RESIDENTIAL,session-${sessionId}:${password}@proxy.apify.com:8000`;

// With Puppeteer
const browser = await puppeteer.launch({
    args: [`--proxy-server=${proxyUrl}`]
});

// With Playwright
const browser = await playwright.chromium.launch({
    proxy: {
        server: 'http://proxy.apify.com:8000',
        username: `groups-RESIDENTIAL,session-${sessionId}`,
        password: password
    }
});

// With axios
const response = await axios.get('https://example.com', {
    proxy: {
        protocol: 'http',
        host: 'proxy.apify.com',
        port: 8000,
        auth: {
            username: 'groups-RESIDENTIAL',
            password: password
        }
    }
});
```

## Session Management

### Creating Sessions
```javascript
// Generate unique session IDs
const sessionId = `session-${Math.random().toString(36).substring(2)}`;
const username = `groups-RESIDENTIAL,session-${sessionId}`;

// Use session across multiple requests
const makeRequest = async (url) => {
    const proxyUrl = `http://${username}:${password}@proxy.apify.com:8000`;
    return await fetch(url, { proxy: proxyUrl });
};

// Maintain session across requests
await makeRequest('https://example.com/login');
await makeRequest('https://example.com/dashboard');
await makeRequest('https://example.com/data');
```

### Session Rotation
```javascript
// Rotate sessions for different tasks
const sessions = ['user1', 'user2', 'user3'];
let currentSessionIndex = 0;

const getNextSession = () => {
    const session = sessions[currentSessionIndex];
    currentSessionIndex = (currentSessionIndex + 1) % sessions.length;
    return `groups-RESIDENTIAL,session-${session}`;
};

// Use different sessions for parallel requests
const requests = urls.map(async (url, index) => {
    const username = getNextSession();
    const proxyUrl = `http://${username}:${password}@proxy.apify.com:8000`;
    return await fetch(url, { proxy: proxyUrl });
});

await Promise.all(requests);
```

## Troubleshooting

### Connection Testing
```javascript
// Test proxy connection
const testProxy = async () => {
    try {
        const response = await fetch('http://proxy.apify.com/', {
            method: 'GET',
            headers: {
                'Proxy-Authorization': `Basic ${Buffer.from(`${username}:${password}`).toString('base64')}`
            }
        });
        
        if (response.ok) {
            console.log('Proxy connection successful');
        } else {
            console.error('Proxy connection failed:', response.status);
        }
    } catch (error) {
        console.error('Proxy test error:', error);
    }
};
```

### Verify Proxied Requests
```javascript
// Check if requests are properly proxied
const verifyProxy = async () => {
    const response = await fetch('https://api.apify.com/v2/browser-info/', {
        proxy: proxyUrl
    });
    
    const info = await response.json();
    console.log('IP Address:', info.clientIp);
    console.log('User Agent:', info.headers['user-agent']);
    console.log('Location:', info.geoLocation);
};
```

### Custom Error Codes
Apify Proxy returns custom error codes (590-599) for detailed diagnostics:

- **590**: Proxy authentication failed
- **591**: Proxy group not found or access denied
- **592**: Session expired or invalid
- **593**: Country not available for group
- **594**: Request blocked by target website
- **595**: Proxy server temporarily unavailable
- **596**: Rate limit exceeded
- **597**: Invalid request format
- **598**: Proxy server error
- **599**: Unknown proxy error

```javascript
// Handle proxy errors
const handleProxyError = (statusCode) => {
    switch (statusCode) {
        case 590:
            console.error('Proxy authentication failed - check credentials');
            break;
        case 591:
            console.error('Proxy group not found - check group name');
            break;
        case 592:
            console.error('Session expired - create new session');
            break;
        case 593:
            console.error('Country not available - try different country');
            break;
        default:
            console.error(`Proxy error: ${statusCode}`);
    }
};
```

## Advanced Features

### SessionPool Integration
```javascript
const { SessionPool } = require('crawlee');

// Automatic session management
const sessionPool = new SessionPool({
    maxPoolSize: 50,
    sessionOptions: {
        maxAgeSecs: 1800, // 30 minutes
        maxUsageCount: 100
    },
    createProxyConfiguration: () => Actor.createProxyConfiguration({
        groups: ['RESIDENTIAL']
    })
});

// Use session from pool
const session = await sessionPool.getSession();
const proxyUrl = session.proxyConfiguration.newUrl();
```

### Geographic Rotation
```javascript
// Rotate between different countries
const countries = ['US', 'GB', 'DE', 'FR', 'CA'];
let countryIndex = 0;

const getProxyForCountry = () => {
    const country = countries[countryIndex];
    countryIndex = (countryIndex + 1) % countries.length;
    
    return `groups-RESIDENTIAL,country-${country},session-${Date.now()}`;
};
```

### Smart Retry Logic
```javascript
// Implement smart retry with proxy rotation
const fetchWithRetry = async (url, maxRetries = 3) => {
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
        try {
            const sessionId = `retry-${attempt}-${Date.now()}`;
            const username = `groups-RESIDENTIAL,session-${sessionId}`;
            const proxyUrl = `http://${username}:${password}@proxy.apify.com:8000`;
            
            const response = await fetch(url, { proxy: proxyUrl });
            
            if (response.ok) {
                return response;
            }
            
            if (response.status >= 590 && response.status <= 599) {
                console.log(`Proxy error ${response.status}, retrying...`);
                continue;
            }
            
            throw new Error(`HTTP ${response.status}`);
            
        } catch (error) {
            if (attempt === maxRetries) {
                throw error;
            }
            
            console.log(`Attempt ${attempt} failed, retrying...`);
            await new Promise(resolve => setTimeout(resolve, 1000 * attempt));
        }
    }
};
```

## Best Practices

### 1. Use Appropriate Proxy Groups
```javascript
// Choose proxy type based on use case
const proxyConfig = {
    // For general web scraping
    datacenter: { groups: ['SHADER'] },
    
    // For social media or geo-restricted content
    residential: { groups: ['RESIDENTIAL'] },
    
    // For Google searches
    googleSerp: { groups: ['GOOGLE_SERP'] }
};
```

### 2. Implement Session Management
```javascript
// Proper session lifecycle
class ProxySessionManager {
    constructor() {
        this.sessions = new Map();
        this.sessionTimeout = 25 * 60 * 1000; // 25 minutes for datacenter
    }
    
    getSession(key) {
        if (!this.sessions.has(key)) {
            this.sessions.set(key, {
                id: `session-${key}-${Date.now()}`,
                createdAt: Date.now()
            });
        }
        
        const session = this.sessions.get(key);
        
        // Check if session is expired
        if (Date.now() - session.createdAt > this.sessionTimeout) {
            session.id = `session-${key}-${Date.now()}`;
            session.createdAt = Date.now();
        }
        
        return session.id;
    }
}
```

### 3. Monitor Proxy Performance
```javascript
// Track proxy performance metrics
const proxyStats = {
    requests: 0,
    successes: 0,
    failures: 0,
    errors: {}
};

const trackProxyRequest = (success, error = null) => {
    proxyStats.requests++;
    
    if (success) {
        proxyStats.successes++;
    } else {
        proxyStats.failures++;
        if (error) {
            proxyStats.errors[error.code] = (proxyStats.errors[error.code] || 0) + 1;
        }
    }
    
    // Log stats periodically
    if (proxyStats.requests % 100 === 0) {
        console.log('Proxy stats:', {
            successRate: (proxyStats.successes / proxyStats.requests * 100).toFixed(2) + '%',
            totalRequests: proxyStats.requests,
            errorBreakdown: proxyStats.errors
        });
    }
};
```

Apify Proxy provides a robust, scalable solution for web scraping and automation with advanced features for session management, geographic targeting, and error handling.