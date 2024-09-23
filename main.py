import logging
import argparse
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

        # TODO: Refactor remove following code
        # To be removed ->
        params = {
            "latitude": 52.52,
            "longitude": 13.41,
            "current": ["temperature_2m", "wind_speed_10m"],
        }
        webreq = WebRequests(url="https://api.open-meteo.com/v1/forecast", params=params)
        response = webreq.send_request()
        if response is not None:
            logger.info(f"Response date: {response}")
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
