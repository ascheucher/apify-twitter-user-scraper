# Running Webserver in Your Actor

## Overview

Each Actor run on the Apify platform is assigned a unique URL that enables HTTP access to an optional web server running inside the Actor run's container. The web server can be accessed through:

- Apify Console's "Container URL" field
- API's `container_url` property
- `Actor.config.container_url` property

## Configuration

The web server must listen on the port defined by `Actor.config.container_port`:
- Locally, the default port is `4321`
- Accessible at `http://localhost:4321`

## Example Implementation

Here's a complete example of running a web server in an Apify Actor:

```python
import asyncio
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from apify import Actor

processed_items = 0
http_server = None

class RequestHandler(BaseHTTPRequestHandler):
    def do_get(self) -> None:
        self.log_request()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(f'Processed items: {processed_items}', encoding='utf-8'))

def run_server() -> None:
    global http_server
    with ThreadingHTTPServer(
        ('', Actor.config.web_server_port), RequestHandler
    ) as server:
        Actor.log.info(f'Server running on {Actor.config.web_server_port}')
        http_server = server
        server.serve_forever()

async def main() -> None:
    global processed_items
    async with Actor:
        # Start the HTTP server in a separate thread
        run_server_task = asyncio.get_running_loop().run_in_executor(None, run_server)
        
        # Simulate doing some work
        for _ in range(100):
            await asyncio.sleep(1)
            processed_items += 1
            Actor.log.info(f'Processed items: {processed_items}')
        
        if http_server is None:
            raise RuntimeError('HTTP server not started')
        
        # Signal the HTTP server to shutdown
        http_server.shutdown()
        
        # Wait for the server task to complete
        await run_server_task
```

## Key Features

- Enables HTTP access to running Actor
- Useful for debugging and monitoring
- Can provide real-time status updates
- Supports custom request handlers
- Accessible via unique container URL