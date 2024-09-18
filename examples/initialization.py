import refinerycalc
from refinerycalc.api.simulations_api import SimulationsApi
from refinerycalc.api.refineries_api import RefineriesApi
from refinerycalc.api_client import ApiClient
from refinerycalc import Configuration
from refinerycalc.api.product_prices_api import ProductPricesApi
import os


class RefineryCalcExampleClient:
    """
    This class is a example wrapper around the RefineryCalc API client. It initializes the client with the
    API key and the API URL from the environment variables. It also initializes the API objects that
    are used to make the API calls.
    """
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
