from bacpypes3.apdu import WritePropertyRequest, ConfirmedRequestSequence, UnconfirmedCOVNotificationRequest
from bacpypes3.app import Application
from bacpypes3.basetypes import PropertyValue
from bacpypes3.local.device import DeviceObject
from bacpypes3.object import *
from bacpypes3.pdu import Address
import logging
import bacpypes3
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def map_json_to_bacnet(object_name, value, class_name, object_params_from_config):
    logger.debug(f"Mapping JSON to BACnet: {object_name}, {value}, {class_name}, {object_params_from_config}")

    try:
        # Dynamically get the class from the string name using getattr
        bacnet_class = getattr(bacpypes3.object, class_name)
    except AttributeError as e:
        logger.error(f"Class '{class_name}' not found in BACnet objects: {e}")
        raise

    # Prepare the parameters required to instantiate the object
    object_params = {
        "objectName": object_name,
        "presentValue": value,
    }
    object_params.update(object_params_from_config)

    try:
        # Dynamically create the BACnet object
        obj = bacnet_class(**object_params)
    except TypeError as e:
        logger.error(f"Error creating BACnet object '{object_name}': {e}")
        raise

    logger.info(f"Successfully created BACnet object: {object_name}")
    return obj


class BACnetApp:
    def __init__(self, device_object_name, device_id, max_apdu_len, seg_supported, vendor_id, ip):
        logger.info(f"Initializing BACnetApp with device {device_object_name} (ID: {device_id})")

        # Create a local BACnet device object
        try:
            self.device = DeviceObject(
                objectName=device_object_name,
                objectIdentifier=device_id,
                maxApduLengthAccepted=max_apdu_len,
                segmentationSupported=seg_supported,
                vendorIdentifier=vendor_id
            )
            logger.info(f"Device object created: {self.device}")
        except Exception as e:
            logger.error(f"Failed to create DeviceObject: {e}")
            raise

        # Create an Application instance with the device and BACnet IP address
        try:
            self.app = Application(self.device, Address(ip))  # BACnet IP address
            logger.info(f"Application created with IP: {ip}")
        except Exception as e:
            logger.error(f"Failed to create Application: {e}")
            raise

        # Dictionary to store BACnet objects already created
        self.bacnet_objects = {}

    def broadcast_data(self, translated_data):
        logger.info("Broadcasting data over the BACnet network...")
        for object_name, body in translated_data.items():
            logger.info(f"Processing object: {object_name} = {body['value']} (Type: {body['bacnet_class']})")
            try:
                # Check if the object already exists in self.bacnet_objects
                if object_name in self.bacnet_objects:
                    # Object exists, so update its present value if it has changed
                    existing_object = self.bacnet_objects[object_name]
                    if existing_object.presentValue != body["value"]:
                        logger.info(f"Updating existing BACnet object: {object_name}")
                        existing_object.presentValue = body["value"]
                        # Send a broadcast over the network
                        self.send_broadcast(existing_object)
                    else:
                        logger.info(f"No change in value for object: {object_name}, skipping broadcast.")
                else:
                    # Object doesn't exist, create and add it
                    obj = map_json_to_bacnet(
                        object_name=body["bacnet_params"].get("objectName", object_name),
                        class_name=body["bacnet_class"],
                        value=body["value"],
                        object_params_from_config=body["bacnet_params"]
                    )
                    # Add object to the BACnet application
                    self.app.add_object(obj)
                    logger.info(f"Added new BACnet object: {object_name}")
                    self.bacnet_objects[object_name] = obj  # Store it to avoid re-adding

                    # Send a broadcast over the network
                    self.send_broadcast(obj)
            except Exception as err:
                logger.error(f"An error occurred while broadcasting {object_name}: {err}")
                raise

    async def send_broadcast_async(self, obj):
        """
        Async method to broadcast the current object's present value on the BACnet network.
        This sends an UnconfirmedCOVNotification or an appropriate broadcast message.
        """
        try:
            # Build the UnconfirmedCOVNotification message to broadcast the present value
            cov_notification = UnconfirmedCOVNotificationRequest(
                initiatingDeviceIdentifier=self.device.objectIdentifier,
                monitoredObjectIdentifier=obj.objectIdentifier,
                timeRemaining=0,  # Could be set based on application needs
                listOfValues=[
                    PropertyValue(propertyIdentifier="presentValue", value=obj.presentValue)
                ]
            )
            # Send the notification over the network asynchronously
            await self.app.request(cov_notification)
            logger.info(f"Broadcasted data for object: {obj.objectName} with value: {obj.presentValue}")
        except Exception as e:
            logger.error(f"Failed to broadcast data for object {obj.objectName}: {e}")
            raise

    def send_broadcast(self, obj):
        """
        Wrapper for sending broadcasts using asyncio.
        Ensures the event loop is running.
        """
        try:
            # Run the asynchronous broadcast in the event loop
            asyncio.run(self.send_broadcast_async(obj))
        except Exception as e:
            logger.error(f"Error in send_broadcast: {e}")
            raise

