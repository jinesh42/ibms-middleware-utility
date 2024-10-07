import logging
import argparse
import time

from ibms_middleware_utility.connectors.bacnet_connector import BACnetApp
from ibms_middleware_utility.data_translator.translator import DataTransformer
from ibms_middleware_utility.logger_config import setup_logging
from ibms_middleware_utility.utils.helper import read_json_file
from ibms_middleware_utility.web.webreq import WebRequests


def main(config_file):
    """
    Main function that initializes the modules, loads configuration, and runs the process.

    Args:
        config_file (str): Path to the configuration file.
    """
    # Setup logging for the entire application
    setup_logging("logs", "app.log")  # TODO: path should be loaded from configuration file

    logger = logging.getLogger(__name__)
    logger.info("Starting the application...")

    try:
        logger.debug(f"Reading configuration from: {config_file}")
        config = read_json_file(config_file)

        # TODO: Initialize the Module Manager

        # TODO: Run with the loaded configuration

        bacnet_config = config.get("bacnet", {})
        bacnet_app = BACnetApp(
            device_object_name=bacnet_config["device_object_name"],
            device_id=bacnet_config["device_id"],
            max_apdu_len=bacnet_config["max_apdu_len"],
            seg_supported=bacnet_config["seg_supported"],
            vendor_id=bacnet_config["vendor_id"],
            ip=bacnet_config["ip"]
        )

        # TODO: Refactor remove following code
        # To be removed ->
        webrequest_config = config.get("webreq", {})
        webreq = WebRequests(url=webrequest_config.get("url"), params=webrequest_config.get("params"))
        response = webreq.send_request()

        interval = config.get("interval")
        
        if response is not None:
            logger.info(f"Response date: {response}")
            translator = DataTransformer(json_data=response, mapping=config.get("mapping"))
            transform_data = translator.transform_data()
            logger.info(f"transformer's output: {transform_data}")
            while 1:
                bacnet_app.broadcast_data(transform_data)
                time.sleep(interval)
        # To be removed <-

    except Exception as e:
        logger.error(f"An error occurred in the main application: {e}", exc_info=True)
    finally:
        logger.info("Shutting down the application.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Middleware utility.")
    parser.add_argument(
        '-c', '--config_file_path',
        type=str,
        help="Path to the configuration JSON file."
    )

    args = parser.parse_args()

    main(args.config_file_path)
