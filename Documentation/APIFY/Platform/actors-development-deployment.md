# Deployment | Platform | Apify Documentation

## Overview

Deployment involves uploading source code and building an Actor on the Apify platform, allowing you to run and scale your Actors in the cloud. The deployment process transforms your local code into a runnable Actor that can be executed on Apify's infrastructure.

## Deployment Methods

### 1. Using Apify CLI (Recommended)

The Apify CLI is the most convenient method for deploying Actors:

#### Installation
```bash
npm install -g apify-cli
```

#### Basic Deployment Process
```bash
# 1. Log in to your Apify account
apify login

# 2. Navigate to your Actor directory
cd my-actor

# 3. Deploy the Actor
apify push
```

#### Features
- **Automatic upload**: Uploads source code as "multiple source files"
- **File size support**: Supports files up to 3 MB
- **Version management**: Automatically handles versioning
- **Build triggering**: Automatically triggers builds after upload

#### Advanced CLI Usage
```bash
# Deploy with specific version tag
apify push --tag=beta

# Deploy with custom build configuration
apify push --build-tag=latest

# Deploy to specific Actor (if you have multiple)
apify push --actor-id=my-actor-id
```

### 2. Pulling an Existing Actor

You can pull existing Actors for modification and redeployment:

```bash
# Pull latest version
apify pull [ACTOR_ID]

# Pull specific version
apify pull [ACTOR_ID] --version=1.2

# Pull to specific directory
apify pull [ACTOR_ID] --dir=./my-actor
```

#### Use Cases
- **Forking Actors**: Create your own version of existing Actors
- **Collaboration**: Work with team members on shared Actors
- **Updates**: Pull latest changes from upstream Actors

## Alternative Deployment Options

### Git Repository
Connect your Actor to a Git repository for automated deployments:

#### Setup Process
1. **Create repository**: Push your Actor code to a Git repository
2. **Configure Actor**: Link Actor to the repository in Apify Console
3. **Set up webhooks**: Configure automatic builds on code changes

#### Supported Platforms
- **GitHub**: Full integration with GitHub Actions
- **GitLab**: Support for GitLab CI/CD
- **Bitbucket**: Integration with Bitbucket Pipelines
- **Custom Git**: Any Git repository with webhook support

#### Example Configuration
```javascript
// .actor/actor.json
{
    "actorSpecification": 1,
    "name": "my-actor",
    "version": "1.0.0",
    "buildTag": "latest",
    "environmentVariables": {},
    "dockerfile": "./Dockerfile",
    "readme": "./README.md",
    "input": "./input_schema.json",
    "storages": {
        "dataset": "./dataset_schema.json"
    }
}
```

### GitHub Gist
Use GitHub Gists for simple, single-file Actors:

#### Process
1. **Create Gist**: Create a new Gist at github.com/gist
2. **Add files**: Include your Actor code and configuration
3. **Link to Actor**: Use the Gist URL in Actor configuration

#### Example Files
- `main.js`: Your Actor code
- `package.json`: Dependencies
- `README.md`: Documentation
- `INPUT_SCHEMA.json`: Input schema

### Zip File
Deploy from a zip file hosted on an external URL:

#### Use Cases
- **Large files**: Automatically used when source exceeds 3MB via CLI
- **External hosting**: Deploy from files hosted elsewhere
- **Batch uploads**: Upload multiple files at once

#### Requirements
- **Accessible URL**: Zip file must be publicly accessible
- **File structure**: Must contain proper Actor structure
- **Main file**: Requires `main.js` if no custom Dockerfile

## Deployment Configuration

### Actor Structure
```
my-actor/
├── .actor/
│   ├── actor.json          # Actor configuration
│   ├── Dockerfile          # Custom Dockerfile (optional)
│   └── README.md           # Actor documentation
├── src/
│   ├── main.js             # Entry point
│   ├── utils.js            # Utility functions
│   └── config.js           # Configuration
├── package.json            # Dependencies
├── package-lock.json       # Dependency lock
└── README.md               # Main documentation
```

### Actor Configuration (actor.json)
```json
{
    "actorSpecification": 1,
    "name": "my-web-scraper",
    "version": "1.0.0",
    "buildTag": "latest",
    "environmentVariables": {
        "NODE_ENV": "production"
    },
    "dockerfile": "./Dockerfile",
    "readme": "./README.md",
    "input": "./input_schema.json",
    "storages": {
        "dataset": "./dataset_schema.json"
    },
    "categories": ["ECOMMERCE"],
    "defaultRunOptions": {
        "build": "latest",
        "memoryMbytes": 1024,
        "timeoutSecs": 3600
    }
}
```

## Build Process

### Automatic Builds
- **Trigger**: Builds are automatically triggered on deployment
- **Docker**: Uses Docker to create container images
- **Caching**: Leverages Docker layer caching for efficiency
- **Versioning**: Each build gets a unique version tag

### Build Configuration
```dockerfile
# Example Dockerfile
FROM apify/actor-node:20

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install --only=prod --no-optional

# Copy source code
COPY . ./

# Set the start command
CMD npm start
```

## Environment Configuration

### Environment Variables
```bash
# Set environment variables during deployment
apify push --env NODE_ENV=production --env API_KEY=secret
```

### Configuration Files
```javascript
// src/config.js
const config = {
    apiKey: process.env.API_KEY,
    nodeEnv: process.env.NODE_ENV || 'development',
    debug: process.env.DEBUG === 'true'
};

module.exports = config;
```

## Version Management

### Semantic Versioning
```bash
# Deploy with version bump
apify push --version-number=1.2.3

# Deploy with automatic version increment
apify push --version-number=auto
```

### Build Tags
```bash
# Deploy to latest tag
apify push --tag=latest

# Deploy to beta tag
apify push --tag=beta

# Deploy to specific tag
apify push --tag=v1.0.0
```

## Monitoring Deployments

### Deployment Logs
```bash
# View deployment logs
apify logs

# View specific build logs
apify logs --build-id=BUILD_ID
```

### Build Status
```bash
# Check build status
apify builds list

# Get build details
apify builds info BUILD_ID
```

## Best Practices

### 1. Use Version Control
```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit"

# Deploy from clean state
apify push
```

### 2. Optimize Docker Builds
```dockerfile
# Use multi-stage builds for optimization
FROM node:18-alpine as builder
COPY package*.json ./
RUN npm ci --only=production

FROM apify/actor-node:20
COPY --from=builder /node_modules ./node_modules
COPY . ./
```

### 3. Test Before Deployment
```bash
# Run tests locally
npm test

# Test with Apify CLI
apify run --input='{"test": true}'

# Deploy after testing
apify push
```

### 4. Environment-specific Configuration
```javascript
// Use environment-specific settings
const config = {
    development: {
        logLevel: 'debug',
        timeout: 30000
    },
    production: {
        logLevel: 'info',
        timeout: 300000
    }
};

module.exports = config[process.env.NODE_ENV || 'development'];
```

## Troubleshooting

### Common Issues

#### Large File Sizes
```bash
# Check file sizes
du -sh ./*

# Use .apifyignore to exclude files
echo "node_modules/" >> .apifyignore
echo "*.log" >> .apifyignore
```

#### Build Failures
```bash
# Check build logs
apify logs --build-id=BUILD_ID

# Test Docker build locally
docker build -t my-actor .
docker run my-actor
```

#### Permission Issues
```bash
# Fix file permissions
chmod +x ./src/main.js

# Check file ownership
ls -la ./src/
```

## Deployment Workflow Example

```bash
# 1. Initialize Actor
apify create my-actor
cd my-actor

# 2. Develop locally
npm install
npm run dev

# 3. Test locally
apify run --input='{"url": "https://example.com"}'

# 4. Deploy to beta
apify push --tag=beta

# 5. Test beta version
apify run --build=beta --input='{"url": "https://example.com"}'

# 6. Deploy to production
apify push --tag=latest

# 7. Verify deployment
apify info
```

## Key Considerations

1. **File Size Limits**: Source files have a 3 MB size limit
2. **Build Time**: Optimize Dockerfile for faster builds
3. **Version Control**: Use proper version control practices
4. **Testing**: Always test before deploying to production
5. **Security**: Don't include sensitive data in source code
6. **Documentation**: Maintain clear documentation for your Actors

Deployment is a crucial step in the Actor development lifecycle, transforming your local code into a scalable, cloud-ready automation tool that can be shared and monetized on the Apify platform.