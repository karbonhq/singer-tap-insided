# singer-tap-insided
Singer.io tap for extracting data from community app inSided (https://www.insided.com/)

See the getting [started guide for running taps.](https://github.com/singer-io/getting-started/blob/master/docs/RUNNING_AND_DEVELOPING.md#running-singer-with-python)

This tap:

- Pulls raw data from the [inSided API](https://api2-us-west-2.insided.com/docs/)
- Extracts from the Community and User API
- Outputs the schema for each resource

### Authentication

The tap uses [OAuth 2.0 client credentials to access an inSided account](https://api2-us-west-2.insided.com/docs/#section/Authentication).

### Config File

```json
  {
      "client_id": <CLIENT_ID>,
      "client_secret": <CLIENT_SECRET>
  }
```
