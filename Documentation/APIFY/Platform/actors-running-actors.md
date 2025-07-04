# Running Actors

## Run your first Apify Actor

Before running an Actor, you need to either choose one from [Apify Store](https://apify.com/store) or build your own. To get started, we recommend trying an Actor from the Store.

> **You will need an Apify account to complete this tutorial. If you don't have one, complete the sign-up process first.**

### 1. Choose your Actor

After signing in to Apify Console, navigate to [Apify Store](https://console.apify.com/store). We'll pick the [Website Content Crawler](https://console.apify.com/actors/aYG0l9s7dbB7j3gbS/information/version-0/readme):

![Apify Store](/assets/images/store-5b5e59758034626dd92a45735c138c20.png)

### 2. Configure it

On the Actor's page, head to the **Input** tab. The Actor is pre-configured to run without extra input. Just click the **Start** button in the bottom-left corner.

Alternatively, you can adjust the settings to customize the results.

![Actor input](/assets/images/apify-input-eeec3989b5a1ed4bb84e06982e6b3068.png)

### 3. Wait for the results

The Actor might take a while to gather its first results and finish its run. Meanwhile, explore the platform options:

- Check other tabs for information about the Actor run
- Access the run **Log** and **Storage**
- Click the API button to explore related API endpoints

![Run](/assets/images/actor-run-bcbc9356dd02906cacd7a09cd6f18528.png)

### 4. Get the results

Shortly you will see the first results:

![Actor results](/assets/images/actor-results-6fc04e56f4a4032e667613502a151137.png)

You can export the data in multiple formats using the export button.

## Running via Apify API

Actors can be invoked using the Apify API by sending an HTTP POST request:

```
https://api.apify.com/v2/acts/compass~crawler-google-places/runs?token=<YOUR_API_TOKEN>
```

Input and options can be passed as payload and query parameters.

## Running Programmatically

Actors can be invoked programmatically from applications or other Actors using API client libraries for JavaScript and Python.

### JavaScript Example

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({
    token: 'MY-API-TOKEN',
});

// Start the Google Maps Scraper Actor and wait for it to finish
const actorRun = await client.actor('compass/crawler-google-places').call({
    queries: 'apify',
});

// Fetch scraped results from the Actor's dataset
const { items } = await client.dataset(actorRun.defaultDatasetId).listItems();
console.dir(items);
```

### Python Example

```python
from apify_client import ApifyClient

apify_client = ApifyClient('MY-API-TOKEN')

# Start the Google Maps Scraper Actor and wait for it to finish
actor_run = apify_client.actor('compass/crawler-google-places').call(
    run_input={ 'queries': 'apify' }
)

# Fetch scraped results from the Actor's dataset
dataset_items = apify_client.dataset(actor_run['defaultDatasetId']).list_items().items
print(dataset_items)
```

### Key Points

- The Actor runs under the account associated with the provided token
- All resources consumed are charged to the user account
- The `call()` function internally:
  - Invokes the "Run Actor" API endpoint
  - Waits for the Actor to finish
  - Reads output using the "Get items" API endpoint

Recommended libraries:
- JavaScript: `apify-client`
- Python: `apify_client`

## Ways to Run Actors

### 1. Apify Console
- Navigate to [Apify Store](https://console.apify.com/store)
- Select an Actor
- Configure input settings
- Click "Start" button
- Monitor run progress and view results

### 2. Apify API
- Send HTTP POST request to Run Actor endpoint
- Requires API token for authentication
- Can specify input and configuration parameters

### 3. Programmatic Execution
- Use client libraries (JavaScript/Python)
- Integrate into applications or workflows
- Support for both synchronous and asynchronous execution

## Key Considerations

- **Account Required**: All methods require an Apify account
- **Resource Consumption**: Runs consume account resources and credits
- **Input Configuration**: Can specify input parameters and settings
- **Output Formats**: Support for multiple output/export formats
- **Monitoring**: Real-time logs and performance metrics available
- **Flexibility**: Multiple execution methods for different use cases