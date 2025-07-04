# actor.json

**Learn how to write the main Actor configuration in the `.actor/actor.json` file.**

Your main Actor configuration is in the `actor/actor.json` file at the root of your Actor's directory. This file links your local development project to an Actor on the Apify platform. It should include details like the Actor's name, version, build tag, and environment variables. Make sure to commit this file to your Git repository.

For example, the `.actor/actor.json` file can look like this:

*   Full actor.json
*   Minimal actor.json

    ```json
    {
        "actorSpecification": 1, // always 1
        "name": "name-of-my-scraper",
        "version": "0.0",
        "buildTag": "latest",
        "minMemoryMbytes": 256,
        "maxMemoryMbytes": 4096,
        "environmentVariables": {
            "MYSQL_USER": "my_username",
            "MYSQL_PASSWORD": "@mySecretPassword"
        },
        "usesStandbyMode": false,
        "dockerfile": "./Dockerfile",
        "readme": "./ACTOR.md",
        "input": "./input_schema.json",
        "storages": {
            "dataset": "./dataset_schema.json"
        },
        "webServerSchema": "./web_server_openapi.json"
    }
    ```

    ```json
    {
        "actorSpecification": 1, // always 1
        "name": "name-of-my-scraper",
        "version": "0.0"
    }
    ```

## Reference

**Deployment metadata**

Actor `name`, `version`, `buildTag`, and `environmentVariables` are currently only used when you deploy your Actor using the [Apify CLI](/cli) and not when deployed, for example, via GitHub integration. There, it serves for informative purposes only.

The documentation then provides a detailed table of properties with their types, descriptions, and optional/required status, including:

- `actorSpecification`