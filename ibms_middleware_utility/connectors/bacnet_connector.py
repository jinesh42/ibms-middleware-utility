import BAC0
import bacpypes3
from BAC0 import connect
from BAC0.core.devices.local.factory import ObjectFactory
import logging

logger = logging.getLogger(__name__)


def map_json_to_bacnet(class_name, object_name, properties, value):
    bacnet_class = getattr(bacpypes3.object, class_name)
    bacnet_object = ObjectFactory(
        objectType=bacnet_class,
        instance=1,
        objectName=object_name,
        properties=properties,
        presentValue=value
    )

    return bacnet_object


class BACnetApp:
    def __init__(self, device_id, local_obj_name, ip, port=47808):
        """
        Initialize BAC0 BACnet device.
        """
        self.device_id = device_id
        self.local_obj_name = local_obj_name
        self.ip = ip
        self.port = port
        self.bacnet_objects = {}
        logger.info(f"Initializing BACnetApp with device (ID: {self.device_id})")

        # Initialize BAC0 device
        try:
            self.device = connect(deviceId=self.device_id, localObjName=self.local_obj_name, ip=self.ip, port=self.port)
            logger.info(f"BACnet device created with IP: {self.ip}, device ID: {self.device_id}")
        except Exception as e:
            logger.error(f"Failed to initialize BACnet device: {e}")
            raise

    def broadcast_data(self, translated_data):
        """
        Broadcast data over BACnet network.
        """
        logger.info("Broadcasting data over the BACnet network...")
        for object_name, body in translated_data.items():
            logger.info(f"Processing object: {object_name} = {body['value']} (Type: {body['bacnet_class']})")
            try:
                # Create/Update the BACnet object and set the present value
                if object_name not in self.bacnet_objects:
                    # Define a new BACnet object with present value
                    bacnet_object = map_json_to_bacnet(class_name=body['bacnet_class'], object_name=object_name,
                                                       properties=body['bacnet_params'],
                                                       value=body['value'])
                    bacnet_object.add_objects_to_application(self.device)
                    logger.info(f"Added new BACnet object: {object_name}")
                    self.bacnet_objects.update({object_name: body['bacnet_params']})
                else:
                    # Update existing object value
                    self.device[object_name].presentValue = body["value"]
                    logger.info(f"Updated BACnet object: {object_name} to value: {body['value']}")
            except Exception as e:
                logger.error(f"Error broadcasting data for {object_name}: {e}")
                raise
