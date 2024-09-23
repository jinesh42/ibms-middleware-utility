import json
import logging

logger = logging.getLogger(__name__)

def read_json_file(file_path):
    """
    Reads a JSON file from the given file path and returns the data.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict or list: Parsed JSON data from the file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        PermissionError: If the file cannot be accessed due to permission issues.
        json.JSONDecodeError: If the file content is not valid JSON.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError as file_error:
        logger.error(f"File not found: '{file_error}'")
        raise
    except PermissionError:
        logger.error(f"Permission denied to access '{file_path}'.")
        raise
    except json.JSONDecodeError:
        logger.error(f"Failed to decode JSON from file '{file_path}'.")
        raise
