# Programming Interface | Platform | Apify Documentation

## Overview

The Programming Interface section provides comprehensive guidance for building Apify Actors, covering essential interfaces and features provided by Apify SDKs that work both locally and on the Apify platform.

## Key Sections

### 1. Basic Commands
Essential commands for initializing, running, and managing Actors:
- Actor initialization and configuration
- Input/output operations
- Storage management
- Exit and status handling

### 2. Environment Variables
Pre-defined environment variables for Actor context:
- Platform-specific variables
- Actor run information
- Resource limits and configuration
- Authentication and API access

### 3. Status Messages
Communicating Actor progress and state:
- Progress reporting
- Custom status messages
- Error handling and logging
- Real-time updates

### 4. System Events
Handling platform and system events:
- Actor lifecycle events
- Resource management events
- Error and timeout handling
- Event-driven programming

### 5. Container Web Server
Running web servers within Actors:
- HTTP server implementation
- Request handling
- API endpoint creation
- Interactive Actor interfaces

### 6. Metamorph
Transforming Actor runs dynamically:
- Actor transformation capabilities
- Dynamic run modification
- Workflow orchestration
- Advanced Actor patterns

### 7. Standby Mode
Using Actors as lightweight API servers:
- Persistent Actor instances
- API server implementation
- Request-response patterns
- Resource optimization

## Purpose and Benefits

The programming interface helps developers:

### Provide Context
- **Actor behavior**: Understand how Actors operate
- **Platform integration**: Leverage platform-specific features
- **Resource management**: Optimize resource usage

### Use Pre-defined Variables
- **Environment configuration**: Access platform-provided variables
- **Run context**: Get information about current Actor run
- **System resources**: Monitor available resources

### Communicate Progress
- **Status updates**: Report Actor progress in real-time
- **Error reporting**: Handle and report errors effectively
- **User feedback**: Provide meaningful updates to users

### Advanced Features
- **Web server capabilities**: Create interactive Actors
- **Dynamic transformation**: Modify Actor behavior at runtime
- **API server mode**: Use Actors as persistent services

## SDK Support

These interfaces are provided by:
- **Apify SDK for JavaScript**: Full-featured SDK for Node.js
- **Apify SDK for Python**: Complete Python implementation
- **Cross-platform compatibility**: Consistent behavior across environments

## Development Environments

The programming interface works in:
- **Local development**: Full functionality during development
- **Apify platform**: Enhanced features and platform integration
- **CI/CD pipelines**: Automated testing and deployment

## Technical Integration

### JavaScript Example
```javascript
const { Actor } = require('apify');

Actor.main(async () => {
    // Access programming interface features
    const input = await Actor.getInput();
    await Actor.setStatusMessage('Processing...');
    
    // Your Actor logic here
    
    await Actor.pushData(results);
});
```

### Python Example
```python
from apify import Actor

async def main():
    async with Actor:
        # Access programming interface features
        input_data = await Actor.get_input()
        await Actor.set_status_message('Processing...')
        
        # Your Actor logic here
        
        await Actor.push_data(results)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

## Best Practices

1. **Use appropriate interfaces**: Choose the right programming interface for your use case
2. **Handle errors gracefully**: Implement proper error handling for all operations
3. **Provide status updates**: Keep users informed about Actor progress
4. **Optimize resource usage**: Use environment variables and system events effectively
5. **Follow SDK patterns**: Use established patterns for consistency

The programming interface provides a comprehensive foundation for building sophisticated web scraping and automation tools using the Apify platform, with detailed documentation for each specific feature area.