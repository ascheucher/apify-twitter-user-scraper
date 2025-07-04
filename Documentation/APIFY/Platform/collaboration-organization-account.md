# Organization Account | Platform | Apify Documentation

## Overview

Organization accounts enable team collaboration on the Apify platform by providing centralized billing, team member management, and permission control. Organizations allow multiple users to work together on Actors, share resources, and manage projects collectively.

## Key Features

### Team Collaboration
- **Multiple team members**: Add and manage team members with different roles
- **Shared resources**: Access shared Actors, datasets, and schedules
- **Permission management**: Control what each team member can access and modify
- **Activity tracking**: Monitor team member activities and usage

### Centralized Billing
- **Unified billing**: All Actor and task runs billed to the organization account
- **Cost transparency**: Track usage and costs across team members
- **Resource allocation**: Monitor and control resource consumption
- **Budget management**: Set limits and monitor spending

### Account Management
- **Easy switching**: Switch between personal and organization accounts in two clicks
- **Multiple organizations**: Can own up to 5 organizations
- **Member of multiple**: Can be a member of multiple organizations
- **Role-based access**: Different permission levels for different team members

## Setup Methods

### 1. Create a New Organization
Create a fresh organization account from scratch:

#### Steps to Create New Organization
1. **Navigate to Console**: Go to Apify Console
2. **Account Settings**: Access account settings menu
3. **Organizations**: Find the organizations section
4. **Create New**: Click "Create new organization"
5. **Configure Details**: Set organization name and settings
6. **Invite Members**: Add team members with appropriate roles

```javascript
// Create organization via API
const { ApifyApi } = require('apify-client');
const client = new ApifyApi({ token: 'YOUR_API_TOKEN' });

const newOrganization = await client.organizations().create({
    name: 'My Company Team',
    description: 'Development team for web scraping projects'
});

console.log('Organization created:', newOrganization.id);
```

### 2. Convert Existing Account
Transform an existing user account into an organization:

#### Important Conversion Notes
⚠️ **Critical Information**:
- **Cannot sign in**: You can't sign in to the converted account after conversion
- **Irreversible**: An organization cannot be converted back to a personal account  
- **New account created**: A new personal account is automatically created for you
- **Data preservation**: All existing Actors, data, and settings are preserved

#### Conversion Process
1. **Backup important data**: Ensure all critical data is backed up
2. **Document access**: Note all API tokens and integrations
3. **Navigate to settings**: Go to account conversion section
4. **Confirm conversion**: Follow the conversion wizard
5. **Set up new personal account**: Complete setup of automatically created account
6. **Update integrations**: Update API tokens and external integrations

```javascript
// Note: Account conversion is typically done via Console
// API tokens will need to be regenerated after conversion
const organizationClient = new ApifyApi({ 
    token: 'NEW_ORGANIZATION_TOKEN' 
});

// Verify organization conversion
const orgInfo = await organizationClient.user().get();
console.log('Organization info:', orgInfo);
```

## Member Management

### Adding Team Members
```javascript
// Invite team member via API
const invitation = await client.organization('ORG_ID').members().create({
    userId: 'USER_ID_TO_INVITE',
    role: 'MEMBER', // or 'ADMIN'
    permissions: [
        'actors:read',
        'actors:write',
        'runs:read',
        'runs:write',
        'datasets:read'
    ]
});

console.log('Invitation sent:', invitation.id);
```

### Role Management
```javascript
// Update member role
await client.organization('ORG_ID').member('MEMBER_ID').update({
    role: 'ADMIN',
    permissions: [
        'actors:read',
        'actors:write',
        'actors:delete',
        'runs:read',
        'runs:write',
        'datasets:read',
        'datasets:write',
        'organization:manage'
    ]
});
```

### Member Roles

#### Admin Role
- **Full access**: Complete organization management
- **Member management**: Add, remove, and modify team members
- **Billing access**: View and manage billing information
- **Resource control**: Create, modify, and delete all resources
- **Settings management**: Modify organization settings

#### Member Role
- **Limited access**: Access based on assigned permissions
- **Resource usage**: Use shared resources within permissions
- **Collaboration**: Participate in team projects
- **No admin functions**: Cannot manage organization settings or members

#### Custom Permissions
```javascript
// Define custom permission sets
const permissionSets = {
    developer: [
        'actors:read',
        'actors:write',
        'runs:read',
        'runs:write',
        'datasets:read',
        'datasets:write'
    ],
    dataAnalyst: [
        'actors:read',
        'runs:read',
        'datasets:read',
        'datasets:export'
    ],
    manager: [
        'actors:read',
        'runs:read',
        'runs:write',
        'datasets:read',
        'schedules:read',
        'schedules:write',
        'billing:read'
    ]
};

// Assign permissions to member
await client.organization('ORG_ID').member('MEMBER_ID').update({
    permissions: permissionSets.developer
});
```

## Account Switching

### Console Switching
Easy account switching in Apify Console:
1. **Account selector**: Click account name in top navigation
2. **Choose account**: Select personal or organization account
3. **Instant switch**: Context immediately changes to selected account
4. **Visual indicators**: Clear indication of current account context

### Programmatic Switching
```javascript
// Different API clients for different accounts
const personalClient = new ApifyApi({ 
    token: 'PERSONAL_API_TOKEN' 
});

const orgClient = new ApifyApi({ 
    token: 'ORGANIZATION_API_TOKEN' 
});

// Check current account context
const personalInfo = await personalClient.user().get();
const orgInfo = await orgClient.user().get();

console.log('Personal account:', personalInfo.username);
console.log('Organization account:', orgInfo.username);
```

### Context Management
```javascript
// Manage multiple account contexts
class AccountManager {
    constructor() {
        this.accounts = new Map();
        this.currentAccount = null;
    }
    
    addAccount(name, token, type = 'personal') {
        this.accounts.set(name, {
            client: new ApifyApi({ token }),
            type,
            token
        });
    }
    
    switchTo(accountName) {
        if (!this.accounts.has(accountName)) {
            throw new Error(`Account ${accountName} not found`);
        }
        
        this.currentAccount = accountName;
        return this.accounts.get(accountName).client;
    }
    
    getCurrentClient() {
        if (!this.currentAccount) {
            throw new Error('No account selected');
        }
        
        return this.accounts.get(this.currentAccount).client;
    }
    
    listAccounts() {
        return Array.from(this.accounts.entries()).map(([name, account]) => ({
            name,
            type: account.type
        }));
    }
}

// Usage
const accountManager = new AccountManager();
accountManager.addAccount('personal', 'PERSONAL_TOKEN', 'personal');
accountManager.addAccount('company', 'ORG_TOKEN', 'organization');

// Switch between accounts
const personalClient = accountManager.switchTo('personal');
const orgClient = accountManager.switchTo('company');
```

## Billing and Usage

### Organization Billing
- **Actor runs**: Billed to organization account
- **Task runs**: Charged to organization
- **Storage usage**: Datasets, key-value stores billed to organization
- **Proxy usage**: Proxy consumption billed to organization

### Usage Monitoring
```javascript
// Monitor organization usage
const getOrganizationUsage = async (orgId) => {
    const client = new ApifyApi({ token: 'ORG_TOKEN' });
    
    // Get organization stats
    const org = await client.organization(orgId).get();
    
    // Get member activity
    const members = await client.organization(orgId).members().list();
    
    // Get recent runs
    const runs = await client.actor().runs().list({
        limit: 100,
        desc: true
    });
    
    // Calculate usage metrics
    const usage = {
        totalMembers: members.items.length,
        activeMembers: members.items.filter(m => m.lastActiveAt > Date.now() - 30 * 24 * 60 * 60 * 1000).length,
        recentRuns: runs.items.length,
        totalComputeUnits: runs.items.reduce((sum, run) => sum + (run.stats?.computeUnits || 0), 0),
        costs: runs.items.reduce((sum, run) => sum + (run.stats?.cost || 0), 0)
    };
    
    return usage;
};

// Usage tracking
const usage = await getOrganizationUsage('ORG_ID');
console.log('Organization usage:', usage);
```

### Cost Control
```javascript
// Implement cost monitoring and alerts
class CostMonitor {
    constructor(organizationId, apiToken, thresholds) {
        this.client = new ApifyApi({ token: apiToken });
        this.orgId = organizationId;
        this.thresholds = thresholds;
    }
    
    async checkCosts() {
        const currentMonth = new Date().getMonth();
        const currentYear = new Date().getFullYear();
        
        const runs = await this.client.actor().runs().list({
            limit: 1000,
            desc: true
        });
        
        // Filter runs for current month
        const monthlyRuns = runs.items.filter(run => {
            const runDate = new Date(run.startedAt);
            return runDate.getMonth() === currentMonth && 
                   runDate.getFullYear() === currentYear;
        });
        
        const monthlyCost = monthlyRuns.reduce(
            (sum, run) => sum + (run.stats?.cost || 0), 0
        );
        
        // Check thresholds
        if (monthlyCost > this.thresholds.critical) {
            await this.sendAlert('CRITICAL', monthlyCost);
        } else if (monthlyCost > this.thresholds.warning) {
            await this.sendAlert('WARNING', monthlyCost);
        }
        
        return {
            monthlyCost,
            runCount: monthlyRuns.length,
            projectedMonthlyCost: this.projectMonthlyCost(monthlyCost)
        };
    }
    
    projectMonthlyCost(currentCost) {
        const dayOfMonth = new Date().getDate();
        const daysInMonth = new Date(
            new Date().getFullYear(), 
            new Date().getMonth() + 1, 
            0
        ).getDate();
        
        return (currentCost / dayOfMonth) * daysInMonth;
    }
    
    async sendAlert(level, cost) {
        console.log(`${level} ALERT: Monthly cost is $${cost.toFixed(2)}`);
        // Implement your alert mechanism (email, Slack, etc.)
    }
}

// Usage
const costMonitor = new CostMonitor('ORG_ID', 'ORG_TOKEN', {
    warning: 100,  // $100
    critical: 500  // $500
});

setInterval(async () => {
    const costInfo = await costMonitor.checkCosts();
    console.log('Cost check:', costInfo);
}, 24 * 60 * 60 * 1000); // Daily check
```

## Resource Sharing

### Shared Actors
```javascript
// Share Actor with organization members
const shareActor = async (actorId, organizationId) => {
    await client.actor(actorId).update({
        accessRights: {
            users: [], // Clear individual user access
            groups: [
                {
                    groupId: organizationId,
                    permission: 'WRITE'
                }
            ]
        }
    });
    
    console.log(`Actor ${actorId} shared with organization ${organizationId}`);
};

// Access shared Actor
const accessSharedActor = async (actorId) => {
    try {
        const actor = await client.actor(actorId).get();
        console.log('Accessing shared Actor:', actor.name);
        
        // Run shared Actor
        const run = await client.actor(actorId).start({
            input: { /* your input */ }
        });
        
        return run;
    } catch (error) {
        console.error('Access denied to Actor:', error.message);
    }
};
```

### Shared Datasets
```javascript
// Share dataset with organization
const shareDataset = async (datasetId, organizationId) => {
    await client.dataset(datasetId).update({
        accessRights: {
            groups: [
                {
                    groupId: organizationId,
                    permission: 'READ'
                }
            ]
        }
    });
};

// Access shared dataset
const accessSharedDataset = async (datasetId) => {
    const dataset = await client.dataset(datasetId);
    const { items } = await dataset.listItems();
    
    console.log(`Shared dataset contains ${items.length} items`);
    return items;
};
```

## Best Practices

### 1. Permission Management
```javascript
// Implement least privilege principle
const assignMinimalPermissions = (role, projectType) => {
    const basePermissions = ['actors:read', 'runs:read'];
    
    const rolePermissions = {
        viewer: [],
        developer: ['actors:write', 'runs:write', 'datasets:read'],
        lead: ['actors:write', 'runs:write', 'datasets:read', 'datasets:write', 'schedules:write'],
        admin: ['actors:delete', 'datasets:delete', 'organization:manage']
    };
    
    const projectPermissions = {
        scraping: ['proxy:use'],
        automation: ['schedules:write'],
        analysis: ['datasets:export']
    };
    
    return [
        ...basePermissions,
        ...(rolePermissions[role] || []),
        ...(projectPermissions[projectType] || [])
    ];
};
```

### 2. Activity Monitoring
```javascript
// Monitor team activity
const monitorTeamActivity = async (organizationId) => {
    const members = await client.organization(organizationId).members().list();
    const activityReport = [];
    
    for (const member of members.items) {
        const memberRuns = await client.actor().runs().list({
            userId: member.userId,
            limit: 50
        });
        
        const recentActivity = memberRuns.items.filter(run => 
            Date.now() - new Date(run.startedAt).getTime() < 7 * 24 * 60 * 60 * 1000
        );
        
        activityReport.push({
            userId: member.userId,
            username: member.username,
            recentRuns: recentActivity.length,
            lastActiveAt: member.lastActiveAt,
            totalCost: recentActivity.reduce((sum, run) => sum + (run.stats?.cost || 0), 0)
        });
    }
    
    return activityReport;
};
```

### 3. Resource Governance
```javascript
// Implement resource usage policies
class ResourceGovernance {
    constructor(organizationId, apiToken) {
        this.client = new ApifyApi({ token: apiToken });
        this.orgId = organizationId;
        this.policies = {
            maxRunsPerUser: 100,
            maxMemoryPerRun: 4096,
            maxTimeoutPerRun: 3600,
            allowedActorTypes: ['web-scraper', 'data-processor']
        };
    }
    
    async enforceRunPolicy(userId, runConfig) {
        // Check user's recent run count
        const userRuns = await this.client.actor().runs().list({
            userId: userId,
            limit: this.policies.maxRunsPerUser + 1
        });
        
        if (userRuns.items.length >= this.policies.maxRunsPerUser) {
            throw new Error(`User ${userId} exceeded maximum runs limit`);
        }
        
        // Check resource limits
        if (runConfig.memoryMbytes > this.policies.maxMemoryPerRun) {
            throw new Error('Memory limit exceeded');
        }
        
        if (runConfig.timeoutSecs > this.policies.maxTimeoutPerRun) {
            throw new Error('Timeout limit exceeded');
        }
        
        return true;
    }
    
    async auditCompliance() {
        const members = await this.client.organization(this.orgId).members().list();
        const violations = [];
        
        for (const member of members.items) {
            const memberRuns = await this.client.actor().runs().list({
                userId: member.userId,
                limit: 10
            });
            
            for (const run of memberRuns.items) {
                if (run.options?.memoryMbytes > this.policies.maxMemoryPerRun) {
                    violations.push({
                        userId: member.userId,
                        runId: run.id,
                        violation: 'memory_exceeded',
                        value: run.options.memoryMbytes
                    });
                }
            }
        }
        
        return violations;
    }
}
```

## Pricing and Plans

Organization accounts are available on all Apify pricing plans:
- **Free Plan**: Basic organization features
- **Starter Plan**: Enhanced collaboration features
- **Professional Plan**: Advanced team management
- **Enterprise Plan**: Full organizational control

For specific pricing details, contact support@apify.com.

Organization accounts provide powerful collaboration capabilities that scale with your team's needs, enabling efficient resource sharing, permission management, and unified billing for professional web scraping and automation projects.