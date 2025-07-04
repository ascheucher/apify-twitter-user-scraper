# Dataset | Platform | Apify Documentation

**Store structured data from your Actor runs and web scraping results. Access and manage datasets from Apify Console or via API with multiple export formats.**

---

Datasets enable you to store and retrieve structured data, typically results from web scraping, data extraction, and other data processing tasks. Each Actor run has a unique dataset assigned by default, but you can also create named datasets for sharing data between runs.

> Named datasets are retained indefinitely.  
> Unnamed datasets expire after 7 days unless otherwise specified.  
> [Learn more](/platform/storage/usage#named-and-unnamed-storages)

## Basic Usage

You can access your datasets in several ways:

- [Apify Console](https://console.apify.com) - provides an easy-to-understand interface
- [Apify API](/api/v2) - for accessing your datasets programmatically
- [Apify API clients](/api) - to access your datasets from any Node.js application
- [Apify SDK](/sdk) - when building your own JavaScript Actor

### Apify Console

In the [Apify Console](https://console.apify.com), you can view your datasets in the [Storage](https://console.apify.com/storage) section under the [Datasets](https://console.apify.com/storage?tab=datasets) tab.

## Features

- Multiple export formats (JSON, CSV, Excel, etc.)
- Table-like data visualization
- Append-only data structure
- Pagination support
- Search and filtering capabilities

## Data Structure

Datasets store data as items in an append-only structure, where each item is a JSON object with arbitrary fields.