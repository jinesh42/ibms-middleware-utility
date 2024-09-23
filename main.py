import logging
from ibms_middleware_utility.logger_config import setup_logging
from ibms_middleware_utility.web.webreq import WebRequests
import json

def main(config_file):
    """
    Main function that initializes the modules, loads configuration, and runs the process.

    Args:
        config_file (str): Path to the configuration file.
    """
    # Setup logging for the entire application
    setup_logging("logs", "app.log") # TODO: path should be loaded from configuration file

    logger = logging.getLogger(__name__)
    logger.info("Starting the application...")

    try:
        logger.debug(f"Reading configuration from: {config_file}")
        # TODO: Load configuration (e.g., request parameters for webreq, mapping for connectors, translators)

        # TODO: Initialize the Module Manager

        # TODO: Run with the loaded configuration

        # TODO: Refactor remove following code

        
        
        with open('config.json','r') as f:
            dict_json=json.load(f)
        
        webreq = WebRequests(url= dict_json['url'],method=dict_json['method'], params=dict_json['params'])
        response = webreq.send_request()
        if response is not None:
            logger.info(f"Response date: {response}")
        

    except Exception as e:
        logger.error(f"An error occurred in the main application: {e}", exc_info=True)
    finally:
        logger.info("Shutting down the application.")

if __name__ == "__main__":
    config_file = "config.json"  # TODO: replace this with CLI argument
    main(config_file)
