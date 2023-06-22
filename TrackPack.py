#import required libraries
import obd
obd.logger.setLevel(obd.logging.DEBUG) # enables all debug information
#establish a connection with the OBD device
connection = obd.OBD()
#create a command varialbe
c = obd.commands.RPM
#query the command and store the response
response = connection.query(c)
#print the response value
print(response.value)
#close the connection
connection.close()
