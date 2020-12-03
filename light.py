import logging
import voluptuous as vol
import asyncio
import ssl
import websockets
import json
from .laresToolbox import *

import homeassistant.helpers.config_validation as cv

from homeassistant.components.light import (PLATFORM_SCHEMA, Light, LightEntity)

from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
	vol.Required(CONF_HOST): cv.string,
	vol.Optional(CONF_PASSWORD): cv.string,
})

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2) 
ssl_context.verify_mode = ssl.CERT_NONE
laresHost = ""
laresPassword = ""

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
	laresHost = config[CONF_HOST]
	laresPassword = config.get(CONF_PASSWORD)
	laresOutputs = []
	async with websockets.connect(
		laresHost, ssl=ssl_context, subprotocols = ['KS_WSOCK']
	) as websocket:
		login_id = await laresLogin(websocket, laresPassword)
		if(login_id >= 0):
			_LOGGER.info("LARES LOGIN ID: " + str(login_id))
			laresOutputs = await getLights(websocket, login_id, laresPassword)
			async_add_entities(LaresLight(laresHost, laresPassword, laresOutputs[i]["ID"], "lares " + laresOutputs[i]["DES"]) for i in range (0, len(laresOutputs)))



class LaresLight(LightEntity):

	def __init__(self, uri, pin, lightID, name):
		self._light_id = lightID
		self._name = name
		self._state = 'off'
		self._uri = uri
		self._pin = pin

	@property
	def name(self):
		return self._name

	@property
	def state(self):
		return self._state

	async def async_turn_on(self):
		self._state = 'on'
		async with websockets.connect(
			self._uri, ssl=ssl_context, subprotocols = ['KS_WSOCK']
		) as websocket:
			login_id = await laresLogin(websocket, self._pin)
			if(login_id >= 0):
				cmd_result = await turnOnLight(websocket, login_id, self._pin, self._light_id)
		self._state = 'off'

	async def async_turn_off(self):
		"""Instruct the light to turn off."""
		
		self._state = 'on'
		async with websockets.connect(
			self._uri, ssl=ssl_context, subprotocols = ['KS_WSOCK']
		) as websocket:
			login_id = await laresLogin(websocket, self._pin)
			if(login_id >= 0):
				cmd_result = await turnOnLight(websocket, login_id, self._pin, self._light_id)
		self._state = 'off'
		
	def is_on(self):
		my_status = False
		if (self._state == "on"):
			my_status = True
		return my_status
