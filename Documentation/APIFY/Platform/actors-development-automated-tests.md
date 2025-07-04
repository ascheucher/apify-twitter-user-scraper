# Automated tests

**Learn how to automate ongoing testing and make sure your Actors perform over time. See code examples for configuring the Actor Testing Actor.**

## Automated tests for Actors

Automated testing is crucial for maintaining the reliability and performance of your Actors over time. This guide will help you set up automated tests using the [Actor Testing Actor](https://apify.com/pocesar/actor-testing).

## Set up automated tests

1. Prepare test tasks - Create 1–5 separate testing tasks for your Actor.
2. Configure Actor testing - Set up a task using the Actor Testing Actor.
3. Validate tests - Run the test task multiple times until all tests pass.
4. Schedule tests - Set up a recurring schedule for your tests.
5. Monitor results - Review and address any issues on a weekly basis.

## Create test tasks

When creating test tasks:

* Include a test for your Actor's default configuration
* Set a low `maxItem` value to conserve credits
* For large data tests, reduce test frequency to conserve credits

## Configure the Actor Testing Actor

Follow the [setup guide](https://apify.com/pocesar/actor-testing) in the Actor's README.

Here are some recommended test scenarios:

* Run status
* Crash information from the log
* Information from statistics (runtime, retries)
* Information about and from within the dataset
* Information about the key-value store

Code examples include various test scenarios with async expectations:

```javascript
await expectAsync(runResult).toHaveStatus('SUCCEEDED');

await expectAsync(runResult).withLog((log) => {
    // Neither ReferenceError or TypeErrors should ever occur
    // in production code – they mean the code is over-optimistic
    // The errors must be dealt with gracefully and displayed with a helpful message to the user
    expect(log)
        .withContext(runResult.format('ReferenceError'))
        .not.toContain('ReferenceError');
    expect(log)
        .withContext(runResult.format('TypeError'))
        .not.toContain('TypeError');
});

await expectAsync(runResult).withStatistics((stats)