# Automated Testing

## Why we test

Apify wants to ensure all Actors in the Apify Store are high-quality. They use an "automated testing procedure" that:
- Tests all Actors daily
- Flags Actors "under maintenance" if they temporarily don't work
- Automatically "deprecate" Actors broken for over a month

## How we test

The test:
- Runs the Actor with default input
- Expects a **Succeeded** status
- Requires a non-empty default dataset
- Must complete within 5 minutes

### Test Failure Process
- 3 consecutive failed days: Developer notified, Actor labeled "under maintenance"
- 14 more failed days: Another notification
- Additional 14 failed days: Actor gets "deprecated"

## Making an Actor Healthy Again

- Fix and rebuild the Actor
- Automatic testing system will recognize changes within 24 hours
- If Actor passes most test runs in 7 days, it may be automatically marked healthy

## Special Circumstances

Actors requiring:
- Authentication
- Longer than 5-minute runtime

Should contact support@apify.com for potential test exclusion.

## Advanced Testing

Developers can use the public [Actor Testing](https://apify.com/pocesar/actor-testing) tool for customized tests.