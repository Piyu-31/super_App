from flask import request,session
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import re

from configparser import ConfigParser
import configparser

import sensitive_Info_db

config = ConfigParser()
config.read('config.ini', encoding='UTF8')

# *************************Mail config**************************************

def mail_config():
    global mail_server
    data = []
    api_key = ''
    mail_server = ''
    mail_data = sensitive_Info_db.get_sms_details()
    for m in mail_data:
        data.append(m)
    api_key = data[1]['api_key']
    mail_server = data[1]['mail_server']
    return [api_key, mail_server]


# ************************************************************************

def send_to_mail(consumer_email,communication_Info):
    mail_info = mail_config()
    message = Mail(
        from_email=config['Sendgrid']['FROM_MAIL'],
        to_emails=consumer_email,
        subject=communication_Info['subject'],
        html_content=communication_Info['message_plain_text'])
    try:
        sg = SendGridAPIClient(mail_info[0])
        response = sg.send(message)
    except Exception as e:
        print(str(e))
    else:
        print(response.status_code)
    return

#=====================================================================================================

def send_comm_to_mail(consumer_email,communication_Info):
    mail_info = mail_config()
    message = Mail(
        from_email=config['Sendgrid']['FROM_MAIL'],
        to_emails=consumer_email,
        subject=communication_Info['subject'],
        html_content=communication_Info['message_plain_text'])
    try:
        sg = SendGridAPIClient(mail_info[0])
        response = sg.send(message)
    except Exception as e:
        print(str(e))
    else:
        print(response.status_code)
    return

#===================================Order entry Mail=====================================================================================

def send_order_entry_to_mail(email,communication_Info):
    mail_info = mail_config()
    message = Mail(
        from_email=config['Sendgrid']['FROM_MAIL'],
        to_emails=email,
        subject=communication_Info['subject'],
        html_content=communication_Info['message_plain_text'])
    try:
        sg = SendGridAPIClient(mail_info[0])
        response = sg.send(message)
    except Exception as e:
        print(str(e))
    else:
        print(response.status_code)
    return



#-----------------------------------------Bulk Mails---------------------------------------------------------------

def send_bulk_log_mail(email_list,all_phone_Po_list,communication_Info):
    mail_info = mail_config()
    for i in all_phone_Po_list:
        final_message =  communication_Info['message_plain_text'] + i[3]
        print("=======================================================Mail Final message")
        print(final_message)
        print("=======================================================Mail Final message")
        print('----------------------')
        print(i)
        print('----------------------')
        print(i[2])
        message = Mail(
        from_email=config['Sendgrid']['FROM_MAIL'],
        to_emails=i[2],
        subject=communication_Info['email_subject'],
        html_content = final_message)
        try:
            sg = SendGridAPIClient(mail_info[0])
            response = sg.send(message)
        except Exception as e:
            print(str(e))
        else:
            print(response.status_code)
    return

def send_dynamic_url_to_consumer_via_email(c_email,communication_Info):
    mail_info = mail_config()
    message = Mail(
        from_email=config['Sendgrid']['FROM_MAIL'],
        to_emails=c_email,
        subject=communication_Info['subject'],
        html_content= communication_Info['message_plain_text'])
    try:
        sg = SendGridAPIClient(mail_info[0])
        response = sg.send(message)
    except Exception as e:
        print(str(e))
    else:
        print(response.status_code)
    return


#------------------------------------------------------------------------------------------------------
def send_bulk_log_mail_for_lead_and_buffer_time(all_phone_Po_list,comm_log,text_message_list_email):
    mail_info = mail_config()
    for i,k in zip(all_phone_Po_list,text_message_list_email):
        final_message = comm_log['salutaion_email'] + k + comm_log['text_body_email'] + i[3] + comm_log['conclusion_email'] + " Reason: " + comm_log['reason'] + config['consumer_portal_url']['CUST_URL']
        print("===========================================================bulk message Mail")
        print(final_message)
        print("===========================================================bulk message Mail")
        print('----------------------')
        print(i)
        print('----------------------')
        print(i[2])
        message = Mail(
        from_email=config['Sendgrid']['FROM_MAIL'],
        to_emails=i[2],
        subject=comm_log['subject_email'],
        html_content = final_message)
        try:
            sg = SendGridAPIClient(mail_info[0])
            response = sg.send(message)
        except Exception as e:
            print(str(e))
        else:
            print(response.status_code)
    return

def send_bulk_log_mail_for_progress_time_line_update(all_phone_Po_list,comm_log,text_message_list_email):
    mail_info = mail_config()
    for i,k in zip(all_phone_Po_list,text_message_list_email):
        final_message = k
        print("===========================================================bulk message Mail")
        print(final_message)
        print("===========================================================bulk message Mail")
        print('----------------------')
        print(i)
        print('----------------------')
        print(i[2])
        message = Mail(
        from_email=config['Sendgrid']['FROM_MAIL'],
        to_emails=i[2],
        subject=comm_log['subject_email'],
        html_content = final_message)
        try:
            sg = SendGridAPIClient(mail_info[0])
            response = sg.send(message)
        except Exception as e:
            print(str(e))
        else:
            print(response.status_code)
    return
#**********************************************************************************************************
def send_consumer_creds_by_mail(password,phone,email,user_id,first_name,org_name):
    print("INSIDE MAIL_________________")
    mail_info = mail_config()
    message = Mail(
        from_email=config['Sendgrid']['FROM_MAIL'],
        to_emails=email,
        subject="Login Credentials",
        html_content='Hello ' + first_name + ', Welcome to Nexus. Your secure credentials for ' + org_name + ' are :- User ID : ' + phone +' and Password : ' + password)
    try:
        sg = SendGridAPIClient(mail_info[0])
        response = sg.send(message)
    except Exception as e:
        print(str(e))
    else:
        print(response.status_code)
    return


#**********************************************************************************************************
def send_consumer_new_reset_creds_by_mail(password,email,org_name):
    print("INSIDE MAIL_________________")
    mail_info = mail_config()
    message = Mail(
        from_email=config['Sendgrid']['FROM_MAIL'],
        to_emails=email,
        subject="Reset Successfull",
        html_content='Welcome to Nexus. Your new password for ' + org_name + ' is ' + password + ".")
    try:
        sg = SendGridAPIClient(mail_info[0])
        response = sg.send(message)
    except Exception as e:
        print(str(e))
    else:
        print(response.status_code)
    return

#**********************************************************************************************************
def send_consumer_welcome_note_by_mail(email,communication_Info_Email):
    print("INSIDE MAIL_________________----------Inside welcome note send email")
    mail_info = mail_config()
    message = Mail(
        from_email=config['Sendgrid']['FROM_MAIL'],
        to_emails=email,
        subject=communication_Info_Email['subject'],
        html_content=communication_Info_Email['message_plain_text'])
    try:
        sg = SendGridAPIClient(mail_info[0])
        response = sg.send(message)
    except Exception as e:
        print(str(e))
    else:
        print(response.status_code)
    return

#================================================================================================

def send_custom_test_email_to_dealer(email,subject,text_message):
    print("INSIDE MAIL_________________----------Inside")
    mail_info = mail_config()
    message = Mail(
        from_email=config['Sendgrid']['FROM_MAIL'],
        to_emails=email,
        subject=subject,
        html_content=text_message)
    try:
        sg = SendGridAPIClient(mail_info[0])
        response = sg.send(message)
    except Exception as e:
        print(str(e))
    else:
        print(response.status_code)
    return



