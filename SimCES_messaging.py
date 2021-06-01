import datetime
def write_abstract_message(type, sim_id, source_ps_id, msg_id, timestamp=None):
	res = {
		"Type" : type,
		"SimulationId" : sim_id,
		"SourceProcessId" : source_ps_id,
		"MessageId" : msg_id}
	if timestamp is not None:
		res["Timestamp"]=timestamp
	else:
		res["Timestamp"]=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
		
	return res
def write_abstract_result(epoch_num, trig_msg_array, last_ud=None, warnings=None):
	res = {
		"EpochNumber" : epoch_num,
		"TriggeringMessageIds" : trig_msg_array
		} 
	if last_ud is not None:
		res["LastUpdatedInEpoch"]=last_ud
	if warnings is not None:
		res["Warnings"]=warnings
	return res
	
#def read_msg_body(body):
    