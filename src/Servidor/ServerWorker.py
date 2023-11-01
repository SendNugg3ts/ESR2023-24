from random import randint
import sys, traceback, threading, socket
import os
import re

from Servidor.VideoStream import VideoStream
from Servidor.RtpPacket import RtpPacket

class ServerWorker:
	SETUP = 'SETUP'
	PLAY = 'PLAY'
	PAUSE = 'PAUSE'
	TEARDOWN = 'TEARDOWN'
	
	INIT = 0
	READY = 1
	PLAYING = 2
	state = INIT

	OK_200 = 0
	FILE_NOT_FOUND_404 = 1
	CON_ERR_500 = 2
	
	clientInfo = {}
	
	def __init__(self, clientInfo):
		self.clientInfo = clientInfo
		
	def run(self):
		threading.Thread(target=self.recvRtspRequest).start()
	
	def recvRtspRequest(self):
		"""Receive RTSP request from the client."""
		connSocket = self.clientInfo['rtspSocket'][0]
		while True:            
			data = connSocket.recv(256)
			if data:
				print("Data received:\n" + data.decode("utf-8"))
				self.processRtspRequest(data.decode("utf-8"))
	
	def processRtspRequest(self, data):
		"""Process RTSP request sent from the client."""
		# Get the request type
		request = str(data).splitlines()
		line1 = str(request[0]).split()
		requestType = str(line1[0])

		# Get the media file name
		filename = str(line1[1])

		current_pwd_path = os.path.dirname(os.path.abspath(__file__))
		#video_pwd_path = re.findall("(?:(.*?)src)", current_pwd_path)[0]
		#path_to_file = os.path.join(video_pwd_path, "video/" + filename)
		path_to_file = os.path.join(os.path.dirname(os.path.dirname(current_pwd_path)), "video", filename)
		print("Video path:", path_to_file)




		# Get the RTSP sequence number
		seq = int(str(request[1]).split()[1])

		# Process SETUP request
		if requestType == self.SETUP:
			if self.state == self.INIT:
				# Update state
				print("Processing SETUP..\n")
				try:
					self.clientInfo['videoStream'] = VideoStream(str(path_to_file))
					self.state = self.READY
				except IOError:
					self.replyRtsp(self.FILE_NOT_FOUND_404, seq)

				# Generate a randomized RTSP session ID
				self.clientInfo['session'] = randint(100000, 999999)

				# Send RTSP reply
				self.replyRtsp(self.OK_200, seq)

				# Get the RTP/UDP port from the last line
				self.clientInfo['rtpPort'] = str(((str(request[2])).split())[3])

		# Process PLAY request
		elif requestType == self.PLAY:
			if self.state == self.READY:
				# Update state
				print("Processing PLAY..\n")
				self.state = self.PLAYING

				# Create a new socket for RTP/UDP
				self.clientInfo["rtpSocket"] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

				self.replyRtsp(self.OK_200, seq)

				# Create a new thread and start sending RTP packets
				self.clientInfo['event'] = threading.Event()
				self.clientInfo['worker'] = threading.Thread(target=self.sendRtp)
				self.clientInfo['worker'].start()

		# Process PAUSE request
		elif requestType == self.PAUSE:
			if self.state == self.PLAYING:
				# Update state
				print("Processing PAUSE..\n")
				self.state = self.READY

				self.clientInfo['event'].set()

				self.replyRtsp(self.OK_200, seq)

		# Process TEARDOWN request
		elif requestType == self.TEARDOWN:
			print("Processing TEARDOWN..\n")

			self.clientInfo['event'].set()

			self.replyRtsp(self.OK_200, seq)

			# Close the RTP socket
			self.clientInfo['rtpSocket'].close()

	def sendRtp(self):
		"""Send RTP packets over UDP."""
		while True:
			self.clientInfo['event'].wait(0.05) 
			
			# Stop sending if request is PAUSE or TEARDOWN
			if self.clientInfo['event'].isSet(): 
				break 
				
			data = self.clientInfo['videoStream'].nextFrame()
			if data: 
				frameNumber = self.clientInfo['videoStream'].frameNbr()
				try:
					address = self.clientInfo['rtspSocket'][1][0]
					port = int(self.clientInfo['rtpPort'])
					self.clientInfo['rtpSocket'].sendto(self.makeRtp(data, frameNumber),(address,port))
				except Exception as e:
					print(f"Connection Error, {e}")

	def makeRtp(self, payload, frameNbr):
		"""RTP-packetize the video data."""
		version = 2
		padding = 0
		extension = 0
		cc = 0
		marker = 0
		pt = 26 # MJPEG type
		seqnum = frameNbr
		ssrc = 0 
		
		rtpPacket = RtpPacket()
		
		rtpPacket.encode(version, padding, extension, cc, seqnum, marker, pt, ssrc, payload)
		
		return rtpPacket.getPacket()

	def send(self):
		if self.request_type == self.SETUP and self.state == self.INIT:
			threading.Thread(target=self.recvRtspReply).start()
			# Update RTSP sequence number.
			self.rtspSeq += 1
			print('\nSETUP event\n')

			# Write the RTSP request to be sent.
			request = f"""SETUP {self.fileName}
				sequenceNumber: {self.rtspSeq}
				hostname: {self.hostname} rtspPort: {self.rtpPort}"""

			# Keep track of the request.
			self.requestSent = self.SETUP

		# Play request
		elif self.request_type == self.PLAY and self.state == self.READY:
			# Update RTSP sequence number.
			self.rtspSeq += 1
			print('\nPLAY event\n')

			# Write the RTSP request to be sent.
			request = f"""PLAY {self.fileName}
				sequenceNumber: {self.rtspSeq}
				hostname: {self.hostname} rtspPort: {self.rtpPort}"""

			# Keep track of the sent request.
			self.requestSent = self.PLAY

		# Pause request
		elif self.request_type == self.PAUSE and self.state == self.PLAYING:
			# Update RTSP sequence number.
			self.rtspSeq += 1
			print('\nPAUSE event\n')

			# Write the RTSP request to be sent.
			request = f"""PAUSE {self.fileName}
				sequenceNumber: {self.rtspSeq}
				hostname: {self.hostname} rtspPort: {self.rtpPort}"""

			# Keep track of the sent request.
			self.requestSent = self.PAUSE

		# Teardown request
		elif self.request_type == self.TEARDOWN and not self.state == self.INIT:
			# Update RTSP sequence number.
			self.rtspSeq += 1
			print('\nTEARDOWN event\n')

			# Write the RTSP request to be sent.
			request = f"""TEARDOWN {self.fileName}
				sequenceNumber: {self.rtspSeq}
				hostname: {self.hostname} rtspPort: {self.rtpPort}"""

			# Keep track of the sent request.
			self.requestSent = self.TEARDOWN
		else:
			return

		# Send the RTSP request using rtspSocket.
		destAddr = (self.serverAddr, self.serverPort)
		self.rtspSocket.sendto(request.encode('utf-8'), destAddr)

		print('\nData sent: \n' + request)

		
	def replyRtsp(self, code, seq):
		"""Send RTSP reply to the client."""
		if code == self.OK_200:
			#print("200 OK")
			reply = 'RTSP/1.0 200 OK\nCSeq: ' + str(seq) + '\nSession: ' + str(self.clientInfo['session'])
			connSocket = self.clientInfo['rtspSocket'][0]
			connSocket.send(reply.encode())
		
		# Error messages
		elif code == self.FILE_NOT_FOUND_404:
			print("404 NOT FOUND")
		elif code == self.CON_ERR_500:
			print("500 CONNECTION ERROR")


