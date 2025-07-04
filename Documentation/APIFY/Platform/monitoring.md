# Monitoring

**Learn how to continuously make sure that your Actors and tasks perform as expected and retrieve correct results. Receive alerts when your jobs or their metrics are not as you expect.**

---

The web is continuously evolving, and so are the websites you interact with. If you implement Apify Actors or the data they provide into your daily workflows, you need to make sure that everything runs as expected.

> Monitoring allows you to track and observe how the software works. It enables you to measure and compare your programs' performance over time and to be notified when something goes wrong.

Also, you can use the data you gain from monitoring to optimize your software and maximize its potential.

## Built-in monitoring

Monitoring is an option you can find on any Actor or saved task in Apify Console. It allows you to display metric statistics about your solution's runs and set up alerts for when your solution behaves differently than you expect.

The monitoring system is free for all users. You can use it to monitor as many Actors and tasks as you want, and it does not use any additional resources on top of your usage when running them.

### Features

Currently, the monitoring option offers the following features:

1. Chart showing **statuses** of runs of the Actor or saved task over last 30 days.
2. Chart displaying **metrics** of the last 200 runs of the Actor or saved task.
3. Option to set up **alerts** with notifications based on the run metrics.

> Both charts can also be added to your Apify Console home page so you can quickly see if there are any issues every time you open Apify Console.

### Alert configuration

When you set up an alert, you have four choices for how you want the metrics to be evaluated:

1. **Alert, when the metric is lower than** - Checked after the run finishes. If the metric is lower than the set value, the alert will be triggered.

2. **Alert, when the metric is higher than** - Checked during and after the run, with periodic checks approximately every 5 minutes.

3. **Alert, when run status is one of following** - Checked after the run finishes, tracking unexpected run statuses.

4. **Alert