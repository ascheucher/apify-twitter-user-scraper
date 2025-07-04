# Running Actors | Platform | Apify Documentation

## Run your first Apify Actor

**In this section, you learn how to run Apify Actors using Apify Console or programmatically. You will learn about their configuration, versioning, data retention, usage, and pricing.**

> **You will need an Apify account to complete this tutorial. If you don't have one, [complete the sign-up process](https://console.apify.com/sign-up) first. Don't worry about the price - it's free.**

### 1. Choose your Actor

After you sign-in to Apify Console, navigate to [Apify Store](https://console.apify.com/store). We'll pick the [Website Content Crawler](https://console.apify.com/actors/aYG0l9s7dbB7j3gbS/information/version-0/readme).

### 2. Configure it

On the Actor's page, head over to the **Input** tab. Don't be put off by all the boxes - the Actor is pre-configured to run without any extra input. Just click the **Start** button in the bottom-left corner.

Alternatively, you can play around with the settings to make the results more interesting for you.

### 3. Wait for the results

The Actor might take a while to gather its first results and finish its run. Meanwhile, let's take some time to explore the platform options:

- Note the other tabs, which provide you with information about the Actor run. For example, you can access the run **Log** and **Storage**.
- At the top right, you can click on the API button to explore the related API endpoints

### 4. Get the results

Shortly you will see the first results popping up, and you can use the export button at the bottom left to export the data in multiple formats.

## Running via Apify API

Actors can also be invoked using the Apify API by sending an HTTP POST request to the [Run Actor](/api/v2#/reference/actors/run-collection/run-actor) endpoint, such as:

```
https://api.apify.com/