# Import Python Modules
import json 
import signal
import requests

# Import objects from the Python xApp Framework
from mdclogpy import Level
from ricxappframe.xapp_frame import RMRXapp, rmr
from ricxappframe.xapp_rest import initResponse
from ricxappframe.xapp_subscribe import NewSubscriber

# Import PyCrate's representaton of the KPM SM
from asn1.kpm import *

# Initialize the xApp
def __init__(self):
  # Register signal handlers
  signal.signal(signal.SIGQUIT, self.signal_handler)
  signal.signal(signal.SIGTERM, self.signal_handler)
  signal.signal(signal.SIGINT, self.signal_handler)
  
  # RMRXapp Class constructor
  self._rmr_xapp = RMRXapp(
    self._default_message_handler,
    config_handler=self.config_handler,
    post_init=self._post_init,
    rmr_port=4560
  )

# Called when xApp descriptor file changes
def config_handler(self, rmr_xapp, config):
  # Check for missing parameters
  if "flag" not in config["controls"]:
    raise ValueError('Missing parameter')
  # Load the new configuration data
  rmr_xapp._config_data = config

# Function called after the constructor
def _post_init(self, rmr_xapp):
  # Create a class attribute
  rmr_xapp.callback_counter = 0
  # Set the log level of the xApp
  rmr_xapp.logger.set_level(Level.DEBUG)

  # Register custom RMR callback handlers
  self._rmr_xapp.register_callback(self._policy_request_handler, A1_POLICY_REQ)
  self._rmr_xapp.register_callback(self._indication_handler, RIC_INDICATION))

  # Create Subscriber Object
  self._submgr = NewSubscriber(
    uri="http://service-ricxapp-example_xapp-http.ricxapp",,
    local_port=8080,
    rmr_port=4560
  )
  # Register Notification Callback Handler
  self._submgr.ResponseHandler(responseCB=self._subscription_notif)
  
  # Hold active subscriptions
  self._subscriptions = []
  # Counter to identify subscriptions
  self._event_instance = 0
  # Iterate list of registered gNodeBs
  for gnb in xapp.get_list_gnb_ids():
    gnb_info = rmr_xapp.GetNodeb(gnb.inventory_name)
  
  # Iterate list of RAN Functions
  for ran_function in gnb_info.ran_functions:
    # Check for matching OID of the KPM
    if ran_function.oid == "1.3.6.1.4.1.53148.1.2.2.2":
      # Subscribe to gNodeB
      self._send_subscription_request(gnb.inventory_name)
      
def signal_handler(self, sig, frame):
  # Log where we are
  self._rmr_xapp.logger.info("signal hander called!")
  # Unsubscribe from all E2 Nodes
  self.unsubscribe()
  # Stop the xApp!
  self._rmr_xapp.stop()

# Example of a default message callback
def _default_message_handler(self, xapp, summary, msg_buf):
  # Logging incoming message types
  xapp.logger.info("Handler called for mtype: " + str(summary[rmr.RMR_MS_MSG_TYPE]))
  # Logging incoming message contents
  xapp.logger.debug("Message content: " + str(summary[rmr.RMR_MS_PAYLOAD]))
  # Modify internal class parameter
  rmr_xapp.callback_counter += 1
  # Return an acknowledgement
  xapp.rmr_rts( msg_buf, new_payload="ack".enncode())
  # Free allocated memory
  xapp.rmr_free(msg_buf)

def _policy_request_handler(self, xapp, summary, msg_buf):
  # Clear message buffer
  self._rmr_xapp.rmr_free(msg_buf)

  try:
    # Get JSON string encoded as bytes
    req = json.loads(
    summary[rmr.RMR_MS_PAYLOAD])
  except (json.decoder.JSONDecodeError, KeyError):
    self.logger.error("Invalid JSON")
  return

  # Check mandatory policy keys
  policy_keys = ["policy_type_id", "operation", "policy_instance_id"]
  if not all(key in policy_keys for key in req.keys()):
    self.logger.error("Invalid policy")
  return

  # Do anything you like!

  # Construct response
  req["handler_id"] = self._rmr_xapp._config_data["name"]
  req["status"] = "OK"
  del req["operation"]

  # Convert dict. to JSON string in UTF-8
  self._xapp.rmr_send(json.dumps(resp).encode(), A1_POLICY_RESP)

# Custom method for creating subscriptions
def _send_subscription_request(self, meid):
  
  # Create trigger condition
  event_definition = {
    "eventDefinition-formats": ("eventDefinition-Format1", {"reportingPeriod": 1000})
  }
  # Encode to ASN.1
  trigger = E2SM_KPM_IEs.E2SM_KPM_EventTriggerDefinition
  trigger.set_val(event_definition)
  encoded_trigger = trigger.to_aper()

  # Create action definition ASN.1
  action_definition = {
    "actionDefinition-formats": (  
      "actionDefinition-Format1", {
        "measInfoList": [
          { 
            "measType": ("measName","DRB.PerDataVolumeDLDist.Bin"),
            "labelInfoList": [ {"measLabel": {"noLabel":"true"}} ],
          },
          { 
            "measType": ("measName","DRB.PerDataVolumeULDist.Bin"),
            "labelInfoList": [ {"measLabel": {"noLabel":"true"}} ],
          }
        ],
        "granulPeriod": 1000 },
    ),
    "ric-Style-Type": 1,
  }

  # Encode to ASN.1
  action = E2SM_KPM_IEs.E2SM_KPM_ActionDefinition
  action.set_val(action_definition)
  encoded_action = action.to_aper()

  # SubMgr URL
  submgr_url = "http://service-ricplt-submgr-http.ricplt:8088/ric/v1/subscriptions"
  # Increment counter
  self._event_instance += 1
  
  # Prepare Subscription Request Payload
  sub_payload = {
      "SubscriptionId": "",
      "ClientEndpoint": {
          "Host": "http://service-ricxapp-example_xapp-http.ricxapp",
          "HTTPPort": 8080,
          "RMRPort": 4560
      },
      "Meid": meid,
      "RANFunctionID": 0,
      "SubscriptionDetails": [{
          "XappEventInstanceId": self._event_instance,
          "EventTriggers": [ encoded_trigger ],
          "ActionToBeSetupList": [{
              "ActionID": 1,
              "ActionType": "report",
              "ActionDefinition": [ encoded_action ],
              "SubsequentAction": {
                  "SubsequentActionType": "continue",
                  "TimeToWait": "10ms"
              }
          }]
      }]
  }

  # Send POST request to the SubMgr
  response = requests.post(
    sub_payload,
    json=sub_payload
  )
  # Handle HTTP Response
  if response.status_code == 201:
    self.logger.debug("Subscription Request Success!")
  else:
    self.logger.debug("Subscription Request Failure!")

# Custom method to handle Notifications
def _subscription_notif(self, name, path, data, ctype):
  # Convert the JSON string to Python
  python_data = json.loads(data)
  
  # Extract the subid from the Notification
  subid = python_data["SubscriptionId"]
  # Store the new subscription
  self._subscriptions.append(subid)
  
  # Extract useful information
  sub_inst= python_data["SubscriptionInstances"][0]
  xapp_event_instance = sub_inst["XappEventInstanceId"]
  e2_event_instance = sub_inst["E2EventInstanceId"]
  error_cause = sub_inst["ErrorCause"]
  error_source = sub_inst["ErrorSource"]
  
  # Respond to the POST request
  response = initResponse()
  return response

# Callback to Handle Indication Messages
def _indication_handler(self, xapp, summary, msg_buf):
  # Get Message Payload
  raw_data = summary[rmr.RMR_MS_PAYLOAD]

  # Populate E2AP ASN.1 Data Structure
  e2ap_pdu.from_aper(raw_data)
  # Decode it from ASN.1 to Python
  pdu = e2ap_pdu.get_val()

  # Parse contents of the message
  if pdu[0] == 'initiatingMessage':
  # Traverse dicts to obtain protocol IEs
  ies = e2ap_pdu.get_val_at(['initiatingMessage', 'value', 'RICindication', 'protocolIEs'])
  # Iterate over protocol IEs
  for ie in ies:
  # If it is the KPM SM message header
  if ie['value'][0] == 'RICindicationHeader':
    # Populate KPM ASN.1 Data Structure
    header = E2SM_KPM_IEs.E2SM_KPM_IndicationHeader
    header.from_aper(ie['value'][1])
    data = header.get_val_at(['indicationHeader-formats', 'indicationHeader-Format1'])
    self.logger.info(f"KPM Hdr {data}")

  # If it is the KPM SM message payload
  elif ie['value'][0] == 'RICindicationMessage':
    # Populate KPM ASN.1 Data Structure
    message = E2SM_KPM_IEs.E2SM_KPM_IndicationMessage
    message.from_aper(ie['value'][1])
    data = message.get_val_at(['indicationMessage-formats','indicationMessage-Format1'])
    self.logger.info(f"KPM Msg {data}")

# Method to Unsubscribe from all E2 Nodes
def unsubscribe(self):
  # Iterate over the active subscriptions
  for subid in self._subscriptions:
    # Unsubscribe to each E2 Node
    data, reason, status = self._submgr.UnSubscribe(subid)
    # Handle Unsubscribe Response
    if status == 204:
      self.logger.debug("Subscription Delete Successful!")
    else:
      self.logger.debug(f"Subscription Delete Failure! {status} {reason}")

