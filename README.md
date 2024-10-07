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
      "json_path": "$.latitude",
	  "bacnet_class": "AnalogValueObject",
	  "bacnet_params": {
		"objectIdentifier": 1,
		"objectName": "Latitude Sensor",
		"units": "degreesAngular"
	  }
    },
    "longitude": {
      "json_path": "$.longitude",
      "bacnet_class": "AnalogValueObject",
	  "bacnet_params": {
		"objectIdentifier": 2,
		"objectName": "Longitude Sensor",
		"units": "degreesAngular"
	  }
    },
    "temperature": {
      "json_path": "$.current.temperature_2m",
      "bacnet_class": "AnalogValueObject",
	  "bacnet_params": {
		"objectIdentifier": 3,
		"objectName": "Temperature Sensor",
		"units": "degreesCelsius"
	  }
    },
    "wind_speed": {
      "json_path": "$.current.wind_speed_10m",
      "bacnet_class": "AnalogValueObject",
	  "bacnet_params": {
		"objectIdentifier": 4,
		"objectName": "Wind Sensor",
		"units": "kilometersPerHour"
	  }
    },
    "flag": {
      "json_path": "$.current.time",
      "bacnet_class": "BinaryValueObject",
	  "bacnet_params": {
		"objectIdentifier": 5,
		"objectName": "Flag Sensor"
	  },
      "transformation_function": "check_if_min_even"
    }
  },
  "bacnet": {
    "device_object_name": "Test Device",
    "device_id": 1234,
    "max_apdu_len": 1476,
    "seg_supported": "segmentedBoth",
    "vendor_id": 15,
    "ip": "192.168.1.103:"
  },
  "interval": 5
}
```