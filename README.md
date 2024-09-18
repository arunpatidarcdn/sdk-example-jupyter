# Refinery Calc SDK Examples
This repository contains some examples on how to use the Refinery Calc Python SDK using Jupyter notebook which wraps the Refinery Calc API.

### Getting Started
* Clone the repository 
* cd into the root directory
* create a python virtual environment using terminal
```
python -m venv .venv
```
Activate the virtual environment (macOS)
```
source .venv/bin/activate
```
Activate the virtual environment (Windows)
```
.venv\Scripts\activate
```

### Runing the Sample Code

#### Api Key
Ensure you add your API Key to an Environment Variable `RefineryCalc_Api_Key`

##### Windows Cmd
```
set RefineryCalc_Api_Key=<YOUR API KEY HERE>
```

#### macOS
```
export RefineryCalc_Api_Key=<YOUR API KEY HERE>
```

### Run Sample Code
#### Add a Jupyter Notebook file
Select the required kernel (.venv) on the right top corner of the notebook file.

In the first cell execute the command to install the Refinery Calc SDK and restart the kernel.
```
pip install refinerycalc-api
```

#### Create a simulation
to create a new simulation, you will need the list of refineries that will be used in that simulation. 
Add the given code below in the new cell and execute the script:
```python
from refinerycalc.models.create_simulation_request import CreateSimulationRequest
from initialization import RefineryCalcExampleClient

# you can get refinery ids with a separate call.
# hardcoded here for convenience
refs = [7, 8, 9, 10]
client = RefineryCalcExampleClient()
req = CreateSimulationRequest()
req.refineries = refs
# 0 is default datasource and 1 for IIR
req.data_source = 0
req.name = "my sample simulation"
req.is_time_series = False
response = client.simulations.v1_simulations_post(body=req)
if response.success:
    print(response.simulation_id)
```
#### Run the simulation
to run a simulation, use the simulation id from the previous step. Add the given code below in the new cell and execute the script:
```python
from initialization import RefineryCalcExampleClient
import time

client = RefineryCalcExampleClient()
simulation_id = "<SIMULATION ID FROM RUN SIMULATION>"
response = client.simulations.v1_simulations_id_run_post(simulation_id)
if response.success:
    print(f"running simulation with id {simulation_id}")
    done = False
    while not done:
        status = client.simulations.v1_simulations_id_run_status_get(simulation_id)
        done = (status.is_solved or status.is_cancelled) and not status.is_solving
        if done or status.is_solved:
            break
        print(f"status ({round(status.percent_solved, 2)}%): {status.solve_status}")
        time.sleep(5)
    print("success")
else:
    print(" run failed with error: " + response.message)
```
### To Use in Your Own Program
Add the following code setup where you need it

```python
    import refinerycalc
    from refinerycalc.api.simulations_api import SimulationsApi
    from refinerycalc.api.refineries_api import RefineriesApi
    from refinerycalc.api_client import ApiClient
    from refinerycalc import Configuration
    from refinerycalc.api.product_prices_api import ProductPricesApi
    import os

    class RefineryCalcExampleClient:
    def __init__(self):
        # Get API key and URL from environment variables
        api_key = os.getenv("RefineryCalc_Api_Key")
        api_url = os.getenv("RefineryCalc_Api_Url", "https://api.refinerycalc.com")  # Default URL if not set
        
        # Error handling for missing API key
        if api_key is None:
            raise ValueError("API key is not set. Please set RefineryCalc_Api_Key in your environment.")
        
        # Set up configuration
        config = Configuration()
        config.api_key = api_key
        config.host = api_url
        
        # Initialize the API client
        self.__apiClient = ApiClient(configuration=config, header_name="x-api-key", header_value=config.api_key)
        
        # Set up APIs
        self.simulations = SimulationsApi(self.__apiClient)
        self.refineries = RefineriesApi(self.__apiClient)
        self.productPrices = ProductPricesApi(self.__apiClient)
```
