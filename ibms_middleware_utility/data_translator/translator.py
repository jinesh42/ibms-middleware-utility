import logging

from ibms_middleware_utility.data_translator.translation_functions import *
from ibms_middleware_utility.utils.helper import extract_value_from_json_path

logger = logging.getLogger(__name__)


class DataTransformer:
    def __init__(self, json_data, mapping):
        self.json_data = json_data
        self.mapping = mapping

    def apply_custom_function(self, value, function_name):
        try:
            # Dynamically call the function by name if it exists
            if function_name in globals():
                return globals()[function_name](value)
            else:
                raise Exception(f"Function {function_name} not found!")
        except Exception as e:
            raise Exception(f"Error applying function {function_name}: {e}")

    def transform_data(self):
        transformed_data = {}
        for key, details in self.mapping.items():
            bacnet_point = details['bacnet_point']
            object_type = details['object_type']
            json_path = details['json_path']
            transformation_function = details.get('transformation_function')

            try:
                if transformation_function:
                    # Extract the value from the JSON using the specified json_path
                    value = extract_value_from_json_path(self.json_data, json_path)

                    if value is not None:
                        transformed_value = self.apply_custom_function(value, transformation_function)
                        if transformed_value is None:
                            raise Exception(f"Unable to transform {key}: {value}")
                        else:
                            transformed_data[bacnet_point] = (transformed_value, object_type)
            except Exception as err:
                logger.error(f"An unexpected error occurred: {err}")
                raise
        return transformed_data
