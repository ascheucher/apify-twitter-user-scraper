# Standby mode

**Use Actors in lightweight Standby mode for fast API responses.**

---

Traditional Actors are designed to run a single job and then stop. They're mostly intended for batch jobs, such as when you need to perform a large scrape or data processing task. However, in some applications, waiting for an Actor to start is not an option. Actor Standby mode solves this problem by letting you have the Actor ready in the background, waiting for the incoming HTTP requests. In a sense, the Actor behaves like a real-time web server or standard API server.

## How do I know if Standby mode is enabled

You will know that the Actor is enabled for Standby mode if you see the **Standby** tab on the Actor's detail page. In the tab, you will find the hostname of the server, the description of the Actor's endpoints, the parameters they accept, and what they return in the Actor README.

To use the Actor in Standby mode, you don't need to click a start button or not need to do anything else. Simply use the provided hostname and endpoint in your application, hit the API endpoint and get results.

![Standby tab](/assets/images/standby-tab-be2a89c92ef176b75d93f573b51e4b03.png)

## How do I pass input to Actors in Standby mode

If you're using an Actor built by someone else, see its Information tab to find out how the input should be passed.

Generally speaking, Actors in Standby mode behave as standard HTTP servers. You can use any of the existing [HTTP request methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods) like GET, POST, PUT, DELETE, etc. You can pass the input via [HTTP request query string](https://en.wikipedia.org/wiki/Query_string) or via [HTTP request body](https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages#body).

## How do I authenticate my requests

To authenticate requests to Actor Standby, follow the same process as [authenticating requests to the Apify API](/platform/integ