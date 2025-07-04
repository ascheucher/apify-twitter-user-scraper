# Running Actors Locally | Apify SDK for Python

## Requirements

- Python version 3.10 or above is required to run Python Actors locally

## Creating Your First Actor

Use the Apify CLI to create a new Actor from a Python template:

```bash
apify create my-first-actor --template python-start
```

This command will:
- Create a new folder called `my-first-actor`
- Download the "Getting started with Python" Actor template
- Create a virtual environment in `my-first-actor/.venv`
- Install Actor dependencies

## Running the Actor

Navigate to the Actor directory and run:

```bash
cd my-first-actor
apify run
```

This will:
- Activate the virtual environment
- Start the Actor
- Configure local storage in the `storage` folder
- Set Actor input in `storage/key_value_stores/default/INPUT.json`

## Adding Dependencies

1. Add dependencies to the `requirements.txt` file

2. Activate the virtual environment:

**Linux / macOS:**
```bash
source .venv/bin/activate
```

**Windows:**
```bash
.venv\Scripts\activate
```

3. Install dependencies:
```bash
python -m pip install -r requirements.txt
```

## Additional Resources
- [Apify CLI Documentation](https://docs.apify.com/cli)
- [Python Actor Templates](https://apify.com/templates/categories/python)