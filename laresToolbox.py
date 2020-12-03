import asyncio
import ssl
import websockets
import time
import json
from .crc import addCRC

cmd_id = 1

async def laresLogin(websocket, pin):
	global cmd_id
	cmd_id = 1
	json_cmd = addCRC('{"SENDER":"UhR1YTtPt", "RECEIVER":"", "CMD":"LOGIN", "ID": "1", "PAYLOAD_TYPE":"UNKNOWN", "PAYLOAD":{"PIN":"' + pin + '"}, "TIMESTAMP":"' + str(int(time.time())) + '", "CRC_16":"0x0000"}');
	await websocket.send(json_cmd)
	json_resp = await websocket.recv()
	response = json.loads(json_resp)
	login_ok = (response["PAYLOAD"]["RESULT"] == "OK")
	login_id = -1
	if(login_ok):
		login_id = int(response["PAYLOAD"]["ID_LOGIN"])
	return login_id

async def refreshStatus(websocket, login_id, pin):
	global cmd_id
	cmd_id = cmd_id + 1
	json_cmd = addCRC('{"SENDER":"UhR1YTtPt","RECEIVER":"","CMD":"READ","ID": "' + str(cmd_id) + '","PAYLOAD_TYPE":"MULTI_TYPES","PAYLOAD":{"ID_LOGIN":"'+ str(login_id)+'","ID_READ":"1","TYPES":["OUTPUTS"]},"TIMESTAMP":"' + str(int(time.time())) + '","CRC_16":"0x0000"}')
	await websocket.send(json_cmd)
	json_resp = await websocket.recv()
	response_outputs = json.loads(json_resp)
	
	lares_outputs = response_outputs["PAYLOAD"]["OUTPUTS"]
	
	cmd_id = cmd_id + 1
	json_cmd = addCRC('{"SENDER":"UhR1YTtPt", "RECEIVER":"", "CMD":"REALTIME", "ID": "'+ str(cmd_id) + '", "PAYLOAD_TYPE":"REGISTER", "PAYLOAD":{"ID_LOGIN":"'+str(login_id)+'","TYPES":["STATUS_OUTPUTS","STATUS_SYSTEM"]},"TIMESTAMP":"'+str(int(time.time()))+'","CRC_16":"0x0000"}')
	
	await websocket.send(json_cmd)
	json_resp = await websocket.recv()
	response_realtime = json.loads(json_resp)
	
	lares_realtime = response_realtime["PAYLOAD"]["STATUS_OUTPUTS"]
	
	light_outputs = []
	roll_outputs = []
	
	lares_outputs_with_states = []
	for i in range (0, len(lares_outputs)):
		lares_outputs_with_states.append({**lares_outputs[i], **lares_realtime[i]})
		
	return lares_outputs_with_states
	
async def getLights(websocket, login_id, pin):
	global cmd_id
	cmd_id = cmd_id + 1
	json_cmd = addCRC('{"SENDER":"UhR1YTtPt","RECEIVER":"","CMD":"READ","ID": "' + str(cmd_id) + '","PAYLOAD_TYPE":"MULTI_TYPES","PAYLOAD":{"ID_LOGIN":"'+ str(login_id)+'","ID_READ":"1","TYPES":["OUTPUTS"]},"TIMESTAMP":"' + str(int(time.time())) + '","CRC_16":"0x0000"}')
	await websocket.send(json_cmd)
	json_resp = await websocket.recv()
	response_outputs = json.loads(json_resp)
	
	lares_outputs = response_outputs["PAYLOAD"]["OUTPUTS"]
	
	cmd_id = cmd_id + 1
	json_cmd = addCRC('{"SENDER":"UhR1YTtPt", "RECEIVER":"", "CMD":"REALTIME", "ID": "'+ str(cmd_id) + '", "PAYLOAD_TYPE":"REGISTER", "PAYLOAD":{"ID_LOGIN":"'+str(login_id)+'","TYPES":["STATUS_OUTPUTS","STATUS_SYSTEM"]},"TIMESTAMP":"'+str(int(time.time()))+'","CRC_16":"0x0000"}')
	
	await websocket.send(json_cmd)
	json_resp = await websocket.recv()
	response_realtime = json.loads(json_resp)
	
	lares_realtime = response_realtime["PAYLOAD"]["STATUS_OUTPUTS"]
	
	lares_outputs_with_states = []
	for i in range (0, len(lares_outputs)):
		if(lares_outputs[i]["CAT"]=="LIGHT"):
			lares_outputs_with_states.append({**lares_outputs[i], **lares_realtime[i]})
		
	return lares_outputs_with_states
	
async def getRolls(websocket, login_id, pin):
	global cmd_id
	cmd_id = cmd_id + 1
	json_cmd = addCRC('{"SENDER":"UhR1YTtPt","RECEIVER":"","CMD":"READ","ID": "' + str(cmd_id) + '","PAYLOAD_TYPE":"MULTI_TYPES","PAYLOAD":{"ID_LOGIN":"'+ str(login_id)+'","ID_READ":"1","TYPES":["OUTPUTS"]},"TIMESTAMP":"' + str(int(time.time())) + '","CRC_16":"0x0000"}')
	await websocket.send(json_cmd)
	json_resp = await websocket.recv()
	response_outputs = json.loads(json_resp)
	
	lares_outputs = response_outputs["PAYLOAD"]["OUTPUTS"]
	
	cmd_id = cmd_id + 1
	json_cmd = addCRC('{"SENDER":"UhR1YTtPt", "RECEIVER":"", "CMD":"REALTIME", "ID": "'+ str(cmd_id) + '", "PAYLOAD_TYPE":"REGISTER", "PAYLOAD":{"ID_LOGIN":"'+str(login_id)+'","TYPES":["STATUS_OUTPUTS","STATUS_SYSTEM"]},"TIMESTAMP":"'+str(int(time.time()))+'","CRC_16":"0x0000"}')
	
	await websocket.send(json_cmd)
	json_resp = await websocket.recv()
	response_realtime = json.loads(json_resp)
	
	lares_realtime = response_realtime["PAYLOAD"]["STATUS_OUTPUTS"]
	
	lares_outputs_with_states = []
	for i in range (0, len(lares_outputs)):
		if(lares_outputs[i]["CAT"]=="ROLL"):
			lares_outputs_with_states.append({**lares_outputs[i], **lares_realtime[i]})
		
	return lares_outputs_with_states


async def setOutput(websocket, login_id, pin, output_id, status):
	global cmd_id
	cmd_id = cmd_id + 1
	json_cmd= addCRC('{"SENDER":"UhR1YTtPt", "RECEIVER":"", "CMD":"CMD_USR", "ID": "' + str(cmd_id) + '", "PAYLOAD_TYPE":"CMD_SET_OUTPUT", "PAYLOAD":{"ID_LOGIN":"'+str(login_id)+'","PIN":"'+pin+'","OUTPUT":{"ID":"'+str(output_id)+'","STA":"'+status+'"}}, "TIMESTAMP":"' + str(int(time.time())) + '", "CRC_16":"0x0000"}')	
	await websocket.send(json_cmd)
	json_resp = await websocket.recv()
	response = json.loads(json_resp)
	cmd_ok = False	
	if(response["PAYLOAD"]["RESULT"]=="OK"):
		cmd_ok = True
	return cmd_ok

async def turnOnLight(websocket, login_id, pin, output_id):
	cmd_ok = await setOutput(websocket, login_id, pin, output_id, "ON")
	
async def turnOffLight(websocket, login_id, pin, output_id):
	cmd_ok = await setOutput(websocket, login_id, pin, output_id, "OFF")
	
	
async def raiseRoll(websocket, login_id, pin, output_id):
	cmd_ok = await setOutput(websocket, login_id, pin, output_id, "UP")

async def lowerRoll(websocket, login_id, pin, output_id):
	cmd_ok = await setOutput(websocket, login_id, pin, output_id, "DOWN")

async def stopRoll(websocket, login_id, pin, output_id):
	cmd_ok = await setOutput(websocket, login_id, pin, output_id, "ALT")

async def setRoll(websocket, login_id, pin, output_id, setpoint):
	rollState = await refreshStatus(websocket, login_id, pin)
	rollStateValue = int(rollState[output_id-1]["POS"])
	if(rollStateValue > setpoint):
		await lowerRoll(websocket, login_id, pin, output_id)
		time.sleep(2)
		await stopRoll(websocket, login_id, pin, output_id)
	else:
		await raiseRoll(websocket, login_id, pin, output_id)
		time.sleep(2)
		await stopRoll(websocket, login_id, pin, output_id)	
	rollState = await refreshStatus(websocket, login_id, pin)
	rollState = int(rollState[output_id-1]["POS"])
	print("Set to: " + rollState)
	