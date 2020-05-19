# KennelApi

KennelAPI is a [DataDog](https://www.datadoghq.com) API wrapper based on configuration files matching attributes from [DataDog API Docs](https://docs.datadoghq.com/api/).

## KennelApi package

The KennelApi package is very simple and easy to expand. In order to properly execute DataDog API calls with KennelApi, you must set your API Key and APP Keys as environment variables before executing this package.

> Environment variables:

`export DATADOG_API_KEY=<API-KEY>`

`export DATADOG_APPLICATION_KEY=<APP-KEY>`

## Create new configurations

* Choose a new endpoint (let's choose [Get a Dashboard](https://docs.datadoghq.com/api/v1/dashboards/#get-a-dashboard) as `get_dashboard`) to consume and define the conf file with all attributes required by the endpoint.

> Create the `config/get_dashboard.conf` file

The required variables are only `dashboard_id`, so our file will only have a single config line. Notice that `kennel.dashboard.id` is the new config key that will be extracted within the Kennel class automatically.

```editorconfig
kennel.dashboard.id=mydashboard-id12323
```


* Copy the DataDog generated code for the chosen endpoint `get_dashboard` and insert it into `KennelApi/kennel.py` as a new function.

> From the DataDog Python code generated, we will choose only the items below `initialize` 

```python
from datadog import initialize, api

options = {
    'api_key': '<DATADOG_API_KEY>',
    'app_key': '<DATADOG_APPLICATION_KEY>'
}

initialize(**options)

dashboard_id = '<DASHBOARD_ID>'

api.Dashboard.get(dashboard_id)
```

> Edit kennel.py and create the `getdashboard` function



```python
def getdashboard(self):
    cnf = self.readconf()
    # extracts the dashboard id from the config file
    dashboard_id = conf['kennel.dashboard.id'] 
    cmd = api.Dashboard.get(dashboard_id)   
    return cmd      
```


* Register the function in the dictionary:

> The Kennel function holds `self.commands` at the `__init__` function:

```json
 self.commands = {
            "all_hosts": self.allhosts,
            "create_dashboard": self.createdashboard,
            "get_dashboard": self.getdashboard
        }
```

You have successfully registered your new endpoint and should be able to run:

`python3 KennelApi -c get_dashboard`

NOTE: When running the cli command, an error may occur due to missing environment keys: `datadog.api.exceptions.ApiNotInitialized: API key is not set. Please run 'initialize' method first.
`
