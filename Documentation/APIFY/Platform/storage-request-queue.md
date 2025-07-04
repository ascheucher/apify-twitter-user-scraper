# Request Queue | Platform | Apify Documentation

**Queue URLs for an Actor to visit in its run. Learn how to share your queues between Actor runs. Access and manage request queues from Apify Console or via API.**

---

Request queues enable you to enqueue and retrieve requests such as URLs with an [HTTP method](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods) and other parameters. They prove essential not only in web crawling scenarios but also in any situation requiring the management of a large number of URLs and the addition of new links.

The storage system for request queues accommodates both breadth-first and depth-first crawling strategies, along with the inclusion of custom data attributes. This system enables you to check if certain URLs have already been encountered, add new URLs to the queue, and retrieve the next set of URLs for processing.

> Named request queues are retained indefinitely.  
> Unnamed request queues expire after 7 days unless otherwise specified.  
> [Learn more](/platform/storage/usage#named-and-unnamed-storages)

## Basic Usage

You can access your request queues in several ways:

- [Apify Console](https://console.apify.com) - provides an easy-to-understand interface.
- [Apify API](/api/v2) - for accessing your request queues programmatically.
- [Apify API clients](/api) - to access your request queues from any Node.js application.
- [Apify SDK](/sdk) - when building your own JavaScript Actor.

### Apify Console

In the [Apify Console](https://console.apify.com), you can view your request queues in the [Storage](https://console.apify.com/storage) section under the [Request queues](https://console.apify.com/storage?tab=requestQueues) tab.

## Features

- Support for breadth-first and depth-first crawling
- Custom data attributes for requests
- Duplicate URL detection
- Request prioritization
- Statistics and monitoring