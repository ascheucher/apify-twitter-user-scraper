# Schedules

**Learn how to automatically start your Actor and task runs and the basics of cron expressions. Set up and manage your schedules from Apify Console or via API.**

---

Schedules allow you to run your Actors and tasks at specific times. You schedule the run frequency using [cron expressions](#cron-expressions).

## Timezone & Daylight Savings Time

Schedules allow timezone settings and support daylight saving time shifts (DST).

You can set up and manage your Schedules using:

- [Apify Console](https://console.apify.com/schedules)
- [Apify API](https://docs.apify.com/api/v2#/reference/schedules)
- [JavaScript API client](https://docs.apify.com/api/client/js/reference/class/ScheduleClient)
- [Python API client](https://docs.apify.com/api/client/python/reference/class/ScheduleClient)

When scheduling a new Actor or task run, you can override its input settings using a JSON object similarly to when invoking an Actor or task using the [Apify REST API](/api/v2#/reference/schedules/).

### Events Startup Variability

In most cases, scheduled events are fired within one second of their scheduled time.  
However, runs can be delayed because of a system overload or a server shutting down.

Each schedule can be associated with a maximum of _10_ Actors and _10_ Actor tasks.

## Setting up a new schedule

Before setting up a new schedule, you should have the [Actor](/platform/actors) or [task](/platform/actors/running/tasks) you want to schedule prepared and tested.

To schedule an Actor, you need to have run it at least once before. To run the Actor, navigate to the Actor's page through [Apify Console](https://console.apify.com/store), where you can configure and initiate the Actor's run with your preferred settings by clicking the **Start** button. After this initial run, you can then use Schedules to automate future runs.

### Name Length

Your schedule's name