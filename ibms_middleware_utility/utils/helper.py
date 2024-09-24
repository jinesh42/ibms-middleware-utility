import json
import logging
from jsonpath_ng import jsonpath, parse

logger = logging.getLogger(__name__)


def read_json_file(file_path):
    """
    Reads a JSON file from the given file path and returns the data.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: Parsed JSON data from the file.

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


def extract_value_from_json_path(json_data, json_path):
    """
    Extracts a value from the JSON data using a jsonpath-ng expression.

    Args:
        json_data (dict): JSON file data.
        json_path (str): jsonpath-ng path to key.

    Returns:
        Any: Extracted JSON data from the file.
    """
    try:
        jsonpath_expr = parse(json_path)
        match = jsonpath_expr.find(json_data)
        if match:
            return match[0].value
        else:
            raise Exception(f"No match found for json_path: {json_path}")
    except Exception as e:
        logger.error(f"Error parsing json_path '{json_path}': {e}")
        raise
