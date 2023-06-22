#import required libraries
import obd
obd.logger.setLevel(obd.logging.DEBUG) # enables all debug information
#establish a connection with the OBD device
connection = obd.OBD("/dev/rfcomm0", protocol="6", baudrate="38400", fast=False, timeout = 30)
#create a command varialbe
c = obd.commands.RPM
#query the command and store the response
response = connection.query(c)
#print the response value
print(response.value)
#close the connection
connection.close()
