# Source Types | Platform | Apify Documentation

## Overview

Apify supports four different source types for deploying Actors, each offering different advantages and use cases. The source type determines how your Actor's code is stored and managed on the Apify platform.

## Source Type Options

### 1. Web IDE

The Web IDE is the default option for hosting source code directly on the Apify platform.

#### Features
- **Quick previews**: Allows immediate code previews and updates
- **Integrated editing**: Built-in code editor with syntax highlighting
- **Instant deployment**: Direct deployment from the web interface
- **Version control**: Basic version management within the platform

#### Requirements
- **Dockerfile**: Requires a `Dockerfile` for build configuration
- **Entry point**: Typically uses `main.js` as the entry point
- **Package definition**: Usually includes `package.json` for dependencies

#### File Structure
```
Actor files:
├── main.js                 # Entry point
├── package.json            # Dependencies
├── Dockerfile              # Build configuration
└── README.md               # Documentation
```

#### Use Cases
- **Rapid prototyping**: Quick development and testing
- **Small projects**: Simple Actors with minimal complexity
- **Learning**: Ideal for beginners learning Actor development

### 2. Git Repository

Connect your Actor to a Git repository for advanced version control and collaboration.

#### Features
- **Multiple files and directories**: Support for complex project structures
- **Custom Dockerfile**: Full control over build process
- **Branch/tag specification**: Can specify specific branch or tag in URL
- **Private repository support**: Supports private repositories via deployment keys
- **GitHub integration**: Enables automatic rebuilds on code changes

#### Configuration
```javascript
// Example repository URL formats
"https://github.com/username/actor-name"
"https://github.com/username/actor-name#branch-name"
"https://github.com/username/actor-name#v1.0.0"
"git@github.com:username/private-actor.git"
```

#### Private Repository Setup
1. **Generate deployment key**: Create SSH key pair
2. **Add public key**: Add to repository deploy keys
3. **Configure Actor**: Use git URL with deployment key

#### GitHub Integration
```yaml
# .github/workflows/deploy.yml
name: Deploy to Apify
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Apify
        uses: apify/action-deploy@v1
        with:
          apify-token: ${{ secrets.APIFY_TOKEN }}
```

#### Monorepo Support
```javascript
// For monorepos, specify subdirectory
"https://github.com/username/monorepo/actors/my-actor"
```

### 3. Zip File

Deploy from a zip file hosted on an external URL.

#### Features
- **Multiple files/directories**: Support for complex structures
- **External hosting**: Deploy from files hosted elsewhere
- **Automatic fallback**: Used automatically when source exceeds 3MB via CLI
- **Batch deployment**: Upload multiple files at once

#### Requirements
- **Accessible URL**: Zip file must be publicly accessible
- **Proper structure**: Must contain valid Actor structure
- **Main file**: Requires `main.js` if no custom Dockerfile provided

#### Example URLs
```
https://example.com/my-actor.zip
https://github.com/username/repo/archive/main.zip
https://api.github.com/repos/username/repo/zipball/main
```

#### Zip File Structure
```
my-actor.zip
├── src/
│   ├── main.js
│   └── utils.js
├── package.json
├── Dockerfile
└── README.md
```

### 4. GitHub Gist

Use GitHub Gists for simple, lightweight Actors.

#### Features
- **Ideal for small projects**: Perfect for single-file or simple Actors
- **Easy sharing**: Public gists are easily shareable
- **Multiple files**: Can include multiple files in a single gist
- **Version history**: Gists maintain version history
- **README support**: Description pulled from `README.md`

#### Setup Process
1. **Create Gist**: Go to github.com/gist
2. **Add files**: Include your Actor files
3. **Configure Actor**: Use the Gist URL

#### Example Gist Structure
```
Gist files:
├── main.js                 # Actor code
├── package.json            # Dependencies
├── README.md               # Documentation
└── INPUT_SCHEMA.json       # Input schema
```

#### Gist URL Format
```
https://gist.github.com/username/gist-id
```

## Choosing the Right Source Type

### Decision Matrix

| Feature | Web IDE | Git Repository | Zip File | GitHub Gist |
|---------|---------|----------------|----------|-------------|
| Ease of use | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| Version control | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐ |
| Collaboration | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐ |
| Complex projects | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| CI/CD integration | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| Privacy | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |

### Recommendations

#### Use Web IDE for:
- **Learning and prototyping**: Quick development and testing
- **Simple Actors**: Single-file or minimal complexity
- **Immediate results**: When you need to deploy quickly

#### Use Git Repository for:
- **Professional development**: Production-ready Actors
- **Team collaboration**: Multiple developers working together
- **Complex projects**: Multi-file, sophisticated Actors
- **CI/CD pipelines**: Automated testing and deployment

#### Use Zip File for:
- **Large projects**: When files exceed CLI limits
- **External hosting**: When code is hosted elsewhere
- **Batch operations**: Deploying multiple files at once

#### Use GitHub Gist for:
- **Quick sharing**: Simple Actors to share with community
- **Single-file Actors**: Minimal, focused functionality
- **Educational examples**: Teaching and demonstration

## Configuration Examples

### Web IDE Configuration
```javascript
// Simple main.js for Web IDE
const { Actor } = require('apify');

Actor.main(async () => {
    const input = await Actor.getInput();
    console.log('Input:', input);
    
    // Your Actor logic here
    
    await Actor.pushData({ result: 'success' });
});
```

### Git Repository Configuration
```javascript
// .actor/actor.json
{
    "actorSpecification": 1,
    "name": "advanced-scraper",
    "version": "1.0.0",
    "buildTag": "latest",
    "dockerfile": "./Dockerfile",
    "readme": "./README.md",
    "input": "./input_schema.json",
    "categories": ["ECOMMERCE"],
    "defaultRunOptions": {
        "build": "latest",
        "memoryMbytes": 2048,
        "timeoutSecs": 3600
    }
}
```

### Zip File Configuration
```bash
# Create zip file with proper structure
zip -r my-actor.zip \
  src/ \
  package.json \
  Dockerfile \
  README.md \
  .actor/
```

### GitHub Gist Configuration
```javascript
// Simple gist main.js
const { Actor } = require('apify');

Actor.main(async () => {
    // Quick and simple Actor logic
    const result = await scrapeWebsite();
    await Actor.pushData(result);
});
```

## Best Practices

### 1. File Organization
```
Recommended structure:
├── .actor/
│   ├── actor.json
│   ├── Dockerfile
│   └── README.md
├── src/
│   ├── main.js
│   ├── utils/
│   └── config/
├── package.json
└── README.md
```

### 2. Version Control
```bash
# Use semantic versioning
git tag v1.0.0
git push origin v1.0.0

# Reference specific versions
"https://github.com/username/actor#v1.0.0"
```

### 3. Security
```javascript
// Don't include secrets in source code
const apiKey = process.env.API_KEY; // Use environment variables

// Use .gitignore for sensitive files
echo "*.env" >> .gitignore
echo "secrets.json" >> .gitignore
```

### 4. Documentation
```markdown
# Actor Documentation
## Description
Brief description of what the Actor does

## Input
Description of input parameters

## Output
Description of output format

## Usage
Example usage instructions
```

## Migration Between Source Types

### From Web IDE to Git Repository
1. **Export code**: Download files from Web IDE
2. **Create repository**: Initialize Git repository
3. **Push code**: Commit and push to repository
4. **Update Actor**: Change source type to Git Repository

### From Gist to Git Repository
1. **Clone gist**: `git clone https://gist.github.com/username/gist-id`
2. **Create new repo**: Initialize new repository
3. **Transfer files**: Copy files to new repository
4. **Update Actor**: Change source type

### From Zip to Git Repository
1. **Extract zip**: Download and extract zip file
2. **Initialize Git**: `git init` in extracted directory
3. **Add files**: `git add .` and `git commit`
4. **Push to remote**: Push to Git hosting service
5. **Update Actor**: Change source type

Each source type offers unique advantages, and the choice depends on your specific needs, team size, project complexity, and development workflow preferences.