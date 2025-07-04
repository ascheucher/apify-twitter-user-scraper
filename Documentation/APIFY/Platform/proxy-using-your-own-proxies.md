# Using Your Own Proxies | Platform | Apify Documentation

## Overview

Apify platform provides flexibility to use your own proxy infrastructure alongside or instead of Apify's built-in proxy services. This allows you to integrate custom proxy solutions, third-party proxy providers, or enterprise proxy infrastructure.

## Configuration Methods

### 1. Console Configuration

#### Steps for Console Setup
1. **Navigate to Actor configuration**: Go to your Actor's settings
2. **Find proxy section**: Scroll to "Input and options" tab
3. **Locate proxy configuration**: Look for "Proxy and browser configuration" section
4. **Enter proxy URLs**: Add your custom proxy URLs directly in the configuration field

#### Console Interface
The Apify Console provides a user-friendly interface for entering proxy URLs:
- **Proxy URL field**: Direct input for proxy connection strings
- **Multiple proxy support**: Add multiple proxy URLs for rotation
- **Validation**: Real-time validation of proxy URL format
- **Test connection**: Built-in proxy connectivity testing

### 2. SDK Configuration

#### JavaScript SDK Integration
```javascript
const { Actor } = require('apify');

// Method 1: Using proxyConfiguration.newUrl()
const proxyConfiguration = {
    newUrl: (sessionId) => {
        // Return your custom proxy URL
        const proxyUrls = [
            'http://user:pass@proxy1.example.com:8080',
            'http://user:pass@proxy2.example.com:8080',
            'http://user:pass@proxy3.example.com:8080'
        ];
        
        // Simple round-robin selection
        const index = sessionId ? sessionId.charCodeAt(0) % proxyUrls.length : 0;
        return proxyUrls[index];
    }
};

// Use with crawler
const crawler = new PuppeteerCrawler({
    proxyConfiguration,
    requestHandler: async ({ page, request }) => {
        // Your scraping logic
        const title = await page.title();
        await Actor.pushData({ url: request.url, title });
    }
});

await crawler.run(['https://example.com']);
```

#### Python SDK Integration
```python
from apify import Actor

class CustomProxyConfiguration:
    def __init__(self, proxy_urls):
        self.proxy_urls = proxy_urls
        self.current_index = 0
    
    def new_url(self, session_id=None):
        """Return next proxy URL in rotation"""
        if session_id:
            # Use session-based selection
            index = hash(session_id) % len(self.proxy_urls)
        else:
            # Simple round-robin
            index = self.current_index
            self.current_index = (self.current_index + 1) % len(self.proxy_urls)
        
        return self.proxy_urls[index]

async def main():
    async with Actor:
        # Configure custom proxies
        proxy_urls = [
            'http://user:pass@proxy1.example.com:8080',
            'http://user:pass@proxy2.example.com:8080',
            'http://user:pass@proxy3.example.com:8080'
        ]
        
        proxy_config = CustomProxyConfiguration(proxy_urls)
        
        # Use in your scraping logic
        for url in urls:
            proxy_url = proxy_config.new_url()
            # Make request with custom proxy
            response = await make_request(url, proxy_url)
            await Actor.push_data(response)
```

## Proxy URL Formats

### HTTP Proxy
```javascript
// Basic HTTP proxy
const httpProxy = 'http://proxy.example.com:8080';

// HTTP proxy with authentication
const httpProxyWithAuth = 'http://username:password@proxy.example.com:8080';

// HTTP proxy with complex password
const encodedPassword = encodeURIComponent('p@ssw0rd!');
const httpProxyEncoded = `http://username:${encodedPassword}@proxy.example.com:8080`;
```

### SOCKS Proxy
```javascript
// SOCKS5 proxy
const socksProxy = 'socks5://proxy.example.com:1080';

// SOCKS5 proxy with authentication
const socksProxyWithAuth = 'socks5://username:password@proxy.example.com:1080';

// SOCKS4 proxy
const socks4Proxy = 'socks4://proxy.example.com:1080';
```

### HTTPS Proxy
```javascript
// HTTPS proxy
const httpsProxy = 'https://proxy.example.com:8443';

// HTTPS proxy with authentication
const httpsProxyWithAuth = 'https://username:password@proxy.example.com:8443';
```

## Advanced Proxy Management

### Proxy Pool Management
```javascript
class ProxyPool {
    constructor(proxyUrls) {
        this.proxies = proxyUrls.map(url => ({
            url,
            failures: 0,
            lastUsed: 0,
            isHealthy: true
        }));
        this.maxFailures = 3;
        this.cooldownPeriod = 300000; // 5 minutes
    }
    
    getProxy(sessionId = null) {
        // Filter healthy proxies
        const healthyProxies = this.proxies.filter(proxy => 
            proxy.isHealthy || 
            (Date.now() - proxy.lastUsed > this.cooldownPeriod)
        );
        
        if (healthyProxies.length === 0) {
            // Reset all proxies if none are healthy
            this.proxies.forEach(proxy => {
                proxy.isHealthy = true;
                proxy.failures = 0;
            });
            return this.proxies[0];
        }
        
        // Select proxy based on session or round-robin
        let selectedProxy;
        if (sessionId) {
            const index = this.hashCode(sessionId) % healthyProxies.length;
            selectedProxy = healthyProxies[index];
        } else {
            // Least recently used
            selectedProxy = healthyProxies.reduce((prev, current) => 
                prev.lastUsed < current.lastUsed ? prev : current
            );
        }
        
        selectedProxy.lastUsed = Date.now();
        return selectedProxy;
    }
    
    reportFailure(proxyUrl) {
        const proxy = this.proxies.find(p => p.url === proxyUrl);
        if (proxy) {
            proxy.failures++;
            if (proxy.failures >= this.maxFailures) {
                proxy.isHealthy = false;
                console.log(`Proxy ${proxyUrl} marked as unhealthy`);
            }
        }
    }
    
    reportSuccess(proxyUrl) {
        const proxy = this.proxies.find(p => p.url === proxyUrl);
        if (proxy) {
            proxy.failures = Math.max(0, proxy.failures - 1);
            proxy.isHealthy = true;
        }
    }
    
    hashCode(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash; // Convert to 32-bit integer
        }
        return Math.abs(hash);
    }
}

// Usage
const proxyPool = new ProxyPool([
    'http://user:pass@proxy1.example.com:8080',
    'http://user:pass@proxy2.example.com:8080',
    'http://user:pass@proxy3.example.com:8080'
]);

const proxyConfiguration = {
    newUrl: (sessionId) => {
        const proxy = proxyPool.getProxy(sessionId);
        return proxy.url;
    }
};
```

### Proxy Authentication Methods
```javascript
// Different authentication methods
class ProxyAuthManager {
    static basicAuth(username, password) {
        return `http://${username}:${encodeURIComponent(password)}@`;
    }
    
    static customHeaders(proxyUrl, authHeaders) {
        // For proxies requiring custom headers
        return {
            proxy: proxyUrl,
            headers: authHeaders
        };
    }
    
    static rotatingCredentials(credentials) {
        let index = 0;
        return () => {
            const cred = credentials[index];
            index = (index + 1) % credentials.length;
            return `http://${cred.username}:${encodeURIComponent(cred.password)}@`;
        };
    }
}

// Example usage
const credentials = [
    { username: 'user1', password: 'pass1' },
    { username: 'user2', password: 'pass2' },
    { username: 'user3', password: 'pass3' }
];

const getRotatingAuth = ProxyAuthManager.rotatingCredentials(credentials);

const buildProxyUrl = (host, port) => {
    return getRotatingAuth() + `${host}:${port}`;
};
```

## Integration Examples

### Third-Party Proxy Services
```javascript
// Bright Data (formerly Luminati) integration
const brightDataProxy = {
    newUrl: (sessionId) => {
        const endpoint = 'zproxy.lum-superproxy.io';
        const port = '22225';
        const username = 'your-username';
        const password = 'your-password';
        const session = sessionId || `session_${Math.random().toString(36).substring(7)}`;
        
        return `http://${username}-session-${session}:${password}@${endpoint}:${port}`;
    }
};

// Smartproxy integration
const smartproxyConfig = {
    newUrl: (sessionId) => {
        const endpoint = 'gate.smartproxy.com';
        const port = '10000';
        const username = 'your-username';
        const password = 'your-password';
        
        return `http://${username}:${password}@${endpoint}:${port}`;
    }
};

// ProxyMesh integration
const proxyMeshConfig = {
    newUrl: (sessionId) => {
        const endpoints = [
            'us-wa.proxymesh.com:31280',
            'us-ca.proxymesh.com:31280',
            'us-il.proxymesh.com:31280'
        ];
        
        const endpoint = endpoints[Math.floor(Math.random() * endpoints.length)];
        const [host, port] = endpoint.split(':');
        const username = 'your-username';
        const password = 'your-password';
        
        return `http://${username}:${password}@${host}:${port}`;
    }
};
```

### Corporate Proxy Integration
```javascript
// Corporate proxy with authentication
const corporateProxyConfig = {
    newUrl: (sessionId) => {
        const proxyHost = process.env.CORPORATE_PROXY_HOST || 'proxy.company.com';
        const proxyPort = process.env.CORPORATE_PROXY_PORT || '8080';
        const username = process.env.CORPORATE_PROXY_USER;
        const password = process.env.CORPORATE_PROXY_PASS;
        
        if (username && password) {
            return `http://${username}:${encodeURIComponent(password)}@${proxyHost}:${proxyPort}`;
        } else {
            return `http://${proxyHost}:${proxyPort}`;
        }
    }
};

// Corporate proxy with domain authentication
const domainProxyConfig = {
    newUrl: (sessionId) => {
        const domain = process.env.CORPORATE_DOMAIN || 'COMPANY';
        const username = process.env.CORPORATE_USER;
        const password = process.env.CORPORATE_PASS;
        const proxyHost = process.env.CORPORATE_PROXY_HOST;
        const proxyPort = process.env.CORPORATE_PROXY_PORT;
        
        const domainUser = `${domain}\\${username}`;
        return `http://${encodeURIComponent(domainUser)}:${encodeURIComponent(password)}@${proxyHost}:${proxyPort}`;
    }
};
```

## Testing and Validation

### Proxy Health Checks
```javascript
// Proxy connectivity testing
const testProxy = async (proxyUrl) => {
    try {
        const response = await fetch('https://httpbin.org/ip', {
            method: 'GET',
            timeout: 10000,
            agent: new HttpsProxyAgent(proxyUrl)
        });
        
        if (response.ok) {
            const data = await response.json();
            return {
                success: true,
                ip: data.origin,
                responseTime: response.headers.get('x-response-time')
            };
        } else {
            return {
                success: false,
                error: `HTTP ${response.status}`
            };
        }
    } catch (error) {
        return {
            success: false,
            error: error.message
        };
    }
};

// Test all proxies
const testAllProxies = async (proxyUrls) => {
    const results = await Promise.all(
        proxyUrls.map(async (url) => {
            const result = await testProxy(url);
            return { url, ...result };
        })
    );
    
    console.log('Proxy test results:');
    results.forEach(result => {
        if (result.success) {
            console.log(`✓ ${result.url} - IP: ${result.ip}`);
        } else {
            console.log(`✗ ${result.url} - Error: ${result.error}`);
        }
    });
    
    return results.filter(r => r.success).map(r => r.url);
};
```

### Performance Monitoring
```javascript
// Monitor proxy performance
class ProxyPerformanceMonitor {
    constructor() {
        this.stats = new Map();
    }
    
    recordRequest(proxyUrl, success, responseTime, error = null) {
        if (!this.stats.has(proxyUrl)) {
            this.stats.set(proxyUrl, {
                total: 0,
                successful: 0,
                failed: 0,
                totalResponseTime: 0,
                errors: {}
            });
        }
        
        const stat = this.stats.get(proxyUrl);
        stat.total++;
        
        if (success) {
            stat.successful++;
            stat.totalResponseTime += responseTime;
        } else {
            stat.failed++;
            if (error) {
                stat.errors[error] = (stat.errors[error] || 0) + 1;
            }
        }
    }
    
    getReport() {
        const report = [];
        
        for (const [proxyUrl, stat] of this.stats) {
            const successRate = (stat.successful / stat.total * 100).toFixed(2);
            const avgResponseTime = stat.successful > 0 
                ? (stat.totalResponseTime / stat.successful).toFixed(0)
                : 0;
            
            report.push({
                proxy: proxyUrl,
                successRate: `${successRate}%`,
                avgResponseTime: `${avgResponseTime}ms`,
                totalRequests: stat.total,
                errors: stat.errors
            });
        }
        
        return report;
    }
}

// Usage
const monitor = new ProxyPerformanceMonitor();

// In your request handler
const startTime = Date.now();
try {
    const response = await fetch(url, { agent: proxyAgent });
    const responseTime = Date.now() - startTime;
    monitor.recordRequest(proxyUrl, true, responseTime);
} catch (error) {
    const responseTime = Date.now() - startTime;
    monitor.recordRequest(proxyUrl, false, responseTime, error.message);
}
```

## Best Practices

### 1. Proxy Rotation Strategy
```javascript
// Implement intelligent proxy rotation
const createSmartProxyRotation = (proxies) => {
    const proxyState = proxies.map(url => ({
        url,
        weight: 1.0,
        consecutiveFailures: 0,
        lastUsed: 0
    }));
    
    return {
        getNext: () => {
            // Weighted random selection based on success rates
            const totalWeight = proxyState.reduce((sum, p) => sum + p.weight, 0);
            let random = Math.random() * totalWeight;
            
            for (const proxy of proxyState) {
                random -= proxy.weight;
                if (random <= 0) {
                    proxy.lastUsed = Date.now();
                    return proxy.url;
                }
            }
            
            // Fallback to first proxy
            return proxyState[0].url;
        },
        
        reportResult: (proxyUrl, success) => {
            const proxy = proxyState.find(p => p.url === proxyUrl);
            if (proxy) {
                if (success) {
                    proxy.weight = Math.min(2.0, proxy.weight * 1.1);
                    proxy.consecutiveFailures = 0;
                } else {
                    proxy.weight = Math.max(0.1, proxy.weight * 0.9);
                    proxy.consecutiveFailures++;
                    
                    // Temporarily disable proxy after too many failures
                    if (proxy.consecutiveFailures >= 5) {
                        proxy.weight = 0.01;
                    }
                }
            }
        }
    };
};
```

### 2. Error Handling
```javascript
// Comprehensive error handling for custom proxies
const handleProxyError = (error, proxyUrl) => {
    if (error.code === 'ECONNREFUSED') {
        console.warn(`Proxy ${proxyUrl} refused connection`);
        return 'PROXY_DOWN';
    } else if (error.code === 'ENOTFOUND') {
        console.warn(`Proxy ${proxyUrl} not found`);
        return 'PROXY_NOT_FOUND';
    } else if (error.code === 'ETIMEDOUT') {
        console.warn(`Proxy ${proxyUrl} timed out`);
        return 'PROXY_TIMEOUT';
    } else if (error.message.includes('407')) {
        console.warn(`Proxy ${proxyUrl} authentication failed`);
        return 'PROXY_AUTH_FAILED';
    } else {
        console.warn(`Proxy ${proxyUrl} unknown error:`, error.message);
        return 'PROXY_UNKNOWN_ERROR';
    }
};
```

### 3. Environment-Based Configuration
```javascript
// Configure proxies based on environment
const getProxyConfiguration = () => {
    const environment = process.env.NODE_ENV || 'development';
    
    switch (environment) {
        case 'development':
            return {
                newUrl: () => null // No proxy in development
            };
            
        case 'staging':
            return {
                newUrl: () => process.env.STAGING_PROXY_URL
            };
            
        case 'production':
            const productionProxies = [
                process.env.PROD_PROXY_1,
                process.env.PROD_PROXY_2,
                process.env.PROD_PROXY_3
            ].filter(Boolean);
            
            return {
                newUrl: (sessionId) => {
                    const index = sessionId 
                        ? Math.abs(sessionId.charCodeAt(0)) % productionProxies.length
                        : Math.floor(Math.random() * productionProxies.length);
                    return productionProxies[index];
                }
            };
            
        default:
            throw new Error(`Unknown environment: ${environment}`);
    }
};
```

Using your own proxies provides maximum flexibility and control over your scraping infrastructure, allowing you to optimize for specific use cases, comply with corporate policies, or integrate with existing proxy investments.