# Residential Proxy | Platform | Apify Documentation

## Overview

Residential proxies use IP addresses from actual home and office internet users, providing higher anonymity compared to datacenter proxies. This makes your web scraping traffic appear indistinguishable from legitimate user traffic.

## Key Features

### Enhanced Anonymity
- **Real user IPs**: IP addresses from actual residential internet connections
- **Natural traffic patterns**: Mimics genuine user behavior
- **Reduced detection**: Lower chance of being blocked by websites
- **Geographic authenticity**: True location-based IP addresses

### IP Address Management
- **Automatic rotation**: New IP for each request by default
- **Session persistence**: Maintain same IP for up to 1 minute
- **Geographic targeting**: Select IPs from specific countries
- **Load balancing**: Distributed across available residential IPs

### Performance Characteristics
- **Variable speeds**: Connection speeds may vary between different IPs
- **Potential interruptions**: Occasional connection disruptions possible
- **Real-world conditions**: Performance reflects actual residential internet

## Pricing Model

### Data-Based Pricing
- **Traffic-based billing**: Charged based on data consumption
- **Bandwidth monitoring**: Track data usage in real-time
- **Cost optimization**: Minimize unnecessary data transfer

### Cost Management
Use traffic optimization techniques to control costs:
- Block unnecessary resources (images, CSS, fonts)
- Optimize request patterns
- Cache responses when possible

## Configuration

### Basic Setup
```javascript
// JavaScript SDK configuration
const proxyConfiguration = await Actor.createProxyConfiguration({
    groups: ['RESIDENTIAL'],
    countryCode: 'US', // Optional: specify country
});

// Use in crawler
const crawler = new PuppeteerCrawler({
    proxyConfiguration,
    requestHandler: async ({ page, request }) => {
        // Your scraping logic
        const content = await page.content();
        await Actor.pushData({
            url: request.url,
            title: await page.title()
        });
    }
});
```

### Manual Configuration
```javascript
// Manual proxy URL construction
const username = 'groups-RESIDENTIAL,session-my-session';
const password = process.env.APIFY_PROXY_PASSWORD;
const proxyUrl = `http://${username}:${password}@proxy.apify.com:8000`;

// Use with Puppeteer
const browser = await puppeteer.launch({
    args: [`--proxy-server=${proxyUrl}`]
});

// Use with Playwright
const browser = await playwright.chromium.launch({
    proxy: {
        server: 'http://proxy.apify.com:8000',
        username: username,
        password: password
    }
});
```

### Country-Specific Configuration
```javascript
// Target specific countries
const countryConfigs = {
    us: await Actor.createProxyConfiguration({
        groups: ['RESIDENTIAL'],
        countryCode: 'US'
    }),
    uk: await Actor.createProxyConfiguration({
        groups: ['RESIDENTIAL'],
        countryCode: 'GB'
    }),
    france: await Actor.createProxyConfiguration({
        groups: ['RESIDENTIAL'],
        countryCode: 'FR'
    })
};

// Use country-specific proxy
const ukProxy = countryConfigs.uk;
```

## Session Management

### Session Persistence
Residential proxies support session persistence for up to 1 minute:

```javascript
// Create session with fixed IP
const sessionId = 'user-session-123';
const username = `groups-RESIDENTIAL,session-${sessionId}`;

// Make multiple requests with same IP
const makeSessionRequest = async (url) => {
    const proxyUrl = `http://${username}:${password}@proxy.apify.com:8000`;
    return await fetch(url, { proxy: proxyUrl });
};

// All requests within 1 minute will use same IP
await makeSessionRequest('https://example.com/page1');
await makeSessionRequest('https://example.com/page2');
await makeSessionRequest('https://example.com/page3');
```

### Session Rotation
```javascript
// Rotate sessions for different tasks
class SessionManager {
    constructor() {
        this.sessions = [];
        this.currentIndex = 0;
        this.sessionDuration = 50000; // 50 seconds (within 1-minute limit)
    }
    
    getSession() {
        const now = Date.now();
        
        // Clean expired sessions
        this.sessions = this.sessions.filter(
            session => now - session.created < this.sessionDuration
        );
        
        // Create new session if needed
        if (this.sessions.length === 0) {
            this.sessions.push({
                id: `residential-${now}`,
                created: now
            });
        }
        
        const session = this.sessions[this.currentIndex % this.sessions.length];
        this.currentIndex++;
        
        return session.id;
    }
}

const sessionManager = new SessionManager();

// Use rotating sessions
const processUrls = async (urls) => {
    for (const url of urls) {
        const sessionId = sessionManager.getSession();
        const username = `groups-RESIDENTIAL,session-${sessionId}`;
        const proxyUrl = `http://${username}:${password}@proxy.apify.com:8000`;
        
        await processUrl(url, proxyUrl);
    }
};
```

## Traffic Optimization

### Block Unnecessary Resources
```javascript
// Reduce data consumption by blocking resources
const crawler = new PuppeteerCrawler({
    proxyConfiguration: await Actor.createProxyConfiguration({
        groups: ['RESIDENTIAL']
    }),
    preNavigationHooks: [
        async ({ page }) => {
            // Block images, CSS, and fonts to save bandwidth
            await page.setRequestInterception(true);
            
            page.on('request', (request) => {
                const resourceType = request.resourceType();
                
                if (['image', 'stylesheet', 'font', 'media'].includes(resourceType)) {
                    request.abort();
                } else {
                    request.continue();
                }
            });
        }
    ],
    requestHandler: async ({ page, request }) => {
        // Your scraping logic with reduced bandwidth usage
        const text = await page.evaluate(() => document.body.textContent);
        await Actor.pushData({
            url: request.url,
            textLength: text.length
        });
    }
});
```

### Optimize Request Patterns
```javascript
// Minimize data transfer
const optimizedScraping = async () => {
    const proxyConfiguration = await Actor.createProxyConfiguration({
        groups: ['RESIDENTIAL']
    });
    
    const crawler = new CheerioCrawler({
        proxyConfiguration,
        requestHandler: async ({ $, request }) => {
            // Extract only essential data
            const title = $('title').text();
            const description = $('meta[name="description"]').attr('content');
            const price = $('.price').first().text();
            
            await Actor.pushData({
                url: request.url,
                title,
                description,
                price
            });
        }
    });
    
    await crawler.run(urls);
};
```

## Best Practices

### 1. Speed Testing
```javascript
// Test connection speed before extensive use
const testConnectionSpeed = async () => {
    const proxyConfiguration = await Actor.createProxyConfiguration({
        groups: ['RESIDENTIAL'],
        countryCode: 'US'
    });
    
    const startTime = Date.now();
    
    try {
        const response = await fetch('https://httpbin.org/json', {
            proxy: proxyConfiguration.newUrl()
        });
        
        const data = await response.json();
        const duration = Date.now() - startTime;
        
        console.log(`Connection speed: ${duration}ms`);
        
        if (duration > 5000) {
            console.warn('Slow connection detected, consider using different proxy');
        }
        
        return duration;
    } catch (error) {
        console.error('Connection test failed:', error);
        return null;
    }
};
```

### 2. Handle Connection Interruptions
```javascript
// Implement retry logic for connection issues
const fetchWithRetry = async (url, proxyConfig, maxRetries = 3) => {
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
        try {
            const response = await fetch(url, {
                proxy: proxyConfig.newUrl(),
                timeout: 30000 // 30 second timeout
            });
            
            if (response.ok) {
                return response;
            }
            
            throw new Error(`HTTP ${response.status}`);
            
        } catch (error) {
            console.log(`Attempt ${attempt} failed:`, error.message);
            
            if (attempt === maxRetries) {
                throw error;
            }
            
            // Wait before retry (exponential backoff)
            await new Promise(resolve => 
                setTimeout(resolve, Math.pow(2, attempt) * 1000)
            );
        }
    }
};
```

### 3. Monitor Data Usage
```javascript
// Track bandwidth consumption
class DataUsageTracker {
    constructor() {
        this.totalBytes = 0;
        this.requestCount = 0;
    }
    
    trackResponse(response) {
        // Estimate data usage from response headers
        const contentLength = response.headers.get('content-length');
        if (contentLength) {
            this.totalBytes += parseInt(contentLength);
        }
        
        this.requestCount++;
        
        // Log usage every 100 requests
        if (this.requestCount % 100 === 0) {
            console.log(`Data usage: ${(this.totalBytes / 1024 / 1024).toFixed(2)} MB over ${this.requestCount} requests`);
        }
    }
    
    getAveragePerRequest() {
        return this.requestCount > 0 ? this.totalBytes / this.requestCount : 0;
    }
}

const dataTracker = new DataUsageTracker();

// Use in requests
const response = await fetch(url, { proxy: proxyUrl });
dataTracker.trackResponse(response);
```

### 4. Geographic Optimization
```javascript
// Use appropriate geographic locations
const getOptimalProxy = (targetDomain) => {
    const domainToCountry = {
        'amazon.com': 'US',
        'amazon.co.uk': 'GB',
        'amazon.de': 'DE',
        'amazon.fr': 'FR',
        'flipkart.com': 'IN',
        'mercadolibre.com': 'AR'
    };
    
    const domain = new URL(targetDomain).hostname;
    const countryCode = domainToCountry[domain] || 'US';
    
    return Actor.createProxyConfiguration({
        groups: ['RESIDENTIAL'],
        countryCode: countryCode
    });
};

// Use optimal proxy for target
const targetUrl = 'https://amazon.co.uk/products';
const proxyConfig = await getOptimalProxy(targetUrl);
```

## Use Cases

### 1. Social Media Scraping
```javascript
// Access social media with residential IPs
const socialMediaCrawler = new PuppeteerCrawler({
    proxyConfiguration: await Actor.createProxyConfiguration({
        groups: ['RESIDENTIAL'],
        countryCode: 'US'
    }),
    requestHandler: async ({ page, request }) => {
        await page.goto(request.url, { waitUntil: 'networkidle2' });
        
        // Scrape social media content
        const posts = await page.evaluate(() => {
            return Array.from(document.querySelectorAll('.post')).map(post => ({
                text: post.textContent.trim(),
                timestamp: post.querySelector('.timestamp')?.textContent
            }));
        });
        
        await Actor.pushData({ url: request.url, posts });
    }
});
```

### 2. Geo-Restricted Content
```javascript
// Access location-specific content
const geoContentScraper = async (country) => {
    const proxyConfig = await Actor.createProxyConfiguration({
        groups: ['RESIDENTIAL'],
        countryCode: country
    });
    
    const crawler = new CheerioCrawler({
        proxyConfiguration: proxyConfig,
        requestHandler: async ({ $, request }) => {
            const localizedContent = $('.localized-content').text();
            const localPrices = $('.price-local').map((i, el) => $(el).text()).get();
            
            await Actor.pushData({
                url: request.url,
                country: country,
                content: localizedContent,
                prices: localPrices
            });
        }
    });
    
    await crawler.run(['https://example.com/products']);
};

// Scrape from multiple locations
await geoContentScraper('US');
await geoContentScraper('GB');
await geoContentScraper('DE');
```

## Troubleshooting

### Connection Issues
```javascript
// Diagnose residential proxy issues
const diagnoseConnection = async () => {
    const proxyConfig = await Actor.createProxyConfiguration({
        groups: ['RESIDENTIAL']
    });
    
    try {
        // Test basic connectivity
        const response = await fetch('https://httpbin.org/ip', {
            proxy: proxyConfig.newUrl()
        });
        
        const data = await response.json();
        console.log('Current IP:', data.origin);
        
        // Test speed
        const speedTest = await testConnectionSpeed();
        console.log('Speed test:', speedTest + 'ms');
        
        return true;
    } catch (error) {
        console.error('Connection diagnosis failed:', error);
        return false;
    }
};
```

### Session Debugging
```javascript
// Debug session behavior
const debugSession = async () => {
    const sessionId = 'debug-session';
    const username = `groups-RESIDENTIAL,session-${sessionId}`;
    
    console.log('Testing session persistence...');
    
    for (let i = 0; i < 5; i++) {
        const response = await fetch('https://httpbin.org/ip', {
            proxy: `http://${username}:${password}@proxy.apify.com:8000`
        });
        
        const data = await response.json();
        console.log(`Request ${i + 1}: IP = ${data.origin}`);
        
        // Wait 10 seconds between requests
        if (i < 4) await new Promise(resolve => setTimeout(resolve, 10000));
    }
};
```

Residential proxies provide the highest level of anonymity for web scraping by using real user IP addresses, making them ideal for accessing geo-restricted content, social media platforms, and websites with strict anti-bot measures.