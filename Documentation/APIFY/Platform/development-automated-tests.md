# Automated Tests for Actors

## Overview

Automated testing is crucial for maintaining the reliability and performance of Actors over time. This guide helps set up automated tests using the Actor Testing Actor.

## Set Up Automated Tests

### Steps to Configure Automated Tests:

1. **Prepare test tasks** - Create 1-5 separate testing tasks for your Actor
2. **Configure Actor testing** - Set up a task using the Actor Testing Actor
3. **Validate tests** - Run the test task multiple times until all tests pass
4. **Schedule tests** - Set up a recurring schedule for your tests
5. **Monitor results** - Review and address any issues on a weekly basis

## Create Test Tasks

When creating test tasks:
- Include a test for your Actor's default configuration
- Set a low `maxItem` value to conserve credits
- For large data tests, reduce test frequency to conserve credits

## Configure the Actor Testing Actor

### Recommended Test Scenarios

#### Run Status Test
```javascript
await expectAsync(runResult).toHaveStatus('SUCCEEDED');
```

#### Error Logging Test
```javascript
await expectAsync(runResult).withLog((log) => {
    expect(log).not.toContain('ReferenceError');
    expect(log).not.toContain('TypeError');
});
```

#### Statistics Test
```javascript
await expectAsync(runResult).withStatistics((stats) => {
    expect(stats.requestsRetries).toBeLessThan(3);
    expect(stats.crawlerRuntimeMillis).toBeWithinRange(1 * 60000, 10 * 60000);
});
```

#### Dataset Validation Test
```javascript
await expectAsync(runResult).withDataset(({ dataset, info }) => {
    expect(info.cleanItemCount).toBe(3);
    expect(dataset.items).toBeNonEmptyArray();
    
    for (const result of dataset.items) {
        expect(result.directUrl).toStartWith('https://www.yelp.com/biz/');
        expect(result.bizId).toBeNonEmptyString();
    }
});
```

#### Key-Value Store Test
```javascript
await expectAsync(runResult).withKeyValueStore(({ contentType }) => {
    expect(contentType).toBe('image/gif');
}, { keyName: 'apify.com-scroll_losless-comp' });
```

## Test Scheduling and Monitoring

### Scheduling Tests
- Create 1-5 separate testing tasks for your Actor
- Set up a recurring schedule for tests
- Monitor results on a weekly basis

### Test Scheduling Best Practices
- For large data tests, reduce test frequency to conserve credits
- Set a low `maxItem` value to minimize credit usage
- Include a test for the Actor's default configuration

### Monitoring Test Results
The document provides example test scenarios to validate:
- Run status
- Crash information from logs
- Runtime and retry statistics
- Dataset content and structure
- Key-value store properties

## Example Test Validation Checks

### Basic Validation
- Verify run status is 'SUCCEEDED'
- Check for absence of critical errors (ReferenceError, TypeError)
- Limit request retries
- Validate dataset item count and structure
- Confirm key-value store content type

### Advanced Validation
- Performance metrics within expected ranges
- Resource consumption within limits
- Output data quality and consistency
- Error handling and recovery mechanisms

## Implementation Workflow

The recommended approach is to:
1. Configure tests using the Actor Testing Actor
2. Run tests multiple times until all pass
3. Set up a recurring schedule
4. Review and address any issues weekly

## Benefits of Automated Testing

- **Reliability**: Ensure consistent Actor performance
- **Early Detection**: Identify issues before they affect production
- **Quality Assurance**: Maintain high standards for data output
- **Resource Optimization**: Monitor and optimize resource usage
- **Confidence**: Deploy changes with greater confidence

## Best Practices Summary

1. **Start Simple**: Begin with basic status and error checks
2. **Expand Coverage**: Add data validation and performance tests
3. **Monitor Regularly**: Review test results weekly
4. **Optimize Costs**: Use appropriate test frequencies and data limits
5. **Stay Updated**: Keep tests aligned with Actor functionality changes

The goal is to ensure ongoing reliability and performance of Actors through systematic, automated testing.