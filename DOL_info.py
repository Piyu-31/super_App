from flask import request
from passlib.hash import sha256_crypt
import random
import string
import datetime
import time
from datetime import datetime
from datetime import timedelta,date
from datetime import date
from flask import session

def generate_id(letters_count, digits_count):
  sample_str = ''.join((random.choice(string.ascii_letters) for i in range(letters_count)))
  sample_str += ''.join((random.choice(string.digits) for i in range(digits_count)))
  sample_list = list(sample_str)
  final_string = ''.join(sample_list)
  return final_string


#----------------------------------------------------------------------------------------------------------


def setWF_OrderData():
  WF_OrderInfo = {}
  nexus_id = generate_id(4,2)
  consumer_id = generate_id(4,2)
  po_number = request.form['po_no']
  
  order_date = request.form['or_date']
  #date_object = datetime.strptime(order_date,'%Y-%m-%d')
  #datetime_object = date_object.date()
  datetime_object = datetime.strptime(order_date,'%Y-%m-%d')

  new_date = datetime_object.strftime("%m-%d-%Y")

  #now = datetime.today().strftime('%Y-%m-%d')
  now = datetime.today()

  new_now = now.strftime("%m-%d-%Y")

  delta = now - datetime_object

  delta_object_today = delta.days
  
  order_price = request.form['or_price']
  order_cost = request.form['or_cost']
  model = request.form['mdl']
  size = request.form['siz']
  user_type = request.form['user_type']
  consumer_first_name = request.form['co_fname']
  consumer_last_name =  request.form['co_lname']
  address = request.form['address']
  city = request.form['ci_ty']
  consumer_mobile_number = request.form['co_mo_num']
  consumer_email = request.form['co_email']
  brand = request.form['br_and']
  job_name = request.form['j_name']
  order_notes = request.form['o_notes']
  consumer_zip_code = request.form['zip_code']
  #Country selection
  cntry = 'checkbox'
  cntry1, cntry2 = False, False
  if request.form.get('country_1'):
    cntry = "Canada"
  elif request.form.get('country_2'):
    cntry = "US"  

  Country = cntry
  
  state = ''
  if cntry == "Canada":
    state = request.form['ca_States']
  elif cntry == "US":
    state = request.form['us_States']

  State = state
  cntry = 'checkbox'
  cntry1, cntry2 = False, False
  if request.form.get('country_1'):
    cntry = "Canada"
  elif request.form.get('country_2'):
    cntry = "US"  

  Country = cntry
  
  state = ''
  if cntry == "Canada":
    state = request.form['ca_States']
  elif cntry == "US":
    state = request.form['us_States']

  State = state

  
  total_lead_time = request.form['totl_lt']
  lead_time_int = int(total_lead_time)
  lead_time_weeks_to_days = lead_time_int*7
  lead_time_in_days = timedelta(days=lead_time_weeks_to_days)
  

  dealer_buffer_time = request.form['delr_bfr_tm']
  buffer_time_int = int(dealer_buffer_time)
  buffer_time_weeks_to_days = buffer_time_int*7
  buffer_time_in_days = timedelta(days=buffer_time_weeks_to_days)

  est_deliver_time = datetime_object + lead_time_in_days + buffer_time_in_days

  est_deliver_time_date = str(est_deliver_time.date())


  est_deliver_time_date_time_object = datetime.strptime(est_deliver_time_date,'%Y-%m-%d')
  new_est_deliver_time_date_time_object_date = est_deliver_time_date_time_object.strftime("%m-%d-%Y")
  
  est_deliver_time_today_raw = (((lead_time_weeks_to_days + buffer_time_weeks_to_days) - delta_object_today)/(lead_time_weeks_to_days + buffer_time_weeks_to_days))*100
  est_deliver_time_today = round((((lead_time_weeks_to_days + buffer_time_weeks_to_days) - delta_object_today)/(lead_time_weeks_to_days + buffer_time_weeks_to_days))*100)





  #set data to the Empty list
  WF_OrderInfo["nexus_id"]=nexus_id.strip()
  WF_OrderInfo["po_number"]=po_number.strip()
  WF_OrderInfo["order_date"]=new_date.strip()
  WF_OrderInfo["order_price"]=order_price.strip()
  WF_OrderInfo["order_cost"]=order_cost.strip()
  WF_OrderInfo["model"]=model.strip()
  WF_OrderInfo["size"]=size.strip()
  WF_OrderInfo["user_type"]=user_type.strip()
  WF_OrderInfo["relationship_number"]=consumer_id.strip()
  WF_OrderInfo["job_name"]=job_name.strip()
  WF_OrderInfo["consumer_first_name"]=consumer_first_name.strip()
  WF_OrderInfo["consumer_last_name"]=consumer_last_name.strip()
  WF_OrderInfo["consumer_mobile_number"]=consumer_mobile_number.strip()
  WF_OrderInfo["consumer_email"] = consumer_email.strip()
  WF_OrderInfo["consumer_date_of_birth"] = ''.strip()
  WF_OrderInfo["country"]=Country.strip()
  WF_OrderInfo["state"]=State.strip()
  WF_OrderInfo["address"]=address.strip()
  WF_OrderInfo["city"]=city.strip()
  WF_OrderInfo["consumer_zip_code"]=consumer_zip_code.strip()
  WF_OrderInfo["dealer_id"] = session['orgId_retailer']
  WF_OrderInfo["dealer_name"] = session['fullname_retailer']
  WF_OrderInfo["dealer_phone"] = "9799857341".strip()
  WF_OrderInfo["dealer_email"] = "souravmohanty0077@gmail.com".strip()
  WF_OrderInfo["brand"] = brand.strip()
  WF_OrderInfo["total_lead_time"] = total_lead_time
  WF_OrderInfo["dealer_buffer_time"] = dealer_buffer_time
  WF_OrderInfo["est_deliver_time"] = new_est_deliver_time_date_time_object_date
  WF_OrderInfo["lead_time_parameter"]=""
  WF_OrderInfo["lead_time_reason"]=""
  WF_OrderInfo["buffer_time_parameter"]=""
  WF_OrderInfo["buffer_time_reason"]=""
  WF_OrderInfo["progress_timeline"]=""
  WF_OrderInfo['progress_stage_number'] = ""
  WF_OrderInfo["preference_reply_back"]="Email N SMS"
  WF_OrderInfo["order_notes"]=order_notes.strip()
  WF_OrderInfo["last_activity"]="".strip()
  WF_OrderInfo["order_completion_date"]="".strip()
  WF_OrderInfo["data_source"]="Nexus"
  return WF_OrderInfo


def setKeyFields():
    key_records = {}
    
    key_records["order_id"] = 'True'
    key_records["po_number"] = 'True'
    key_records["order_date"] = 'True'
    key_records["work_flow_name"] = 'True'
    key_records["order_value"] = 'True'
    key_records["order_cost"] = 'True'
    key_records["model"] = 'True'
    key_records["size"] = 'True'
    key_records["user_type"] = 'True'
    key_records["job_name"] = 'True'
    key_records["consumer_first_name"] = 'True'
    key_records["consumer_last_name"] = 'True'
    key_records["consumer_mobile_number"] = 'True'
    key_records["consumer_email"] = 'True'
    key_records["country"] = 'True'
    key_records["state"] = 'True'
    key_records["address"] = 'True'
    key_records["city"] = 'True'
    key_records["dealer_id"] = session['orgId_retailer']
    key_records["brand"] = 'True'
    key_records["total_lead_time"] = 'True'
    key_records["dealer_buffer_time"] = 'True'
    key_records["est_deliver_time"] = 'True'
    key_records["lead_time_parameter"] = 'True'
    key_records["buffer_time_parameter"] = 'True'
    key_records["progress_timeline"] = 'True'
    key_records["preference_reply_back"] = 'True'
    key_records["order_notes"] = 'True'

    return key_records


def set_VendorData():
  vendor_info = {}
  vendor_id = generate_id(4,2)

  vendor_name = request.form['v_name']
  vendor_industry = request.form['v_inds']
  vendor_address = request.form['v_addrs']
  vendor_contact_name = request.form['v_cname']
  vendor_contact_number = request.form['v_cnumber']
  vendor_email_ids = request.form['v_email']
  vendor_country = request.form['v_con']
  vendor_city = request.form['v_city']
  vendor_zip_code = request.form['v_zip']
  vedor_description = request.form['v_desc']

  vendor_info['vendor_id'] = vendor_id.strip()
  vendor_info['vendor_name'] = vendor_name.strip()
  vendor_info['vendor_industry'] = vendor_industry.strip()
  vendor_info['vendor_address'] = vendor_address.strip()
  vendor_info['vendor_contact_name'] = vendor_contact_name.strip()
  vendor_info['vendor_contact_number'] = vendor_contact_number.strip()
  vendor_info['vendor_email_ids'] = vendor_email_ids.strip()
  vendor_info['vendor_country'] = vendor_country.strip()
  vendor_info['vendor_city'] = vendor_city.strip()
  vendor_info['vendor_zip_code'] = vendor_zip_code.strip()
  vendor_info['vendor_description'] = vedor_description.strip()

  return vendor_info


def set_ConsumerData():
  consumer_info = {}
  consumer_id = generate_id(4,2)

  consumer_first_name = request.form['c_fname']
  consumer_last_name = request.form['c_lname']
  consumer_mobile_number = request.form['c_mobile']
  consumer_email = request.form['c_email']
  consumer_date_of_birth = request.form['c_dob']
  consumer_address = request.form['c_addrs']
  consumer_city = request.form['c_city']
  consumer_country = request.form['c_con']
  consumer_state = request.form['c_state']
  consumer_zip_code = request.form['c_zip_code']
  user_type = request.form['c_user_type']

  currentDT = datetime.today()
  current_welcome_datetime = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")
  welcome_datetime = current_welcome_datetime
  cons_datetime = current_welcome_datetime

  consumer_info['consumer_id'] = consumer_id.strip()
  consumer_info['consumer_first_name'] = consumer_first_name.strip()
  consumer_info['consumer_last_name'] = consumer_last_name.strip()
  consumer_info['consumer_mobile_number'] = consumer_mobile_number.strip()
  consumer_info['consumer_email'] = consumer_email.strip()
  consumer_info['consumer_date_of_birth'] = consumer_date_of_birth.strip()
  consumer_info['consumer_address'] = consumer_address.strip()
  consumer_info['consumer_city'] = consumer_city.strip()
  consumer_info['consumer_country'] = consumer_country.strip()
  consumer_info['consumer_state'] = consumer_state.strip()
  consumer_info["consumer_zip_code"] = consumer_zip_code.strip()
  consumer_info['user_type'] = user_type.strip()
  consumer_info['welcome_email'] = False
  consumer_info['welcome_email_datetime'] = welcome_datetime
  consumer_info['consumer_origin'] = "Manual Entry"
  consumer_info['receive_mail_notification'] = True
  consumer_info['receive_sms_notification'] = True
  consumer_info['nexus_upload'] = "Nexus"
  consumer_info['consumer_datetime'] = cons_datetime
  return consumer_info

def set_ContractorData():
  contractor_info = {}
  contractor_id = generate_id(4,2)

  contractor_first_name = request.form['cont_fname']
  contractor_last_name = request.form['cont_lname']
  contractor_mobile_number = request.form['cont_mobile']
  contractor_email = request.form['cont_email']
  contractor_address = request.form['cont_addrs']
  contractor_city = request.form['cont_city']
  contractor_country = request.form['cont_con']
  contractor_state = request.form['cont_state']
  contractor_zip_code = request.form['cont_zip']

  contractor_info['contractor_id'] = contractor_id.strip()
  contractor_info['contractor_first_name'] = contractor_first_name.strip()
  contractor_info['contractor_last_name'] = contractor_last_name.strip()
  contractor_info['contractor_mobile_number'] = contractor_mobile_number.strip()
  contractor_info['contractor_email'] = contractor_email.strip()
  contractor_info['contractor_address'] = contractor_address.strip()
  contractor_info['contractor_city'] = contractor_city.strip()
  contractor_info['contractor_country'] = contractor_country.strip()
  contractor_info['contractor_state'] = contractor_state.strip()
  contractor_info['contractor_zip_code'] = contractor_zip_code.strip()

  return contractor_info














