# Local development

**Create your first Actor locally on your machine, deploy it to the Apify platform, and run it in the cloud.**

## Prerequisites

You need to have [Node.js](https://nodejs.org/en/) version 16 or higher with `npm` installed on your computer.

## Install Apify CLI

### MacOS/Linux

You can install the Apify CLI via the [Homebrew package manager](https://brew.sh/).

```bash
brew install apify-cli
```

### Other platforms

Use [NPM](https://www.npmjs.com/) to install the Apify CLI.

```bash
npm -g install apify-cli
```

Visit [Apify CLI documentation](https://docs.apify.com/cli/) for more information regarding installation and advanced usage.

## Create your Actor

To create a new Actor, use the following command:

```bash
apify create
```

The CLI will prompt you to:

1. _Name your Actor_: Enter a descriptive name for your Actor, such as `your-actor-name`
2. _Choose a programming language_: Select the language you want to use for your Actor (JavaScript, TypeScript, or Python).
3. _Select a development template_: Choose a template from the list of available options.

After selecting the template, the CLI will:

- Create a `your-actor-name` directory with the boilerplate code.
- Install all project dependencies

Navigate to the newly created Actor directory:

```bash
cd your-actor-name
```

## Explore the source code in your editor

### `src` Directory

- `src/main.js`: This file contains the actual code of your Actor

### `.actor` Directory

- `actor.json`: This file defines the Actor's configuration
- `Dockerfile`: This file contains instructions for building the Docker image

### `storage` Directory

- This directory emulates the Apify Storage
  - Dataset
  - Key-Value Store
  - Request Queue

## Run it locally

To run your Actor locally, use the following command:

```bash
apify run
```

## Deploy it to Apify