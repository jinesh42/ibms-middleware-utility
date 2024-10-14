import logging
import argparse
import asyncio

from ibms_middleware_utility.connectors.bacnet_connector import BACnetApp
from ibms_middleware_utility.data_translator.translator import DataTransformer
from ibms_middleware_utility.logger_config import setup_logging
from ibms_middleware_utility.utils.helper import read_json_file
from ibms_middleware_utility.web.webreq import WebRequests


async def fetch_api_data(webreq, bacnet_app, interval, mapping, logger):
    """Fetch API data in a loop."""
    while True:
        response = webreq.send_request()
        if response:
            logger.info(f"API Response: {response}")
            translator = DataTransformer(json_data=response, mapping=mapping)
            transform_data = translator.transform_data()
            bacnet_app.broadcast_data(transform_data)
        await asyncio.sleep(interval)


async def main(config_file):
    """Main function that initializes the modules, loads configuration, and runs the process."""
    setup_logging("logs", "app.log")  # Path should be loaded from configuration file

    logger = logging.getLogger(__name__)
    logger.info("Starting the application...")

    try:
        logger.debug(f"Reading configuration from: {config_file}")
        config = read_json_file(config_file)

        bacnet_config = config.get("bacnet", {})
        bacnet_app = BACnetApp(
            device_id=bacnet_config["device_id"],
            local_obj_name="Middleware Utility",
            ip=bacnet_config["ip"]
        )

        webrequest_config = config.get("webreq", {})
        webreq = WebRequests(url=webrequest_config.get("url"), params=webrequest_config.get("params"))

        # Fetch API data in a loop
        await fetch_api_data(webreq, bacnet_app, config.get("interval"), config.get("mapping"), logger)

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

    # Run the main function in an asyncio event loop
    asyncio.run(main(args.config_file_path))
