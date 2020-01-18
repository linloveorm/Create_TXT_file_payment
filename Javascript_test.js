# Shell:
$ export AIRTABLE_API_KEY=YOUR_API_KEY

# Node:
const base = require('airtable').base('appPPfFjCC9DChJWc');

Example using custom configuration

var Airtable = require('airtable');
Airtable.configure({
    endpointUrl: 'https://api.airtable.com',
    apiKey: 'YOUR_API_KEY'
});
var base = Airtable.base('appPPfFjCC9DChJWc');
