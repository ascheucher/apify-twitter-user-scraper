# Secret input

**Learn about making some Actor input fields secret and encrypted. Ideal for passing passwords, API tokens, or login cookies to Actors.**

## How to set a secret input field

To make an input field secret, you need to add a `"isSecret": true` setting to the input field in the Actor's input schema, like this:

```json
{
    // ...
    "properties": {
        // ...
        "password": {
            "title": "Password",
            "type": "string",
            "description": "A secret, encrypted input field",
            "editor": "textfield",
            "isSecret": true
        },
        // ...
    },
    // ...
}
```

The editor for this input field will then turn into a secret input, and when you edit the field value, it will be stored encrypted.

![Secret input editor](/assets/images/secret-input-editor-c5569783ff1c5e99f663baa6813a8b32.png)

**Type restriction**: This is only available for `string` inputs, and the editor type is limited to `textfield` or `textarea`.

## Read secret input fields

When you read the Actor input through `Actor.getInput()`, the encrypted fields are automatically decrypted (starting with the [`apify` package](https://www.npmjs.com/package/apify) version 3.1.0).

```javascript
> await Actor.getInput();
{
    username: 'username',
    password: 'password'
}
```

If you read the `INPUT` key from the Actor run's default key-value store directly, you will still get the original, encrypted input value.

```javascript
> await Actor.getValue('INPUT');
{
    username: 'username',
    password: 'ENCRYPTED_VALUE:Hw/uqRMRNHmxXYYDJCyaQX6xcwUnVYQnH4fWIlKZL2Vhtq1rZmtoGXQSnhIXmF58+DjKlMZpTlK2zN3