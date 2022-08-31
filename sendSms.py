# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
import sensitive_Info_db
import DOL_DB
import datetime
import time

from configparser import ConfigParser
import configparser

config = ConfigParser()
config.read('config.ini', encoding='UTF8')

#=====================================Chat logs=============================================================================
def send_log_msg(consumer_phone,communication_Info):
	print(consumer_phone)
	sms_Info = []
	sms_logs = {}
	sms_cursor = sensitive_Info_db.get_sms_details()
	for s in sms_cursor:
		sms_Info.append(s)
		if sms_Info[0]['account_name'] == 'Twilio':
			account_sid = sms_Info[0]['account_sid_no']
			auth_token =  sms_Info[0]['auth_token']
			client = Client(account_sid, auth_token)
			message = communication_Info['message_plain_text']
			print(message)
			prefix = '+1'
			num = prefix + consumer_phone
			message = client.messages.create(
										body=message,
										from_='+12058589412',
										to=num
										)
			count_of_nums = len(consumer_phone)
			print(count_of_nums)
			msg_status = len(message.status)
			print('message_status--------',msg_status)
			sms_logs['consumer_id'] = "4086"
			sms_logs['nexus_id'] = communication_Info['nexus_id']
			sms_logs['po_number'] = communication_Info['po_number']
			sms_logs['twilio_sid'] = message.sid
			#sms_logs['twilio_delivery_status'] = message.status
			sms_logs['twilio_delivery_status'] = ""
			print(sms_logs)
			DOL_DB.save_to_message_delivery_status_records(sms_logs)
			return

	# we will be adding logger id and logger name in place of modern garage doors


#=====================================Lead time Logs=================================================================

def send_comm_log_msg(consumer_phone,communication_Info):
	print(consumer_phone)
	sms_Info = []
	sms_logs = {}
	sms_cursor = sensitive_Info_db.get_sms_details()
	for s in sms_cursor:
		sms_Info.append(s)
		if sms_Info[0]['account_name'] == 'Twilio':
			account_sid = sms_Info[0]['account_sid_no']
			auth_token =  sms_Info[0]['auth_token']
			client = Client(account_sid, auth_token)
			#final_message = communication_Info['subject'] + ' : ' + "Hello from Modern Garage Doors! Order status update. " + communication_Info['message_plain_text']
			final_message = communication_Info['message_plain_text']

			print(final_message)
			prefix = '+1'
			num = prefix + consumer_phone
			message = client.messages.create(
									body=final_message,
									from_='+12058589412',
									to=num
									)
			count_of_nums = len(consumer_phone)
			print(count_of_nums)
			msg_status = len(message.status)
			print('message_status--------',msg_status)
			sms_logs['consumer_id'] = "4086"
			sms_logs['nexus_id'] = communication_Info['nexus_id']
			sms_logs['po_number'] = communication_Info['po_number']
			sms_logs['twilio_sid'] = message.sid
			#sms_logs['twilio_delivery_status'] = message.status
			sms_logs['twilio_delivery_status'] = ""
			print(sms_logs)
			DOL_DB.save_to_message_delivery_status_records(sms_logs)
			return

#================================Login_reset password========================================================================
#add the function send_mail(sms_info)
def send_msg(message_info):
	print("Inside Send message")
	sms_logs = {}
	msg_info = msg_config()
	account_sid = msg_info[0]
	auth_token = msg_info[1]
	client = Client(account_sid, auth_token)
	final_message= message_info['message']
	prefix = '+1'
	num=prefix + message_info['number']
	message = client.messages.create(
		body=final_message,
		from_=config['sms']['FROM'],
		to=num
		)
	msg_status = len(message.status)
	print('message_status--------',msg_status)
	sms_logs['consumer_id'] = "4086"
	sms_logs['nexus_id'] = communication_Info['nexus_id']
	sms_logs['po_number'] = communication_Info['po_number']
	sms_logs['twilio_sid'] = message.sid
	#sms_logs['twilio_delivery_status'] = message.status
	sms_logs['twilio_delivery_status'] = ""
	print(sms_logs)
	DOL_DB.save_to_message_delivery_status_records(sms_logs)
	return

#=============================Save Order entry=======================================================================================

def send_order_entry_log_msg(mobile_num,communication_Info):
	sms_Info = []
	sms_logs = {}
	sms_cursor = sensitive_Info_db.get_sms_details()
	for s in sms_cursor:
		sms_Info.append(s)
		if sms_Info[0]['account_name'] == 'Twilio':
			account_sid = sms_Info[0]['account_sid_no']
			auth_token =  sms_Info[0]['auth_token']
			client = Client(account_sid, auth_token)
			final_message = communication_Info['message_plain_text']
			print(final_message)
			prefix = '+1'
			num = prefix + mobile_num
			message = client.messages.create(
				body=final_message,
				from_='+12058589412',
				to=num)
			msg_status = len(message.status)
			print('message_status--------',msg_status)
			sms_logs['consumer_id'] = "4086"
			sms_logs['nexus_id'] = communication_Info['nexus_id']
			sms_logs['po_number'] = communication_Info['po_number']
			sms_logs['twilio_sid'] = message.sid
			#sms_logs['twilio_delivery_status'] = message.status
			sms_logs['twilio_delivery_status'] = ""
			print(sms_logs)
			DOL_DB.save_to_message_delivery_status_records(sms_logs)

			return


#=============================Bulk Message =======================================================================================

def send_bulk_log_msg(phone_list,all_phone_Po_list,communication_Info):
	sms_Info = []
	sms_logs = {}
	sms_cursor = sensitive_Info_db.get_sms_details()
	for s in sms_cursor:
		sms_Info.append(s)

	acc_name = sms_Info[0]['account_name']
	if acc_name == 'Twilio':
		account_sid = sms_Info[0]['account_sid_no']
		auth_token =  sms_Info[0]['auth_token']
		client = Client(account_sid, auth_token)
		message_text = communication_Info['message_plain_text']
		print(message_text)
		prefix = '+1'
		for i in all_phone_Po_list:
			num = prefix + i[0]
			final_message = message_text + " Order ID " + i[3] 
			print('=====================SMS=====================final message')
			print(final_message)
			print('==========================================final message')
			message = client.messages.create(
					body=final_message,
					from_='+12058589412',
					to=num
					)
			msg_status = len(message.status)
			print('message_status--------',msg_status)
			sms_logs['consumer_id'] = "4086"
			sms_logs['nexus_id'] = communication_Info['nexus_id']
			sms_logs['po_number'] = communication_Info['po_number']
			sms_logs['twilio_sid'] = message.sid
			sms_logs['twilio_delivery_status'] = ""
			print(sms_logs)
			DOL_DB.save_to_message_delivery_status_records(sms_logs)
			sms_logs = {}
	return

#===============================================================================================================
def send_bulk_log_msg_for_lead_and_buffer_time(all_phone_Po_list,comm_log,text_message_list):
	sms_Info = []
	sms_logs = {}
	sms_cursor = sensitive_Info_db.get_sms_details()
	for s in sms_cursor:
		sms_Info.append(s)

	acc_name = sms_Info[0]['account_name']
	if acc_name == 'Twilio':
		account_sid = sms_Info[0]['account_sid_no']
		auth_token =  sms_Info[0]['auth_token']
		client = Client(account_sid, auth_token)
		prefix = '+1'
		for i,k in zip(all_phone_Po_list,text_message_list):
			num = prefix + i[0]
			final_message = comm_log['salutaion_sms'] + k + comm_log['text_body_sms'] + i[3] + comm_log['conclusion_sms'] + " Reason: "+ comm_log['reason'] + config['consumer_portal_url']['CUST_URL']
			print('=========================SMS=================final message')
			print(final_message)
			message = client.messages.create(
					body=final_message,
					from_='+12058589412',
					to=num
					)
			msg_status = len(message.status)
			print('message_status--------',msg_status)
			sms_logs['consumer_id'] = "4086"
			sms_logs['nexus_id'] = i[3]
			sms_logs['po_number'] = i[1]
			sms_logs['twilio_sid'] = message.sid
			sms_logs['twilio_delivery_status'] = ""
			print(sms_logs)
			DOL_DB.save_to_message_delivery_status_records(sms_logs)
			sms_logs = {}
	return


def send_bulk_log_msg_for_progress_time_line_update(all_phone_Po_list,text_message_list):
	sms_Info = []
	sms_logs = {}
	sms_cursor = sensitive_Info_db.get_sms_details()
	for s in sms_cursor:
		sms_Info.append(s)

	acc_name = sms_Info[0]['account_name']
	if acc_name == 'Twilio':
		account_sid = sms_Info[0]['account_sid_no']
		auth_token =  sms_Info[0]['auth_token']
		client = Client(account_sid, auth_token)
		prefix = '+1'
		for i,k in zip(all_phone_Po_list,text_message_list):
			num = prefix + i[0]
			final_message =  k
			print('=========================SMS=================final message')
			print(final_message)
			message = client.messages.create(
					body=final_message,
					from_='+12058589412',
					to=num
					)
			msg_status = len(message.status)
			print('message_status--------',msg_status)
			sms_logs['consumer_id'] = "4086"
			sms_logs['nexus_id'] = i[3]
			sms_logs['po_number'] = i[1]
			sms_logs['twilio_sid'] = message.sid
			sms_logs['twilio_delivery_status'] = ""
			print(sms_logs)
			DOL_DB.save_to_message_delivery_status_records(sms_logs)
			sms_logs = {}
	return


#==========================================Check for delivery status=========================================================
def send_sid_to_check_delivery_status(n_id,msid):
	sms_Info = []
	sms_cursor = sensitive_Info_db.get_sms_details()
	for s in sms_cursor:
		sms_Info.append(s)
		if sms_Info[0]['account_name'] == 'Twilio':
			account_sid = sms_Info[0]['account_sid_no']
			auth_token =  sms_Info[0]['auth_token']
			client = Client(account_sid, auth_token)

			msg = client.messages(msid).fetch()
			print(msg.status)
			msg_status = msg.status
			print(msg_status)
			DOL_DB.update_deliery_status(n_id,msg_status)

	return

#=================================Dynamic_url=================================================================

def send_dynamic_url_to_consumer_via_SMS(c_ph_num,communication_Info):
	sms_Info = []
	sms_logs = {}
	sms_cursor = sensitive_Info_db.get_sms_details()
	for s in sms_cursor:
		sms_Info.append(s)
	account_sid = sms_Info[0]['account_sid_no']
	auth_token =  sms_Info[0]['auth_token']
	acc_name = sms_Info[0]['account_name']
	if acc_name == 'Twilio':
		account_sid = account_sid
		auth_token = auth_token
		client = Client(account_sid, auth_token)
		final_message =  communication_Info['message_plain_text']
		print(final_message)
		prefix = '+1'
		num = prefix + c_ph_num
		message = client.messages.create(
								body=final_message,
								from_='+12058589412',
								to=num)

		sms_logs['consumer_id'] = "4086"
		sms_logs['nexus_id'] = communication_Info['nexus_id']
		sms_logs['po_number'] = communication_Info['po_number']
		sms_logs['twilio_sid'] = message.sid
		sms_logs['twilio_delivery_status'] = ""
		print(sms_logs)
		DOL_DB.save_to_message_delivery_status_records(sms_logs)
	return

#=================================================================================================

def send_consumer_creds_by_msg(password,phone,user_id,first_name,org_name):
	print("----------Inside send sms")
	sms_Info = []
	sms_cursor = sensitive_Info_db.get_sms_details()
	for s in sms_cursor:
		sms_Info.append(s)
	if sms_Info[0]['account_name'] == 'Twilio':
		account_sid = sms_Info[0]['account_sid_no']
		auth_token =  sms_Info[0]['auth_token']
		client = Client(account_sid, auth_token)
		message = 'Hello ' + first_name + ', Welcome to Nexus. Your secure credentials for ' + org_name + ' are :- User ID : ' + phone +' and Password : ' + password + "." + " Platform Link : " + config['consumer_portal_url']['CUST_URL']
		prefix = '+1'
		num=prefix + phone
		message = client.messages.create(
	                              body=message,
	                              from_='+12058589412',
	                              to=num
	                          )
	return

#=================================================================================================

def send_consumer_new_reset_creds_by_msg(password,phone,org):
	print("----------Inside send sms")
	sms_Info = []
	sms_cursor = sensitive_Info_db.get_sms_details()
	for s in sms_cursor:
		sms_Info.append(s)
	if sms_Info[0]['account_name'] == 'Twilio':
		account_sid = sms_Info[0]['account_sid_no']
		auth_token =  sms_Info[0]['auth_token']
		client = Client(account_sid, auth_token)
		message = 'Welcome to Nexus. Your password for ' + org + ' is ' + password + "."
		prefix = '+1'
		num=prefix + phone
		message = client.messages.create(
	                              body=message,
	                              from_='+12058589412',
	                              to=num
	                          )
	return


#========================================================================================================
def send_consumer_welcome_note_by_msg(phone,communication_Info):
	print("----------Inside welcome note send sms")
	sms_Info = []
	sms_cursor = sensitive_Info_db.get_sms_details()
	for s in sms_cursor:
		sms_Info.append(s)
	if sms_Info[0]['account_name'] == 'Twilio':
		account_sid = sms_Info[0]['account_sid_no']
		auth_token =  sms_Info[0]['auth_token']
		client = Client(account_sid, auth_token)
		message = communication_Info['message_plain_text']
		prefix = '+1'
		num=prefix + phone
		message = client.messages.create(
	                              body=message,
	                              from_='+12058589412',
	                              to=num
	                          )
	return

#================================================================================================================
def send_custom_test_message_to_dealer(phone,text_message):
	print("----------Inside welcome note send sms:",phone)
	sms_Info = []
	sms_cursor = sensitive_Info_db.get_sms_details()
	for s in sms_cursor:
		sms_Info.append(s)
	if sms_Info[0]['account_name'] == 'Twilio':
		account_sid = sms_Info[0]['account_sid_no']
		auth_token =  sms_Info[0]['auth_token']
		client = Client(account_sid, auth_token)
		message = text_message
		print("--------",message)
		prefix = '+1'
		num=prefix + phone
		message = client.messages.create(
	                              body=message,
	                              from_='+12058589412',
	                              to=num
	                          	)
	return

