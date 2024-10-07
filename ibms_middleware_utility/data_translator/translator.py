import logging

from ibms_middleware_utility.data_translator.translation_functions import *
from ibms_middleware_utility.utils.helper import extract_value_from_json_path

logger = logging.getLogger(__name__)


def apply_custom_function(value, function_name):
    try:
        # Dynamically call the function by name if it exists
        if function_name in globals():
            return globals()[function_name](value)
        else:
            raise Exception(f"Function {function_name} not found!")
    except Exception as e:
        raise Exception(f"Error applying function {function_name}: {e}")


class DataTransformer:
    def __init__(self, json_data, mapping):
        self.json_data = json_data
        self.mapping = mapping

    def transform_data(self):
        transformed_data = {}
        for key, details in self.mapping.items():
            bacnet_class = details['bacnet_class']
            bacnet_params = details['bacnet_params']
            json_path = details['json_path']
            transformation_function = details.get('transformation_function')

            try:
                # Extract the value from the JSON using the specified json_path
                value = extract_value_from_json_path(self.json_data, json_path)
                if transformation_function:

                    if value is not None:
                        transformed_value = apply_custom_function(value, transformation_function)
                        if transformed_value is None:
                            raise Exception(f"Unable to transform {key}: {value}")
                        else:
                            transformed_data[key] = {
                                "value": transformed_value,
                                "bacnet_class": bacnet_class,
                                "bacnet_params": bacnet_params
                            }

                else:
                    transformed_data[key] = {
                        "value": value,
                        "bacnet_class": bacnet_class,
                        "bacnet_params": bacnet_params
                    }
            except Exception as err:
                logger.error(f"An unexpected error occurred: {err}")
                raise
        return transformed_data
