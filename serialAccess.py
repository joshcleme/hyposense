import socket
import sys
import serial
arduinoPort = serial.Serial('COM6', 9600)
arduinoPort.flushInput()

ser_bytes = arduinoPort.readline()
decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
print(decoded_bytes)