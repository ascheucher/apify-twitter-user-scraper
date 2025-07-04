# Actor status badge

The Actor status badge can be embedded in the README or documentation to show users the current status and usage of your Actor on the Apify platform.

---

This is the badge generated for the [Apify's Website Content Crawler](https://apify.com/apify/website-content-crawler) Actor:

[![Website Content Crawler Actor](https://apify.com/actor-badge?actor=apify/website-content-crawler)](https://apify.com/apify/website-content-crawler)

This is how such a badge looks in a GitHub repository README:

![Actor badge in GitHub README](/assets/images/github-badge-screenshot-23af8e9a39a94a7f9b3222cd3e45f2ad.png)

### How to embed the badge

The Badge is a dynamic SVG image loaded from the Apify platform. The Badge is served from the URL Template:

```
https://apify.com/actor-badge?actor=<USERNAME>/<ACTOR>
```

In order to embed the badge in the HTML documentation, just use it as an image wrapped in a link as shown in the example below. Don't froget to use the `username` and `actor-name` of your Actor.

#### Example

*   HTML
*   Markdown

```html
<a href="https://apify.com/apify/website-content-crawler">  <img src="https://apify.com/actor-badge?actor=apify/website-content-crawler"></a>
```

```markdown
[![Website Content Crawler Actor](https://apify.com/actor-badge?actor=apify/website-content-crawler)](https://apify.com/apify/website-content-crawler)
```

### Supported Actor states

The badge indicates the state of the Actor in the Apify platform as the result of the [automated testing](/platform/actors/development/automated-tests).

#### Actor OK

![Actor badge OK](badge image)

#### Actor under maintenance

![Actor badge under maintenance](badge image)

#### Actor deprecated

![Actor badge deprecated](badge image)

#### Actor not found

![Actor badge not found](badge image)