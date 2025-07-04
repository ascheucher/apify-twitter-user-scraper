# Continuous Integration | Platform | Apify Documentation

## Overview

Continuous Integration (CI) for Actors on Apify automates the build, test, and deployment process, reducing manual work and potential errors. This setup ensures your Actors are automatically built and deployed when code changes are made.

## Key Steps for CI Setup

### 1. Create a GitHub Repository

First, create a GitHub repository for your Actor code:

```bash
# Initialize repository
git init
git add .
git commit -m "Initial commit"

# Create GitHub repository and push
git remote add origin https://github.com/username/my-actor.git
git push -u origin main
```

### 2. Obtain Apify API Token

1. **Navigate to Apify Console**: Go to your Apify account settings
2. **Generate API token**: Create a new API token with appropriate permissions
3. **Copy token**: Save the token securely for use in CI configuration

### 3. Configure GitHub Secrets

Add required secrets to your GitHub repository:

1. **Go to repository settings**: Navigate to Settings → Secrets and variables → Actions
2. **Add secrets**:
   - `APIFY_TOKEN`: Your Apify API token
   - `LATEST_BUILD_URL`: Build Actor API endpoint URL for production
   - `BETA_BUILD_URL`: Build Actor API endpoint URL for beta (optional)

### 4. Create GitHub Actions Workflow Files

Create workflow files in `.github/workflows/` directory:

#### Latest Version Workflow (`latest.yml`)
```yaml
name: Test and build latest version
on:
  push:
    branches:
      - master
      - main
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
        
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '18'
          
      - name: Install dependencies
        run: npm install
        
      - name: Run tests
        run: npm run test
        
      - name: Build Actor
        uses: distributhor/workflow-webhook@v1
        env:
          webhook_url: ${{ secrets.LATEST_BUILD_URL }}
          webhook_secret: ${{ secrets.APIFY_TOKEN }}
```

#### Beta Version Workflow (`beta.yml`)
```yaml
name: Test and build beta version
on:
  push:
    branches:
      - develop
      - beta
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
        
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '18'
          
      - name: Install dependencies
        run: npm install
        
      - name: Run tests
        run: npm run test
        
      - name: Build Actor
        uses: distributhor/workflow-webhook@v1
        env:
          webhook_url: ${{ secrets.BETA_BUILD_URL }}
          webhook_secret: ${{ secrets.APIFY_TOKEN }}
```

## Advanced CI Configuration

### Comprehensive Testing Workflow
```yaml
name: Comprehensive CI/CD
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [16, 18, 20]
        
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
        
      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v2
        with:
          node-version: ${{ matrix.node-version }}
          
      - name: Cache dependencies
        uses: actions/cache@v2
        with:
          path: ~/.npm
          key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
          
      - name: Install dependencies
        run: npm ci
        
      - name: Run linter
        run: npm run lint
        
      - name: Run tests
        run: npm run test
        
      - name: Run security audit
        run: npm audit
        
      - name: Build Actor locally
        run: npm run build
        
  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - name: Deploy to Apify
        uses: distributhor/workflow-webhook@v1
        env:
          webhook_url: ${{ secrets.LATEST_BUILD_URL }}
          webhook_secret: ${{ secrets.APIFY_TOKEN }}
```

### Multi-Environment Deployment
```yaml
name: Multi-environment deployment
on:
  push:
    branches: [main, develop, staging]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
        
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '18'
          
      - name: Install and test
        run: |
          npm ci
          npm run test
          
      - name: Deploy to production
        if: github.ref == 'refs/heads/main'
        uses: distributhor/workflow-webhook@v1
        env:
          webhook_url: ${{ secrets.PRODUCTION_BUILD_URL }}
          webhook_secret: ${{ secrets.APIFY_TOKEN }}
          
      - name: Deploy to staging
        if: github.ref == 'refs/heads/staging'
        uses: distributhor/workflow-webhook@v1
        env:
          webhook_url: ${{ secrets.STAGING_BUILD_URL }}
          webhook_secret: ${{ secrets.APIFY_TOKEN }}
          
      - name: Deploy to development
        if: github.ref == 'refs/heads/develop'
        uses: distributhor/workflow-webhook@v1
        env:
          webhook_url: ${{ secrets.DEVELOPMENT_BUILD_URL }}
          webhook_secret: ${{ secrets.APIFY_TOKEN }}
```

## GitHub Integration Setup

### Additional GitHub Integration Steps

1. **Copy Build Actor API endpoint URL**: From Apify Console
2. **Add webhook in repository settings**:
   - Go to Settings → Webhooks
   - Click "Add webhook"
   - Paste API URL in "Payload URL" field
   - Set content type to "application/json"
   - Select events that trigger the webhook

### Webhook Configuration
```json
{
  "name": "web",
  "active": true,
  "events": ["push", "pull_request"],
  "config": {
    "url": "https://api.apify.com/v2/acts/YOUR_ACTOR_ID/builds",
    "content_type": "application/json",
    "secret": "YOUR_APIFY_TOKEN"
  }
}
```

## Testing Strategies

### Unit Testing
```javascript
// tests/main.test.js
const { Actor } = require('apify');
const { main } = require('../src/main');

describe('Actor Main Function', () => {
    beforeAll(async () => {
        await Actor.init();
    });

    afterAll(async () => {
        await Actor.exit();
    });

    test('should process input correctly', async () => {
        const mockInput = { url: 'https://example.com' };
        Actor.getInput = jest.fn().mockResolvedValue(mockInput);
        
        await main();
        
        expect(Actor.getInput).toHaveBeenCalled();
    });
});
```

### Integration Testing
```javascript
// tests/integration.test.js
const { Actor } = require('apify');

describe('Integration Tests', () => {
    test('should scrape and store data', async () => {
        await Actor.init();
        
        const input = { url: 'https://example.com' };
        await Actor.call('YOUR_ACTOR_ID', input);
        
        const dataset = await Actor.openDataset();
        const { items } = await dataset.getData();
        
        expect(items.length).toBeGreaterThan(0);
        
        await Actor.exit();
    });
});
```

### End-to-End Testing
```yaml
# .github/workflows/e2e.yml
name: End-to-End Tests
on:
  schedule:
    - cron: '0 2 * * *' # Daily at 2 AM
  workflow_dispatch:

jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
        
      - name: Run E2E tests
        run: |
          npm ci
          npm run test:e2e
        env:
          APIFY_TOKEN: ${{ secrets.APIFY_TOKEN }}
          ACTOR_ID: ${{ secrets.ACTOR_ID }}
```

## Quality Assurance

### Code Quality Checks
```yaml
# .github/workflows/quality.yml
name: Code Quality
on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
        
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '18'
          
      - name: Install dependencies
        run: npm ci
        
      - name: Run ESLint
        run: npm run lint
        
      - name: Run Prettier
        run: npm run format:check
        
      - name: Run type checking
        run: npm run type-check
        
      - name: Security audit
        run: npm audit --audit-level=moderate
        
      - name: Check bundle size
        run: npm run bundle-size
```

### Performance Testing
```javascript
// tests/performance.test.js
const { Actor } = require('apify');

describe('Performance Tests', () => {
    test('should complete within time limit', async () => {
        const startTime = Date.now();
        
        await Actor.init();
        // Run your Actor logic
        const result = await runActor();
        await Actor.exit();
        
        const duration = Date.now() - startTime;
        expect(duration).toBeLessThan(60000); // 1 minute max
    });
});
```

## Deployment Notifications

### Slack Notifications
```yaml
- name: Notify Slack
  if: always()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    text: 'Actor deployment completed'
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### Email Notifications
```yaml
- name: Send email notification
  if: failure()
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 465
    username: ${{ secrets.EMAIL_USERNAME }}
    password: ${{ secrets.EMAIL_PASSWORD }}
    subject: 'Actor deployment failed'
    body: 'The Actor deployment has failed. Please check the logs.'
    to: team@company.com
```

## Best Practices

### 1. Environment Management
```yaml
# Use environment-specific configurations
- name: Set environment variables
  run: |
    echo "NODE_ENV=production" >> $GITHUB_ENV
    echo "LOG_LEVEL=info" >> $GITHUB_ENV
```

### 2. Dependency Management
```yaml
# Cache dependencies for faster builds
- name: Cache node modules
  uses: actions/cache@v2
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

### 3. Security
```yaml
# Never log secrets
- name: Deploy without logging secrets
  run: |
    curl -X POST "${{ secrets.BUILD_URL }}" \
      -H "Authorization: Bearer ${{ secrets.APIFY_TOKEN }}" \
      -H "Content-Type: application/json" \
      -d '{"tag": "latest"}'
```

### 4. Rollback Strategy
```yaml
# Implement rollback capability
- name: Rollback on failure
  if: failure()
  run: |
    # Rollback to previous version
    curl -X POST "${{ secrets.ROLLBACK_URL }}" \
      -H "Authorization: Bearer ${{ secrets.APIFY_TOKEN }}"
```

## Monitoring and Alerting

### Build Status Monitoring
```yaml
- name: Check build status
  run: |
    BUILD_ID=$(curl -s "${{ secrets.BUILD_STATUS_URL }}" | jq -r '.data.id')
    echo "Build ID: $BUILD_ID"
    
    # Wait for build completion
    while [ "$(curl -s "${{ secrets.BUILD_STATUS_URL }}/$BUILD_ID" | jq -r '.data.status')" == "RUNNING" ]; do
      echo "Build still running..."
      sleep 30
    done
```

### Performance Monitoring
```javascript
// src/monitoring.js
const { Actor } = require('apify');

async function monitorPerformance() {
    const startTime = Date.now();
    const startMemory = process.memoryUsage();
    
    // Your Actor logic here
    
    const endTime = Date.now();
    const endMemory = process.memoryUsage();
    
    await Actor.setValue('performance_metrics', {
        duration: endTime - startTime,
        memoryUsed: endMemory.heapUsed - startMemory.heapUsed,
        timestamp: new Date().toISOString()
    });
}
```

## Troubleshooting

### Common Issues

#### Build Failures
```yaml
- name: Debug build failure
  if: failure()
  run: |
    echo "Build failed. Checking logs..."
    curl -s "${{ secrets.BUILD_LOGS_URL }}" | jq '.data.log'
```

#### Test Failures
```yaml
- name: Upload test results
  if: always()
  uses: actions/upload-artifact@v2
  with:
    name: test-results
    path: test-results.xml
```

#### Deployment Issues
```yaml
- name: Verify deployment
  run: |
    # Check if Actor is accessible
    ACTOR_STATUS=$(curl -s "${{ secrets.ACTOR_STATUS_URL }}" | jq -r '.data.status')
    if [ "$ACTOR_STATUS" != "READY" ]; then
      echo "Deployment verification failed"
      exit 1
    fi
```

Continuous Integration automates the entire development lifecycle, ensuring consistent, reliable, and efficient Actor deployment while maintaining high code quality and reducing manual intervention.