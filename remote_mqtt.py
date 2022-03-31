#!/usr/bin/python

import time
import io, json				#needed for exporting payloads to json file
import paho.mqtt.client as mqtt  
from RB_packet_decoder import Decoder 
import argparse
import logging
import base64
import binascii


class mqttStoreForward:

	#class variables
	isConnected = False 
	remote_connected = False	
	isOnMessage = False
				#checks ethernet connection
	lora_client = mqtt.Client()
	remote_client = mqtt.Client()
	packet = None 						#will carry msg payload...empty to begin
	isJsonEmpty = True 					#keep track of whether file is empty
	jsonFilePath = 'packetStorage.json' #INPUT DESIRED JSON FILE NAME HERE OR LEAVE DEFAULT
	payloadData = None
	devEUI = None
	##User Information
	remote_broker_address= '192.168.2.164'
	remote_topic = 'lorawan/up'
	remote_user = 'russmin'
	remote_password = 'Taemin26!'
	bytes = None
	

	def __init__ (self):
		#touch jston file if it does not exist
		file = open(self.jsonFilePath, 'a')
		file.close()

	#connect lora client to localhost
	def setLoraClient(self):
		self.lora_client.connect("127.0.0.1")
		self.remote_client.connect("192.168.2.164")

	#callback function initiated on on_connect property for lora client
	def loraOnConnect(self, client, userdata, flags, rc):
		print("Lora Client Connection: " + str(rc)) 	#Returns a 0
		self.lora_client.subscribe("lora/+/up", qos=0)
		self.isConnected = True

	def remoteOnConnect(self, client, userdata, flags, rc):
		print("Remote Client Connection: " + str(rc)) 	#Returns a 0
		self.remote_connected = True
		#self.remote_client.username_pw_set(self.remote_user,password=self.remote_password)
	#callback function initiated on on_disconnect property for both clients
	def onDisconnect(self, client, userdata, rc):
		self.isConnected = False
		print("The connection has failed.")
	def remoteOnDisconnect(self, client, userdata, flags, rc):
		print("Remote Client Connection has failed " + str(rc)) 	#Returns a 0
		self.remote_connected = False
#  formats the payload message from the endpoint
	def rbPayloadFormatters(self, msg):
		msgObj = json.loads(msg)
		newMsg = {}
		msgHex = base64.b64decode(msgObj["data"])
		newMsg["payload"] = binascii.hexlify(msgHex)
		newMsg["appeui"] = msgObj["appeui"]
		newMsg["seqnumber"] = msgObj["seqn"]
		newMsg["deveui"] = msgObj["deveui"]
		return json.dumps(newMsg)

	#call back function initiated on on_message
	def onMessage(self, mqtt_client, userdata, msg):
		self.packet = self.rbPayloadFormatters(msg.payload)
		pkt = json.loads(self.packet)
		self.devEUI = pkt["deveui"]
		self.payloadData = pkt["payload"]
		self.bytes = bytearray.fromhex(self.payloadData)
		

		print(self.packet)
		self.remote_client.publish(self.remote_topic, payload=self.packet, qos=0)
		self.remote_client.publish(self.remote_topic, )
		DECODE = Decoder()
		print(self.payloadData)
		print(DECODE.Generic_Decoder(self.bytes))
	
		
   	#set callback properties of both clients to their respective functions(from above)
	def setVals(self):
		self.lora_client.on_connect = self.loraOnConnect
		self.lora_client.on_message = self.onMessage
		self.lora_client.on_disconnect = self.onDisconnect
		self.remote_client.on_connect = self.remoteOnConnect
		self.remote_client.on_disconnect = self.remoteOnDisconnect
			#takes packet parameter and appends it to a file
	def writeToJson(self, data):
		with open(self.jsonFilePath, 'a') as myFile:
			myFile.write(data + "\r\n")

	
	#Creates infinite loop needed for paho mqtt loop_forever()
	def runLoop(self):
		while(True):
			time.sleep(1)

	#Creates event loop and new thread that initializes the paho mqtt loops for both clients
	def startLoop(self):
		#UI thread = terminal interaction
		self.lora_client.loop_start()
		self.remote_client.loop_start()

	

def main():
	instance = mqttStoreForward() 	#create instance of class
	instance.startLoop()
	#need to call setVals first because they wont connect to the call backs if the setClient functions are called first
	instance.setVals() 				#set connect and message properties & infinite loop
	instance.setLoraClient() 
	#connect to local host
	instance.runLoop()
	
if __name__ == "__main__":
	main()

		   
