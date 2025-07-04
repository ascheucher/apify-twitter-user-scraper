# Builds | Platform | Apify Documentation

## Overview

A build creates a snapshot of an Actor's version, including source code and environment variables. This process generates a Docker image with all necessary dependencies, making it ready for execution.

## Build Process

### What Happens During a Build
- **Source code compilation**: Actor source code is processed and prepared
- **Docker image creation**: A complete Docker image is built with all dependencies
- **Environment setup**: Environment variables and configuration are included
- **Dependency installation**: All required packages and libraries are installed
- **Optimization**: Docker layers are optimized for performance

### Build Triggers
Builds can be triggered by:
- **Manual deployment**: Using Apify CLI or Console
- **Code changes**: Automatic builds via Git integration
- **API calls**: Programmatic build creation
- **Scheduled builds**: CI/CD pipeline triggers

## Build Numbers and Versioning

### Build Number Format
Build numbers follow the format: **MAJOR.MINOR.BUILD**

Example: `1.2.345`
- **MAJOR.MINOR**: Represents the Actor version (1.2)
- **BUILD**: Auto-incremented number starting at 1 (345)

### Semantic Versioning
Apify follows Semantic Versioning principles:
- **MAJOR**: Incompatible API changes
- **MINOR**: Backward-compatible functionality additions
- **PATCH**: Backward-compatible bug fixes

### Multiple Versions
You can maintain multiple versions simultaneously:
- **Production**: Version 1.1 (stable release)
- **Beta**: Version 1.2 (testing features)
- **Development**: Version 2.0 (next major release)

## Build Tags

### Purpose of Tags
Tags simplify specifying which build to use without remembering specific build numbers.

### Common Tags
- **`latest`**: Most recent stable build
- **`beta`**: Latest beta version for testing
- **`stable`**: Confirmed stable release
- **`dev`**: Development version

### Tag Management
```bash
# Create build with specific tag
apify push --tag=beta

# List builds with tags
apify builds list

# Use tagged build in run
apify run --build=latest
```

### Tag Constraints
- Only one build can be associated with a specific tag
- Assigning a tag to a new build removes it from the previous build
- Tags are case-sensitive

## Build Resources

### Default Build Resources
- **Timeout**: 1800 seconds (30 minutes)
- **Memory**: 4096 MB (4 GB)
- **Disk Space**: Varies based on plan

### Resource Configuration
```json
{
  "buildOptions": {
    "memoryMbytes": 4096,
    "timeoutSecs": 1800,
    "diskMbytes": 8192
  }
}
```

### Resource Optimization
```dockerfile
# Optimize Dockerfile for smaller builds
FROM apify/actor-node:20-alpine

# Multi-stage builds for size reduction
FROM node:18-alpine as builder
COPY package*.json ./
RUN npm ci --only=production

FROM apify/actor-node:20-alpine
COPY --from=builder /node_modules ./node_modules
COPY . ./
```

## Build Caching

### Cache Benefits
- **Faster builds**: Reuses previously built Docker layers
- **Resource efficiency**: Reduces build time and server load
- **Cost optimization**: Lower build costs due to reduced processing

### Enabling Cache
```bash
# Using CLI with cache
apify push --build-options='{"useCache": true}'

# Using API with cache
curl -X POST "https://api.apify.com/v2/acts/ACTOR_ID/builds" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"useCache": true, "tag": "latest"}'
```

### Cache Behavior
- **Best-effort basis**: Caching attempts but doesn't guarantee success
- **Layer reuse**: Docker layers are cached when possible
- **Dependency caching**: npm/pip packages cached between builds
- **Source code changes**: New source code invalidates relevant cache layers

### Cache Optimization Tips
```dockerfile
# Copy package files first for better caching
COPY package*.json ./
RUN npm install

# Copy source code after dependencies
COPY . ./
```

## Clean Builds

### When to Use Clean Builds
- **Cache issues**: When cached builds cause problems
- **Dependency updates**: After major dependency changes
- **Build corruption**: When builds fail unexpectedly
- **Security updates**: After base image updates

### Running Clean Builds
1. **Via Console**: Go to Source → Code → Start button dropdown → "Start clean build"
2. **Via API**: Set `useCache: false` in build options
3. **Via CLI**: Use `--no-cache` flag

```bash
# Clean build via CLI
apify push --build-options='{"useCache": false}'
```

## Build Management

### Creating Builds
```javascript
// Using Apify Client
const build = await apifyClient.actor('ACTOR_ID').builds().create({
  tag: 'latest',
  useCache: true,
  betaPackages: false
});
```

### Listing Builds
```javascript
// List all builds
const builds = await apifyClient.actor('ACTOR_ID').builds().list();

// List builds with specific status
const runningBuilds = builds.items.filter(build => build.status === 'RUNNING');
```

### Build Information
```javascript
// Get specific build details
const build = await apifyClient.actor('ACTOR_ID').build('BUILD_ID').get();

console.log('Build details:', {
  id: build.id,
  number: build.buildNumber,
  status: build.status,
  tag: build.tag,
  startedAt: build.startedAt,
  finishedAt: build.finishedAt
});
```

### Deleting Builds
```javascript
// Delete specific build
await apifyClient.actor('ACTOR_ID').build('BUILD_ID').delete();

// Delete builds older than 30 days
const oldDate = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000);
const builds = await apifyClient.actor('ACTOR_ID').builds().list();

for (const build of builds.items) {
  if (new Date(build.startedAt) < oldDate) {
    await apifyClient.actor('ACTOR_ID').build(build.id).delete();
  }
}
```

## Build Status and Monitoring

### Build Statuses
- **READY**: Build completed successfully, ready for use
- **RUNNING**: Build is currently in progress
- **FAILED**: Build failed due to errors
- **ABORTED**: Build was manually cancelled

### Monitoring Builds
```javascript
// Wait for build completion
const build = await apifyClient.actor('ACTOR_ID').build('BUILD_ID').waitForFinish();

// Get build log
const log = await apifyClient.actor('ACTOR_ID').build('BUILD_ID').log().get();

// Monitor build progress
const checkBuildStatus = async (buildId) => {
  const build = await apifyClient.actor('ACTOR_ID').build(buildId).get();
  
  if (build.status === 'RUNNING') {
    console.log('Build still running...');
    setTimeout(() => checkBuildStatus(buildId), 10000); // Check every 10 seconds
  } else {
    console.log(`Build finished with status: ${build.status}`);
  }
};
```

## Build Configuration

### Actor Configuration
```json
{
  "actorSpecification": 1,
  "name": "my-actor",
  "version": "1.0.0",
  "buildTag": "latest",
  "dockerfile": "./Dockerfile",
  "environmentVariables": {
    "NODE_ENV": "production"
  },
  "defaultRunOptions": {
    "build": "latest",
    "memoryMbytes": 1024,
    "timeoutSecs": 3600
  }
}
```

### Dockerfile Optimization
```dockerfile
# Use specific base image versions
FROM apify/actor-node:20.1.0

# Set working directory
WORKDIR /usr/src/app

# Copy package files for better caching
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production \
    && npm cache clean --force

# Copy source code
COPY . .

# Remove unnecessary files
RUN rm -rf tests/ docs/ *.md

# Set command
CMD ["npm", "start"]
```

## Best Practices

### 1. Version Management
```bash
# Use semantic versioning
git tag v1.2.3
apify push --version-number=1.2.3

# Maintain separate branches
git checkout -b feature/new-functionality
apify push --tag=feature-branch
```

### 2. Build Optimization
```dockerfile
# Layer optimization
FROM apify/actor-node:20
COPY package*.json ./
RUN npm ci --only=production
COPY src/ ./src/
COPY config/ ./config/
```

### 3. Resource Management
```javascript
// Monitor build resource usage
const build = await apifyClient.actor('ACTOR_ID').build('BUILD_ID').get();

if (build.stats.buildDurationSecs > 300) { // 5 minutes
  console.warn('Build taking longer than expected');
}
```

### 4. Error Handling
```javascript
// Handle build failures
try {
  const build = await apifyClient.actor('ACTOR_ID').builds().create({
    tag: 'latest',
    useCache: true
  });
  
  await build.waitForFinish();
  
  if (build.status === 'FAILED') {
    throw new Error(`Build failed: ${build.statusMessage}`);
  }
} catch (error) {
  console.error('Build error:', error);
  // Retry with clean build
  await apifyClient.actor('ACTOR_ID').builds().create({
    tag: 'latest',
    useCache: false
  });
}
```

## Troubleshooting

### Common Build Issues

#### Build Timeouts
```json
{
  "buildOptions": {
    "timeoutSecs": 3600,
    "memoryMbytes": 8192
  }
}
```

#### Dependency Issues
```dockerfile
# Clear npm cache
RUN npm cache clean --force

# Use specific package versions
COPY package-lock.json ./
RUN npm ci --only=production
```

#### Memory Issues
```dockerfile
# Increase Node.js memory limit
ENV NODE_OPTIONS="--max-old-space-size=4096"
```

### Build Debugging
```bash
# Get build logs
apify logs --build-id=BUILD_ID

# Test build locally
docker build -t test-build .
docker run test-build
```

## Build API

### Creating Builds
```javascript
const build = await apifyClient.actor('ACTOR_ID').builds().create({
  tag: 'latest',
  useCache: true,
  betaPackages: false
});
```

### Build Information
```javascript
const build = await apifyClient.actor('ACTOR_ID').build('BUILD_ID').get();
```

### Build Logs
```javascript
const log = await apifyClient.actor('ACTOR_ID').build('BUILD_ID').log().get();
```

Builds are fundamental to the Actor development process, providing versioned, reproducible environments for your automation code. Understanding build management, caching, and optimization is crucial for efficient Actor development and deployment.