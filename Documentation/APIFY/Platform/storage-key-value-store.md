# Key-value Store | Platform | Apify Documentation

**Store diverse data types including JSON, HTML, images, and strings. Access and manage key-value stores from Apify Console or via API.**

---

Key-value stores enable you to store and retrieve data using unique keys. Unlike datasets, which are append-only, key-value stores allow you to create, update, and delete records. This makes them ideal for storing configuration files, temporary data, and various file types.

> Named key-value stores are retained indefinitely.  
> Unnamed key-value stores expire after 7 days unless otherwise specified.  
> [Learn more](/platform/storage/usage#named-and-unnamed-storages)

## Basic Usage

You can access your key-value stores in several ways:

- [Apify Console](https://console.apify.com) - provides an easy-to-understand interface
- [Apify API](/api/v2) - for accessing your key-value stores programmatically
- [Apify API clients](/api) - to access your key-value stores from any Node.js application
- [Apify SDK](/sdk) - when building your own JavaScript Actor

### Apify Console

In the [Apify Console](https://console.apify.com), you can view your key-value stores in the [Storage](https://console.apify.com/storage) section under the [Key-value stores](https://console.apify.com/storage?tab=keyValueStores) tab.

## Supported Data Types

- JSON objects
- HTML content
- Images (PNG, JPG, etc.)
- Text files
- Binary data
- XML documents

## Features

- Create, read, update, delete operations
- Binary and text data support
- Content-type detection
- Direct file downloads