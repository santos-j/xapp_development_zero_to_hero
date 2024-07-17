# Import Python Modules
import json 
import signal
import requests

# Import objects from the Python xApp Framework
from mdclogpy import Level
from ricxappframe.xapp_frame import Xapp, rmr
from ricxappframe.xapp_rest import ThreadedHTTPServer, initResponse

# Initialize the xApp
def __init__(self):
  # Register signal handlers
  signal.signal(signal.SIGQUIT, self.signal_handler)
  signal.signal(signal.SIGTERM, self.signal_handler)
  signal.signal(signal.SIGINT, self.signal_handler)
  
  # Xapp Class constructor
  self._xapp = Xapp(self._entrypoint, rmr_port=4560)
  # Potential flag to control xApp shutdown
   self.shutdown = False

# Function called after the constructor
def _entrypoint(self, xapp):
  # Set log level
  self._xapp.logger.set_level(Level.DEBUG)
  # Load configuration file
  self._xapp._config_data = load(open(self._xapp._config_path))

  # Create a threaded  HTTP server and set the URI for handler callbacks
  self.server = ThreadedHTTPServer("0.0.0.0", 8080)

  # Set new handler to treat requests on a particular URI
  self.server.handler.add_handler(self.server.handler, "GET", "getConfiguration", "/ric/v1/config", self.configGetHandler)

  # Set new handler to treat requests on a particular URI
  self.server.handler.add_handler(self.server.handler, "GET", "healthAlive", "/ric/v1/health/alive", self.healthyGetAliveHandler)

  # Set new handler to treat requests on a particular URI
  self.server.handler.add_handler(self.server.handler, "GET", "healthReady", "/ric/v1/health/ready", self.healthyGetReadyHandler)

  # Set new handler to treat requests on a particular URI
  self.server.handler.add_handler(self.server.handler, "GET", "toggleLogging", "/ric/v1/logging", self.toggleLoggingHandler)

  # Start the REST server
  self.server.start()

  # Flag to toggle logging
  self.logging = False

  # Get namespace name from the xApp Descriptor
  namespace = xapp._config_data["controls"].get("namespace", "my_namespace")
  # Get a variable name from the xApp Descriptor
  entry = xapp._config_data["controls"].get("entry", "my_variable")
  # Get starting value from the xApp Descriptor
  starting_value = xapp._config_data["controls"].get("starting_value", 0)
  # Get sleep interval from the xApp Descriptor
  sleep_interval = xapp._config_data["controls"].get("sleep_interval", 1)

  # Loop while not set to shutdown
  while not self.shutdown:
    # Flag that we are ready to go
    self.ready = True

    # Health check the RMR and SDL
    if not xapp.healthcheck():
      # Oops, something is going wrong
      xapp.logger.error("Healthcheck failed. Terminating.")
      # Let us stop the xApp here
      self.shutdown = True
      
      xapp.rmr_send("test",30000)
      xapp.rmr_send({"yet_another_test": 0}, 30001)

      # Save data the current value on persistent storage
      xapp.sdl.set(namespace, entry, current_value)
      
      # Check for incoming messages
      for (summary, msg_buf) in xapp.rmr_get_messages():
        # If we are set to log information
        if self.logging:
          # Log the received message
          xapp.logger.info("Msg:"+str(summary))
    
        # Dispatch mtypes to custom callbacks
        if summary[rmr.RMR_MS_MSG_TYPE] == 30002:
          self._message_handler(xapp, summary, msg_buf)

    # Sleep for a while
    sleep(1)
      
def signal_handler(self, sig, frame):
  # Log where we are
  self._rmr_xapp.logger.info("signal hander called!")
  # Let's first stop the entrypoint loop
  self.shutdown = True  
  # Low-level command to shutdown registration with the AppMgr
  self._xapp.stop()

# Example of a default message callback
def _message_handler(self, xapp, summary, msg_buf):
  # If we are set to log information
  if self.logging:
    # Logging incoming message types
    xapp.logger.info("Handler called for mtype: " + str(summary[rmr.RMR_MS_MSG_TYPE]))
    # Logging incoming message contents
    xapp.logger.debug("Message content: " + str(summary[rmr.RMR_MS_PAYLOAD]))
    
  # Free allocated memory
  xapp.rmr_free(msg_buf)

def healthyGetAliveHandler(self, name, path, data, ctype):
    response = initResponse()
  
    # If we are set to log information
    if self.logging:
      self._xapp.logger.info("REST GetAliveHandler")
      
    response['payload'] = dumps({'status': 'alive'})
    return response

def configGetHandler(self, name, path, data, ctype):
    response = initResponse()

    # If we are set to log information
    if self.logging:
      self._xapp.logger.info("REST GetConfigHandler")
      
    response['payload'] = dumps(self._xapp._config_data)
    return response

def healthyGetReadyHandler(self, name, path, data, ctype):
    response = initResponse()

    # If we are set to log information
    if self.logging:
      self._xapp.logger.info("REST GetReadyHandler")
      
    response['payload'] = dumps({'status': 'ready' if self.ready else 'not_ready'})
    return response

def toggleLoggingHandler(self, name, path, data, ctype):
    response = initResponse()

    # If we are set to log information
    if self.logging:
      self._xapp.logger.info("REST ToggleLoggingHandler")

    # Toggle the logging flag
    self.logging = not self.logging
    return response
