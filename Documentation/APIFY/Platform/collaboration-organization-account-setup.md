# Organization Account Setup | Platform | Apify Documentation

## Overview

Setting up an organization account involves configuring account details, adding team members, assigning roles and permissions, and establishing security settings. This process enables effective team collaboration on the Apify platform.

## Account Configuration

### Basic Account Settings

#### Organization Email Address
Set the primary email address for the organization:
- **Primary contact**: Main point of contact for billing and notifications
- **Admin notifications**: Receives important account updates
- **Support communications**: Used for technical support correspondence

```javascript
// Update organization email via API
const { ApifyApi } = require('apify-client');
const client = new ApifyApi({ token: 'ORG_API_TOKEN' });

await client.user().update({
    email: 'admin@company.com'
});
```

#### Username Configuration
Change the organization username:
- **Unique identifier**: Must be unique across Apify platform
- **URL component**: Used in Actor and resource URLs
- **Branding**: Reflects organization identity

```javascript
// Update organization username
await client.user().update({
    username: 'my-company-org'
});
```

#### Security Settings
Configure organization-wide security policies:
- **Maximum session lifespan**: Control how long users stay logged in
- **Two-factor authentication**: Require 2FA for all members
- **Password policies**: Set minimum password requirements

### Account Deletion
Option to delete the organization account:
- **Data preservation**: Consider data backup before deletion
- **Member notification**: Inform team members before deletion
- **Irreversible action**: Cannot be undone once completed

## Adding Users

### User Addition Methods

#### By User ID
Add members using their Apify User ID:
```javascript
// Add member by User ID
await client.organization('ORG_ID').members().create({
    userId: 'USER_ID_12345',
    role: 'MEMBER'
});
```

#### By Username
Add members using their Apify username:
```javascript
// Add member by username
await client.organization('ORG_ID').invitations().create({
    username: 'john.doe',
    role: 'DEVELOPER'
});
```

#### By Email Address
Invite users via email address:
```javascript
// Send invitation by email
await client.organization('ORG_ID').invitations().create({
    email: 'jane.smith@company.com',
    role: 'ANALYST',
    message: 'Welcome to our web scraping team!'
});
```

### Role Assignment
Each member must be assigned exactly one role to avoid conflicting permissions:

#### Single Role Restriction
- **One role per member**: Each member can only have one role
- **No role conflicts**: Prevents permission ambiguities
- **Clear responsibility**: Defines exact access level

```javascript
// Correct: Single role assignment
await client.organization('ORG_ID').member('MEMBER_ID').update({
    role: 'DEVELOPER'
});

// Incorrect: Multiple roles not supported
// This would overwrite the previous role
await client.organization('ORG_ID').member('MEMBER_ID').update({
    role: 'ANALYST' // Replaces 'DEVELOPER' role
});
```

### Invitation Management
```javascript
// List pending invitations
const invitations = await client.organization('ORG_ID').invitations().list();

// Resend invitation
await client.organization('ORG_ID').invitation('INVITATION_ID').resend();

// Cancel invitation
await client.organization('ORG_ID').invitation('INVITATION_ID').delete();
```

## Roles and Permissions

### Pre-defined Roles
Three default roles come with new organizations:

#### 1. Admin Role
Full organizational control:
- **Member management**: Add, remove, and modify team members
- **Resource control**: Create, edit, and delete all resources
- **Billing access**: View and manage billing information
- **Security settings**: Modify organization security policies

#### 2. Developer Role
Development-focused permissions:
- **Actor development**: Create and modify Actors
- **Run management**: Start and monitor Actor runs
- **Storage access**: Read and write to datasets and storage
- **Limited admin**: Cannot manage organization settings

#### 3. Viewer Role
Read-only access:
- **Resource viewing**: View Actors, runs, and data
- **No modifications**: Cannot create or modify resources
- **Monitoring**: Monitor team activities and progress
- **Reporting**: Generate reports from available data

### Custom Role Creation
```javascript
// Create custom role
const customRole = await client.organization('ORG_ID').roles().create({
    name: 'Data Analyst',
    description: 'Specialized role for data analysis tasks',
    permissions: [
        'actors:read',
        'runs:read',
        'datasets:read',
        'datasets:export',
        'key-value-stores:read'
    ]
});
```

### Permission Configuration
Configure permissions for different resource types:

#### Actor Permissions
- **Read**: View Actor settings and source code
- **Write**: Edit Actor configuration and code
- **Run**: Execute Actor builds
- **Delete**: Remove Actors
- **Manage access**: Control Actor sharing

#### Storage Permissions
- **Read**: View storage contents
- **Write**: Modify storage data
- **Delete**: Remove storage items
- **Export**: Download storage data
- **Manage access**: Control storage sharing

```javascript
// Configure detailed permissions
const detailedPermissions = {
    actors: ['read', 'write', 'run'],
    datasets: ['read', 'write', 'export'],
    keyValueStores: ['read', 'write'],
    requestQueues: ['read'],
    proxy: ['use'],
    billing: [],
    organization: []
};

await client.organization('ORG_ID').role('ROLE_ID').update({
    permissions: flattenPermissions(detailedPermissions)
});

function flattenPermissions(permissions) {
    const flat = [];
    for (const [resource, actions] of Object.entries(permissions)) {
        for (const action of actions) {
            flat.push(`${resource}:${action}`);
        }
    }
    return flat;
}
```

## Security Settings

### Session Management
Configure maximum session lifespan:
- **Short sessions**: Enhanced security, frequent re-authentication
- **Medium sessions**: Balance between security and convenience
- **Long sessions**: Convenience-focused, less frequent logins

```javascript
// Set session policies
await client.organization('ORG_ID').update({
    securitySettings: {
        maxSessionLifespanHours: 8, // 8-hour sessions
        requireTwoFactorAuth: true,
        allowedIPRanges: ['192.168.1.0/24', '10.0.0.0/8']
    }
});
```

### Two-Factor Authentication
Require 2FA for all organization members:
- **Enhanced security**: Additional authentication factor
- **Compliance**: Meet security compliance requirements
- **Account protection**: Prevent unauthorized access

### IP Address Restrictions
Limit access to specific IP ranges:
```javascript
// Configure IP restrictions
await client.organization('ORG_ID').update({
    securitySettings: {
        allowedIPRanges: [
            '203.0.113.0/24',  // Office network
            '198.51.100.0/24'  // VPN range
        ],
        blockUnknownIPs: true
    }
});
```

## Permission Dependencies

### Understanding Dependencies
Some permissions have dependencies that must be considered:

#### Storage Read Permission
Users with "read" storage permission can access **all organization storages**:
- **Broad access**: Cannot limit to specific datasets
- **Security consideration**: Consider data sensitivity
- **Role design**: Design roles with this in mind

```javascript
// Example: Role with broad storage access
const analystRole = {
    name: 'Data Analyst',
    permissions: [
        'actors:read',
        'runs:read',
        'datasets:read', // Grants access to ALL datasets
        'key-value-stores:read' // Grants access to ALL stores
    ]
};
```

#### Dependent Permissions
```javascript
// Permission dependencies mapping
const permissionDependencies = {
    'actors:run': ['actors:read'],
    'actors:delete': ['actors:read', 'actors:write'],
    'datasets:write': ['datasets:read'],
    'schedules:write': ['actors:read', 'actors:run']
};

// Validate permission set
function validatePermissions(permissions) {
    for (const permission of permissions) {
        const deps = permissionDependencies[permission] || [];
        for (const dep of deps) {
            if (!permissions.includes(dep)) {
                throw new Error(`Permission ${permission} requires ${dep}`);
            }
        }
    }
    return true;
}
```

## Setup Best Practices

### 1. Progressive Setup
```javascript
// Implement step-by-step setup
class OrganizationSetup {
    constructor(apiToken) {
        this.client = new ApifyApi({ token: apiToken });
        this.steps = [
            'configureBasics',
            'createRoles',
            'addMembers',
            'configureSecurity',
            'validateSetup'
        ];
        this.currentStep = 0;
    }
    
    async configureBasics(orgDetails) {
        await this.client.user().update({
            email: orgDetails.email,
            username: orgDetails.username
        });
        
        console.log('✓ Basic configuration completed');
        this.currentStep++;
    }
    
    async createRoles(customRoles) {
        for (const role of customRoles) {
            await this.client.organization().roles().create(role);
        }
        
        console.log('✓ Custom roles created');
        this.currentStep++;
    }
    
    async addMembers(memberList) {
        for (const member of memberList) {
            if (member.email) {
                await this.client.organization().invitations().create(member);
            } else {
                await this.client.organization().members().create(member);
            }
        }
        
        console.log('✓ Team members added');
        this.currentStep++;
    }
    
    async configureSecurity(securitySettings) {
        await this.client.organization().update({
            securitySettings: securitySettings
        });
        
        console.log('✓ Security settings configured');
        this.currentStep++;
    }
    
    async validateSetup() {
        const org = await this.client.organization().get();
        const members = await this.client.organization().members().list();
        const roles = await this.client.organization().roles().list();
        
        console.log('Setup validation:', {
            organizationName: org.username,
            memberCount: members.items.length,
            roleCount: roles.items.length
        });
        
        console.log('✓ Setup validation completed');
        this.currentStep++;
    }
}
```

### 2. Role Template System
```javascript
// Create role templates for common scenarios
const roleTemplates = {
    webScrapingTeam: {
        admin: {
            name: 'Scraping Admin',
            permissions: [
                'actors:read', 'actors:write', 'actors:delete', 'actors:run',
                'datasets:read', 'datasets:write', 'datasets:export',
                'schedules:read', 'schedules:write',
                'proxy:use',
                'organization:manage'
            ]
        },
        developer: {
            name: 'Scraping Developer',
            permissions: [
                'actors:read', 'actors:write', 'actors:run',
                'datasets:read', 'datasets:write',
                'key-value-stores:read', 'key-value-stores:write',
                'proxy:use'
            ]
        },
        analyst: {
            name: 'Data Analyst',
            permissions: [
                'actors:read',
                'runs:read',
                'datasets:read', 'datasets:export',
                'key-value-stores:read'
            ]
        }
    }
};

// Apply role template
async function applyRoleTemplate(orgId, templateName) {
    const template = roleTemplates[templateName];
    
    for (const [roleName, roleConfig] of Object.entries(template)) {
        await client.organization(orgId).roles().create(roleConfig);
        console.log(`Created role: ${roleConfig.name}`);
    }
}
```

### 3. Setup Validation
```javascript
// Comprehensive setup validation
async function validateOrganizationSetup(orgId) {
    const validationResults = {
        basicConfig: false,
        roles: false,
        members: false,
        security: false,
        permissions: false
    };
    
    try {
        // Check basic configuration
        const org = await client.organization(orgId).get();
        validationResults.basicConfig = !!(org.email && org.username);
        
        // Check roles
        const roles = await client.organization(orgId).roles().list();
        validationResults.roles = roles.items.length >= 3; // At least 3 roles
        
        // Check members
        const members = await client.organization(orgId).members().list();
        validationResults.members = members.items.length >= 1; // At least 1 member
        
        // Check security settings
        const securitySettings = org.securitySettings || {};
        validationResults.security = !!(
            securitySettings.maxSessionLifespanHours &&
            securitySettings.requireTwoFactorAuth !== undefined
        );
        
        // Check permission validity
        for (const role of roles.items) {
            validatePermissions(role.permissions);
        }
        validationResults.permissions = true;
        
    } catch (error) {
        console.error('Validation error:', error);
    }
    
    return validationResults;
}
```

## Video Tutorial Reference

For comprehensive visual guidance, Apify provides a [video tutorial](https://www.youtube.com/watch?v=BIL6HqtnvKk) that demonstrates the complete organization account setup process.

Organization account setup is a foundational step that determines how effectively your team can collaborate on the Apify platform. Proper configuration of roles, permissions, and security settings ensures both productivity and security for your automation projects.