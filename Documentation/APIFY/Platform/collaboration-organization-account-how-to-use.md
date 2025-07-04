# How to Use Organization Accounts | Platform | Apify Documentation

## Overview

Organization accounts provide a collaborative environment where team members can work together while maintaining controlled access through permission-based security. Understanding how to effectively use these accounts is essential for team productivity.

## Important Account Restrictions

### Login Limitations
Organization accounts **cannot be directly logged into**:
- **No direct access**: Organization accounts are not user accounts
- **Member-based access**: Access through individual member accounts
- **Collaborative structure**: Designed for team collaboration, not individual use

### Access Method
All access to organization resources happens through:
- **Member accounts**: Individual user accounts with organization permissions
- **Account switching**: Toggle between personal and organization contexts
- **Permission-based access**: Actions limited by assigned role permissions

## Account Switching

### Console Account Switching
Easy switching between personal and organization accounts:

#### Switch Process
1. **Locate account button**: Top-left corner of Apify Console
2. **Click account selector**: Shows available accounts
3. **Select organization**: Choose the organization account to access
4. **Context change**: Interface updates to organization context
5. **Permission application**: Available actions reflect your organization role

```javascript
// Check current account context programmatically
const accountInfo = await client.user().get();
console.log('Current account:', {
    username: accountInfo.username,
    isOrganization: accountInfo.isOrganization,
    organizationId: accountInfo.organizationId
});
```

#### Visual Indicators
The console provides clear indicators of current context:
- **Account name**: Shows in header
- **Organization badge**: Indicates organization context
- **Permission hints**: UI elements reflect available actions
- **Breadcrumb context**: Navigation shows organization scope

### Programmatic Account Management
```javascript
// Manage multiple account contexts
class AccountSwitcher {
    constructor() {
        this.contexts = new Map();
        this.currentContext = null;
    }
    
    addContext(name, token, type) {
        this.contexts.set(name, {
            client: new ApifyApi({ token }),
            type: type, // 'personal' or 'organization'
            token
        });
    }
    
    async switchTo(contextName) {
        if (!this.contexts.has(contextName)) {
            throw new Error(`Context ${contextName} not found`);
        }
        
        this.currentContext = contextName;
        const context = this.contexts.get(contextName);
        
        // Verify context switch
        const userInfo = await context.client.user().get();
        console.log(`Switched to ${contextName}:`, userInfo.username);
        
        return context.client;
    }
    
    getCurrentContext() {
        if (!this.currentContext) {
            throw new Error('No context selected');
        }
        
        return this.contexts.get(this.currentContext);
    }
    
    async validatePermissions(permission) {
        const context = this.getCurrentContext();
        const userInfo = await context.client.user().get();
        
        return userInfo.permissions?.includes(permission) || false;
    }
}

// Usage example
const switcher = new AccountSwitcher();
switcher.addContext('personal', 'PERSONAL_TOKEN', 'personal');
switcher.addContext('company', 'ORG_TOKEN', 'organization');

// Switch to organization context
const orgClient = await switcher.switchTo('company');
```

## Managing Organizations

### Organization Access
View and manage organizations from your account:

#### Organization Tab Access
1. **Navigate to account**: Go to your account page
2. **Organizations tab**: Click "Organizations" tab
3. **View organizations**: See all organizations you're part of
4. **Management options**: Access organization-specific settings

```javascript
// List organizations you're a member of
const organizations = await client.user().get();
console.log('Member of organizations:', organizations.organizations);

// Get detailed organization information
for (const orgId of organizations.organizations) {
    const org = await client.organization(orgId).get();
    console.log(`Organization: ${org.username} (${org.name})`);
}
```

### Leaving Organizations
Members can leave organizations with restrictions:

#### Leave Process
- **Standard members**: Can leave directly
- **Organization owners**: Must transfer ownership first
- **Final member**: Cannot leave if you're the last member

```javascript
// Leave organization
const leaveOrganization = async (orgId, userId) => {
    try {
        // Check if user is owner
        const org = await client.organization(orgId).get();
        if (org.ownerId === userId) {
            throw new Error('Owner must transfer ownership before leaving');
        }
        
        // Leave organization
        await client.organization(orgId).member(userId).delete();
        console.log('Successfully left organization');
        
    } catch (error) {
        console.error('Failed to leave organization:', error.message);
    }
};
```

#### Ownership Transfer
```javascript
// Transfer ownership before leaving
const transferOwnership = async (orgId, newOwnerId) => {
    await client.organization(orgId).update({
        ownerId: newOwnerId
    });
    
    console.log(`Ownership transferred to user ${newOwnerId}`);
};
```

## Permission-Based Actions

### Understanding Your Permissions
Your available actions depend on assigned permissions:

#### Permission Check
```javascript
// Check your permissions in organization
const checkPermissions = async (orgId) => {
    const userInfo = await client.user().get();
    const orgMembership = userInfo.organizations.find(o => o.id === orgId);
    
    if (!orgMembership) {
        throw new Error('Not a member of this organization');
    }
    
    console.log('Your role:', orgMembership.role);
    console.log('Your permissions:', orgMembership.permissions);
    
    return orgMembership.permissions;
};
```

#### Action Validation
```javascript
// Validate action before attempting
const canPerformAction = (userPermissions, requiredPermission) => {
    return userPermissions.includes(requiredPermission);
};

// Example usage
const permissions = await checkPermissions('ORG_ID');

if (canPerformAction(permissions, 'actors:write')) {
    // User can create/edit actors
    await createActor();
} else {
    console.log('Insufficient permissions to create actors');
}
```

### Resource Access Patterns
```javascript
// Safe resource access with permission checking
class PermissionAwareClient {
    constructor(apiClient, userPermissions) {
        this.client = apiClient;
        this.permissions = userPermissions;
    }
    
    async safeActorCreate(actorConfig) {
        if (!this.hasPermission('actors:write')) {
            throw new Error('Permission denied: actors:write required');
        }
        
        return await this.client.actors().create(actorConfig);
    }
    
    async safeActorRun(actorId, input) {
        if (!this.hasPermission('actors:run')) {
            throw new Error('Permission denied: actors:run required');
        }
        
        return await this.client.actor(actorId).start({ input });
    }
    
    async safeDatasetRead(datasetId) {
        if (!this.hasPermission('datasets:read')) {
            throw new Error('Permission denied: datasets:read required');
        }
        
        return await this.client.dataset(datasetId).listItems();
    }
    
    hasPermission(permission) {
        return this.permissions.includes(permission);
    }
    
    getAvailableActions() {
        const actionMap = {
            'actors:read': 'View actors',
            'actors:write': 'Create/edit actors',
            'actors:run': 'Run actors',
            'datasets:read': 'View datasets',
            'datasets:write': 'Modify datasets',
            'proxy:use': 'Use proxy services'
        };
        
        return this.permissions
            .filter(p => actionMap[p])
            .map(p => actionMap[p]);
    }
}
```

## API Access

### Organization API Tokens
Members receive API tokens reflecting their organization permissions:

#### Token Characteristics
- **Permission-scoped**: Reflects your organization role
- **Organization context**: Operates within organization scope
- **Action limitations**: Restricted by assigned permissions

```javascript
// Use organization-scoped API token
const orgClient = new ApifyApi({ 
    token: 'ORGANIZATION_MEMBER_TOKEN' 
});

// Actions are automatically scoped to your permissions
try {
    const run = await orgClient.actor('ACTOR_ID').start({
        input: { url: 'https://example.com' }
    });
    console.log('Run started:', run.id);
} catch (error) {
    if (error.statusCode === 403) {
        console.error('Permission denied:', error.message);
    }
}
```

### Resource Access Through API
API access follows organization permissions:

#### Actor Runs
```javascript
// Access Actor runs based on permissions
const accessActorRuns = async (actorId) => {
    try {
        // View runs (requires runs:read permission)
        const runs = await orgClient.actor(actorId).runs().list();
        console.log(`Found ${runs.items.length} runs`);
        
        // Start run (requires actors:run permission)
        if (canPerformAction(userPermissions, 'actors:run')) {
            const newRun = await orgClient.actor(actorId).start({
                input: { test: true }
            });
            console.log('New run started:', newRun.id);
        }
        
    } catch (error) {
        console.error('Access error:', error.message);
    }
};
```

#### Storage Access
```javascript
// Access storage with appropriate permissions
const accessStorage = async () => {
    try {
        // List datasets (requires datasets:read)
        const datasets = await orgClient.datasets().list();
        console.log('Accessible datasets:', datasets.items.length);
        
        // Read dataset content
        for (const dataset of datasets.items) {
            const { items } = await orgClient.dataset(dataset.id).listItems();
            console.log(`Dataset ${dataset.name}: ${items.length} items`);
        }
        
    } catch (error) {
        console.error('Storage access error:', error.message);
    }
};
```

#### Webhooks and Schedules
```javascript
// Manage webhooks and schedules
const manageAutomation = async () => {
    // Access webhooks (requires webhooks:read permission)
    if (canPerformAction(userPermissions, 'webhooks:read')) {
        const webhooks = await orgClient.webhooks().list();
        console.log('Organization webhooks:', webhooks.items.length);
    }
    
    // Access schedules (requires schedules:read permission)
    if (canPerformAction(userPermissions, 'schedules:read')) {
        const schedules = await orgClient.schedules().list();
        console.log('Organization schedules:', schedules.items.length);
    }
    
    // Create schedule (requires schedules:write permission)
    if (canPerformAction(userPermissions, 'schedules:write')) {
        const newSchedule = await orgClient.schedules().create({
            name: 'Daily Data Collection',
            cronExpression: '0 8 * * *',
            actions: [{
                type: 'RUN_ACTOR',
                actorId: 'ACTOR_ID'
            }]
        });
        console.log('Schedule created:', newSchedule.id);
    }
};
```

## Important Billing Considerations

### Account Context for Billing
Be careful which account context you use to start runs:

#### Billing Account Selection
- **Personal account runs**: Billed to personal account
- **Organization account runs**: Billed to organization account
- **Context matters**: Current account context determines billing

```javascript
// Check current billing context
const checkBillingContext = async () => {
    const userInfo = await client.user().get();
    
    if (userInfo.isOrganization) {
        console.log('Runs will be billed to organization:', userInfo.username);
    } else {
        console.log('Runs will be billed to personal account:', userInfo.username);
    }
    
    return userInfo.isOrganization ? 'organization' : 'personal';
};

// Switch to correct context before starting runs
const runWithCorrectBilling = async (actorId, input, targetContext) => {
    const currentContext = await checkBillingContext();
    
    if (currentContext !== targetContext) {
        console.warn(`Current context: ${currentContext}, but target: ${targetContext}`);
        console.warn('Please switch accounts in Console before running');
        return;
    }
    
    const run = await client.actor(actorId).start({ input });
    console.log(`Run started in ${targetContext} context:`, run.id);
};
```

### Cost Monitoring
```javascript
// Monitor organization costs
const monitorOrganizationCosts = async (orgId) => {
    const runs = await orgClient.actor().runs().list({
        limit: 100,
        desc: true
    });
    
    const thisMonth = new Date().getMonth();
    const monthlyRuns = runs.items.filter(run => 
        new Date(run.startedAt).getMonth() === thisMonth
    );
    
    const totalCost = monthlyRuns.reduce(
        (sum, run) => sum + (run.stats?.cost || 0), 0
    );
    
    console.log(`Organization monthly cost: $${totalCost.toFixed(2)}`);
    console.log(`Runs this month: ${monthlyRuns.length}`);
    
    return { totalCost, runCount: monthlyRuns.length };
};
```

## Security Best Practices

### Token Security
- **Never share API tokens**: Each member should use their own token
- **Never share passwords**: Individual credentials only
- **Regular token rotation**: Update tokens periodically
- **Scope limitations**: Use tokens with minimal required permissions

### Access Control
```javascript
// Implement access control checking
const secureActorExecution = async (actorId, input) => {
    // Verify permission before action
    const permissions = await checkPermissions();
    
    if (!permissions.includes('actors:run')) {
        throw new Error('Insufficient permissions for actor execution');
    }
    
    // Validate input if sensitive
    if (containsSensitiveData(input)) {
        if (!permissions.includes('sensitive-data:access')) {
            throw new Error('Cannot process sensitive data with current permissions');
        }
    }
    
    // Proceed with execution
    return await client.actor(actorId).start({ input });
};

function containsSensitiveData(input) {
    // Implement your sensitive data detection logic
    const sensitivePatterns = [
        /\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b/, // Credit card
        /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/, // Email
        /\b\d{3}[-.]?\d{3}[-.]?\d{4}\b/ // Phone
    ];
    
    const inputString = JSON.stringify(input);
    return sensitivePatterns.some(pattern => pattern.test(inputString));
}
```

## Organization Dashboard

### Custom Dashboard Creation
```javascript
// Create organization-specific dashboard
class OrganizationDashboard {
    constructor(orgClient, permissions) {
        this.client = orgClient;
        this.permissions = permissions;
    }
    
    async getDashboardData() {
        const dashboard = {
            overview: {},
            activities: [],
            resources: {},
            costs: {}
        };
        
        // Organization overview
        if (this.hasPermission('organization:read')) {
            const org = await this.client.organization().get();
            dashboard.overview = {
                name: org.name,
                memberCount: org.memberCount,
                createdAt: org.createdAt
            };
        }
        
        // Recent activities
        if (this.hasPermission('runs:read')) {
            const runs = await this.client.actor().runs().list({ limit: 10 });
            dashboard.activities = runs.items.map(run => ({
                id: run.id,
                actorName: run.actorName,
                status: run.status,
                startedAt: run.startedAt
            }));
        }
        
        // Resource counts
        if (this.hasPermission('actors:read')) {
            const actors = await this.client.actors().list();
            dashboard.resources.actors = actors.items.length;
        }
        
        if (this.hasPermission('datasets:read')) {
            const datasets = await this.client.datasets().list();
            dashboard.resources.datasets = datasets.items.length;
        }
        
        return dashboard;
    }
    
    hasPermission(permission) {
        return this.permissions.includes(permission);
    }
}
```

Organization accounts provide a powerful framework for team collaboration while maintaining security and access control. Understanding how to effectively navigate between contexts, manage permissions, and monitor usage is essential for productive team-based automation projects.