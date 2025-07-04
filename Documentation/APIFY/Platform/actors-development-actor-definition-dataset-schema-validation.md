# Dataset Schema Validation | Platform | Apify Documentation

## Overview

Dataset schema validation allows you to specify a schema for your Actor's dataset, providing monitoring and validation at the field level. This helps ensure data quality and consistency by validating data inserted into datasets.

## Configuration Methods

You can configure dataset schema validation in two ways:

1. **Directly in `actor.json`** - Define the schema inline
2. **In a separate linked JSON schema file** - Reference an external schema file

## Schema Requirements

When defining a dataset schema, you must follow these requirements:

- **Single item schema**: Must define a schema for a single item, not an array
- **JSON Schema draft-07**: Use JSON Schema draft-07 specification
- **Include `$schema` property**: Must include `"$schema": "http://json-schema.org/draft-07/schema#"`

## Validation Behavior

The validation process works as follows:

### Successful Validation
- Data is stored successfully
- Returns 201 status code

### Failed Validation
- Entire request is discarded
- Returns 400 status code
- Detailed error response with validation errors

## Schema Examples

Here's an example of a dataset schema with various field types:

```json
{
  "fields": {
    "name": { 
      "type": "string" 
    },
    "price": { 
      "type": ["string", "number"],
      "nullable": true 
    },
    "comments": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "author_name": { 
            "type": "string" 
          }
        }
      }
    }
  }
}
```

## Field Statistics

Dataset field statistics are automatically tracked for validated fields:

- **Null count**: Number of null values
- **Empty count**: Number of empty values  
- **Minimum/maximum values**: Range of values for numeric fields
- **Various data type measurements**: Type-specific statistics

## Implementation

Validation can be implemented through:

- **Apify JS client**: Using the JavaScript SDK
- **Apify SDK**: Using the Python SDK
- **Error handling**: Use try/catch blocks to handle validation errors

## Best Practices

1. **Define clear schemas**: Create comprehensive schemas that cover all expected data fields
2. **Handle validation errors**: Implement proper error handling for validation failures
3. **Test schemas**: Validate your schemas with sample data before production
4. **Monitor statistics**: Use field statistics to monitor data quality over time

The dataset schema validation feature ensures your Actor produces consistent, high-quality data while providing valuable insights into data patterns and quality metrics.