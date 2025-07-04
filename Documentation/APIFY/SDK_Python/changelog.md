# Apify SDK for Python Changelog

## 2.6.1 - Not Yet Released

### 🚀 Features
- Exposed `logger` argument on `Actor.call` to control log redirection from started Actor run

## 2.6.0 (2025-06-09)

### 🚀 Features
- Added `RemainingTime` option for `timeout` argument of `Actor.call` and `Actor.start`

### 🐛 Bug Fixes
- Fixed duplicate logs from Apify logger in Scrapy integration
- Preferred proxy password from environment variable

## 2.5.0 (2025-03-27)

### 🚀 Features
- Implemented Scrapy HTTP cache backend

### 🐛 Bug Fixes
- Fixed calculation of CPU utilization from SystemInfo events

## 2.4.0 (2025-03-07)

### 🚀 Features
- Updated to Crawlee v0.6
- Added Actor `exit_process` option
- Upgraded websockets to v14
- Added signing of public URL

## 2.3.1 (2025-02-25)

### 🐛 Bug Fixes
- Allowed None value in 'inputBodyLen' in ActorRunStats

## 2.3.0 (2025-02-19)

### 🚀 Features
- Added `rate_limit_errors` property for `ApifyStorageClient`
- Unified Apify and Scrapy event loop
- Supported pay-per-event via `Actor.charge`

### 🐛 Bug Fixes
- Fixed RQ usage in Scrapy scheduler
- Ensured Actor instances with non-default configurations are accessible

## Recent Updates

The changelog contains comprehensive version history including:
- Feature additions and enhancements
- Bug fixes and improvements
- Breaking changes and migration notes
- Performance optimizations
- Integration updates
- Security improvements

For the complete changelog with all version details, please refer to the official Apify SDK for Python documentation.