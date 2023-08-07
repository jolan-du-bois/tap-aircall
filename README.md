# tap-aircall

`tap-aircall` is a Singer tap for extracting data from the [aircall API](https://developer.aircall.io/api-references/).

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Capabilities 

- catalog
- state 
- discover 
- about 
- stream-maps
- schema-flattening
-  batch

## Settings

Setting | Required | Default | Description
--- | --- | --- | --- 
api_token | True | None | The token to authenticate against the API service
api_id | True | None | The id to authenticate against the API service
auth_token | False | None | The token to authenticate against the API service
project_ids | False | None | Project IDs to replicate
start_date | False | None | The earliest record date to sync in UTC Timezone
api_url | False | https://api.mysample.com | The url for the API service
stream_maps | False | None | Config object for stream maps capability. For more information check out [Stream Maps](https://sdk.meltano.com/en/latest/stream_maps.html)
stream_map_config | False | None | User-defined config values to be used within map expressions
flattening_max_depth | False | None | 'True' to enable schema flattening and automatically expand nested properties
flattening_max_depth | False | None | The max depth to flatten schemas

A full list of supported settings and capabilities for this
tap is available by running:

```bash
poetry run tap-aircall --about
```

## Installation

- [ ] `Developer TODO:` Update the below as needed to correctly describe the install procedure. For instance, if you do not have a PyPi repo, or if you want users to directly install from your git repo, you can modify this step as appropriate.

```bash
pipx install tap-aircall
```

## Configuration

### Authorization Method

To run tap-aircall, you will need an API ID and an API token. Create a file named .secret/config.json and fill it with an array containing the following fields:

- api_id
- api_token
- start_date

The config file should look like this:
```json
{
    "api_id": "123456789",
    "api_token": "ABCDEFGHI",
    "start_date": "2023-08-07 09:30:00"
  }
```

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

## Usage

You can easily run `tap-aircall` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

You can launch the tap in two different ways:

1. **catalog:** this option retrieves all data starting from the date specified in `.secrets/config.json` and updates the `samples/state.json` file with the latest retrieved item.

```bash
./tap-aircall.sh catalog
```

2. **state:** this option retrieves all data starting from the state indicated in `samples/state.json`.


```bash
./tap-aricall.sh state
```

## Developer Resources

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tap_aircall/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-aircall` CLI interface directly using `poetry run`:

```bash
poetry run tap-aircall --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any _"TODO"_ items listed in
the file.

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-aircall
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-aircall --version
# OR run a test `elt` pipeline:
meltano elt tap-aircall target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
