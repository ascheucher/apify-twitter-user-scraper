# Dockerfile | Platform | Apify Documentation

## Overview

Dockerfiles define how your Actor's environment is built and configured. Apify provides multiple base Docker images optimized for different use cases and programming languages.

## Base Docker Images

### Node.js Base Images

#### `actor-node`
- **Description**: Slim Alpine Linux image with Node.js
- **Use case**: Basic JavaScript/Node.js Actors
- **Features**: Lightweight, minimal dependencies

#### `actor-node-puppeteer-chrome`
- **Description**: Includes Chromium and Google Chrome
- **Use case**: Web scraping with Puppeteer
- **Features**: Pre-installed browser engines

#### `actor-node-playwright-*`
- **Description**: Various images with different browser support
- **Use case**: Web scraping with Playwright
- **Features**: Multiple browser engine options

### Python Base Images

#### `actor-python`
- **Description**: Slim Debian image with Apify SDK
- **Use case**: Basic Python Actors
- **Features**: Python runtime with Apify SDK

#### `actor-python-playwright`
- **Description**: Includes Playwright browsers
- **Use case**: Web scraping with Playwright in Python
- **Features**: Pre-installed browser engines

#### `actor-python-selenium`
- **Description**: Includes Selenium and ChromeDriver
- **Use case**: Web scraping with Selenium
- **Features**: Selenium WebDriver support

## Image Versioning

Each base image has two versions:

- **`latest`**: Stable, production-ready version
- **`beta`**: For testing new features and updates

## Custom Dockerfile Configuration

You can customize your Dockerfile by:

1. **Referencing it in `.actor/actor.json`**
2. **Storing it in `.actor/Dockerfile`** or **`Dockerfile`**

## Default Dockerfile Example

Here's a typical Dockerfile for a Node.js Actor:

```dockerfile
FROM apify/actor-node:20
COPY package*.json ./
RUN npm --quiet set progress=false \
    && npm install --only=prod --no-optional
COPY . ./
```

## Default Startup Behavior

By default, Apify images start the application using:
- `npm start` from `package.json` (for Node.js)
- Equivalent startup commands for other languages

## Build Optimization

### Pre-cached Images
- Apify base images are pre-cached on Apify servers
- Provides faster build times compared to custom base images

### Custom Base Images
- You can use custom base images if needed
- Apify images offer performance advantages due to pre-caching

## Best Practices

1. **Use Apify base images**: Take advantage of pre-cached images for faster builds
2. **Choose appropriate base**: Select the base image that matches your Actor's requirements
3. **Optimize layer caching**: Structure your Dockerfile to leverage Docker's layer caching
4. **Install dependencies early**: Copy package files and install dependencies before copying source code
5. **Use specific versions**: Pin base image versions for consistent builds

## Example Configurations

### Simple Node.js Actor
```dockerfile
FROM apify/actor-node:20
COPY package*.json ./
RUN npm install --omit=dev --omit=optional
COPY . ./
CMD npm start --silent
```

### Python Actor with Playwright
```dockerfile
FROM apify/actor-python-playwright:3.11
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . ./
CMD python src/main.py
```

The Dockerfile configuration is crucial for defining your Actor's runtime environment and ensuring consistent, reliable execution across different environments.