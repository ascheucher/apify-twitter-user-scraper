# Performance

**Learn how to get the maximum value out of your Actors, minimize costs, and maximize results.**

## Optimization Tips

### Run Batch Jobs Instead of Single Jobs

Running a single job causes the Actor to start and stop for each execution, which is an expensive operation. If your Actor runs a web browser or other resource-intensive dependencies, their startup times further contribute to the cost.

**Recommendation**: Group URLs into batches and run the Actor once for each batch. This approach reuses the browser instance, resulting in a more cost-efficient implementation.

### Leverage Docker Layer Caching to Speed Up Builds

Docker caches layers that haven't changed, meaning if you modify only a small part of your Dockerfile, Docker doesn't need to rebuild the entire image.

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

**Additional Optimization Tips**:
- Use as few layers as possible in Docker images
- Use the [dive](https://github.com/wagoodman/dive) CLI tool to analyze Docker image layers

### Use Standardized Images to Accelerate Actor Startup Times

Using [Apify's standardized images](https://github.com/apify/apify-actor-docker) can accelerate Actor startup time. These images are cached on each worker machine, so only the layers you added in your Actor's Dockerfile need to be pulled.