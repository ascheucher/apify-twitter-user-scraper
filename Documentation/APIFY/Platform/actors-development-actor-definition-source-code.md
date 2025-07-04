# Source Code | Platform | Apify Documentation

## Overview

Source code configuration defines how your Actor's code is organized and executed. The structure is defined by the Actor's Dockerfile and supports any programming language and technologies.

## Source Code Placement

### Conventional Structure
- **Location**: Conventionally placed in the `/src` directory
- **Flexibility**: Can be organized according to your project needs
- **Language Support**: Supports any programming language and technologies

### Dockerfile Definition
The source code structure is defined by the Actor's Dockerfile, which specifies:
- How to copy source files
- Where to place them in the container
- How to execute the Actor

## Dockerfile Example

Here's a typical Dockerfile for a JavaScript Actor:

```dockerfile
FROM apify/actor-node:20
COPY package*.json ./
RUN npm install --omit=dev --omit=optional
COPY . ./
CMD npm start --silent
```

## Build Optimization Strategies

### 1. Copy Dependencies First
```dockerfile
# Copy package files first
COPY package*.json ./
# Install dependencies
RUN npm install --omit=dev --omit=optional
# Copy source code after dependencies
COPY . ./
```

### 2. Leverage Docker Caching
- **Strategy**: Copy `package.json` and `package-lock.json` before full source code
- **Benefit**: Reduces build times by leveraging Docker's caching mechanism
- **Result**: Dependencies only reinstall when package files change

## Package.json Configuration

Example `package.json` for a Node.js Actor:

```json
{
    "name": "getting-started-node",
    "scripts": {
        "start": "node src/main.js",
        "test": "echo \"Error: oops, the Actor has no tests yet, sad!\" && exit 1"
    }
}
```

### Key Elements
- **`start` script**: Defines how to execute the Actor
- **`test` script**: Defines how to run tests (optional)
- **Dependencies**: List required packages for the Actor

## Key Requirements

### 1. Dockerfile
- **Must define a Dockerfile** that builds the image
- **Must include all dependencies** and source code
- **Must specify a start command** to execute the Actor

### 2. Entry Point
- **Define clear entry point**: Specify how the Actor starts
- **Use appropriate commands**: `npm start`, `python main.py`, etc.
- **Handle errors gracefully**: Implement proper error handling

### 3. Dependencies
- **Include all required dependencies** in the build process
- **Optimize dependency installation** for faster builds
- **Use lock files** for consistent dependency versions

## Best Practices

### 1. Project Structure
```
actor-project/
├── src/
│   ├── main.js          # Entry point
│   ├── utils/           # Utility functions
│   └── config/          # Configuration files
├── package.json         # Node.js dependencies
├── package-lock.json    # Lock file
└── Dockerfile          # Build instructions
```

### 2. Build Optimization
- **Layer caching**: Structure Dockerfile to maximize Docker layer caching
- **Minimize layers**: Combine related commands to reduce image size
- **Use .dockerignore**: Exclude unnecessary files from build context

### 3. Code Organization
- **Modular structure**: Organize code in logical modules
- **Configuration management**: Separate configuration from code
- **Error handling**: Implement comprehensive error handling

## Example Source Code Structure

### JavaScript Actor
```javascript
// src/main.js
const { Actor } = require('apify');

Actor.main(async () => {
    const input = await Actor.getInput();
    console.log('Input:', input);
    
    // Your Actor logic here
    
    await Actor.pushData({ 
        message: 'Hello from Actor!' 
    });
});
```

### Python Actor
```python
# src/main.py
from apify import Actor

async def main():
    async with Actor:
        actor_input = await Actor.get_input()
        print('Input:', actor_input)
        
        # Your Actor logic here
        
        await Actor.push_data({
            'message': 'Hello from Actor!'
        })

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

The source code configuration provides maximum flexibility while maintaining clear guidelines for structuring and building Apify Actors across different programming languages and use cases.