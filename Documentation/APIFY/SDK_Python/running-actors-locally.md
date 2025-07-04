# Running Actors locally | SDK for Python | Apify Documentation

**Source URL**: https://docs.apify.com/sdk/python/docs/overview/running-actors-locally

## Requirements

The Apify SDK requires Python version 3.10 or above to run Python Actors locally.

## Creating your first Actor

To create a new Apify Actor, use the [Apify CLI](https://docs.apify.com/cli) and select a Python Actor template:

```bash
apify create my-first-actor --template python-start
```

This command will:
- Create a new folder called `my-first-actor`
- Download the "Getting started with Python" Actor template
- Create a virtual environment in `my-first-actor/.venv`
- Install Actor dependencies

## Running the Actor

To run the Actor, use the `apify run` command:

```bash
cd my-first-actor
apify run
```

This will:
- Activate the virtual environment in `.venv`
- Start the Actor
- Configure local storages in the `storage` folder

Actor input will be located at `storage/key_value_stores/default/INPUT.json`.

## Adding dependencies

1. Add dependencies to the `requirements.txt` file

2. Activate the virtual environment:

For Linux / macOS:
```bash
source .venv/bin/activate
```

For Windows:
```bash
.venv\Scripts\activate
```

3. Install dependencies:
```bash
python -m pip install -r requirements.txt
```