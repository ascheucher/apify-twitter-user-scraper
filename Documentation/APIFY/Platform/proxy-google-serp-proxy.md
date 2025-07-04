# Google SERP Proxy | Platform | Apify Documentation

## Overview

Google SERP proxy allows extracting search results from Google Search and Shopping services across multiple country domains. It provides access to pure HTML code of search result pages with country-specific localization and pricing based on number of requests.

## Supported Services

### Google Search
Extract organic search results, featured snippets, and related searches:
- **Organic results**: Web page listings
- **Featured snippets**: Direct answer boxes
- **Related searches**: Suggested queries
- **Knowledge panels**: Information cards
- **Local results**: Map-based listings

### Google Shopping
Access product listings and shopping data:
- **Product results**: Shopping listings
- **Price comparisons**: Multi-vendor pricing
- **Product details**: Specifications and reviews
- **Store information**: Merchant details
- **Shopping ads**: Sponsored product listings

### Google Shopping Search
Specialized shopping queries:
- **Product searches**: Specific item queries
- **Category browsing**: Product category exploration
- **Price filtering**: Budget-based searches
- **Brand filtering**: Manufacturer-specific results

## Configuration

### Basic Setup
```javascript
// JavaScript SDK configuration
const proxyConfiguration = await Actor.createProxyConfiguration({
    groups: ['GOOGLE_SERP'],
    countryCode: 'US' // Determines proxy location
});

// Use in web scraper
const crawler = new CheerioCrawler({
    proxyConfiguration,
    requestHandler: async ({ $, request }) => {
        // Extract search results
        const results = $('.g').map((i, el) => ({
            title: $(el).find('h3').text(),
            url: $(el).find('a').attr('href'),
            description: $(el).find('.VwiC3b').text()
        })).get();
        
        await Actor.pushData({
            query: getQueryFromUrl(request.url),
            results: results
        });
    }
});
```

### Manual Configuration
```javascript
// Manual proxy URL construction
const username = 'groups-GOOGLE_SERP';
const password = process.env.APIFY_PROXY_PASSWORD;
const proxyUrl = `http://${username}:${password}@proxy.apify.com:8000`;

// Note: No session parameter available for Google SERP proxy
```

## Country-Specific Searches

### Domain Selection
Use correct Google domain for desired country:

```javascript
// Country-specific Google domains
const googleDomains = {
    US: 'www.google.com',
    UK: 'www.google.co.uk',
    Germany: 'www.google.de',
    France: 'www.google.fr',
    Japan: 'www.google.co.jp',
    Australia: 'www.google.com.au',
    Canada: 'www.google.ca',
    India: 'www.google.co.in'
};

// Build search URLs
const buildSearchUrl = (query, country = 'US') => {
    const domain = googleDomains[country];
    return `http://${domain}/search?q=${encodeURIComponent(query)}`;
};

// Build shopping URLs
const buildShoppingUrl = (query, country = 'US') => {
    const domain = googleDomains[country];
    return `http://${domain}/search?tbm=shop&q=${encodeURIComponent(query)}`;
};
```

### Proxy Configuration by Country
```javascript
// Configure proxy for specific countries
const getGoogleSerpProxy = (countryCode) => {
    return Actor.createProxyConfiguration({
        groups: ['GOOGLE_SERP'],
        countryCode: countryCode
    });
};

// Use country-specific proxy
const usProxy = await getGoogleSerpProxy('US');
const ukProxy = await getGoogleSerpProxy('GB');
const deProxy = await getGoogleSerpProxy('DE');
```

## Usage Examples

### Basic Search Scraping
```javascript
const { Actor } = require('apify');
const { CheerioCrawler } = require('crawlee');

Actor.main(async () => {
    const input = await Actor.getInput();
    const { queries, country = 'US' } = input;
    
    const proxyConfiguration = await Actor.createProxyConfiguration({
        groups: ['GOOGLE_SERP'],
        countryCode: country
    });
    
    // Build search URLs
    const searchUrls = queries.map(query => ({
        url: buildSearchUrl(query, country),
        userData: { query, type: 'search' }
    }));
    
    const crawler = new CheerioCrawler({
        proxyConfiguration,
        requestHandler: async ({ $, request }) => {
            const { query, type } = request.userData;
            
            if (type === 'search') {
                const results = extractSearchResults($);
                await Actor.pushData({
                    query,
                    country,
                    type: 'organic',
                    results,
                    scrapedAt: new Date().toISOString()
                });
            }
        }
    });
    
    await crawler.run(searchUrls);
});

// Extract search results helper
function extractSearchResults($) {
    return $('.g').map((i, el) => {
        const $el = $(el);
        return {
            title: $el.find('h3').text().trim(),
            url: $el.find('a').attr('href'),
            description: $el.find('.VwiC3b, .s3v9rd').text().trim(),
            position: i + 1
        };
    }).get();
}
```

### Shopping Results Scraping
```javascript
// Google Shopping scraper
const scrapeGoogleShopping = async () => {
    const proxyConfiguration = await Actor.createProxyConfiguration({
        groups: ['GOOGLE_SERP'],
        countryCode: 'US'
    });
    
    const crawler = new CheerioCrawler({
        proxyConfiguration,
        requestHandler: async ({ $, request }) => {
            const { query } = request.userData;
            
            // Extract shopping results
            const products = $('.sh-dgr__content').map((i, el) => {
                const $el = $(el);
                return {
                    title: $el.find('.Lq5OHd').text().trim(),
                    price: $el.find('.a8Pemb').text().trim(),
                    merchant: $el.find('.aULzUe').text().trim(),
                    rating: $el.find('.NzUzee .Rsc7Yb').text().trim(),
                    image: $el.find('img').attr('src'),
                    link: $el.find('a').attr('href')
                };
            }).get();
            
            await Actor.pushData({
                query,
                type: 'shopping',
                products,
                totalResults: products.length
            });
        }
    });
    
    const shoppingUrls = queries.map(query => ({
        url: buildShoppingUrl(query, 'US'),
        userData: { query }
    }));
    
    await crawler.run(shoppingUrls);
};
```

### Multi-Country Comparison
```javascript
// Compare search results across countries
const compareSearchResults = async (query) => {
    const countries = ['US', 'GB', 'DE', 'FR'];
    const results = [];
    
    for (const country of countries) {
        const proxyConfig = await Actor.createProxyConfiguration({
            groups: ['GOOGLE_SERP'],
            countryCode: country
        });
        
        const crawler = new CheerioCrawler({
            proxyConfiguration: proxyConfig,
            maxRequestsPerCrawl: 1,
            requestHandler: async ({ $, request }) => {
                const searchResults = extractSearchResults($);
                results.push({
                    country,
                    query,
                    results: searchResults.slice(0, 10), // Top 10 results
                    totalFound: searchResults.length
                });
            }
        });
        
        const domain = googleDomains[country];
        const searchUrl = `http://${domain}/search?q=${encodeURIComponent(query)}`;
        
        await crawler.run([searchUrl]);
    }
    
    await Actor.pushData({
        comparisonQuery: query,
        countryResults: results,
        comparedAt: new Date().toISOString()
    });
};
```

## Advanced Features

### Search Parameters
```javascript
// Advanced search parameters
const buildAdvancedSearchUrl = (params) => {
    const {
        query,
        country = 'US',
        language = 'en',
        timeRange = '', // qdr=d (day), qdr=w (week), qdr=m (month), qdr=y (year)
        safeSearch = '', // safe=strict, safe=moderate, safe=off
        resultType = '', // tbm=isch (images), tbm=vid (videos), tbm=nws (news)
        exactPhrase = '',
        excludeTerms = '',
        site = ''
    } = params;
    
    const domain = googleDomains[country];
    let url = `http://${domain}/search?`;
    
    const searchParams = new URLSearchParams();
    
    // Build query with modifiers
    let searchQuery = query;
    if (exactPhrase) searchQuery += ` "${exactPhrase}"`;
    if (excludeTerms) searchQuery += ` -${excludeTerms}`;
    if (site) searchQuery += ` site:${site}`;
    
    searchParams.append('q', searchQuery);
    if (language) searchParams.append('hl', language);
    if (timeRange) searchParams.append('qdr', timeRange);
    if (safeSearch) searchParams.append('safe', safeSearch);
    if (resultType) searchParams.append('tbm', resultType);
    
    return url + searchParams.toString();
};

// Usage example
const advancedSearches = [
    {
        query: 'machine learning',
        country: 'US',
        timeRange: 'y', // Last year
        site: 'arxiv.org'
    },
    {
        query: 'climate change',
        country: 'GB',
        resultType: 'nws', // News results
        safeSearch: 'strict'
    }
];
```

### Result Parsing
```javascript
// Comprehensive result extraction
const extractAllResults = ($) => {
    const results = {
        organic: [],
        featured: null,
        ads: [],
        related: [],
        knowledge: null
    };
    
    // Organic results
    results.organic = $('.g').map((i, el) => {
        const $el = $(el);
        return {
            title: $el.find('h3').text().trim(),
            url: $el.find('a').attr('href'),
            description: $el.find('.VwiC3b, .s3v9rd').text().trim(),
            position: i + 1
        };
    }).get();
    
    // Featured snippet
    const featuredSnippet = $('.g .xpdopen');
    if (featuredSnippet.length) {
        results.featured = {
            title: featuredSnippet.find('h3').text().trim(),
            description: featuredSnippet.find('.hgKElc').text().trim(),
            url: featuredSnippet.find('a').attr('href')
        };
    }
    
    // Ads
    results.ads = $('.uEierd').map((i, el) => {
        const $el = $(el);
        return {
            title: $el.find('h3').text().trim(),
            url: $el.find('a').attr('href'),
            description: $el.find('.MUxGbd').text().trim()
        };
    }).get();
    
    // Related searches
    results.related = $('.k8XOCe').map((i, el) => {
        return $(el).text().trim();
    }).get();
    
    // Knowledge panel
    const knowledgePanel = $('.kp-blk');
    if (knowledgePanel.length) {
        results.knowledge = {
            title: knowledgePanel.find('.qrShPb').text().trim(),
            description: knowledgePanel.find('.kno-rdesc').text().trim(),
            details: knowledgePanel.find('.w8qArf').map((i, el) => {
                return $(el).text().trim();
            }).get()
        };
    }
    
    return results;
};
```

## Best Practices

### 1. Request Rate Management
```javascript
// Implement proper delays between requests
const crawler = new CheerioCrawler({
    proxyConfiguration: await Actor.createProxyConfiguration({
        groups: ['GOOGLE_SERP']
    }),
    minConcurrency: 1,
    maxConcurrency: 3, // Lower concurrency for Google
    requestHandlerTimeoutSecs: 60,
    requestHandler: async ({ $, request }) => {
        // Process results
        const results = extractAllResults($);
        await Actor.pushData(results);
        
        // Add delay between requests
        await new Promise(resolve => setTimeout(resolve, 2000));
    }
});
```

### 2. Error Handling
```javascript
// Handle Google-specific errors
const handleGoogleErrors = async ({ response, request }) => {
    if (response.status === 429) {
        console.log('Rate limited, implementing backoff...');
        await new Promise(resolve => setTimeout(resolve, 60000)); // 1 minute
        throw new Error('Rate limited - will retry');
    }
    
    if (response.status === 503) {
        console.log('Service unavailable, switching proxy...');
        throw new Error('Service unavailable - will retry with new proxy');
    }
    
    if (response.body.includes('Our systems have detected unusual traffic')) {
        console.log('Detected as bot, implementing longer delay...');
        await new Promise(resolve => setTimeout(resolve, 300000)); // 5 minutes
        throw new Error('Bot detection - will retry after delay');
    }
};
```

### 3. Results Validation
```javascript
// Validate extracted results
const validateResults = (results) => {
    const issues = [];
    
    if (!results.organic || results.organic.length === 0) {
        issues.push('No organic results found');
    }
    
    if (results.organic.some(r => !r.title || !r.url)) {
        issues.push('Some results missing title or URL');
    }
    
    if (issues.length > 0) {
        console.warn('Result validation issues:', issues);
    }
    
    return issues.length === 0;
};
```

## Pricing Considerations

### Request-Based Billing
- **Per-request pricing**: Charged for each search request
- **No data volume charges**: Unlike residential proxies
- **Cost predictability**: Fixed cost per search query

### Cost Optimization
```javascript
// Optimize costs by batching queries
const batchQueries = (queries, batchSize = 10) => {
    const batches = [];
    for (let i = 0; i < queries.length; i += batchSize) {
        batches.push(queries.slice(i, i + batchSize));
    }
    return batches;
};

// Process in batches with delays
const processBatches = async (queries) => {
    const batches = batchQueries(queries, 10);
    
    for (let i = 0; i < batches.length; i++) {
        console.log(`Processing batch ${i + 1}/${batches.length}`);
        
        await Promise.all(batches[i].map(query => processQuery(query)));
        
        // Delay between batches
        if (i < batches.length - 1) {
            await new Promise(resolve => setTimeout(resolve, 10000));
        }
    }
};
```

## Troubleshooting

### Common Issues
```javascript
// Debug Google SERP issues
const debugGoogleScraping = async (query) => {
    const proxyConfig = await Actor.createProxyConfiguration({
        groups: ['GOOGLE_SERP'],
        countryCode: 'US'
    });
    
    try {
        const response = await fetch(buildSearchUrl(query), {
            proxy: proxyConfig.newUrl()
        });
        
        console.log('Response status:', response.status);
        console.log('Response headers:', Object.fromEntries(response.headers));
        
        const html = await response.text();
        
        if (html.includes('detected unusual traffic')) {
            console.log('Bot detection triggered');
        } else if (html.includes('did not match any documents')) {
            console.log('No results found for query');
        } else {
            console.log('Response appears normal');
        }
        
    } catch (error) {
        console.error('Debug error:', error);
    }
};
```

### Monitoring Success Rates
```javascript
// Track scraping success rates
class GoogleSerpMonitor {
    constructor() {
        this.totalRequests = 0;
        this.successfulRequests = 0;
        this.errorCounts = {};
    }
    
    recordRequest(success, error = null) {
        this.totalRequests++;
        
        if (success) {
            this.successfulRequests++;
        } else if (error) {
            this.errorCounts[error.message] = (this.errorCounts[error.message] || 0) + 1;
        }
    }
    
    getStats() {
        const successRate = this.totalRequests > 0 
            ? (this.successfulRequests / this.totalRequests * 100).toFixed(2)
            : 0;
            
        return {
            successRate: `${successRate}%`,
            totalRequests: this.totalRequests,
            errors: this.errorCounts
        };
    }
}
```

Google SERP proxy provides specialized access to Google search results with country-specific targeting and request-based pricing, making it ideal for SEO research, market analysis, and competitive intelligence.