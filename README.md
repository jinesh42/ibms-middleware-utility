# ibms-middleware-utility
A middleware application that can interface between edge devices (such as battery monitoring systems) and the IBMS (Intelligent Building Management System) server, which listens for data over BACnet. 

## Sample config.json
```json
{
  "webreq": {
    "url": "https://api.open-meteo.com/v1/forecast",
    "method": "GET",
    "params": {
      "latitude": 52.52,
      "longitude": 13.41,
      "current": [
        "temperature_2m",
        "wind_speed_10m"
      ]
    }
  },
  "mapping": {
    "latitude": {
      "bacnet_point": "analogInput.1.presentValue",
      "json_path": "$.latitude",
      "object_type": "AnalogInput"
    },
    "longitude": {
      "bacnet_point": "analogInput.2.presentValue",
      "json_path": "$.longitude",
      "object_type": "AnalogInput"
    },
    "temperature": {
      "bacnet_point": "analogInput.3.presentValue",
      "json_path": "$.current.temperature_2m",
      "object_type": "AnalogInput"
    },
    "wind_speed": {
      "bacnet_point": "analogInput.4.presentValue",
      "json_path": "$.current.wind_speed_10m",
      "object_type": "AnalogInput"
    },
    "flag": {
      "bacnet_point": "binaryInput.1.presentValue",
      "json_path": "$.current.time",
      "object_type": "BinaryInput",
      "transformation_function": "check_if_min_even"
    }
  }
}
```