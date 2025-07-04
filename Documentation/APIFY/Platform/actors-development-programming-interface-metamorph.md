# Metamorph | Platform | Apify Documentation

## Overview

Metamorph is an Apify platform operation that transforms an Actor run into another Actor run with new input. This powerful feature enables dynamic Actor chaining and transformation during execution.

## How Metamorph Works

### Transformation Process
1. **Stops current Docker container**: The currently running Actor container is terminated
2. **Starts new container**: Launches a new container with a different Docker image
3. **Preserves default storages**: Maintains access to existing datasets and key-value stores
4. **Stores new input**: Places the new input under the `_INPUT-METAMORPH-1_` key in the default key-value store

### Key Characteristics
- **Seamless transition**: Users see a single continuous run
- **Storage persistence**: All data from the original run remains accessible
- **Input preservation**: Original input is preserved, new input is stored separately
- **Limited transformations**: Number of metamorph operations per run is limited

## Benefits of Metamorph

### 1. Build New Actors on Existing Ones
- Extend functionality of existing Actors
- Create specialized versions without duplicating code
- Implement progressive enhancement patterns

### 2. Improve Input Structure
- Transform legacy input formats to modern schemas
- Add validation and preprocessing steps
- Normalize input data before main processing

### 3. Maintain User Transparency
- Single run ID for the entire process
- Continuous execution from user perspective
- Unified billing and monitoring

### 4. Seamless Actor Chaining
- Chain multiple Actors in sequence
- Pass data between different Actor types
- Create complex workflows

## Implementation

### JavaScript Example
```javascript
const { Actor } = require('apify');

Actor.main(async () => {
    // Get original input
    const input = await Actor.getInput();
    console.log('Original input:', input);
    
    // Process and transform input
    const { hotelUrl } = input;
    
    // Create new input for the target Actor
    const newInput = {
        startUrls: [{ url: hotelUrl }],
        pageFunction: () => {
            // Scrape hotel reviews
            return [...document.querySelectorAll('.review')].map(el => ({
                rating: el.querySelector('.rating').textContent,
                text: el.querySelector('.review-text').textContent,
                author: el.querySelector('.author').textContent
            }));
        },
        proxyConfiguration: {
            useApifyProxy: true
        }
    };
    
    // Metamorph to the web scraper
    console.log('Metamorphing to web scraper...');
    await Actor.metamorph('apify/web-scraper', newInput);
});
```

### Python Example
```python
from apify import Actor

async def main():
    async with Actor:
        # Get original input
        input_data = await Actor.get_input()
        print('Original input:', input_data)
        
        # Process and transform input
        hotel_url = input_data.get('hotelUrl')
        
        # Create new input for the target Actor
        new_input = {
            'startUrls': [{'url': hotel_url}],
            'pageFunction': '''
                () => {
                    // Scrape hotel reviews
                    return [...document.querySelectorAll('.review')].map(el => ({
                        rating: el.querySelector('.rating').textContent,
                        text: el.querySelector('.review-text').textContent,
                        author: el.querySelector('.author').textContent
                    }));
                }
            ''',
            'proxyConfiguration': {
                'useApifyProxy': True
            }
        }
        
        # Metamorph to the web scraper
        print('Metamorphing to web scraper...')
        await Actor.metamorph('apify/web-scraper', new_input)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

## Advanced Use Cases

### Input Validation and Preprocessing
```javascript
Actor.main(async () => {
    const input = await Actor.getInput();
    
    // Validate input
    if (!input || !input.url) {
        throw new Error('URL is required');
    }
    
    // Preprocess input
    const processedInput = {
        startUrls: [{ url: input.url }],
        maxRequestsPerCrawl: input.maxPages || 100,
        pageFunction: input.customPageFunction || defaultPageFunction,
        proxyConfiguration: {
            useApifyProxy: true,
            groups: input.proxyGroups || ['RESIDENTIAL']
        }
    };
    
    // Add additional configuration based on URL
    if (input.url.includes('ecommerce')) {
        processedInput.requestInterceptors = [ecommerceInterceptor];
    }
    
    // Metamorph to specialized scraper
    await Actor.metamorph('my-company/specialized-scraper', processedInput);
});
```

### Dynamic Actor Selection
```javascript
Actor.main(async () => {
    const input = await Actor.getInput();
    
    // Determine target Actor based on input
    let targetActor;
    let transformedInput;
    
    if (input.type === 'social-media') {
        targetActor = 'apify/social-media-scraper';
        transformedInput = {
            platform: input.platform,
            queries: input.keywords,
            maxItems: input.limit
        };
    } else if (input.type === 'ecommerce') {
        targetActor = 'apify/ecommerce-scraper';
        transformedInput = {
            startUrls: input.urls,
            maxItems: input.limit,
            extractImages: input.includeImages
        };
    } else {
        targetActor = 'apify/web-scraper';
        transformedInput = {
            startUrls: input.urls,
            pageFunction: input.pageFunction
        };
    }
    
    console.log(`Metamorphing to ${targetActor}`);
    await Actor.metamorph(targetActor, transformedInput);
});
```

### Progressive Enhancement
```javascript
Actor.main(async () => {
    const input = await Actor.getInput();
    
    // Stage 1: Basic data collection
    console.log('Stage 1: Collecting basic data...');
    const basicData = await collectBasicData(input);
    
    // Store intermediate results
    await Actor.pushData(basicData);
    
    // Stage 2: Enhanced processing
    const enhancedInput = {
        ...input,
        basicData: basicData,
        enhancedProcessing: true,
        additionalFields: ['detailed_info', 'related_items']
    };
    
    console.log('Stage 2: Enhanced processing...');
    await Actor.metamorph('my-company/enhanced-processor', enhancedInput);
});
```

## Best Practices

### 1. Use Actor.getInput() Instead of Actor.getValue('INPUT')
```javascript
// Correct: Handles metamorph input automatically
const input = await Actor.getInput();

// Incorrect: May not get the correct input after metamorph
const input = await Actor.getValue('INPUT');
```

### 2. Preserve Original Input Context
```javascript
Actor.main(async () => {
    const input = await Actor.getInput();
    
    // Store original input for reference
    await Actor.setValue('original_input', input);
    
    // Transform input
    const newInput = {
        ...transformInput(input),
        metadata: {
            originalInput: input,
            transformedAt: new Date().toISOString(),
            transformedBy: 'input-transformer-v1'
        }
    };
    
    await Actor.metamorph('target-actor', newInput);
});
```

### 3. Handle Metamorph Limits
```javascript
Actor.main(async () => {
    const input = await Actor.getInput();
    
    // Check if we've already metamorphed
    const metamorphCount = input.metadata?.metamorphCount || 0;
    
    if (metamorphCount >= 5) {
        console.log('Metamorph limit reached, processing directly');
        await processDirect(input);
    } else {
        const newInput = {
            ...input,
            metadata: {
                ...input.metadata,
                metamorphCount: metamorphCount + 1
            }
        };
        
        await Actor.metamorph('next-actor', newInput);
    }
});
```

### 4. Error Handling
```javascript
Actor.main(async () => {
    try {
        const input = await Actor.getInput();
        
        // Validate target Actor exists
        if (!await validateActorExists('target-actor')) {
            throw new Error('Target Actor not found');
        }
        
        const newInput = transformInput(input);
        await Actor.metamorph('target-actor', newInput);
        
    } catch (error) {
        console.error('Metamorph failed:', error);
        
        // Fallback to direct processing
        await processDirect(input);
    }
});
```

## Common Patterns

### 1. Input Adapter Pattern
```javascript
// Create adapters for different input formats
const inputAdapters = {
    'v1': (input) => ({
        startUrls: input.urls,
        pageFunction: input.extractorFunction
    }),
    'v2': (input) => ({
        startUrls: input.targetUrls,
        pageFunction: input.pageFunction,
        proxyConfiguration: input.proxy
    })
};

Actor.main(async () => {
    const input = await Actor.getInput();
    const version = input.version || 'v1';
    
    const adaptedInput = inputAdapters[version](input);
    await Actor.metamorph('standardized-scraper', adaptedInput);
});
```

### 2. Feature Flag Pattern
```javascript
Actor.main(async () => {
    const input = await Actor.getInput();
    
    // Use feature flags to determine Actor variant
    const useNewVersion = input.features?.newVersion || false;
    const targetActor = useNewVersion ? 'scraper-v2' : 'scraper-v1';
    
    await Actor.metamorph(targetActor, input);
});
```

## Important Considerations

1. **Runtime Limits**: There are limits on how many times you can metamorph a single run
2. **Storage Access**: New Actor has access to all storages from the original run
3. **Input Preservation**: Original input is preserved and accessible
4. **Resource Usage**: Each metamorph counts towards your resource consumption
5. **Debugging**: Use logs and stored data to track metamorph chain

## Troubleshooting

### Check Metamorph Chain
```javascript
// Track metamorph operations
const metamorphHistory = await Actor.getValue('metamorph_history') || [];
metamorphHistory.push({
    from: process.env.ACTOR_ID,
    to: 'target-actor',
    timestamp: new Date().toISOString(),
    input: newInput
});
await Actor.setValue('metamorph_history', metamorphHistory);
```

### Debug Input Issues
```javascript
// Log input sources for debugging
const currentInput = await Actor.getInput();
const originalInput = await Actor.getValue('INPUT');
const metamorphInput = await Actor.getValue('_INPUT-METAMORPH-1_');

console.log('Current input:', currentInput);
console.log('Original input:', originalInput);
console.log('Metamorph input:', metamorphInput);
```

Metamorph is a powerful feature that enables sophisticated Actor orchestration and dynamic workflow management, making it possible to create flexible, composable automation solutions.