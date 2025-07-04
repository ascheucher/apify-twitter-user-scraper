# Actors

**Learn how to develop, run and share serverless cloud programs. Create your own web scraping and automation tools and publish them on the Apify platform.**

## What is an Actor?

Actors are serverless programs running in the cloud. They can perform anything from simple actions (such as filling out a web form or sending an email) to complex operations (such as crawling an entire website or removing duplicates from a large dataset). Actor runs can be as short or as long as necessary. They could last seconds, hours, or even infinitely.

> **To get better idea of what Apify Actors are, visit [Apify Store](https://apify.com/store), and try out some of them!**

You can use Actors [manually in Apify Console](https://console.apify.com/actors), by using the [API](/api/v2) or [scheduler](/platform/schedules). You can easily [integrate them with other apps](/platform/integrations) and share your Actors with other Apify users via [Apify Store](https://apify.com/store) or [access rights](/platform/collaboration/access-rights) system.

## Actors are containers

A single isolated Actor consists of source code and various settings. You can think of an Actor as a cloud app or service that runs on the Apify platform. The run of an Actor is not limited to the lifetime of a single HTTP transaction. It can run for as long as necessary, even forever.

Basically, Actors are programs packaged as [Docker images](https://hub.docker.com/), which accept a well-defined JSON input, perform an action, and optionally produce an output.

## Public and private Actors

Actors can be [public](/platform/actors/running/actors-in-store) or private. Private Actors are yours to use and keep; no one will see them if you don't want them to. Public Actors are [available to everyone](/platform/actors/running/actors-in-store) in [Apify Store](https://apify.com/store). You can make them free to use, or you can [charge for them](https://blog.apify.com/make-regular-passive-