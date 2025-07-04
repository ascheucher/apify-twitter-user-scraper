# Actor tasks

**Create and save reusable configurations of Apify Actors tailored to specific use cases.**

---

Actor tasks let you create multiple reusable configurations of a single Actor, adapted for specific use cases. For example, you can create one [Web Scraper](https://apify.com/apify/web-scraper) configuration (task) that scrapes the latest reviews from imdb.com, another that scrapes nike.com for the latest sneakers, and a third that scrapes your competitor's e-shop. You can then use and reuse these configurations directly from [Apify Console](https://console.apify.com/actors/tasks), [Schedules](/platform/schedules), or [API](/api/v2#/reference/actor-tasks/run-collection/run-task).

You can find all your tasks in the [Apify Console](https://console.apify.com/actors/tasks).

## Create

To create a task, open any Actor from [Apify Store](https://console.apify.com/store) or your list of [Actors](https://console.apify.com/actors) in Apify Console. At the top-right section of the page, click the **Create task** button.

![Create a new Apify task](/assets/images/tasks-create-task-fe2022d6fab46890d47ca528749cd4c1.png)

## Configure

You can set up your task's input under the **Input** tab. A task's input configuration works just like an Actor's. After all, it's just a copy of an Actor you can pre-configure for a specific scenario. You can use either JSON or the visual input UI.

![Apify task configuration](/assets/images/tasks-create-configure-c3a0cc4d2e00baeee1d9e29fd1ac2ec1.png)

An Actors' input fields may vary depending on their purpose, but they all follow the same principle: *you provide an Actor with the information it needs so it can do what you want it to do.*

You can set run options such as timeout and [memory](/platform/actors/running/usage-