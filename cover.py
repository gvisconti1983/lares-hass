import logging
import voluptuous as vol
import asyncio
import ssl
import websockets
import json
from .laresToolbox import *

import homeassistant.helpers.config_validation as cv

from homeassistant.components.cover import SUPPORT_CLOSE, PLATFORM_SCHEMA, SUPPORT_OPEN, SUPPORT_STOP, STATE_CLOSED, STATE_OPEN, CoverEntity
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
	vol.Required(CONF_HOST): cv.string,
	vol.Optional(CONF_PASSWORD): cv.string,
})

ssl_context = ssl.SSLContext() 
ssl_context.verify_mode = ssl.CERT_NONE
ssl_context.options = (ssl.OP_ALL|ssl.OP_NO_SSLv2|ssl.OP_NO_SSLv3|ssl.OP_NO_RENEGOTIATION)

laresHost = ""
laresPassword = ""

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
	laresHost = config[CONF_HOST]
	laresPassword = config.get(CONF_PASSWORD)
	laresRolls = []
	async with websockets.connect(
		laresHost, ssl=ssl_context, subprotocols = ['KS_WSOCK']
	) as websocket:
		login_id = await laresLogin(websocket, laresPassword)
		if(login_id >= 0):
			_LOGGER.info("LARES LOGIN ID: " + str(login_id))
			laresRolls = await getRolls(websocket, login_id, laresPassword)
			
			async_add_entities(LaresCover(laresHost, laresPassword, laresRolls[i]["ID"], "lares " + laresRolls[i]["DES"]) for i in range (0, len(laresRolls)))


class LaresCover(CoverEntity):

	def __init__(self, uri, pin, rollID, name):
		self._roll_id = rollID
		self._name = name
		self._state = None
		self._uri = uri
		self._pin = pin
		self._supported_features = (SUPPORT_OPEN | SUPPORT_CLOSE | SUPPORT_STOP)

	@property
	def name(self):
		return self._name
	@property
	def supported_features(self):
		return self._supported_features	
	@property	
	def state(self):
		return self._state
		
	async def async_open_cover(self):
		async with websockets.connect(
			self._uri, ssl=ssl_context, subprotocols = ['KS_WSOCK']
		) as websocket:
			login_id = await laresLogin(websocket, self._pin)
			if(login_id >= 0):
				cmd_result = await raiseRoll(websocket, login_id, self._pin, self._roll_id)

	async def async_close_cover(self):
		async with websockets.connect(
			self._uri, ssl=ssl_context, subprotocols = ['KS_WSOCK']
		) as websocket:
			login_id = await laresLogin(websocket, self._pin)
			if(login_id >= 0):
				cmd_result = await lowerRoll(websocket, login_id, self._pin, self._roll_id)

	async def async_stop_cover(self):
		async with websockets.connect(
			self._uri, ssl=ssl_context, subprotocols = ['KS_WSOCK']
		) as websocket:
			login_id = await laresLogin(websocket, self._pin)
			if(login_id >= 0):
				cmd_result = await stopRoll(websocket, login_id, self._pin, self._roll_id)
	
	def is_closed(self):
		return None
	
	async def is_closed(self):
		return None
