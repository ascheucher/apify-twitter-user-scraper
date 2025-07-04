# Web IDE | Platform | Apify Documentation

## Development in web IDE

**Create your first Actor using the web IDE in Apify Console.**

### Create the Actor

#### Prerequisites

To use Web IDE, you will need an Apify account. You can [sign-up for a free account](https://console.apify.com/sign-up) on the Apify website.

After you sign in to [Apify Console](https://console.apify.com), navigate to the **My Actors** subsection. Then, click the **Develop new** button at the top right corner of the page.

You will be redirected to a page containing various Actor development templates for popular languages such as `JavaScript`, `TypeScript`, and `Python`. These templates provide boilerplate code and a preconfigured environment tailored to specific use cases. You can choose the template that best suits your technology stack. For demonstration purposes, let's choose **Crawlee + Puppeteer + Chrome**.

#### Explore the source code

The provided boilerplate code utilizes the [Apify SDK](https://docs.apify.com/sdk/js/) combined with [Crawlee](https://crawlee.dev/), Apify's popular open-source Node.js web scraping library. By default the code performs a recursive crawl of the [apify.com](https://apify.com) website, but you can change it to a website of your choosing.

> Crawlee is an open-source Node.js library designed for web scraping and browser automation.

#### Build the Actor

To run your Actor, you need to build it first. Click the **Build** button below the source code to start the build process.

Once the build has been initiated, the UI will transition to the **Last build** tab, displaying the progress of the build and the Docker build log.

#### Actor creation flow

The UI includes four tabs:
- **Code**
- **Last build**
- **Input**
- **Last run**

#### Run the Actor

Once the Actor is built, you can look at its input, which consists of one field - **Start URL**, the URL where the crawling starts.

You can adjust