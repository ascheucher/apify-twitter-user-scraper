# List of Permissions | Platform | Apify Documentation

## Overview

Apify's permission system provides granular control over what actions team members can perform within an organization. Permissions are organized by resource type and action, allowing for precise access control tailored to different roles and responsibilities.

## Actor Permissions

### Actor Resource
Controls access to Actor development and management:

#### Read Permission
**Scope**: `actors:read`
**Allows**:
- View Actor settings and configuration
- Access Actor source code
- View build history and details
- Inspect Actor metadata and documentation

```javascript
// Example: Read Actor information
const actor = await client.actor('ACTOR_ID').get();
console.log('Actor details:', {
    name: actor.name,
    description: actor.description,
    version: actor.version,
    stats: actor.stats
});

// View Actor builds
const builds = await client.actor('ACTOR_ID').builds().list();
console.log('Available builds:', builds.items.length);
```

#### Write Permission
**Scope**: `actors:write`
**Allows**:
- Edit Actor settings and configuration
- Modify Actor source code
- Update Actor documentation
- Delete Actor instances
- Create new Actor versions

```javascript
// Example: Update Actor configuration
await client.actor('ACTOR_ID').update({
    name: 'Updated Actor Name',
    description: 'Updated description',
    version: {
        versionNumber: '1.1.0',
        sourceType: 'GIT_REPO',
        gitRepoUrl: 'https://github.com/user/repo'
    }
});
```

#### Run Permission
**Scope**: `actors:run`
**Allows**:
- Execute Actor builds
- Start new Actor runs
- Provide input parameters
- Monitor run progress

```javascript
// Example: Start Actor run
const run = await client.actor('ACTOR_ID').start({
    input: {
        url: 'https://example.com',
        maxPages: 10
    },
    options: {
        build: 'latest',
        memoryMbytes: 1024
    }
});
```

#### View Runs Permission
**Scope**: `runs:read`
**Allows**:
- See Actor run details and history
- Access run logs and statistics
- View run status and progress
- Download run results

```javascript
// Example: View Actor runs
const runs = await client.actor('ACTOR_ID').runs().list();

for (const run of runs.items) {
    console.log('Run details:', {
        id: run.id,
        status: run.status,
        startedAt: run.startedAt,
        finishedAt: run.finishedAt,
        stats: run.stats
    });
    
    // Access run log
    const log = await client.actor('ACTOR_ID').run(run.id).log().get();
}
```

#### Manage Access Rights Permission
**Scope**: `actors:manage-access`
**Allows**:
- Control Actor sharing settings
- Grant/revoke access to other users
- Modify Actor visibility settings
- Manage collaboration permissions

```javascript
// Example: Share Actor with team
await client.actor('ACTOR_ID').update({
    accessRights: {
        users: [
            { userId: 'USER_ID_1', permission: 'READ' },
            { userId: 'USER_ID_2', permission: 'WRITE' }
        ],
        groups: [
            { groupId: 'TEAM_ID', permission: 'READ' }
        ]
    }
});
```

## Actor Task Permissions

### Actor Task Resource
Controls access to Actor task management:

#### Read Permission
**Scope**: `tasks:read`
**Allows**:
- View task configuration and settings
- Access task input schemas
- See task scheduling information
- Review task metadata

```javascript
// Example: View Actor task
const task = await client.task('TASK_ID').get();
console.log('Task configuration:', {
    name: task.name,
    actorId: task.actorId,
    input: task.input,
    options: task.options
});
```

#### Write Permission
**Scope**: `tasks:write`
**Allows**:
- Edit task settings and configuration
- Modify task input parameters
- Update task scheduling
- Delete task instances

```javascript
// Example: Update Actor task
await client.task('TASK_ID').update({
    name: 'Updated Task Name',
    input: {
        url: 'https://newsite.com',
        frequency: 'daily'
    },
    options: {
        memoryMbytes: 2048,
        timeoutSecs: 3600
    }
});
```

#### View Runs Permission
**Scope**: `task-runs:read`
**Allows**:
- See task run details and history
- Access task run logs
- Monitor task execution progress
- View task run statistics

#### Manage Access Rights Permission
**Scope**: `tasks:manage-access`
**Allows**:
- Control task sharing settings
- Manage task collaboration permissions
- Set task visibility options

## Storage Permissions

### Dataset Permissions

#### Read Permission
**Scope**: `datasets:read`
**Allows**:
- View dataset information and metadata
- Access dataset data and records
- Download dataset contents
- Export data in various formats

**Important**: Users with dataset read permission can access **ALL organization datasets**

```javascript
// Example: Read dataset
const dataset = await client.dataset('DATASET_ID');
const info = await dataset.get();
const { items } = await dataset.listItems();

console.log('Dataset info:', {
    name: info.name,
    itemCount: info.itemCount,
    fields: info.fields
});

console.log('Sample data:', items.slice(0, 5));
```

#### Write Permission
**Scope**: `datasets:write`
**Allows**:
- Edit dataset settings and metadata
- Push/add new data to datasets
- Remove/delete dataset records
- Modify dataset structure

```javascript
// Example: Write to dataset
await client.dataset('DATASET_ID').pushItems([
    { name: 'Product 1', price: 29.99 },
    { name: 'Product 2', price: 39.99 }
]);

// Update dataset settings
await client.dataset('DATASET_ID').update({
    name: 'Updated Dataset Name'
});
```

#### Manage Access Rights Permission
**Scope**: `datasets:manage-access`
**Allows**:
- Control dataset sharing settings
- Grant/revoke dataset access
- Manage dataset collaboration permissions

### Key-Value Store Permissions

#### Read Permission
**Scope**: `key-value-stores:read`
**Allows**:
- View store details and metadata
- Access stored records and files
- Download stored content
- List store keys

```javascript
// Example: Read from key-value store
const store = await client.keyValueStore('STORE_ID');
const storeInfo = await store.get();
const record = await store.getRecord('my-key');

console.log('Store info:', storeInfo);
console.log('Record content:', record);
```

#### Write Permission
**Scope**: `key-value-stores:write`
**Allows**:
- Edit store settings and metadata
- Store/modify records and files
- Delete stored content
- Manage store structure

```javascript
// Example: Write to key-value store
await client.keyValueStore('STORE_ID').setRecord({
    key: 'config',
    value: { setting1: 'value1', setting2: 'value2' },
    contentType: 'application/json'
});
```

#### Manage Access Rights Permission
**Scope**: `key-value-stores:manage-access`
**Allows**:
- Control store sharing settings
- Manage store access permissions

### Request Queue Permissions

#### Read Permission
**Scope**: `request-queues:read`
**Allows**:
- View queue details and metadata
- Access queued requests
- Monitor queue statistics
- List queue contents

```javascript
// Example: Read request queue
const queue = await client.requestQueue('QUEUE_ID');
const queueInfo = await queue.get();
const requests = await queue.listRequests();

console.log('Queue info:', {
    name: queueInfo.name,
    totalRequestCount: queueInfo.totalRequestCount,
    handledRequestCount: queueInfo.handledRequestCount
});
```

#### Write Permission
**Scope**: `request-queues:write`
**Allows**:
- Edit queue settings and metadata
- Add/modify queued requests
- Remove requests from queue
- Manage queue processing

```javascript
// Example: Write to request queue
await client.requestQueue('QUEUE_ID').addRequests([
    { url: 'https://example1.com' },
    { url: 'https://example2.com' }
]);
```

#### Manage Access Rights Permission
**Scope**: `request-queues:manage-access`
**Allows**:
- Control queue sharing settings
- Manage queue access permissions

## Proxy Permissions

### Proxy Usage Permission
**Scope**: `proxy:use`
**Allows**:
- Use Apify Proxy services
- Access datacenter and residential proxies
- Utilize Google SERP proxy
- Configure proxy settings in Actors

```javascript
// Example: Use proxy in Actor
const proxyConfiguration = await Actor.createProxyConfiguration({
    groups: ['RESIDENTIAL'],
    countryCode: 'US'
});

const crawler = new PuppeteerCrawler({
    proxyConfiguration,
    requestHandler: async ({ page, request }) => {
        // Scraping logic with proxy
    }
});
```

## User Permissions

### Account Management Permissions

#### Manage Access Keys Permission
**Scope**: `user:manage-access-keys`
**Allows**:
- Create and manage API tokens
- Set token permissions and expiration
- Revoke access tokens
- View token usage statistics

```javascript
// Example: Create API token
const token = await client.user().createToken({
    name: 'Automation Token',
    expiresAt: '2024-12-31T23:59:59.000Z',
    scopes: ['actors:read', 'runs:write']
});
```

#### Update Subscription Permission
**Scope**: `user:update-subscription`
**Allows**:
- Modify subscription plans
- Update billing information
- Change payment methods
- Access billing history

#### Update Profile Permission
**Scope**: `user:update-profile`
**Allows**:
- Edit profile information
- Update display name and bio
- Modify account settings
- Change avatar and preferences

#### Update Email Permission
**Scope**: `user:update-email`
**Allows**:
- Change account email address
- Verify new email addresses
- Update email preferences
- Manage email notifications

#### Reset Password Permission
**Scope**: `user:reset-password`
**Allows**:
- Change account password
- Reset forgotten passwords
- Update security settings
- Manage two-factor authentication

#### View Invoices Permission
**Scope**: `billing:read`
**Allows**:
- Access billing invoices
- View payment history
- Download billing statements
- Monitor usage costs

```javascript
// Example: View invoices
const invoices = await client.user().invoices().list();
for (const invoice of invoices.items) {
    console.log('Invoice:', {
        id: invoice.id,
        amount: invoice.amount,
        date: invoice.date,
        status: invoice.status
    });
}
```

#### Manage Organization Permission
**Scope**: `organization:manage`
**Allows**:
- Create and delete organizations
- Manage organization settings
- Add/remove organization members
- Control organization permissions
- Access organization billing

```javascript
// Example: Manage organization
await client.organization('ORG_ID').update({
    name: 'Updated Organization Name',
    description: 'Updated description'
});

// Add member to organization
await client.organization('ORG_ID').members().create({
    userId: 'USER_ID',
    role: 'MEMBER'
});
```

## Permission Dependencies

### Understanding Dependencies
Some permissions require other permissions to function properly:

```javascript
// Permission dependency mapping
const permissionDependencies = {
    'actors:run': ['actors:read'],
    'actors:delete': ['actors:read', 'actors:write'],
    'tasks:write': ['actors:read'],
    'datasets:write': ['datasets:read'],
    'schedules:write': ['actors:read', 'actors:run']
};

// Validate permission set
function validatePermissions(permissions) {
    const errors = [];
    
    for (const permission of permissions) {
        const dependencies = permissionDependencies[permission] || [];
        
        for (const dependency of dependencies) {
            if (!permissions.includes(dependency)) {
                errors.push(`Permission '${permission}' requires '${dependency}'`);
            }
        }
    }
    
    return errors;
}

// Example usage
const userPermissions = ['actors:run', 'datasets:write'];
const errors = validatePermissions(userPermissions);

if (errors.length > 0) {
    console.error('Permission validation errors:', errors);
}
```

## Permission Checking Utilities

### Runtime Permission Checking
```javascript
// Utility class for permission checking
class PermissionChecker {
    constructor(userPermissions) {
        this.permissions = userPermissions;
    }
    
    hasPermission(permission) {
        return this.permissions.includes(permission);
    }
    
    hasAnyPermission(permissions) {
        return permissions.some(p => this.hasPermission(p));
    }
    
    hasAllPermissions(permissions) {
        return permissions.every(p => this.hasPermission(p));
    }
    
    getResourcePermissions(resource) {
        return this.permissions.filter(p => p.startsWith(`${resource}:`));
    }
    
    canRead(resource) {
        return this.hasPermission(`${resource}:read`);
    }
    
    canWrite(resource) {
        return this.hasPermission(`${resource}:write`);
    }
    
    canManageAccess(resource) {
        return this.hasPermission(`${resource}:manage-access`);
    }
}

// Usage example
const userPermissions = [
    'actors:read', 'actors:write', 'actors:run',
    'datasets:read', 'datasets:write',
    'proxy:use'
];

const checker = new PermissionChecker(userPermissions);

console.log('Can read actors:', checker.canRead('actors'));
console.log('Can write datasets:', checker.canWrite('datasets'));
console.log('Can use proxy:', checker.hasPermission('proxy:use'));
console.log('Actor permissions:', checker.getResourcePermissions('actors'));
```

## Security Best Practices

### Principle of Least Privilege
```javascript
// Define role-based permission sets
const roleTem

const roleTemplates = {
    viewer: [
        'actors:read',
        'runs:read',
        'datasets:read',
        'key-value-stores:read'
    ],
    developer: [
        'actors:read', 'actors:write', 'actors:run',
        'runs:read',
        'datasets:read', 'datasets:write',
        'key-value-stores:read', 'key-value-stores:write',
        'proxy:use'
    ],
    admin: [
        'actors:read', 'actors:write', 'actors:run', 'actors:manage-access',
        'runs:read',
        'datasets:read', 'datasets:write', 'datasets:manage-access',
        'key-value-stores:read', 'key-value-stores:write', 'key-value-stores:manage-access',
        'tasks:read', 'tasks:write', 'tasks:manage-access',
        'proxy:use',
        'organization:manage'
    ]
};

// Assign minimal required permissions
function assignRole(userId, role) {
    const permissions = roleTemplates[role];
    if (!permissions) {
        throw new Error(`Unknown role: ${role}`);
    }
    
    return permissions;
}
```

Understanding Apify's permission system is crucial for implementing proper access control in organization accounts. Each permission grants specific capabilities while maintaining security boundaries, enabling teams to collaborate effectively while protecting sensitive resources and data.