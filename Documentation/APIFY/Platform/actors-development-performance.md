# Performance

**Learn how to get the maximum value out of your Actors, minimize costs, and maximize results.**

## Optimization Tips

This guide provides tips to help you maximize the performance of your Actors, minimize costs, and achieve optimal results.

### Run batch jobs instead of single jobs

"Running a single job causes the Actor to start and stop for each execution, which is an expensive operation." To minimize costs, run batch jobs instead of single jobs. Group URLs into batches and run the Actor once for each batch to reuse browser instances efficiently.

### Leverage Docker layer caching to speed up builds

When building a Docker image, Docker caches unchanged layers. This means if you modify only a small part of your Dockerfile, Docker rebuilds only the changed layers.

Example Dockerfile:

```dockerfile
FROM apify/actor-node:16
COPY package*.json ./
RUN npm --quiet set progress=false \
    && npm install --omit=dev --omit=optional \
    && echo "Installed NPM packages:" \
    && (npm list --omit=dev --all || true) \
    && echo "Node.js version:" \
    && node --version \
    && echo "NPM version:" \
    && npm --version \
    && rm -r ~/.npm
COPY . ./
CMD npm start --silent
```

Additional optimization tips:
- Use fewer layers in Docker images
- Use [dive](https://github.com/wagoodman/dive) CLI tool to analyze Docker image layers

### Use standardized images to accelerate Actor startup times

Using [Apify's standardized images](https://github.com/apify/apify-actor-docker) can accelerate Actor startup time. These images are cached on each worker machine, so only your custom layers need to be pulled.