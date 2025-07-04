# Runs and builds

**Learn about Actor builds and runs, their lifecycle, sharing, and data retention policy.**

## Builds

An Actor is a combination of source code and various settings in a Docker container. To run, it needs to be built. An Actor build consists of the source code built as a Docker image, making the Actor ready to run on the Apify platform.

> A Docker image is a lightweight, standalone, executable package of software that includes everything needed to run an application.

With every new version of an Actor, a new build is created. Each Actor build has its number (for example, **1.2.34**), and some builds are tagged for easier use (for example, _latest_ or _beta_). When running an Actor, you can choose what build you want to run by selecting a tag or number in the run options.

Each build may have different features, input, or output. By fixing the build to an exact version, you can ensure that you won't be affected by a breaking change in a new Actor version.

## Runs

When you start an Actor, an Actor run is created. An Actor run is a Docker container created from the build's Docker image with dedicated resources (CPU, memory, disk space).

Each run has its own (default) storages assigned:

- [Key-value store](/platform/storage/key-value-store) containing the input and enabling Actor to store other files.
- [Dataset](/platform/storage/dataset) enabling Actor to store the results.
- [Request queue](/platform/storage/request-queue) to maintain a queue of URLs to be processed.

### Origin

Both **Actor runs** and **builds** have the **Origin** field indicating how the Actor run or build was invoked.

| Name | Origin |
|------|--------|
| `DEVELOPMENT` | Manually from Apify Console in the Development mode |
| `WEB` | Manually from Apify Console in "normal" mode |
| `API` | From Apify API |
| `CLI` | From Apify CLI |
| `SCHEDULER` | Using a schedule |
| `WEBHOOK` | Using a webhook |
| `ACTOR` | From another Actor run |
| `STAND