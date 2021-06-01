import pika
import json
from SimCES_messaging import write_abstract_message, write_abstract_result
import datetime, time
from random import seed
from random import random

seed( time.time() )

connection = pika.BlockingConnection(
   pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
#channel.exchange_declare(exchange='simexe5', exchange_type='fanout')

#print("Give config file (leave blank for default)")
#print(" > ", end = "")
#config_filename = input()
#config = tools.get_config(config_filename)

#channel = connection.channel()

simStartTime = datetime.datetime.utcnow()
t=0
x='simexe30'
x1='simexe31'

################################################################################# Start message 1
epoch=0

msg = {**write_abstract_message('Start', 'SimTest30', 'PlatformManager', 
		'SimulationManager'+str(epoch)), **write_abstract_result( epoch,[]  ) }

epoch_time_beg = simStartTime + datetime.timedelta(hours=epoch)
epoch_time_end = simStartTime + datetime.timedelta(hours=epoch+1)
msg["StartTime"]=epoch_time_beg.strftime('%d-%m-%YT%H:00:00Z')
msg["EndTime"]=epoch_time_end.strftime('%d-%m-%YT%H:00:00Z')
msg["Type"]="Start"
msg["SimulationId"]="SimTest30"
msg["SimulationSpecificExchange"]="simexe30"
msg["SimulationManager"] = {"MaxEpochCount": 2}


message = json.dumps( msg )
#channel.basic_publish(exchange='procem-management11', routing_key='Start', body=message)
#print(message)
time.sleep(0)

############################################################################ SimState message 1


msg = {**write_abstract_message('SimState', 'SimTest30', 'SimulationManager', 
		'SimulationManager1'+str(epoch)), **write_abstract_result( epoch, ['PlatformManager'+str(epoch)] ) }

epoch_time_beg = simStartTime + datetime.timedelta(hours=epoch)
epoch_time_end = simStartTime + datetime.timedelta(hours=epoch+1)
msg["StartTime"]=epoch_time_beg.strftime('%d-%m-%YT%H:00:00Z')
msg["EndTime"]=epoch_time_end.strftime('%d-%m-%YT%H:00:00Z')
msg["SimulationState"]="running"

message = json.dumps( msg )
channel.basic_publish(exchange='simexe30', routing_key='SimState', body=message)
print(message)
time.sleep(0)


################################################################### Ready message from grid
msg = {**write_abstract_message('Status', 'SimTest30', 'Grid', 
		'Grid1'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }

epoch_time_beg = simStartTime + datetime.timedelta(hours=epoch)
epoch_time_end = simStartTime + datetime.timedelta(hours=epoch+1)
msg["Value"]="ready"

message = json.dumps( msg )
channel.basic_publish(exchange='simexe30', routing_key='Status.Ready', body=message)
print(message)
time.sleep(0)



####################################################################################################


for epoch in range(1,3):
	#
	# ########################################################################################Epoch msg 1
	#
	msg = {**write_abstract_message('Epoch', 'SimTest30', 'SimulationManager', 
		'SimulationManager'+str(epoch)), **write_abstract_result( epoch, [] ) }
		
	epoch_time_beg = simStartTime + datetime.timedelta(hours=epoch)
	epoch_time_end = simStartTime + datetime.timedelta(hours=epoch+1)
	msg["StartTime"]=epoch_time_beg.strftime('%Y-%m-%dT%H:00:00Z')
	msg["EndTime"]=epoch_time_end.strftime('%Y-%m-%dT%H:00:00Z')
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='Epoch', body=message)
	print(message)
	time.sleep(0)
	


	########################################################################################## Init.NIS.NetworkBusInfo 1
	msg = {**write_abstract_message('Init.NIS.NetworkBusInfo', 'SimTest30', 'Grid', 
		'BusInitialization'+str(epoch)), **write_abstract_result( epoch, ['Epoch'+str(epoch)] ) }
	#msg["BusName"] = ["bus1","bus2","bus3","bus4","bus5","bus6","bus7","bus8","bus9","bus10","bus11","bus12"]
	#msg["BusType"] = ["root","dummy","dummy","dummy","dummy","usage-point","dummy","usage-point","dummy","dummy","usage-point","usage-point"]
	#msg["BusVoltageBase"] = {"UnitOfMeasure": "kV",
    #"Values": [20,20,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4]}
	msg["BusName"] = ["ovspt1", "kj_bus_pohja932", "kj_bus_pohja933", "kj_bus_pohja2", "kj_bus_pohja934", "kj_bus_pohja935", "kj_bus_pohja936", "kj_bus_pohja3", "kj_bus_pohja937", "kj_bus_pohja5", "kj_bus_pohja4", "kj_bus_pohja938", "kj_bus_pohja6", "kj_bus_pohja939", "kj_bus_pohja7", "kj_bus_pohja940", "kj_bus_pohja941", "kj_bus_pohja942", "kj_bus_pohja10", "kj_bus_pohja943", "kj_bus_pohja8", "kj_bus_pohja9", "kj_bus_pohja944", "kj_bus_pohja945", "kj_bus_pohja946", "kj_bus_pohja947", "kj_bus_pohja12", "kj_bus_pohja948", "kj_bus_pohja949", "kj_bus_pohja950", "kj_bus_pohja13", "kj_bus_pohja951", "kj_bus_pohja11", "kj_bus_pohja952", "kj_bus_pohja15", "kj_bus_pohja953", "kj_bus_pohja954", "kj_bus_pohja18", "kj_bus_pohja14", "kj_bus_pohja955", "kj_bus_pohja19", "kj_bus_pohja956", "kj_bus_pohja16", "kj_bus_pohja957", "kj_bus_pohja958", "kj_bus_pohja20", "kj_bus_pohja17", "kj_bus_pohja21", "kj_bus_pohja25", "kj_bus_pohja23", "kj_bus_pohja959", "kj_bus_pohja960", "kj_bus_pohja961", "kj_bus_pohja962", "kj_bus_pohja963", "kj_bus_pohja964", "kj_bus_pohja965", "kj_bus_pohja24", "kj_bus_pohja966", "kj_bus_pohja22", "kj_bus_pohja967", "kj_bus_pohja968", "kj_bus_pohja26", "kj_bus_pohja27", "kj_bus_pohja30", "kj_bus_pohja28", "kj_bus_pohja969", "kj_bus_pohja970", "kj_bus_pohja971", "kj_bus_pohja972", "kj_bus_pohja32", "kj_bus_pohja29", "kj_bus_pohja973", "kj_bus_pohja974", "kj_bus_pohja975", "kj_bus_pohja31", "kj_bus_pohja976", "kj_bus_pohja977", "kj_bus_pohja33", "kj_bus_pohja978", "kj_bus_pohja34", "kj_bus_pohja981", "kj_bus_pohja35", "kj_bus_pohja37", "kj_bus_pohja982", "kj_bus_pohja983", "kj_bus_pohja38", "kj_bus_pohja984", "kj_bus_pohja36", "kj_bus_pohja985", "kj_bus_pohja39", "kj_bus_pohja986", "kj_bus_pohja40", "kj_bus_pohja41", "kj_bus_pohja43", "kj_bus_pohja51", "kj_bus_pohja44", "kj_bus_pohja987", "kj_bus_pohja988", "kj_bus_pohja989", "kj_bus_pohja990", "kj_bus_pohja991", "kj_bus_pohja55", "kj_bus_pohja46", "kj_bus_pohja992", "kj_bus_pohja47", "kj_bus_pohja42", "kj_bus_pohja49", "kj_bus_pohja993", "kj_bus_pohja994", "kj_bus_pohja995", "kj_bus_pohja996", "kj_bus_pohja997", "kj_bus_pohja54", "kj_bus_pohja45", "kj_bus_pohja998", "kj_bus_pohja999", "kj_bus_pohja48", "kj_bus_pohja50", "kj_bus_pohja1000", "kj_bus_pohja56", "kj_bus_pohja1001", "kj_bus_pohja57", "kj_bus_pohja1002", "kj_bus_pohja61", "kj_bus_pohja1003", "kj_bus_pohja1004", "kj_bus_pohja52", "kj_bus_pohja1005", "kj_bus_pohja53", "kj_bus_pohja62", "kj_bus_pohja58", "kj_bus_pohja1006", "kj_bus_pohja59", "kj_bus_pohja60", "kj_bus_pohja1007", "kj_bus_pohja66", "kj_bus_pohja1008", "kj_bus_pohja1009", "kj_bus_pohja9999", "kj_bus_pohja1010", "kj_bus_pohja1011", "kj_bus_pohja64", "kj_bus_pohja65", "kj_bus_pohja1012", "kj_bus_pohja1013", "kj_bus_pohja67", "kj_bus_pohja72", "kj_bus_pohja69", "kj_bus_pohja63", "kj_bus_pohja1014", "kj_bus_pohja1015", "kj_bus_pohja70", "kj_bus_pohja71", "kj_bus_pohja76", "kj_bus_pohja68", "kj_bus_pohja73", "kj_bus_pohja74", "kj_bus_pohja78", "kj_bus_pohja84", "kj_bus_pohja77", "kj_bus_pohja1016", "kj_bus_pohja1017", "kj_bus_pohja75", "kj_bus_pohja1018", "kj_bus_pohja1019", "kj_bus_pohja79", "kj_bus_pohja89", "kj_bus_pohja1020", "kj_bus_pohja1021", "kj_bus_pohja1022", "kj_bus_pohja85", "kj_bus_pohja1023", "kj_bus_pohja86", "kj_bus_pohja1024", "kj_bus_pohja80", "kj_bus_pohja81", "kj_bus_pohja82", "kj_bus_pohja88", "kj_bus_pohja83", "kj_bus_pohja1025", "kj_bus_pohja1026", "kj_bus_pohja90", "kj_bus_pohja1027", "kj_bus_pohja1028", "kj_bus_pohja87", "kj_bus_pohja1029", "kj_bus_pohja1030", "kj_bus_pohja1031", "kj_bus_pohja91", "kj_bus_pohja92", "kj_bus_pohja1032", "kj_bus_pohja1033", "kj_bus_pohja1034", "kj_bus_pohja1035", "kj_bus_pohja1036", "kj_bus_pohja95", "kj_bus_pohja93", "kj_bus_pohja1037", "kj_bus_pohja94", "kj_bus_pohja96", "kj_bus_pohja1038", "kj_bus_pohja1039", "kj_bus_pohja99", "kj_bus_pohja97", "kj_bus_pohja1040", "kj_bus_pohja1041", "kj_bus_pohja98", "kj_bus_pohja102", "kj_bus_pohja1042", "kj_bus_pohja100", "kj_bus_pohja1043", "kj_bus_pohja106", "kj_bus_pohja101", "kj_bus_pohja1044", "kj_bus_pohja1045", "kj_bus_pohja104", "kj_bus_pohja1046", "kj_bus_pohja1047", "kj_bus_pohja1048", "kj_bus_pohja1049", "kj_bus_pohja1050", "kj_bus_pohja1051", "kj_bus_pohja1052", "kj_bus_pohja107", "kj_bus_pohja103", "kj_bus_pohja105", "kj_bus_pohja1053", "kj_bus_pohja1054", "kj_bus_pohja1055", "kj_bus_pohja1056", "kj_bus_pohja109", "kj_bus_pohja108", "kj_bus_pohja1057", "kj_bus_pohja1058", "kj_bus_pohja1059", "kj_bus_pohja1060", "kj_bus_pohja111", "kj_bus_pohja110", "kj_bus_pohja1061", "kj_bus_pohja1062", "kj_bus_pohja1063", "kj_bus_pohja1064", "kj_bus_pohja112", "kj_bus_pohja113", "kj_bus_pohja1065", "kj_bus_pohja1066", "kj_bus_pohja114", "kj_bus_pohja1067", "scd_102001", "scd_101996", "scd_101995", "scd_150460", "scd_101990", "scd_101988", "scd_101994", "scd_101992", "scd_101987", "scd_151258", "scd_101985", "scd_153085", "scd_101986", "scd_101856", "scd_101855", "scd_101962", "scd_101961", "scd_101853", "scd_101844", "scd_101857", "scd_101965", "scd_101850", "scd_101849", "scd_101848", "scd_101847", "scd_101834", "scd_101852", "scd_101829", "scd_101833", "scd_101828", "scd_101846", "scd_101837", "scd_152196", "scd_101822", "scd_152198", "scd_152199", "scd_152197", "scd_101825", "scd_104065", "scd_104036", "scd_103910", "scd_101656", "scd_103915", "scd_103908", "scd_104061", "scd_104045", "scd_151261", "scd_152195", "scd_103911", "scd_103909", "scd_103914", "scd_101637", "scd_104041", "scd_104035", "scd_104043", "scd_103913", "scd_103893", "scd_104040", "scd_104046", "scd_101832", "scd_101655", "scd_101815", "scd_104042", "scd_103912", "scd_101658", "scd_101670", "scd_101816", "scd_101817", "scd_104037", "scd_101669", "scd_101818", "scd_101819", "scd_101657", "scd_101668", "scd_152613", "scd_152612", "scd_152611", "scd_152610", "scd_152609", "scd_152608", "scd_101665", "scd_101660", "scd_101659", "scd_101666", "scd_101823", "scd_101672", "scd_101664", "scd_151371", "scd_101671", "scd_101631", "scd_101667", "scd_101632", "scd_101683", "scd_101681", "scd_101633", "scd_101680", "scd_101679", "scd_101673", "scd_101685", "scd_101687", "scd_101689", "scd_101674", "scd_101675", "scd_101648", "scd_101682", "scd_101649", "scd_101690", "scd_101691", "scd_101709", "scd_101692"]

	msg["BusType"] = ["root", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy", "dummy"]


	msg["BusVoltageBase"] = {"Values": [20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4], "UnitOfMeasure": "kV"}
    
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='Init.NIS.NetworkBusInfo', body=message)
	print(message)
	time.sleep(1)
 ########################################################################### Init.NIS.NetworkComponentInfo 1

	msg = {**write_abstract_message('Init.NIS.NetworkComponentInfo', 'SimTest30', 'Grid', 
		'BusInitialization'+str(epoch)), **write_abstract_result( epoch, ['Epoch'+str(epoch)] ) }
	#msg["PowerBase"] = {
   #"Value" : 50,
   #"UnitOfMeasure" : "kV.A"
	#}
	#msg["DeviceId"] = [ "line1-2","line2-3","line3-4","line4-5","trans5-6","line3-7","line7-8","line2-9","line9-10","line10-11","line9-12"]
	#msg["SendingEndBus"] = ["bus1","bus2","bus3","bus4","bus5","bus3","bus7","bus2","bus9","bus10","bus9"]
	#msg["ReceivingEndBus"] = ["bus2","bus3","bus4","bus5","bus6","bus7","bus8","bus9","bus10","bus11","bus12"]
	#msg["Resistance"] = {"UnitOfMeasure" : "{pu}","Values" : [0.072,0.056,0.084,0.054,0.064,0.249,0.143,0.016,0.074,0.077,0.001]}
	#msg["Reactance"] = {
    #"UnitOfMeasure": "{pu}",
    #"Values" : [0.008,0.007,0.006,0.005,0.038,0.134,0.002,0.002,0.011,0.006,0]}
	#msg["ShuntAdmittance"] = {
    #"UnitOfMeasure": "{pu}",
    #"Values" : [0,0,0,0,0,0,0,0,0,0,0]}
	#msg["ShuntConductance"] = {
  #"UnitOfMeasure": "{pu}",
  #"Values" : [0.00256,0,0,0,0,0,0,0,0,0,0]}
	#msg["RatedCurrent"] = {
  #"UnitOfMeasure": "{pu}",
  #"Values" : [1.739130435,1.12,0.72,1,0.72,1.12,0.624,1.12,1.12,0.72,0.8]}
	msg["PowerBase"] ={ "Value" : 1000,"UnitOfMeasure" : "kV.A"}
	msg["DeviceId"] = ["2396828", "48808417", "2396789", "2396801", "2396810", "2396814", "2396818", "2396824", "21541131", "2397617", "2397484", "2397470", "2397474", "36183130", "2397490", "2397498", "36183126", "29410740", "7703250", "2397528", "2397538", "29410780", "29410763", "7703169", "7703173", "7703251", "2397578", "2397582", "2397614", "46183617", "2397586", "4999556", "4999555", "2398234", "46183656", "1343895", "1343875", "2142203", "2142197", "2142189", "2142183", "1343956", "3882789", "1343857", "1343902", "2142177", "2142161", "33054147", "33054150", "1344035", "7729840", "7729839", "1343946", "1343928", "7730791", "7730792", "1343914", "1344012", "1344090", "1343942", "33309137", "1343938", "33309141", "1343932", "9430096", "9430097", "1344000", "1344020", "1344054", "1344076", "1344104", "1344050", "1344060", "1344094", "1344100", "7702907", "7702932", "50611292", "50498938", "36711227", "36711298", "1343332", "36693745", "45181629", "45181607", "45181609", "43791891", "3655435", "36700000", "36700047", "1344300", "5005052", "36693791", "45181626", "36723229", "45181613", "45181616", "1341577", "1341582", "1337081", "9548264", "1341602", "1342194", "4529611", "5005048", "5005038", "28654177", "5005051", "1342061", "1341586", "1341590", "1341596", "1342060", "5004715", "1336537", "1342198", "1342202", "1342208", "33309147", "1342149", "1342111", "1342105", "1342101", "1342097", "9342948", "1341619", "42343231", "5004631", "5004630", "5004716", "1336877", "1342645", "1341571", "9342949", "1341611", "1341607", "36700090", "36700101", "36700131", "1336883", "1336889", "1343296", "1343295", "1341631", "1341565", "1341561", "1337076", "1336897", "1336901", "1343280", "1343268", "1341635", "1341557", "1337072", "1336921", "1343256", "1343250", "1337025", "7728882", "7728881", "36700165", "1336929", "1343242", "1343238", "30502148", "1337009", "1337021", "1337015", "7728857", "36718304", "36718258", "36718197", "36718144", "36708652", "1336935", "1343232", "1337068", "7728872", "7728871", "7728865", "7728858", "49305738", "4355112", "49305734", "36708644", "1336977", "1336969", "1336943", "7872230", "29253715", "7872231", "1336951", "1336955", "1336959", "1336963", "1337053", "1336511", "1337029", "2649501", "2649498", "1336519", "2649494", "2649484", "2649450", "1337058", "2649480", "2649466", "2649462", "29245545", "2649442", "2649438", "4344899", "2649420", "2649388", "32814684", "2649392", "30831374", "29245549", "2649456", "2649428", "4344905", "4344900", "2649424", "2649410", "2649406", "2649396", "36183115", "2649400", "36818573", "36987683", "2647602", "2652093", "33444500", "33444498", "33444507", "2652736", "4389498", "4389501", "2647590", "2647582", "4389532", "4389502", "2647606", "2647586", "2647574", "2647568", "1290609", "8114408", "rostinm\u00c3\u00a4ki", "hiukkaa", "majaniemi", "pitopalvelu", "haukkavuori", "maivia", "nuottij\u00c3\u00a4rvi", "kari", "rummakko", "oksvuorentie", "s\u00c3\u00a4rkivuori", "riihiniemi_1", "lahnaj\u00c3\u00a4rvi", "karpalepohja", "tammioja", "matinlahti", "vinki\u00c3\u00a4", "l\u00c3\u00a4hdekorpi", "kyt\u00c3\u00b6niemi", "hannula", "pajusto", "myllym\u00c3\u00a4ki", "tennil\u00c3\u00a4", "v\u00c3\u00a4stil\u00c3\u00a4", "attila", "rekisaari", "puharila", "aittosaari", "pohjalainen", "solala", "m\u00c3\u00a4ntym\u00c3\u00a4ki", "solaniemi", "mustasuu_50", "lev\u00c3\u00a4ssuo", "attilantie_44", "attilantie_122", "mustasuu_1", "vitastenlahti", "rekola", "hietalahti", "omenaj\u00c3\u00a4rvi", "lintuvaara", "annanluoto", "multakorpi", "haikka", "kotiniemi", "kotiniementie_65", "rauham\u00c3\u00a4entie_1", "uiherla", "koskis_heikkil\u00c3\u00a4", "palttala", "pyh\u00c3\u00a4lahti", "savilahti", "vihasj\u00c3\u00a4rvi", "uusi_laurila", "kaislaranta", "nunnankirkko", "kaanaa", "ruotti", "rantalahti", "er\u00c3\u00a4pyh\u00c3\u00a4", "heinisuo", "kes\u00c3\u00a4koti", "syrj\u00c3\u00a4nm\u00c3\u00a4ki", "er\u00c3\u00a4j\u00c3\u00a4rvi", "kuivastenniemi", "ruokostenpohja", "riekkola", "er\u00c3\u00a4linna", "v\u00c3\u00a4lim\u00c3\u00a4ki", "sulkulahti", "perhoj\u00c3\u00a4rvi", "kauppi", "meijeri", "talaspolku_1", "nuottasaunantie_8", "lev\u00c3\u00a4slahdentie_60", "er\u00c3\u00a4j\u00c3\u00a4rventie_1221", "er\u00c3\u00a4j\u00c3\u00a4rventie_1317", "katajatie_38", "kuivanen", "h\u00c3\u00a4meoja", "r\u00c3\u00b6k\u00c3\u00a4s", "kuoresalmi", "ojonen", "hietamaa", "wetterkulla", "er\u00c3\u00a4j\u00c3\u00a4rventie_1100", "navettasaari", "pajulahti", "r\u00c3\u00b6nnin_lava", "pajunkanta", "kotam\u00c3\u00a4ki", "kuotikasvuori", "mukkula", "koppala", "p\u00c3\u00a4rn\u00c3\u00a4", "maunula", "ojala", "ilom\u00c3\u00a4ki", "koulu", "p\u00c3\u00a4im\u00c3\u00a4ki", "p\u00c3\u00a4ilahti", "pentinkulma", "perkj\u00c3\u00a4rvi", "ansiolahti", "lyytikk\u00c3\u00a4l\u00c3\u00a4", "laahus", "kortelahti", "pehula"]



	msg["SendingEndBus"] = ["kj_bus_pohja932", "kj_bus_pohja933", "kj_bus_pohja934", "kj_bus_pohja935", "kj_bus_pohja936", "kj_bus_pohja936", "kj_bus_pohja936", "kj_bus_pohja937", "kj_bus_pohja4", "kj_bus_pohja938", "kj_bus_pohja6", "kj_bus_pohja938", "kj_bus_pohja939", "kj_bus_pohja940", "kj_bus_pohja941", "kj_bus_pohja941", "kj_bus_pohja942", "kj_bus_pohja943", "kj_bus_pohja9", "kj_bus_pohja945", "kj_bus_pohja946", "kj_bus_pohja947", "kj_bus_pohja943", "kj_bus_pohja948", "kj_bus_pohja944", "kj_bus_pohja946", "kj_bus_pohja946", "kj_bus_pohja949", "kj_bus_pohja13", "kj_bus_pohja11", "kj_bus_pohja950", "kj_bus_pohja950", "kj_bus_pohja951", "kj_bus_pohja954", "kj_bus_pohja952", "kj_bus_pohja14", "kj_bus_pohja14", "kj_bus_pohja954", "kj_bus_pohja956", "kj_bus_pohja16", "kj_bus_pohja957", "kj_bus_pohja958", "kj_bus_pohja17", "kj_bus_pohja17", "kj_bus_pohja955", "kj_bus_pohja957", "kj_bus_pohja957", "kj_bus_pohja959", "kj_bus_pohja961", "kj_bus_pohja958", "kj_bus_pohja958", "kj_bus_pohja963", "kj_bus_pohja964", "kj_bus_pohja965", "kj_bus_pohja25", "kj_bus_pohja22", "kj_bus_pohja22", "kj_bus_pohja968", "kj_bus_pohja27", "kj_bus_pohja964", "kj_bus_pohja969", "kj_bus_pohja970", "kj_bus_pohja971", "kj_bus_pohja965", "kj_bus_pohja965", "kj_bus_pohja967", "kj_bus_pohja968", "kj_bus_pohja968", "kj_bus_pohja29", "kj_bus_pohja974", "kj_bus_pohja975", "kj_bus_pohja973", "kj_bus_pohja974", "kj_bus_pohja974", "kj_bus_pohja975", "kj_bus_pohja975", "kj_bus_pohja977", "kj_bus_pohja978", "kj_bus_pohja34", "kj_bus_pohja981", "kj_bus_pohja981", "kj_bus_pohja37", "kj_bus_pohja35", "kj_bus_pohja983", "kj_bus_pohja984", "kj_bus_pohja985", "kj_bus_pohja39", "kj_bus_pohja986", "kj_bus_pohja982", "kj_bus_pohja41", "kj_bus_pohja43", "kj_bus_pohja44", "kj_bus_pohja38", "kj_bus_pohja988", "kj_bus_pohja39", "kj_bus_pohja989", "kj_bus_pohja990", "kj_bus_pohja991", "kj_bus_pohja46", "kj_bus_pohja992", "kj_bus_pohja42", "kj_bus_pohja993", "kj_bus_pohja51", "kj_bus_pohja995", "kj_bus_pohja997", "kj_bus_pohja987", "kj_bus_pohja45", "kj_bus_pohja998", "kj_bus_pohja992", "kj_bus_pohja992", "kj_bus_pohja48", "kj_bus_pohja993", "kj_bus_pohja50", "kj_bus_pohja50", "kj_bus_pohja56", "kj_bus_pohja994", "kj_bus_pohja1002", "kj_bus_pohja1002", "kj_bus_pohja1003", "kj_bus_pohja995", "kj_bus_pohja52", "kj_bus_pohja1005", "kj_bus_pohja53", "kj_bus_pohja998", "kj_bus_pohja998", "kj_bus_pohja58", "kj_bus_pohja41", "kj_bus_pohja60", "kj_bus_pohja1000", "kj_bus_pohja1001", "kj_bus_pohja1001", "kj_bus_pohja61", "kj_bus_pohja1009", "kj_bus_pohja1006", "kj_bus_pohja1010", "kj_bus_pohja1009", "kj_bus_pohja1011", "kj_bus_pohja59", "kj_bus_pohja59", "kj_bus_pohja66", "kj_bus_pohja1012", "kj_bus_pohja1008", "kj_bus_pohja1008", "kj_bus_pohja1009", "kj_bus_pohja63", "kj_bus_pohja63", "kj_bus_pohja1015", "kj_bus_pohja1013", "kj_bus_pohja1013", "kj_bus_pohja68", "kj_bus_pohja68", "kj_bus_pohja1014", "kj_bus_pohja1015", "kj_bus_pohja1015", "kj_bus_pohja76", "kj_bus_pohja73", "kj_bus_pohja1016", "kj_bus_pohja1017", "kj_bus_pohja75", "kj_bus_pohja75", "kj_bus_pohja65", "kj_bus_pohja84", "kj_bus_pohja1016", "kj_bus_pohja1021", "kj_bus_pohja1022", "kj_bus_pohja1023", "kj_bus_pohja1017", "kj_bus_pohja1019", "kj_bus_pohja1019", "kj_bus_pohja80", "kj_bus_pohja81", "kj_bus_pohja82", "kj_bus_pohja82", "kj_bus_pohja83", "kj_bus_pohja89", "kj_bus_pohja1021", "kj_bus_pohja1023", "kj_bus_pohja1027", "kj_bus_pohja1028", "kj_bus_pohja1024", "kj_bus_pohja87", "kj_bus_pohja1029", "kj_bus_pohja88", "kj_bus_pohja1030", "kj_bus_pohja1025", "kj_bus_pohja1031", "kj_bus_pohja1031", "kj_bus_pohja1026", "kj_bus_pohja1026", "kj_bus_pohja92", "kj_bus_pohja1033", "kj_bus_pohja1033", "kj_bus_pohja1034", "kj_bus_pohja1035", "kj_bus_pohja1036", "kj_bus_pohja93", "kj_bus_pohja94", "kj_bus_pohja95", "kj_bus_pohja1038", "kj_bus_pohja1039", "kj_bus_pohja96", "kj_bus_pohja1039", "kj_bus_pohja1040", "kj_bus_pohja1041", "kj_bus_pohja99", "kj_bus_pohja1042", "kj_bus_pohja1040", "kj_bus_pohja1040", "kj_bus_pohja1043", "kj_bus_pohja1041", "kj_bus_pohja1044", "kj_bus_pohja102", "kj_bus_pohja104", "kj_bus_pohja1047", "kj_bus_pohja1048", "kj_bus_pohja1049", "kj_bus_pohja1050", "kj_bus_pohja1052", "kj_bus_pohja1044", "kj_bus_pohja1044", "kj_bus_pohja1045", "kj_bus_pohja103", "kj_bus_pohja103", "kj_bus_pohja105", "kj_bus_pohja1051", "kj_bus_pohja1051", "kj_bus_pohja1053", "kj_bus_pohja1054", "kj_bus_pohja1055", "kj_bus_pohja1056", "kj_bus_pohja108", "kj_bus_pohja109", "kj_bus_pohja1057", "kj_bus_pohja1060", "kj_bus_pohja1060", "kj_bus_pohja1058", "kj_bus_pohja1058", "kj_bus_pohja1061", "kj_bus_pohja1063", "kj_bus_pohja1064", "kj_bus_pohja1062", "kj_bus_pohja1062", "kj_bus_pohja1063", "kj_bus_pohja1064", "kj_bus_pohja1064", "kj_bus_pohja114", "kj_bus_pohja1067", "ovspt1", "kj_bus_pohja2", "kj_bus_pohja3", "kj_bus_pohja5", "kj_bus_pohja4", "kj_bus_pohja6", "kj_bus_pohja7", "kj_bus_pohja8", "kj_bus_pohja9", "kj_bus_pohja10", "kj_bus_pohja12", "kj_bus_pohja13", "kj_bus_pohja11", "kj_bus_pohja15", "kj_bus_pohja18", "kj_bus_pohja14", "kj_bus_pohja19", "kj_bus_pohja16", "kj_bus_pohja20", "kj_bus_pohja21", "kj_bus_pohja17", "kj_bus_pohja23", "kj_bus_pohja24", "kj_bus_pohja25", "kj_bus_pohja22", "kj_bus_pohja26", "kj_bus_pohja27", "kj_bus_pohja28", "kj_bus_pohja29", "kj_bus_pohja30", "kj_bus_pohja31", "kj_bus_pohja32", "kj_bus_pohja33", "kj_bus_pohja36", "kj_bus_pohja37", "kj_bus_pohja38", "kj_bus_pohja35", "kj_bus_pohja39", "kj_bus_pohja40", "kj_bus_pohja43", "kj_bus_pohja44", "kj_bus_pohja46", "kj_bus_pohja47", "kj_bus_pohja49", "kj_bus_pohja42", "kj_bus_pohja51", "kj_bus_pohja54", "kj_bus_pohja45", "kj_bus_pohja41", "kj_bus_pohja55", "kj_bus_pohja48", "kj_bus_pohja50", "kj_bus_pohja56", "kj_bus_pohja57", "kj_bus_pohja52", "kj_bus_pohja53", "kj_bus_pohja58", "kj_bus_pohja60", "kj_bus_pohja61", "kj_bus_pohja62", "kj_bus_pohja64", "kj_bus_pohja66", "kj_bus_pohja67", "kj_bus_pohja69", "kj_bus_pohja63", "kj_bus_pohja70", "kj_bus_pohja71", "kj_bus_pohja72", "kj_bus_pohja68", "kj_bus_pohja74", "kj_bus_pohja76", "kj_bus_pohja77", "kj_bus_pohja73", "kj_bus_pohja78", "kj_bus_pohja75", "kj_bus_pohja65", "kj_bus_pohja79", "kj_bus_pohja80", "kj_bus_pohja81", "kj_bus_pohja82", "kj_bus_pohja83", "kj_bus_pohja84", "kj_bus_pohja85", "kj_bus_pohja86", "kj_bus_pohja89", "kj_bus_pohja90", "kj_bus_pohja87", "kj_bus_pohja91", "kj_bus_pohja92", "kj_bus_pohja93", "kj_bus_pohja94", "kj_bus_pohja95", "kj_bus_pohja96", "kj_bus_pohja97", "kj_bus_pohja98", "kj_bus_pohja99", "kj_bus_pohja100", "kj_bus_pohja101", "kj_bus_pohja102", "kj_bus_pohja104", "kj_bus_pohja106", "kj_bus_pohja107", "kj_bus_pohja103", "kj_bus_pohja105", "kj_bus_pohja108", "kj_bus_pohja109", "kj_bus_pohja110", "kj_bus_pohja111", "kj_bus_pohja112", "kj_bus_pohja113", "kj_bus_pohja114"]



	msg["ReceivingEndBus"] = ["kj_bus_pohja933", "kj_bus_pohja2", "kj_bus_pohja935", "kj_bus_pohja2", "kj_bus_pohja935", "kj_bus_pohja3", "kj_bus_pohja937", "kj_bus_pohja5", "kj_bus_pohja937", "kj_bus_pohja4", "kj_bus_pohja939", "kj_bus_pohja7", "kj_bus_pohja938", "kj_bus_pohja939", "kj_bus_pohja940", "kj_bus_pohja942", "kj_bus_pohja10", "kj_bus_pohja8", "kj_bus_pohja944", "kj_bus_pohja10", "kj_bus_pohja945", "kj_bus_pohja12", "kj_bus_pohja947", "kj_bus_pohja943", "kj_bus_pohja948", "kj_bus_pohja944", "kj_bus_pohja949", "kj_bus_pohja950", "kj_bus_pohja951", "kj_bus_pohja952", "kj_bus_pohja15", "kj_bus_pohja953", "kj_bus_pohja953", "kj_bus_pohja951", "kj_bus_pohja18", "kj_bus_pohja952", "kj_bus_pohja955", "kj_bus_pohja19", "kj_bus_pohja954", "kj_bus_pohja956", "kj_bus_pohja16", "kj_bus_pohja20", "kj_bus_pohja21", "kj_bus_pohja955", "kj_bus_pohja25", "kj_bus_pohja23", "kj_bus_pohja959", "kj_bus_pohja960", "kj_bus_pohja960", "kj_bus_pohja961", "kj_bus_pohja962", "kj_bus_pohja962", "kj_bus_pohja963", "kj_bus_pohja24", "kj_bus_pohja966", "kj_bus_pohja966", "kj_bus_pohja967", "kj_bus_pohja26", "kj_bus_pohja30", "kj_bus_pohja28", "kj_bus_pohja964", "kj_bus_pohja969", "kj_bus_pohja970", "kj_bus_pohja971", "kj_bus_pohja972", "kj_bus_pohja972", "kj_bus_pohja967", "kj_bus_pohja32", "kj_bus_pohja973", "kj_bus_pohja30", "kj_bus_pohja31", "kj_bus_pohja32", "kj_bus_pohja973", "kj_bus_pohja976", "kj_bus_pohja976", "kj_bus_pohja977", "kj_bus_pohja33", "kj_bus_pohja977", "kj_bus_pohja978", "kj_bus_pohja34", "kj_bus_pohja35", "kj_bus_pohja982", "kj_bus_pohja983", "kj_bus_pohja38", "kj_bus_pohja36", "kj_bus_pohja984", "kj_bus_pohja985", "kj_bus_pohja40", "kj_bus_pohja986", "kj_bus_pohja982", "kj_bus_pohja51", "kj_bus_pohja987", "kj_bus_pohja988", "kj_bus_pohja39", "kj_bus_pohja989", "kj_bus_pohja990", "kj_bus_pohja41", "kj_bus_pohja55", "kj_bus_pohja992", "kj_bus_pohja47", "kj_bus_pohja49", "kj_bus_pohja42", "kj_bus_pohja994", "kj_bus_pohja996", "kj_bus_pohja54", "kj_bus_pohja997", "kj_bus_pohja987", "kj_bus_pohja45", "kj_bus_pohja55", "kj_bus_pohja999", "kj_bus_pohja999", "kj_bus_pohja48", "kj_bus_pohja993", "kj_bus_pohja1000", "kj_bus_pohja1001", "kj_bus_pohja57", "kj_bus_pohja994", "kj_bus_pohja61", "kj_bus_pohja1004", "kj_bus_pohja1003", "kj_bus_pohja995", "kj_bus_pohja52", "kj_bus_pohja1005", "kj_bus_pohja53", "kj_bus_pohja62", "kj_bus_pohja1006", "kj_bus_pohja59", "kj_bus_pohja1007", "kj_bus_pohja1007", "kj_bus_pohja1000", "kj_bus_pohja66", "kj_bus_pohja1008", "kj_bus_pohja9999", "kj_bus_pohja62", "kj_bus_pohja1006", "kj_bus_pohja1010", "kj_bus_pohja64", "kj_bus_pohja1011", "kj_bus_pohja65", "kj_bus_pohja1012", "kj_bus_pohja1013", "kj_bus_pohja67", "kj_bus_pohja72", "kj_bus_pohja69", "kj_bus_pohja1009", "kj_bus_pohja1014", "kj_bus_pohja70", "kj_bus_pohja71", "kj_bus_pohja76", "kj_bus_pohja72", "kj_bus_pohja73", "kj_bus_pohja74", "kj_bus_pohja1014", "kj_bus_pohja78", "kj_bus_pohja84", "kj_bus_pohja77", "kj_bus_pohja73", "kj_bus_pohja78", "kj_bus_pohja1018", "kj_bus_pohja1019", "kj_bus_pohja79", "kj_bus_pohja89", "kj_bus_pohja1020", "kj_bus_pohja1016", "kj_bus_pohja85", "kj_bus_pohja1022", "kj_bus_pohja86", "kj_bus_pohja1017", "kj_bus_pohja1024", "kj_bus_pohja79", "kj_bus_pohja80", "kj_bus_pohja81", "kj_bus_pohja88", "kj_bus_pohja1025", "kj_bus_pohja1026", "kj_bus_pohja90", "kj_bus_pohja1021", "kj_bus_pohja1023", "kj_bus_pohja1027", "kj_bus_pohja1028", "kj_bus_pohja1024", "kj_bus_pohja87", "kj_bus_pohja1029", "kj_bus_pohja88", "kj_bus_pohja1030", "kj_bus_pohja1025", "kj_bus_pohja1026", "kj_bus_pohja91", "kj_bus_pohja92", "kj_bus_pohja1032", "kj_bus_pohja1032", "kj_bus_pohja1034", "kj_bus_pohja1035", "kj_bus_pohja1036", "kj_bus_pohja95", "kj_bus_pohja1037", "kj_bus_pohja96", "kj_bus_pohja1037", "kj_bus_pohja1037", "kj_bus_pohja1038", "kj_bus_pohja99", "kj_bus_pohja97", "kj_bus_pohja1039", "kj_bus_pohja98", "kj_bus_pohja102", "kj_bus_pohja100", "kj_bus_pohja1042", "kj_bus_pohja1043", "kj_bus_pohja106", "kj_bus_pohja101", "kj_bus_pohja1041", "kj_bus_pohja1045", "kj_bus_pohja1046", "kj_bus_pohja1048", "kj_bus_pohja1049", "kj_bus_pohja1050", "kj_bus_pohja1051", "kj_bus_pohja106", "kj_bus_pohja1052", "kj_bus_pohja1051", "kj_bus_pohja107", "kj_bus_pohja1045", "kj_bus_pohja1046", "kj_bus_pohja1046", "kj_bus_pohja105", "kj_bus_pohja1053", "kj_bus_pohja1054", "kj_bus_pohja1055", "kj_bus_pohja1056", "kj_bus_pohja109", "kj_bus_pohja1057", "kj_bus_pohja1058", "kj_bus_pohja1059", "kj_bus_pohja1057", "kj_bus_pohja111", "kj_bus_pohja110", "kj_bus_pohja1061", "kj_bus_pohja1062", "kj_bus_pohja111", "kj_bus_pohja112", "kj_bus_pohja113", "kj_bus_pohja1065", "kj_bus_pohja1065", "kj_bus_pohja1063", "kj_bus_pohja1066", "kj_bus_pohja1066", "kj_bus_pohja1066", "kj_bus_pohja1067", "scd_102001", "scd_101996", "scd_101995", "scd_150460", "scd_101990", "scd_101988", "scd_101994", "scd_101992", "scd_101987", "scd_151258", "scd_101985", "scd_153085", "scd_101986", "scd_101856", "scd_101855", "scd_101962", "scd_101961", "scd_101853", "scd_101844", "scd_101857", "scd_101965", "scd_101850", "scd_101849", "scd_101848", "scd_101847", "scd_101834", "scd_101852", "scd_101829", "scd_101833", "scd_101828", "scd_101846", "scd_101837", "scd_152196", "scd_101822", "scd_152198", "scd_152199", "scd_152197", "scd_101825", "scd_104065", "scd_104036", "scd_103910", "scd_101656", "scd_103915", "scd_103908", "scd_104061", "scd_104045", "scd_151261", "scd_152195", "scd_103911", "scd_103909", "scd_103914", "scd_101637", "scd_104041", "scd_104035", "scd_104043", "scd_103913", "scd_103893", "scd_104040", "scd_104046", "scd_101832", "scd_101655", "scd_101815", "scd_104042", "scd_103912", "scd_101658", "scd_101670", "scd_101816", "scd_101817", "scd_104037", "scd_101669", "scd_101818", "scd_101819", "scd_101657", "scd_101668", "scd_152613", "scd_152612", "scd_152611", "scd_152610", "scd_152609", "scd_152608", "scd_101665", "scd_101660", "scd_101659", "scd_101666", "scd_101823", "scd_101672", "scd_101664", "scd_151371", "scd_101671", "scd_101631", "scd_101667", "scd_101632", "scd_101683", "scd_101681", "scd_101633", "scd_101680", "scd_101679", "scd_101673", "scd_101685", "scd_101687", "scd_101689", "scd_101674", "scd_101675", "scd_101648", "scd_101682", "scd_101649", "scd_101690", "scd_101691", "scd_101709", "scd_101692"]



	msg["Resistance"] = {"Values": [0.15729690685, 0.07103573244999999, 0.995188464925, 0.785874620875, 0.6977482251500001, 0.12326793536749998, 0.46539785889999996, 1.4707459994149998, 0.9057255215000001, 0.25921998155000003, 1.8003349824075, 1.2927678608075002, 0.55230814345, 0.5891925053375, 0.1309411323, 0.3861189440875, 0.011466760662499999, 0.05133360385999999, 0.685012931295, 2.283535757225, 0.8545321846999999, 2.6997849774, 0.6943694633999998, 4.77213905091, 0.09707070180499999, 0.8945962460050001, 0.6661976795124999, 0.0840251646375, 0.7425884222374999, 2.4809700904, 0.32614139442499995, 0.5195952461125, 1.5114026581625, 0.712127476325, 0.1190891634625, 2.3816051409149996, 2.2148408461024998, 0.65339250075, 1.1838358715500001, 2.43276691375, 0.7003475173000001, 0.13776269506999997, 1.0546912853000001, 2.2143110666599997, 1.09473831005, 1.32725411588, 0.7474887707875, 0.08093974875, 0.07389475105, 1.67153216665, 0.24786347368750003, 0.4975249125125001, 0.1533840827, 0.9190537998749999, 0.60850550068, 1.43050960745, 0.30530849349, 1.6523846221575003, 1.2783209417824999, 0.3774042250825, 0.3929227985625, 0.1084190661, 0.049384473712499995, 0.9151971360875001, 0.45057023225, 0.42185477733750004, 0.5573402477875, 1.0594557077375, 0.3331942787249999, 1.255867105185, 0.31172864761499997, 1.7081610647000003, 1.0040223875999998, 0.1199180203875, 0.77020596085, 0.2693257797875, 1.3452195016249997, 0.411689634225, 6.3560675e-05, 0.093765948425, 0.16898700719999998, 2.1433446634599997, 0.3365372672, 0.39025602239999996, 0.32236754068, 0.3192458786925, 0.45501984815749996, 3.189476557125, 0.12691671608, 0.5920423670374999, 2.304217241095, 0.6327945957025, 0.26042835599999997, 0.391467324, 0.0200658904, 0.3957787656, 0.38695946, 0.2087415004675, 2.4994869029999998, 3.3366482009999996, 0.7963191557474999, 0.985782216265, 2.443683617375, 0.30785150925, 0.9423087532875, 0.41964068786250003, 0.6974983846599999, 0.4397142607549999, 0.48076751645999993, 0.4574658476849999, 1.4837631887924998, 2.2156767694599995, 1.2218831359349998, 1.216747639415, 2.1434983071425, 0.28799998073, 1.47869959622, 0.4768384507425, 0.12601467574999997, 0.8394659935250001, 0.36500560778749996, 0.16762763914999998, 0.5072350769124999, 0.6647889509500001, 1.8948073814, 1.5625525919849999, 0.34401209520000003, 2.686875019675, 0.12815938366000001, 0.5216323506624999, 0.6886460658, 0.5806068982175, 1.7949474652724997, 0.6080964387625001, 0.5853425798, 0.19097661205, 2.0900854410975, 0.13640720535249998, 0.6764702088, 1.3984669749049998, 0.9795082352824999, 2.4842711903624997, 0.9255983051699999, 2.7062123155375, 0.23665120985000002, 0.8670581249875, 0.529813335205, 1.00242332267, 0.12403074568499999, 2.190930779345, 2.8613776499999997, 1.1371253512500001, 0.489764848525, 0.4656108811875001, 2.2513699042449997, 2.3013078257399995, 1.1294673513750002, 0.223841111, 0.052687336432499995, 0.276492236405, 0.693874864, 3.625998145875, 0.10508029377999999, 1.249656401455, 0.17250395175000002, 0.156036715875, 0.877032383625, 0.6291937531499999, 0.4002253211875, 1.4578888823999998, 0.6441402815999999, 0.6513542367999999, 0.34404711679999994, 0.043471682399999996, 1.5446850052499999, 1.26465795302, 1.1281866936724998, 0.3093745911025, 0.36431279616249995, 0.22560562526249997, 0.6104927907, 1.4551814502125, 0.0923733367375, 0.0672490011125, 0.20618740569999996, 0.29444846761250004, 1.466499309675, 2.935421717625, 0.1305077288, 0.06369517533749999, 0.20812345166250001, 0.31495214553, 0.5911656254625001, 0.286595293105, 0.0954199316875, 1.5256497054875, 2.36066900762, 0.518823266525, 0.21782851871, 0.23699364195000003, 1.6343908355774999, 0.6140519383074999, 0.2470343387125, 1.8245849481474998, 2.4703680072225, 0.6980094750474999, 1.0407524675624997, 0.3913860324625, 0.74503481005, 0.4012476223525, 1.3402543102024995, 1.4412607753775, 1.5858382334025, 0.1906702853825, 0.1596389284875, 0.15825439899500002, 1.0542706849674999, 0.1275391636, 0.466686216475, 0.7916153648124999, 0.21858795670000003, 0.6390056678774999, 1.7206665139125, 0.08624258392749998, 0.1429566790575, 0.118315172425, 0.11887525991249999, 0.11178751571250002, 0.971096189775, 0.1268244905375, 0.1301162225825, 3.74647694775, 0.11264470043749998, 0.490529086385, 2.032134533275, 0.1739067408925, 0.6379855298625, 0.2589837161875, 0.29410100219499996, 1.4622314648750003, 1.709410508575, 0.0622584783125, 0.12188256981250001, 1.0704223062625, 2.1338290144125, 0.1610022539875, 1.5909280234000003, 0.0085560164375, 0.020625, 0.021875000000000002, 0.021875000000000002, 0.0295, 0.0134025, 0.021875000000000002, 0.0325, 0.032916675, 0.040833325, 0.019712499999999997, 0.048749999999999995, 0.024374999999999997, 0.039, 0.0195, 0.040833325, 0.033333325, 0.0325, 0.02425, 0.017187499999999998, 0.028749999999999998, 0.0325, 0.02425, 0.028124999999999997, 0.03, 0.03325, 0.028124999999999997, 0.0192625, 0.022875, 0.028249999999999997, 0.02425, 0.0385, 0.0207625, 0.022125, 0.021875000000000002, 0.02775, 0.021875000000000002, 0.0215, 0.03, 0.019475, 0.021062499999999998, 0.021875000000000002, 0.0195, 0.023125000000000003, 0.028124999999999997, 0.023375, 0.028124999999999997, 0.03925, 0.021875000000000002, 0.03, 0.03, 0.028124999999999997, 0.039, 0.0193, 0.02225, 0.0325, 0.0375, 0.03, 0.03, 0.04140625, 0.023999999999999997, 0.0295, 0.0295, 0.0375, 0.017562499999999998, 0.017187499999999998, 0.028499999999999994, 0.0375, 0.021875000000000002, 0.0178125, 0.0325, 0.0325, 0.0325, 0.021875000000000002, 0.022, 0.018725, 0.022799999999999997, 0.022574999999999998, 0.022574999999999998, 0.018574999999999998, 0.024424999999999995, 0.0187375, 0.021974999999999998, 0.021875000000000002, 0.020625, 0.028124999999999997, 0.0275, 0.028124999999999997, 0.03125, 0.028249999999999997, 0.0325, 0.0184375, 0.02425, 0.018962499999999997, 0.033333325, 0.0325, 0.022, 0.03, 0.034749999999999996, 0.022187499999999995, 0.048749999999999995, 0.021875000000000002, 0.0198875, 0.020625, 0.0149125, 0.0390625, 0.040833325, 0.03, 0.020999999999999998, 0.028749999999999998, 0.019112499999999998], "UnitOfMeasure": "{pu}"}


	msg["Reactance"] = {"Values": [0.10819675088, 0.04886196175999999, 0.6845408506399999, 0.5405642252, 0.47994644272, 0.05573981020749999, 0.32012413471999995, 0.665048072935, 0.6230037232, 0.17830458544, 0.8140829967675001, 0.5845691743675, 0.37990541456000004, 0.40527634011999997, 0.09006791904, 0.26559209612, 0.007887416679999999, 0.02321224354, 0.309752010255, 1.57073113768, 0.58779036256, 1.1699068235399999, 0.30089343413999997, 2.15788578099, 0.043893835645, 0.404522269445, 0.45824438516, 0.05779674875999999, 0.51078979324, 0.9768819730950001, 0.147475978825, 0.35740383283999994, 1.03961902468, 0.4898372173599999, 0.053850235662499996, 1.076924166435, 1.0015159906225, 0.19262978911, 0.8143020574400001, 1.1455261681249997, 0.48173436704, 0.062294111230000004, 0.72546989344, 1.0012764327399999, 0.49502334445, 0.60016331332, 0.5141605002799999, 0.055674444000000003, 0.050828539039999995, 1.14976418192, 0.1704930062, 0.34222274355999993, 0.10550531295999999, 0.270950675815, 0.27515656052, 0.6468538130500001, 0.13805567061000001, 0.7471821845175, 0.5780365061425, 0.17065621984249998, 0.27027213059999994, 0.07457610528, 0.03396913332, 0.6295187777200001, 0.30992494479999994, 0.29017300572, 0.3833667498799999, 0.7287471036399998, 0.15066518152499997, 0.5678832364649999, 0.140958762735, 1.1749593865599999, 0.6906172684799999, 0.08248566635999999, 0.52978653008, 0.18525586348, 0.9253098627999998, 0.28318090728, 4.3720240000000005e-05, 0.06449695144, 0.06653863408499999, 0.96918654794, 0.13251154895999998, 0.15366330881999998, 0.07292245459999999, 0.0722163064125, 0.10292960683749998, 0.9403049405449999, 0.057389731119999995, 0.13392534043749998, 1.041930582455, 0.28613970502249997, 0.10254366517499998, 0.15414025882500001, 0.007900944345, 0.155837888955, 0.152365287375, 0.09438960410750001, 0.73688576844, 0.98369332148, 0.36008292402750003, 0.44575512258499994, 1.104995071375, 0.09075918569, 0.6481675162799999, 0.28865004323999993, 0.31539773474, 0.198831832195, 0.21739546493999998, 0.20685881896499997, 0.6709342400325, 1.0018939819400001, 0.5525162232149999, 0.550194032935, 0.9692560231824999, 0.13022903497, 0.6686445635799999, 0.2156188035825, 0.08667925359999999, 0.57742707592, 0.25106927788, 0.11530274992, 0.34890188467999994, 0.45727539056000005, 1.30334414272, 0.7065615616650001, 0.13545476248500002, 1.214962376075, 0.05795164574, 0.23587389646249998, 0.3113948562, 0.2625412538575, 0.8116468467524999, 0.4182794195599999, 0.40262816704000004, 0.13136335183999998, 0.9451035701775001, 0.0308565441125, 0.266360144715, 0.6323646415449999, 0.44291812764249994, 1.1233481297624999, 0.41854091013, 1.2237063953375, 0.16278064528000002, 0.59640633644, 0.239573208245, 0.45327996762999995, 0.056084740965, 0.9907042367050001, 0.843576522, 0.33524139985000007, 0.33688497992, 0.3202706622, 1.018033852805, 1.04061499086, 0.33298370803499994, 0.1539692128, 0.0238243799925, 0.125025415045, 0.2732132277, 1.068997971895, 0.047515646419999995, 0.565074854495, 0.05085672059, 0.046001935495, 0.258562139765, 0.43279121711999996, 0.27529517419999994, 0.574043747445, 0.25363023588, 0.25647073074, 0.13546855223999998, 0.017116974945, 0.45539602377, 0.57185831878, 0.5101481743524999, 0.1398942956225, 0.25059272707999997, 0.15518293475999997, 0.41992775136, 1.0009472405199997, 0.06353904284, 0.04625725684, 0.14182610335999998, 0.20253651604, 1.0087322354400001, 0.8654058100850001, 0.08976980223999999, 0.04381275612, 0.14315781348, 0.16855943272499999, 0.40663355172, 0.1533831114125, 0.06563464459999999, 1.0494188628399999, 1.06745717818, 0.35687282632, 0.11657977907499999, 0.16301618735999995, 0.7390456788975, 0.2776645718675, 0.16992268531999996, 0.8250484476275, 1.1170613303024999, 0.3156288417275, 0.47061180056249996, 0.26921506531999995, 0.51247254224, 0.18143782687250004, 0.6060417955225, 0.6517153210975, 0.7170909603225001, 0.0862180865425, 0.07218619788750001, 0.071560135555, 0.47672452460750003, 0.08772787328, 0.32101033208000007, 0.5445129985999999, 0.15035582815999998, 0.2889482535975, 0.7780581757125, 0.0389975320475, 0.06464274861750001, 0.08138314663999999, 0.08176840308, 0.07689309492, 0.6679689679199999, 0.08723628508, 0.0588364973425, 2.5770159191999995, 0.050936151437499994, 0.13009351745, 0.918899086475, 0.0786378769325, 0.43883864484, 0.1781420702, 0.13298782035499998, 1.0057965964, 0.772968388175, 0.042824523399999995, 0.08383698259999998, 0.7362904835599999, 1.4677552846800002, 0.11074547564, 1.09432058432, 0.005231392907499999, 0.03996595, 0.0399617, 0.0399617, 0.03993032, 0.04538734, 0.0399617, 0.03991541, 0.038911, 0.059911009999999994, 0.04207045, 0.05987312, 0.07, 0.039878130000000005, 0.03596618, 0.058909500000000004, 0.039911010000000004, 0.03991541, 0.039952930000000005, 0.04497899, 0.03993382, 0.03991541, 0.039952930000000005, 0.04093821, 0.03992794, 0.041915680000000004, 0.04093821, 0.042872310000000004, 0.04346149, 0.040937659999999994, 0.039952930000000005, 0.06492699, 0.0399655, 0.037358090000000004, 0.0399617, 0.07, 0.03876052, 0.03615911, 0.03992794, 0.042471430000000004, 0.039964490000000005, 0.0399617, 0.04057002, 0.03595243, 0.04093821, 0.04195835, 0.04093821, 0.0629217, 0.0399617, 0.03992794, 0.03992794, 0.04093821, 0.0629227, 0.04037048000000001, 0.04196226, 0.03991541, 0.05992495, 0.03992794, 0.03992794, 0.03986261, 0.0349473, 0.03993032, 0.03993032, 0.05992495, 0.03897468, 0.04497899, 0.03993497, 0.05992495, 0.0399617, 0.04997969000000001, 0.03991541, 0.03991541, 0.03991541, 0.0399617, 0.03996126, 0.038771070000000005, 0.0387571, 0.03985911, 0.038357510000000004, 0.03837124, 0.03794973, 0.038370730000000006, 0.040962290000000005, 0.0399617, 0.03996595, 0.04093821, 0.03993945, 0.04093821, 0.04092371, 0.0399361, 0.03991541, 0.04997824, 0.039952930000000005, 0.04027144, 0.039911010000000004, 0.03991541, 0.03996126, 0.03992794, 0.06494052, 0.04096156, 0.05786873, 0.0399617, 0.04217, 0.03996595, 0.04198305000000001, 0.03987774, 0.059911009999999994, 0.03992794, 0.03796284, 0.03993382, 0.04077134], "UnitOfMeasure": "{pu}"}


	msg["ShuntAdmittance"] = {"Values": [3.1404739135962935e-16, 1.418246990102404e-16, 1.986919816668285e-15, 1.5690192487820776e-15, 1.3930725932400548e-15, 1.5545170916064295e-16, 9.291790058610541e-16, 1.854740072254985e-15, 1.8083047086625843e-15, 5.175394775670934e-16, 2.2703807704945896e-15, 1.6302939844927315e-15, 1.1026976636136724e-15, 1.1763382574734105e-15, 2.6142739767734413e-16, 7.708965775204242e-16, 2.2893687775039297e-17, 6.473618977734826e-17, 8.638615601817352e-16, 4.5591389048534694e-15, 1.706095871890185e-15, 4.005211640878409e-15, 1.0301178357390819e-15, 6.018087101114828e-15, 1.22414693326557e-16, 1.1281645550042823e-15, 1.3300811031220798e-15, 1.677584403368721e-16, 1.4825972202996938e-15, 8.281334747887684e-15, 4.11292985805688e-16, 1.0373855079051429e-15, 3.0175549640183074e-15, 1.4217811445500935e-15, 1.501819102231652e-16, 3.00341356896468e-15, 2.7931091245989525e-15, 5.169745535486915e-16, 2.3635593013457326e-15, 2.5228536949566273e-16, 1.3982621480471782e-15, 1.7373087610627929e-16, 2.10571875487709e-15, 2.7924410261224973e-15, 1.3805613022847353e-15, 1.6737841855542432e-15, 1.4923808944335275e-15, 1.6159832676481727e-16, 1.4753280447244684e-16, 3.337257718683117e-15, 4.948659123928317e-16, 9.933215092396995e-16, 3.062353355362541e-16, 7.27170004755532e-16, 7.673789605735427e-16, 1.803998442789307e-15, 3.850208652622141e-16, 2.0838023524880926e-15, 1.6120751488494945e-15, 4.759399243494645e-16, 7.84480651052791e-16, 2.1646150305308578e-16, 9.859739427596261e-17, 1.827215035081175e-15, 8.995752611801268e-16, 8.422441038956715e-16, 1.112744391625612e-15, 2.1152310489698085e-15, 4.2018729328052814e-16, 1.5837588858579148e-15, 3.9311724433135797e-16, 3.4103882723051913e-15, 2.0045569744936575e-15, 2.394194662430212e-16, 1.5377363589561223e-15, 5.377159682410015e-16, 2.6857659425833264e-15, 8.219491296256296e-16, 1.2690055117131001e-19, 1.872061701080602e-16, 5.640688616448732e-16, 2.7029461494740496e-15, 1.1233419441881241e-15, 1.3026520438029519e-15, 5.371827600141543e-16, 5.319809242501091e-16, 7.582302404853499e-16, 2.5235646526108593e-15, 1.6005314258629e-16, 9.865600987607385e-16, 2.9058206202428073e-15, 7.980096458685962e-16, 8.692947981208215e-16, 1.3066952985237839e-15, 6.697878223515158e-17, 1.3210866413592838e-15, 1.2916483090713903e-15, 2.6324139301667398e-16, 1.9776338484081176e-15, 2.640009201331531e-15, 1.0042284997250512e-15, 1.2431580842309092e-15, 3.081699988210898e-15, 2.4357701744529797e-16, 1.8813440883963822e-15, 8.378236163108543e-16, 8.796068150969601e-16, 5.545183601306202e-16, 6.062901266238697e-16, 5.769046726810435e-16, 1.871155893053535e-15, 2.7941632974806783e-15, 1.5409021113996959e-15, 1.5344257985690924e-15, 2.7031399076721985e-15, 3.631933082130174e-16, 1.8647702574254085e-15, 6.013352291530152e-16, 2.5159159823820176e-16, 1.6760158268912951e-15, 7.287432490113228e-16, 3.3467296877637727e-16, 1.0127081066023619e-15, 1.3272685396772766e-15, 3.7830325285741006e-15, 1.9705162608045338e-15, 1.1482924879654992e-15, 3.3883857376558085e-15, 1.6162025570985787e-16, 6.578242770288888e-16, 8.684432623634826e-16, 7.321963689039464e-16, 2.2635866375007084e-15, 1.2140804553172541e-15, 1.1686517803760976e-15, 3.8128980426929773e-16, 2.635781585387417e-15, 2.2730451987351576e-16, 2.2580184532345855e-15, 1.7635898646763003e-15, 1.2352460423518648e-15, 3.1328844878358722e-15, 1.1672608785561512e-15, 3.41277176864926e-15, 4.724803341896912e-16, 1.731104239507783e-15, 6.681412181373526e-16, 1.2641439831613087e-15, 1.5641368006789656e-16, 2.7629564272854354e-15, 2.2639675714749987e-15, 8.99711689553498e-16, 9.778283383893526e-16, 9.296043104333473e-16, 2.839175480016935e-15, 2.902151591567632e-15, 8.936525580790631e-16, 4.469046365649576e-16, 6.64433656257485e-17, 3.486810303966358e-16, 2.31611418620633e-15, 2.868947486358354e-15, 1.3251549333169275e-16, 1.5759266421601476e-15, 1.3648787419349833e-16, 1.2345873488613367e-16, 6.939219909194513e-16, 1.2562017956587176e-15, 7.990603285979629e-16, 4.866348815366702e-15, 2.150103025090559e-15, 2.1741827905414328e-15, 1.1484093880418561e-15, 1.4510596294621798e-16, 1.2221793792335271e-15, 1.5948449182218687e-15, 1.4227426561565013e-15, 3.9014857200600524e-16, 7.273600324694846e-16, 4.504275354715675e-16, 1.2188648346786942e-15, 2.905307850903604e-15, 1.8442578442601136e-16, 1.3426439078716975e-16, 4.1165855189411546e-16, 5.878740720040163e-16, 2.9279042535357465e-15, 2.3225524171220258e-15, 2.6056209624639526e-16, 1.27169084615322e-16, 4.1552391832916734e-16, 4.932748648885528e-16, 1.1802776434442126e-15, 4.488626494230318e-16, 1.9050839098031134e-16, 3.0459995668817325e-15, 2.9770112633349158e-15, 1.0358442304541602e-15, 3.411608228759122e-16, 4.731640088396024e-16, 2.061110604875109e-15, 7.743735062871321e-16, 4.932105227148128e-16, 2.3009621103225946e-15, 3.1153513509706927e-15, 8.802513450311687e-16, 1.3124804063068855e-15, 7.814124573133226e-16, 1.487481497595129e-15, 5.060085455749883e-16, 1.6901785740935513e-15, 1.8175566112198915e-15, 1.9998815028397843e-15, 2.404520012482652e-16, 2.0131873068183466e-16, 1.9957271720841367e-16, 1.3295280675185975e-15, 2.546352781301942e-16, 9.317512454789192e-16, 1.5804807943021985e-15, 4.364165765174842e-16, 8.05842354207917e-16, 2.1699118240744503e-15, 1.0875948424049582e-16, 1.8028094677796478e-16, 2.362193383355523e-16, 2.373375676631657e-16, 2.2318670086476785e-16, 1.938818958779254e-15, 2.532084146562217e-16, 1.6408800171491422e-16, 7.479939280381812e-15, 1.4205487549290765e-16, 8.174016774011511e-16, 2.562700393254514e-15, 2.1931169712301225e-16, 1.2737548079669e-15, 5.170677675872365e-16, 3.7088723292695455e-16, 2.919383389692912e-15, 2.1557170112642975e-15, 1.2430068140313646e-16, 2.433417405869576e-16, 2.1371261499468982e-15, 4.260245474647327e-15, 3.2144521389738224e-16, 3.1763294370826427e-15, 5.2223064288998826e-17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "UnitOfMeasure": "{pu}"}


	msg["ShuntConductance"] = {"Values": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "UnitOfMeasure": "{pu}"}

	msg["RatedCurrent"] = {"Values": [8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 0.1, 0.1, 0.1, 0.050000000999999995, 0.5, 0.1, 0.03, 0.03, 0.03, 0.1, 0.03, 0.10000000199999999, 0.050000000999999995, 0.050000000999999995, 0.03, 0.03, 0.03, 0.099999999, 0.2, 0.050000000999999995, 0.03, 0.099999999, 0.05, 0.050000000999999995, 0.050000000999999995, 0.05, 0.1, 0.1, 0.05, 0.099999999, 0.050000000999999995, 0.1, 0.05, 0.1, 0.049999998, 0.1, 0.05, 0.050000000999999995, 0.1, 0.1, 0.1, 0.1, 0.05, 0.05, 0.1, 0.05, 0.050000000999999995, 0.1, 0.050000000999999995, 0.050000000999999995, 0.05, 0.050000000999999995, 0.1, 0.1, 0.03, 0.050000000999999995, 0.050000000999999995, 0.050000000999999995, 0.015999998999999997, 0.050000000999999995, 0.050000000999999995, 0.050000000999999995, 0.050000000999999995, 0.2, 0.2, 0.050000000999999995, 0.050000000999999995, 0.1, 0.2, 0.03, 0.03, 0.03, 0.1, 0.099999999, 0.1, 0.05, 0.05, 0.05, 0.1, 0.05, 0.1, 0.1, 0.1, 0.1, 0.05, 0.05, 0.05, 0.03, 0.05, 0.03, 0.2, 0.099999999, 0.1, 0.03, 0.03, 0.099999999, 0.050000000999999995, 0.099999999, 0.1, 0.03, 0.1, 0.1, 0.1, 0.2, 0.015999998999999997, 0.03, 0.050000000999999995, 0.1, 0.050000000999999995, 0.1], "UnitOfMeasure": "{pu}"}

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='Init.NIS.NetworkComponentInfo', body=message)
	print(message)
	time.sleep(1000)

 ########################################################################################## Init.CIS 1
	msg = {**write_abstract_message('Init.CIS.CustomerInfo', 'SimTest30', 'Grid', 
		'BusInitialization'+str(epoch)), **write_abstract_result( epoch, ['Epoch'+str(epoch)] ) }
	msg["ResourceId"] = [
    "HeatPump1",
    "Heater1",
    "Motor1",
    "HeatPump2",
    "Motor2",
    "Heater2",
    "Home1",
    "Home2"
	]
	msg["CustomerId"] = [
    "gridA-1",
    "gridA-2",
    "gridA-3",
    "gridA-4",
    "gridA-5",
    "gridA-6",
    "gridA-7",
	"gridA-8"
  ]
	msg["BusName"] = [
    "bus7",
    "bus3",
    "bus9",
    "bus5",
    "bus8",
    "bus6",
    "bus4",
    "bus2"
  ]

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='Init.CIS.CustomerInfo', body=message)
	print(message)
	time.sleep(0)

 ############################################################################################### voltage value 1.1

	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           11.56,
           11.56,
           11.56,
           11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus1"
	msg["Node"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)
 ##################################################################################### voltage value 1.2
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           11.56,
           11.56,
           11.56,
           11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus1"
	msg["Node"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

##################################################################################### voltage value 1.3
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           11.56,
           11.56,
           11.56,
           11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus1"
	msg["Node"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

	##################################################################################### voltage value 2.1
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           11.56,
           11.56,
           11.56,
           11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus2"
	msg["Node"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

	##################################################################################### voltage value 2.2
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           11.56,
           11.56,
           11.56,
           11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus2"
	msg["Node"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

	##################################################################################### voltage value 2.3
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           11.56,
           11.56,
           11.56,
           11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56,
		   11.56
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus2"
	msg["Node"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

	##################################################################################### voltage value 3.1
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           0.23,
           0.23,
           0.23,
           0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus3"
	msg["Node"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

	##################################################################################### voltage value 3.2
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
		 [
           0.23,
           0.23,
           0.23,
           0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus3"
	msg["Node"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

	##################################################################################### voltage value 3.3
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           0.23,
           0.23,
           0.23,
           0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus3"
	msg["Node"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

	##################################################################################### voltage value 4.1
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           0.23,
           0.23,
           0.23,
           0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.25,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus4"
	msg["Node"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

	##################################################################################### voltage value 4.2
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           0.23,
           0.23,
           0.23,
           0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus4"
	msg["Node"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

	##################################################################################### voltage value 4.3
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           0.23,
           0.23,
           0.23,
           0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus4"
	msg["Node"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

	##################################################################################### voltage value 5.1
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           0.23,
           0.23,
           0.23,
           0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus5"
	msg["Node"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

	##################################################################################### voltage value 5.2
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           0.23,
           0.23,
           0.23,
           0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus5"
	msg["Node"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

	##################################################################################### voltage value 5.3
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           0.23,
           0.23,
           0.23,
           0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus5"
	msg["Node"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

	##################################################################################### voltage value 6.1
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           0.23,
           0.23,
           0.23,
           0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus6"
	msg["Node"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

	##################################################################################### voltage value 6.2
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           0.23,
           0.23,
           0.23,
           0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus6"
	msg["Node"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

	##################################################################################### voltage value 6.3
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           0.23,
           0.23,
           0.23,
           0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus6"
	msg["Node"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

	##################################################################################### voltage value 7.1
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           0.23,
           0.23,
           0.23,
           0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus7"
	msg["Node"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

	##################################################################################### voltage value 7.2
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           0.23,
           0.23,
           0.23,
           0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus7"
	msg["Node"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

	##################################################################################### voltage value 7.3
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           0.23,
           0.23,
           0.23,
           0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus7"
	msg["Node"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

	##################################################################################### voltage value 8.1
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           0.23,
           0.23,
           0.23,
           0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus8"
	msg["Node"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

	##################################################################################### voltage value 8.2
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           0.23,
           0.23,
           0.23,
           0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus8"
	msg["Node"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

	##################################################################################### voltage value 8.3
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           0.23,
           0.23,
           0.23,
           0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus8"
	msg["Node"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

	##################################################################################### voltage value 9.1
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           0.23,
           0.23,
           0.23,
           0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus9"
	msg["Node"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

	##################################################################################### voltage value 9.2
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           0.23,
           0.23,
           0.23,
           0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus9"
	msg["Node"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

	##################################################################################### voltage value 9.3
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           0.23,
           0.23,
           0.23,
           0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus9"
	msg["Node"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

	##################################################################################### voltage value 10.1
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           0.23,
           0.23,
           0.23,
           0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus10"
	msg["Node"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

	##################################################################################### voltage value 10.2
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           0.23,
           0.23,
           0.23,
           0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus10"
	msg["Node"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

	##################################################################################### voltage value 10.3
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           0.23,
           0.23,
           0.23,
           0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus10"
	msg["Node"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

	##################################################################################### voltage value 11.1
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           0.23,
           0.23,
           0.23,
           0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus11"
	msg["Node"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

##################################################################################### voltage value 11.2
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           0.23,
           0.23,
           0.23,
           0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus11"
	msg["Node"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

	##################################################################################### voltage value 11.3
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           0.23,
           0.23,
           0.23,
           0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus11"
	msg["Node"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

	##################################################################################### voltage value 12.1
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           0.23,
           0.23,
           0.23,
           0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus12"
	msg["Node"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

##################################################################################### voltage value 12.2
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           0.23,
           0.23,
           0.23,
           0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus12"
	msg["Node"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(0)

##################################################################################### voltage value 12.3
	msg = {**write_abstract_message('NetworkForecastState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Forecast"] = {
   "TimeIndex" :
   [
     "2021-05-10T16:00:00Z",
     "2021-05-10T17:00:00Z",
	 "2021-05-10T18:00:00Z",
	 "2021-05-10T19:00:00Z",
	 "2021-05-10T20:00:00Z",
	 "2021-05-10T21:00:00Z",
	 "2021-05-10T22:00:00Z",
	 "2021-05-10T23:00:00Z",
	 "2021-05-10T24:00:00Z",
	 "2021-05-11T01:00:00Z",
	 "2021-05-11T02:00:00Z",
	 "2021-05-11T03:00:00Z",
	 "2021-05-11T04:00:00Z",
	 "2021-05-11T05:00:00Z",
	 "2021-05-11T06:00:00Z",
	 "2021-05-11T07:00:00Z",
	 "2021-05-11T08:00:00Z",
	 "2021-05-11T09:00:00Z",
	 "2021-05-11T10:00:00Z",
	 "2021-05-11T11:00:00Z",
	 "2021-05-11T12:00:00Z",
	 "2021-05-11T13:00:00Z",
	 "2021-05-11T14:00:00Z",
	 "2021-05-11T15:00:00Z",
	 "2021-05-11T16:00:00Z",
	 "2021-05-11T17:00:00Z",
	 "2021-05-11T18:00:00Z",
	 "2021-05-11T19:00:00Z",
	 "2021-05-11T20:00:00Z",
	 "2021-05-11T21:00:00Z",
	 "2021-05-11T22:00:00Z",
	 "2021-05-11T23:00:00Z",
	 "2021-05-11T24:00:00Z"
   ],
  "Series" :
   {
     "Magnitude" :
       {
         "UnitOfMeasure" : "kV",
         "Values" :
         [
           0.23,
           0.23,
           0.23,
           0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23,
		   0.23
         ]
       },
     "Angle" :
      {
       "UnitOfMeasure" : "deg",
       "Values" :
       [
          2,
           0.27,
           0.15,
           0.21,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2,
		   2
       ]
      }
     }
    }
	msg["Bus"] = "bus12"
	msg["Node"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkForecastState.Voltage', body=message)
	print(message)
	time.sleep(100)











	#############################################################################################################################################
	# Network state.Current msgs
	#


	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'transformer1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "t1"
	msg["Phase"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)


	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'transformer1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "t1"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'transformer1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = 't1'
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l1"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l1"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l1"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load2-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l2"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load2-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l2"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load2-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l2"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load3-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l3"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load3-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l3"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)
	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load3-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l3"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load4-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l4"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load4-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l4"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load4-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l4"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load5-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l5"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load5-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l5"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load5-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l5"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load6-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l6"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load6-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l6"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load6-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l6"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load7-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l7"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load7-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l7"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load7-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l7"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load8-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l8"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load8-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l8"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load8-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l8"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load9-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l9"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load9-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l9"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load9-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l9"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)	

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load10-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l10"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load10-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l10"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load10-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l10"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)


################### Send ready message to the simulation manager



	msg = {**write_abstract_message('Status', 'SimTest30', 'Grid', 
		'Grid'+str(epoch)), **write_abstract_result( epoch, [] ) }

	epoch_time_beg = simStartTime + datetime.timedelta(hours=epoch)
	epoch_time_end = simStartTime + datetime.timedelta(hours=epoch+1)
	msg["Value"]="ready"

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='Status.Ready', body=message)
	print(message)
	time.sleep(t)
#########################################################31######################################################################################################
	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "sourcebus"
	msg["Node"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "sourcebus"
	msg["Node"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "1"
	msg["Node"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "1"
	msg["Node"] = 2
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "1"
	msg["Node"] = 3
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "2"
	msg["Node"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "2"
	msg["Node"] = 2
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "2"
	msg["Node"] = 3
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "3"
	msg["Node"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "3"
	msg["Node"] = 2
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "3"
	msg["Node"] = 3
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "4"
	msg["Node"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "4"
	msg["Node"] = 2
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "4"
	msg["Node"] = 3
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "5"
	msg["Node"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "5"
	msg["Node"] = 2
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "5"
	msg["Node"] = 3
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "6"
	msg["Node"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "6"
	msg["Node"] = 2
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "6"
	msg["Node"] = 3
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "7"
	msg["Node"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "7"
	msg["Node"] = 2
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "7"
	msg["Node"] = 3
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "8"
	msg["Node"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "8"
	msg["Node"] = 2
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "8"
	msg["Node"] = 3
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "9"
	msg["Node"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "9"
	msg["Node"] = 2
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "9"
	msg["Node"] = 3
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "10"
	msg["Node"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "10"
	msg["Node"] = 2
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "10"
	msg["Node"] = 3
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "11"
	msg["Node"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)	

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "11"
	msg["Node"] = 2
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "11"
	msg["Node"] = 3
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	#############################################################################################################################################
	# Network state.Current msgs
	#


	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "t1"
	msg["Phase"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)


	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "t1"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = 't1'
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l1"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l1"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l1"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l2"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l2"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l2"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l3"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l3"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)
	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l3"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l4"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l4"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l4"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l5"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l5"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l5"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l6"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l6"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l6"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l7"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l7"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l7"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l8"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l8"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l8"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l9"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l9"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l9"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)	

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l10"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l10"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l10"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)




	msg = {**write_abstract_message('Status', 'SimTest31', 'Grid', 
		'Grid'+str(epoch)), **write_abstract_result( epoch, [] ) }

	epoch_time_beg = simStartTime + datetime.timedelta(hours=epoch)
	epoch_time_end = simStartTime + datetime.timedelta(hours=epoch+1)
	msg["Value"]="ready"

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='Status.Ready', body=message)
	print(message)
	time.sleep(t)









connection.close()
