from pymongo import MongoClient
import certifi
import datetime
import sys

from bson.objectid import ObjectId

from configparser import ConfigParser
import configparser

from flask import session

config = configparser.ConfigParser()
config.read('config.ini')

global con_order
global db_order
global col_logs
global col_del_logs
global col_consumer_sms_delvery_logs
global col_work_flow_unit
global col_work_Flow_order
global con_login
global db_login
global col_login
global col_login_consumer
global emp_keys
global col_review_info
global col_vendor_data
global col_consumer_data
global col_contractors_data
global col_cstm_msgs
global col_review_links_info


def connect_order_db():
  global con_order
  global db_order
  global col_logs
  global col_del_logs
  global col_consumer_sms_delvery_logs
  global col_work_flow_unit
  global col_work_Flow_order
  global emp_keys
  global col_review_info
  global col_vendor_data
  global col_consumer_data
  global col_contractors_data
  global col_cstm_msgs
  global col_review_links_info

  retailer_dbs = session['orgId_retailer']
  ca = certifi.where()
  con_order = MongoClient('mongodb+srv://'+
                        config['database']['USERNAME']+':'+
                        config['database']['PASSWORD']+'@'+
                        config['database']['HOST']+'/'
                        +retailer_dbs+
                        '?retryWrites=true&w=majority',tlsCAFile = ca)
  
  db_order = con_order.RETAILERS_DB[retailer_dbs]
  
  col_logs = db_order.rertailers_logbooks
  col_del_logs = db_order.retailers_delete_logbooks
  col_consumer_sms_delvery_logs = db_order.consumer_sms_delivery_logbook
  col_work_flow_unit = db_order.workFlow_info
  col_work_Flow_order = db_order.workFlow_Order_Info
  emp_keys = db_order.order_decision_info
  col_review_info = db_order.dealer_review
  col_vendor_data = db_order.vendor_book
  col_consumer_data = db_order.consumer_book
  col_contractors_data = db_order.contractors_book
  col_cstm_msgs = db_order.custom_order_messages
  col_review_links_info = db_order.dealer_review_links


#========================================== Work Flow Order Logs ==========================================================
def save_wforder_details(orderInfo):
  global col_work_Flow_order
  connect_order_db()
  col_work_Flow_order.insert(orderInfo)
  return "saved Successfully"

def get_wforder_details():
    global col_work_Flow_order
    connect_order_db()
    org_id = session['orgId_retailer']
    orderdata_from_db = col_work_Flow_order.find({"dealer_id": str(org_id)},{"_id":0})
    return orderdata_from_db

def get_wforder_count():
    global col_work_Flow_order
    connect_order_db()
    org_id = session['orgId_retailer']
    orderdata_from_db = col_work_Flow_order.find({"dealer_id": str(org_id)},{"_id":0}).count()
    return orderdata_from_db

def get_wforder_details_paginated(pageNum, recordsPerPage):
    global col_work_Flow_order
    connect_order_db()
    org_id = session['orgId_retailer']
    page_no = pageNum
    rec_per_page = recordsPerPage
    count_orders = col_work_Flow_order.count()
    total_pages = (count_orders + rec_per_page - 1)//rec_per_page
    orderdata_from_db = col_work_Flow_order.find({"dealer_id": str(org_id)},{"_id":0}).skip(page_no*rec_per_page).limit(rec_per_page)
    return [orderdata_from_db,rec_per_page,count_orders,total_pages]

def get_one_wforder_detail(nid):
  global col_work_Flow_order
  connect_order_db()
  orderr_data = col_work_Flow_order.find({"nexus_id": str(nid)},{"_id":0})
  return orderr_data

def get_consumer_details_from_wforder_detail(nid):
  global col_work_Flow_order
  connect_order_db()
  orderr_data = col_work_Flow_order.find({"nexus_id": str(nid)},{"consumer_first_name":1,"consumer_last_name":1,"consumer_mobile_number":1,"consumer_email":1,"progress_timeline":1,"work_flow_name":1,"work_flow_stages":1,"_id":0})
  return orderr_data

def update_one_wforder_record(nid, order_info):
    global col_work_Flow_order
    connect_order_db()
    col_work_Flow_order.update_one({"nexus_id": str(nid)}, {'$set' :{'po_number':order_info["po_number"],
                                                   'order_price':order_info["order_price"],
                                                   'order_cost':order_info["order_cost"],
                                                   'model':order_info["model"],
                                                   'size':order_info["size"],
                                                   'user_type':order_info["user_type"],
                                                   'job_name':order_info["job_name"],
                                                   'consumer_first_name':order_info["consumer_first_name"], 
                                                   'consumer_last_name':order_info["consumer_last_name"],
                                                   'consumer_mobile_number':order_info["consumer_mobile_number"],
                                                   'consumer_email':order_info["consumer_email"],
                                                   'country':order_info['country'],
                                                   'state':order_info['state'],
                                                   'address':order_info['address'],
                                                   'city':order_info['city'],
                                                   'consumer_zip_code':order_info['consumer_zip_code'],
                                                   'brand':order_info['brand'],
                                                   'order_notes':order_info['order_notes']
                                                    } })
    return

def update_wf_leadtime_record(nid, lTime_info):
    global col_work_Flow_order
    connect_order_db()
    col_work_Flow_order.update_one({"nexus_id": str(nid)}, {'$set' :{'total_lead_time':lTime_info["total_lead_time"],
                                                    'est_deliver_time':lTime_info["est_deliver_time"],
                                                    'lead_time_parameter':lTime_info["lead_time_parameter"],
                                                    'lead_time_reason':lTime_info["lead_time_reason"]
                                                    } })
    return

def update_wf_buffertime_record(nid, bTime_info):
    global col_work_Flow_order
    connect_order_db()
    col_work_Flow_order.update_one({"nexus_id": str(nid)}, {'$set' :{'dealer_buffer_time':bTime_info["dealer_buffer_time"],
                                                    'est_deliver_time':bTime_info["est_deliver_time"],
                                                    'buffer_time_parameter':bTime_info["buffer_time_parameter"],
                                                    'buffer_time_reason':bTime_info["buffer_time_reason"]
                                                    } })
    return

def update_wf_timeline_progress(NexusId,pgrs_info):
  global col_work_Flow_order
  connect_order_db()
  print("===================================================================")
  print("NexusId:",NexusId)
  print("inside progress timeline update  ::", pgrs_info)
  print("===================================================================")
  col_work_Flow_order.update_one({"nexus_id": str(NexusId)}, {'$set' :{'progress_timeline':pgrs_info['progress_timeline'],
                                                                        'progress_stage_number':pgrs_info['progress_stage_number']  } })
  return

def update_wf_preference_replyback(NexusId,pfrnc_reply):
  global col_work_Flow_order
  connect_order_db()
  col_work_Flow_order.update_one({"nexus_id": str(NexusId)}, {'$set' :{'preference_reply_back':pfrnc_reply} })
  return


def delete_an_wf_Order(nid):
  global col_work_Flow_order
  connect_order_db()
  col_work_Flow_order.remove({"nexus_id": str(nid)})
  return "Deleted Successfully"


def get_count_of_orders_associated_by_po(po_no):
  global col_work_Flow_order
  connect_order_db()
  count_wf_orders = col_work_Flow_order.find({'po_number' : str(po_no)}, {'_id' : 0}).count()
  return count_wf_orders


def get_search_result_per_linked_po(po_no):
  global col_work_Flow_order
  connect_order_db()
  org_id = session['orgId_retailer']
  orderData = col_work_Flow_order.find({"po_number": str(po_no) }, {'_id': 0})
  return orderData


def get_search_result_per_linked_po_n_id(nid):
  global col_work_Flow_order
  connect_order_db()
  org_id = session['orgId_retailer']
  orderData = col_work_Flow_order.find({"nexus_id": str(nid) }, {'_id': 0})
  return orderData

def get_workflow_stage_from_order(wrkflw_type):
  global col_work_Flow_order
  connect_order_db()
  orderr_data = col_work_Flow_order.find({"work_flow_name": str(wrkflw_type)},{"_id":0})
  return orderr_data

def get_wforder_details_using_p(p):
  global col_work_Flow_order
  connect_order_db()
  orderr_data = col_work_Flow_order.find({"progress_timeline": str(p)},{"_id":0})
  return orderr_data

def get_wforder_count_using_o(o):
  global col_work_Flow_order
  connect_order_db()
  orderr_data = col_work_Flow_order.find({"order_completion_date": str(o)},{"_id":0})
  return orderr_data

def get_wforder_details_using_o(o):
  global col_work_Flow_order
  connect_order_db()
  orderr_data = col_work_Flow_order.find({"order_completion_date": str(o)},{"_id":0})
  return orderr_data

def get_wforder_open_orders_using_p(p):
  global col_work_Flow_order
  connect_order_db()
  orderr_data = col_work_Flow_order.find({"progress_timeline": str(p)},{"_id":0}).count()
  return orderr_data

# def get_wforder_open_orders_using_p_data(p):
#   global col_work_Flow_order
#   connect_order_db()
#   orderr_data = col_work_Flow_order.find({"progress_timeline": str(p)},{"_id":0})
#   return orderr_data


def update_last_activity_of_an_order_change(nx_id,last_activity):
    global col_work_Flow_order
    connect_order_db()
    col_work_Flow_order.update_one({"nexus_id": str(nx_id)}, {'$set' :{'last_activity':last_activity} })
    return

def update_submitted_date_of_an_order(NexusId,order_submitted_date):
    global col_work_Flow_order
    connect_order_db()
    print("--------------------inside update")
    col_work_Flow_order.update_one({"nexus_id": str(NexusId)}, {'$set' :{'order_completion_date':order_submitted_date} })
    return

def get_wforder_details_using_todays_date(dt):
    global col_work_Flow_order
    connect_order_db()
    orderr_data = col_work_Flow_order.find({"order_completion_date": str(dt)}, {"_id":0})
    return orderr_data

def get_wforder_details_using_current_month(cur_mon):
    global col_work_Flow_order
    connect_order_db()
    orderr_data_from_db = col_work_Flow_order.find({"order_completion_date":{"$regex":(str(cur_mon))}})
    return orderr_data_from_db

def get_wforder_details_using_current_year(cur_year):
    global col_work_Flow_order
    connect_order_db()
    orderr_data_from_db = col_work_Flow_order.find({"order_completion_date":{"$regex":(str(cur_year))}})
    return orderr_data_from_db

def get_wforder_details_todays_date(or_date):
    global col_work_Flow_order
    connect_order_db()
    orderr_data_from_db = col_work_Flow_order.find({"order_date":str(or_date)})
    return orderr_data_from_db

def get_wforder_details_todays_date_count(or_date):
    global col_work_Flow_order
    connect_order_db()
    orderr_data_from_db = col_work_Flow_order.find({"order_date":str(or_date)}).count()
    return orderr_data_from_db





#------------------------------------------------Reviews and Feedbacks---------------------------------------------------------



#============================================Vendor Book==============================================================

def save_vendor_informaton(vendor_Data):
  global col_vendor_data
  connect_order_db()
  col_vendor_data.insert(vendor_Data)
  return "Saved!!"

def get_vendor_data():
  global col_vendor_data
  connect_order_db()
  v_Data = col_vendor_data.find({},{'_id':0})
  return v_Data

def get_vendor_info_by_v_id(v_id):
  global col_vendor_data
  connect_order_db()
  v_Data = col_vendor_data.find({"vendor_id" : str(v_id)},{'_id':0})
  return v_Data


def update_vendor_data(v_id,v_disc):
  global col_vendor_data
  connect_order_db()
  col_vendor_data.update_one({"vendor_id": str(v_id)}, {'$set' :{'vendor_name':v_disc['vendor_name'],
                                                                'vendor_industry':v_disc['vendor_industry'],
                                                                'vendor_address':v_disc['vendor_address'],
                                                                'vendor_contact_name':v_disc['vendor_contact_name'],
                                                                'vendor_contact_number':v_disc['vendor_contact_number'],
                                                                'vendor_email_ids':v_disc['vendor_email_ids'],
                                                                'vendor_country':v_disc['vendor_country'],
                                                                'vendor_city':v_disc['vendor_city'],
                                                                'vendor_zip_code':v_disc['vendor_zip_code'],
                                                                'vendor_description':v_disc['vendor_description']  }})
  return

def delete_a_vendor(v_id):
  global col_vendor_data
  connect_order_db()
  col_vendor_data.remove({"vendor_id": str(v_id)})
  return "Deleted Successfully"


#============================================Consumers Book==============================================================

def save_consumer_informaton(consumer_Data):
  global col_consumer_data
  connect_order_db()
  col_consumer_data.insert(consumer_Data)
  return "Saved!!"

def get_consumer_data():
  global col_consumer_data
  connect_order_db()
  consumer_data = col_consumer_data.find({},{'_id':0})
  return consumer_data

def get_consumer_data_by_phone(mobile_num):
  global col_consumer_data
  connect_order_db()
  consumer_data = col_consumer_data.find({"consumer_mobile_number":str(mobile_num)},{'_id':0})
  return consumer_data

def get_consumer_info_by_c_id(c_id):
  global col_consumer_data
  connect_order_db()
  consumer_data = col_consumer_data.find({"consumer_id" : str(c_id)},{'_id':0})
  return consumer_data

def get_consumer_info_by_ph_num(ph_num):
  global col_consumer_data
  connect_order_db()
  consumer_data = col_consumer_data.find({"consumer_mobile_number" : str(ph_num)},{'_id':0})
  return consumer_data



def update_consumer_data(c_id,c_disc):
  global col_consumer_data
  connect_order_db()
  col_consumer_data.update_one({"consumer_id": str(c_id)}, {'$set' :{'consumer_first_name':c_disc['consumer_first_name'],
                                                                'consumer_last_name':c_disc['consumer_last_name'],
                                                                'consumer_mobile_number':c_disc['consumer_mobile_number'],
                                                                'consumer_email':c_disc['consumer_email'],
                                                                'consumer_date_of_birth':c_disc['consumer_date_of_birth'],
                                                                'consumer_address':c_disc['consumer_address'],
                                                                'consumer_city':c_disc['consumer_city'],
                                                                'consumer_country':c_disc['consumer_country'],
                                                                'consumer_state':c_disc['consumer_state'],
                                                                'consumer_zip_code':c_disc['consumer_zip_code'],
                                                                'user_type':c_disc['user_type']
                                                                  }})
  return

def delete_a_consumer(c_id,ph_num):
  global col_consumer_data
  connect_order_db()
  col_consumer_data.remove( {'$and': [{"consumer_id" : str(c_id) },{"consumer_mobile_number" : str(ph_num)} ]},{"_id":0})
  return "Deleted Successfully"








#============================================contractors Book==============================================================

def save_contractors_information(contractors_data):
  global col_contractors_data
  connect_order_db()
  col_contractors_data.insert(contractors_data)
  return "Saved!!"

def get_contractors_data():
  global col_contractors_data
  connect_order_db()
  v_Data = col_contractors_data.find({},{'_id':0})
  return v_Data

def get_contractors_info_by_cont_id(cont_id):
  global col_contractors_data
  connect_order_db()
  v_Data = col_contractors_data.find({"contractor_id" : str(cont_id)},{'_id':0})
  return v_Data


def update_contractors_data(cont_id,cont_disc):
  global col_contractors_data
  connect_order_db()
  col_contractors_data.update_one({"contractor_id": str(cont_id)}, {'$set' :{'contractor_first_name':cont_disc['contractor_first_name'],
                                                                'contractor_last_name':cont_disc['contractor_last_name'],
                                                                'contractor_mobile_number':cont_disc['contractor_mobile_number'],
                                                                'contractor_email':cont_disc['contractor_email'],
                                                                'contractor_address':cont_disc['contractor_address'],
                                                                'contractor_city':cont_disc['contractor_city'],
                                                                'contractor_country':cont_disc['contractor_country'],
                                                                'contractor_state':cont_disc['contractor_state'],
                                                                'contractor_zip_code':cont_disc['contractor_zip_code']  }})
  return

def delete_a_contractor(cont_id):
  global col_contractors_data
  connect_order_db()
  col_contractors_data.remove({"contractor_id": str(cont_id)})
  return "Deleted Successfully"

#===================================Search==============================================================


def search_by_po_number(search_term, pagenum, records_pages):
  global col_order
  connect_order_db()
  org_id = session['orgId_retailer']
  page_no = pagenum
  rec_per_page = records_pages
  count_dolUser = col_order.count({'po_number':str(search_term)})
  total_pages = (count_dolUser + rec_per_page - 1)//rec_per_page
  searched_data = col_order.find({"dealer_id":str(org_id),'po_number':str(search_term)},{"_id":0}).skip(page_no*rec_per_page).limit(rec_per_page)
  return [searched_data, rec_per_page, count_dolUser, total_pages]

def search_by_city(search_term, pagenum, records_pages):
  global col_order
  connect_order_db()
  org_id = session['orgId_retailer']
  page_no = pagenum
  rec_per_page = records_pages
  count_dolUser = col_order.count({'city':str(search_term)})
  total_pages = (count_dolUser + rec_per_page - 1)//rec_per_page
  searched_data = col_order.find({'city':str(search_term)},{"_id":0}).skip(page_no*rec_per_page).limit(rec_per_page)
  return [searched_data, rec_per_page, count_dolUser, total_pages]

def search_by_state(search_term, pagenum, records_pages):
  global col_order
  connect_order_db()
  org_id = session['orgId_retailer']
  page_no = pagenum
  rec_per_page = records_pages
  count_dolUser = col_order.count({'state':str(search_term)})
  total_pages = (count_dolUser + rec_per_page - 1)//rec_per_page
  searched_data = col_order.find({'state':str(search_term)},{"_id":0}).skip(page_no*rec_per_page).limit(rec_per_page)
  return [searched_data, rec_per_page, count_dolUser, total_pages]


def search_by_order_type(search_term, pagenum, records_pages):
  global col_order
  connect_order_db()
  org_id = session['orgId_retailer']
  page_no = pagenum
  rec_per_page = records_pages
  count_dolUser = col_order.count({'order_type':str(search_term)})
  total_pages = (count_dolUser + rec_per_page - 1)//rec_per_page
  searched_data = col_order.find({'order_type':str(search_term)},{"_id":0}).skip(page_no*rec_per_page).limit(rec_per_page)
  return [searched_data, rec_per_page, count_dolUser, total_pages]
#----------------------------------------------------vendor Search------------------------------------------------------------------------

def search_by_v_name(search_term, pagenum, records_pages):
  global col_vendor_data
  connect_order_db()
  org_id = session['orgId_retailer']
  page_no = pagenum
  rec_per_page = records_pages
  count_User = col_vendor_data.count({'vendor_name':str(search_term)})
  total_pages = (count_User + rec_per_page - 1)//rec_per_page
  searched_data = col_vendor_data.find({'vendor_name':str(search_term)},{"_id":0}).skip(page_no*rec_per_page).limit(rec_per_page)
  return [searched_data, rec_per_page, count_User, total_pages]


def search_by_con_name(search_term, pagenum, records_pages):
  global col_vendor_data
  connect_order_db()
  org_id = session['orgId_retailer']
  page_no = pagenum
  rec_per_page = records_pages
  count_Usermnum = col_vendor_data.count({'vendor_contact_name':str(search_term)})
  total_pages = (count_Usermnum + rec_per_page - 1)//rec_per_page
  searched_data = col_vendor_data.find({'vendor_contact_name':str(search_term)},{"_id":0}).skip(page_no*rec_per_page).limit(rec_per_page)
  return [searched_data, rec_per_page, count_Usermnum, total_pages]


def search_by_con_number(search_term, pagenum, records_pages):
  global col_vendor_data
  connect_order_db()
  org_id = session['orgId_retailer']
  page_no = pagenum
  rec_per_page = records_pages
  count_city = col_vendor_data.count({'vendor_contact_number':str(search_term)})
  total_pages = (count_city + rec_per_page - 1)//rec_per_page
  searched_data = col_vendor_data.find({'vendor_contact_number':str(search_term)},{"_id":0}).skip(page_no*rec_per_page).limit(rec_per_page)
  return [searched_data, rec_per_page, count_city, total_pages]

def search_by_v_city(search_term, pagenum, records_pages):
  global col_vendor_data
  connect_order_db()
  org_id = session['orgId_retailer']
  page_no = pagenum
  rec_per_page = records_pages
  count_state = col_vendor_data.count({'vendor_city':str(search_term)})
  total_pages = (count_state + rec_per_page - 1)//rec_per_page
  searched_data = col_vendor_data.find({'vendor_city':str(search_term)},{"_id":0}).skip(page_no*rec_per_page).limit(rec_per_page)
  return [searched_data, rec_per_page, count_state, total_pages]

#----------------------------------------------------Consumer Search------------------------------------------------------------------------

def search_by_c_first_name(search_term, pagenum, records_pages):
  global col_consumer_data
  connect_order_db()
  org_id = session['orgId_retailer']
  page_no = pagenum
  rec_per_page = records_pages
  count_User = col_consumer_data.count({'consumer_first_name':str(search_term)})
  total_pages = (count_User + rec_per_page - 1)//rec_per_page
  searched_data = col_consumer_data.find({'consumer_first_name':str(search_term)},{"_id":0}).skip(page_no*rec_per_page).limit(rec_per_page)
  return [searched_data, rec_per_page, count_User, total_pages]


def search_by_mob_number(search_term, pagenum, records_pages):
  global col_consumer_data
  connect_order_db()
  org_id = session['orgId_retailer']
  page_no = pagenum
  rec_per_page = records_pages
  count_Usermnum = col_consumer_data.count({'consumer_mobile_number':str(search_term)})
  total_pages = (count_Usermnum + rec_per_page - 1)//rec_per_page
  searched_data = col_consumer_data.find({'consumer_mobile_number':str(search_term)},{"_id":0}).skip(page_no*rec_per_page).limit(rec_per_page)
  return [searched_data, rec_per_page, count_Usermnum, total_pages]


def search_by_c_city(search_term, pagenum, records_pages):
  global col_consumer_data
  connect_order_db()
  org_id = session['orgId_retailer']
  page_no = pagenum
  rec_per_page = records_pages
  count_city = col_consumer_data.count({'consumer_city':str(search_term)})
  total_pages = (count_city + rec_per_page - 1)//rec_per_page
  searched_data = col_consumer_data.find({'consumer_city':str(search_term)},{"_id":0}).skip(page_no*rec_per_page).limit(rec_per_page)
  return [searched_data, rec_per_page, count_city, total_pages]

def search_by_c_state(search_term, pagenum, records_pages):
  global col_consumer_data
  connect_order_db()
  org_id = session['orgId_retailer']
  page_no = pagenum
  rec_per_page = records_pages
  count_state = col_consumer_data.count({'consumer_state':str(search_term)})
  total_pages = (count_state + rec_per_page - 1)//rec_per_page
  searched_data = col_consumer_data.find({'consumer_state':str(search_term)},{"_id":0}).skip(page_no*rec_per_page).limit(rec_per_page)
  return [searched_data, rec_per_page, count_state, total_pages]


#----------------------------------------------------Contractor Search------------------------------------------------------------------------

def search_by_cont_first_name(search_term, pagenum, records_pages):
  global col_contractors_data
  connect_order_db()
  org_id = session['orgId_retailer']
  page_no = pagenum
  rec_per_page = records_pages
  count_User = col_contractors_data.count({'contractor_first_name':str(search_term)})
  total_pages = (count_User + rec_per_page - 1)//rec_per_page
  searched_data = col_contractors_data.find({'contractor_first_name':str(search_term)},{"_id":0}).skip(page_no*rec_per_page).limit(rec_per_page)
  return [searched_data, rec_per_page, count_User, total_pages]


def search_by_cont_mob_number(search_term, pagenum, records_pages):
  global col_contractors_data
  connect_order_db()
  org_id = session['orgId_retailer']
  page_no = pagenum
  rec_per_page = records_pages
  count_Usermnum = col_contractors_data.count({'contractor_mobile_number':str(search_term)})
  total_pages = (count_Usermnum + rec_per_page - 1)//rec_per_page
  searched_data = col_contractors_data.find({'contractor_mobile_number':str(search_term)},{"_id":0}).skip(page_no*rec_per_page).limit(rec_per_page)
  return [searched_data, rec_per_page, count_Usermnum, total_pages]


def search_by_cont_city(search_term, pagenum, records_pages):
  global col_contractors_data
  connect_order_db()
  org_id = session['orgId_retailer']
  page_no = pagenum
  rec_per_page = records_pages
  count_city = col_contractors_data.count({'contractor_city':str(search_term)})
  total_pages = (count_city + rec_per_page - 1)//rec_per_page
  searched_data = col_contractors_data.find({'contractor_city':str(search_term)},{"_id":0}).skip(page_no*rec_per_page).limit(rec_per_page)
  return [searched_data, rec_per_page, count_city, total_pages]

def search_by_cont_state(search_term, pagenum, records_pages):
  global col_contractors_data
  connect_order_db()
  org_id = session['orgId_retailer']
  page_no = pagenum
  rec_per_page = records_pages
  count_state = col_contractors_data.count({'contractor_state':str(search_term)})
  total_pages = (count_state + rec_per_page - 1)//rec_per_page
  searched_data = col_contractors_data.find({'contractor_state':str(search_term)},{"_id":0}).skip(page_no*rec_per_page).limit(rec_per_page)
  return [searched_data, rec_per_page, count_state, total_pages]


#===================================Work flow Search==============================================================
def search_by_job_name(search_term, pagenum, records_pages):
  global col_work_Flow_order
  connect_order_db()
  org_id = session['orgId_retailer']
  page_no = pagenum
  rec_per_page = records_pages
  count_dolUser = col_work_Flow_order.count({'job_name':str(search_term)})
  total_pages = (count_dolUser + rec_per_page - 1)//rec_per_page
  searched_data = col_work_Flow_order.find({"dealer_id":str(org_id),'job_name':str(search_term)},{"_id":0}).skip(page_no*rec_per_page).limit(rec_per_page)
  return [searched_data, rec_per_page, count_dolUser, total_pages]

def search_by_cons_first_name(search_term, pagenum, records_pages):
  global col_work_Flow_order
  connect_order_db()
  org_id = session['orgId_retailer']
  page_no = pagenum
  rec_per_page = records_pages
  count_dolUser = col_work_Flow_order.count({'consumer_first_name':str(search_term)})
  total_pages = (count_dolUser + rec_per_page - 1)//rec_per_page
  searched_data = col_work_Flow_order.find({"dealer_id":str(org_id),'consumer_first_name':str(search_term)},{"_id":0}).skip(page_no*rec_per_page).limit(rec_per_page)
  return [searched_data, rec_per_page, count_dolUser, total_pages]

def search_by_cons_last_name(search_term, pagenum, records_pages):
  global col_work_Flow_order
  connect_order_db()
  org_id = session['orgId_retailer']
  page_no = pagenum
  rec_per_page = records_pages
  count_dolUser = col_work_Flow_order.count({'consumer_last_name':str(search_term)})
  total_pages = (count_dolUser + rec_per_page - 1)//rec_per_page
  searched_data = col_work_Flow_order.find({"dealer_id":str(org_id),'consumer_last_name':str(search_term)},{"_id":0}).skip(page_no*rec_per_page).limit(rec_per_page)
  return [searched_data, rec_per_page, count_dolUser, total_pages]

def search_by_WFpo_number(search_term, pagenum, records_pages):
  global col_work_Flow_order
  connect_order_db()
  org_id = session['orgId_retailer']
  page_no = pagenum
  rec_per_page = records_pages
  count_dolUser = col_work_Flow_order.count({'po_number':str(search_term)})
  total_pages = (count_dolUser + rec_per_page - 1)//rec_per_page
  searched_data = col_work_Flow_order.find({"dealer_id":str(org_id),'po_number':str(search_term)},{"_id":0}).skip(page_no*rec_per_page).limit(rec_per_page)
  return [searched_data, rec_per_page, count_dolUser, total_pages]

def search_by_WFcity(search_term, pagenum, records_pages):
  global col_work_Flow_order
  connect_order_db()
  org_id = session['orgId_retailer']
  page_no = pagenum
  rec_per_page = records_pages
  count_dolUser = col_work_Flow_order.count({'city':str(search_term)})
  total_pages = (count_dolUser + rec_per_page - 1)//rec_per_page
  searched_data = col_work_Flow_order.find({'city':str(search_term)},{"_id":0}).skip(page_no*rec_per_page).limit(rec_per_page)
  return [searched_data, rec_per_page, count_dolUser, total_pages]

def search_by_WFstate(search_term, pagenum, records_pages):
  global col_work_Flow_order
  connect_order_db()
  org_id = session['orgId_retailer']
  page_no = pagenum
  rec_per_page = records_pages
  count_dolUser = col_work_Flow_order.count({'state':str(search_term)})
  total_pages = (count_dolUser + rec_per_page - 1)//rec_per_page
  searched_data = col_work_Flow_order.find({'state':str(search_term)},{"_id":0}).skip(page_no*rec_per_page).limit(rec_per_page)
  return [searched_data, rec_per_page, count_dolUser, total_pages]


def search_by_WF_type(search_term, pagenum, records_pages):
  global col_work_Flow_order
  connect_order_db()
  print(search_term)
  org_id = session['orgId_retailer']
  page_no = pagenum
  rec_per_page = records_pages
  count_dolUser = col_work_Flow_order.count({'work_flow_name':str(search_term)})
  total_pages = (count_dolUser + rec_per_page - 1)//rec_per_page
  searched_data = col_work_Flow_order.find({'work_flow_name':str(search_term)},{"_id":0}).skip(page_no*rec_per_page).limit(rec_per_page)
  return [searched_data, rec_per_page, count_dolUser, total_pages]

#======================================Communication=Logs===============================================================


def save_communication_logs(communication_Info):
  global col_logs
  connect_order_db()
  col_logs.insert(communication_Info)
  return "saved successfully!!"

def get_all_logs_of_consumer_type(year,month,to_date):
  global col_logs
  connect_order_db()
  logs_from_db = col_logs.find({'$and': [{"logger_type" :'Consumer'},{"action_taken":""},{"current_log_datetime": {"$regex":(str(year + "\s" + month + "\s" + to_date))}}] },{"_id":0})
  return logs_from_db

def get_all_logs_info_of_consumer_type():
  global col_logs
  connect_order_db()
  logs_from_db = col_logs.find({'$and': [{"logger_type" :'Consumer'},{"action_taken":""}] },{"_id":0})
  return logs_from_db

def get_all_logs_of_consumer_type_for_4_days(year,month,to_date,yest_date,day_before_yest_date,day_bfr_before_yest_date):
  global col_logs
  connect_order_db()
  logs_from_db = col_logs.find({'$and': [{"logger_type" :'Consumer'},{"action_taken":""},{'$or': [{"current_log_datetime": {"$regex":(str(year + "\s" + month + "\s" + to_date))}}, {"current_log_datetime": {"$regex":(str(year + "\s" + month + "\s" + yest_date))}}, {"current_log_datetime": {"$regex":(str(year + "\s" + month + "\s" + day_before_yest_date))}}, {"current_log_datetime": {"$regex":(str(year + "\s" + month + "\s" + day_bfr_before_yest_date))}} ]}] },{"_id":0})
  return logs_from_db

def get_all_logs_of_consumer_type_for_7_days(year,month,to_date,yest_date,day_before_yest_date,day_bfr_before_yest_date,day_5_before_yest_date,day_6_before_yest_date,day_7_before_yest_date):
  global col_logs
  connect_order_db()
  logs_from_db = col_logs.find({'$and': [{"logger_type" :'Consumer'},{"action_taken":""},{'$or': [{"current_log_datetime": {"$regex":(str(year + "\s" + month + "\s" + to_date))}}, {"current_log_datetime": {"$regex":(str(year + "\s" + month + "\s" + yest_date))}}, {"current_log_datetime": {"$regex":(str(year + "\s" + month + "\s" + day_before_yest_date))}}, {"current_log_datetime": {"$regex":(str(year + "\s" + month + "\s" + day_bfr_before_yest_date))}}, {"current_log_datetime": {"$regex":(str(year + "\s" + month + "\s" + day_5_before_yest_date))}}, {"current_log_datetime": {"$regex":(str(year + "\s" + month + "\s" + day_6_before_yest_date))}},{"current_log_datetime": {"$regex":(str(year + "\s" + month + "\s" + day_7_before_yest_date))}} ]}] },{"_id":0})
  return logs_from_db


def get_all_logs_for_specific_po(n_id):
  global col_logs
  connect_order_db()
  logs_from_db = col_logs.find({"nexus_id":str(n_id)})
  return logs_from_db

def get_dealer_logs_per_month(year,month):
  global col_logs
  connect_order_db()
  print(year, month)
  logs_from_db = col_logs.find({'$and': [{"logger_type" :'Dealer'},{"current_log_datetime":{"$regex":(str(year + "\s" + month))}}] }).count()
  print("------------------------------logs_from_db")
  print(logs_from_db)
  print("===========================================")
  return logs_from_db

# def get_dealer_logs_per_month_only_mail(year,month):
#   global col_logs
#   connect_order_db()
#   logs_from_db = col_logs.find({"sending_mode":'Email'}).count()
#   return logs_from_db

def get_dealer_email_logs_per_month(year,month):
  global col_logs
  connect_order_db()
  print(year,month)
  logs_from_db = col_logs.find({'$and': [{"sending_mode" :'Email'}, {"logger_type" :'Dealer'},{"current_log_datetime":{"$regex":(str(year + "\s" + month))}}] }).count()
  return logs_from_db

def get_dealer_sms_logs_per_month(year,month):
  global col_logs
  connect_order_db()
  logs_from_db = col_logs.find({'$and': [{"sending_mode" :'SMS'},{"current_log_datetime":{"$regex":(str(year + "\s" + month))}}] }).count()
  return logs_from_db

def update_action_taken_value_for_a_consumer(act_disc,nid):
    global col_logs
    connect_order_db()
    print("inside update",nid)
    col_logs.update_many({"nexus_id": str(nid)}, {'$set' :{'action_taken':act_disc['action_taken']}})
    return

#-----------------------------------------Delete Logs------------------------------------------------
def save_delete_logs(delete_logs):
  global col_del_logs
  connect_order_db()
  col_del_logs.insert(delete_logs)
  return "deleted successfully!!"



#------------------------------------------Custom Order Messages----------------------------------------------------------
def save_custom_order_related_texts(order_entry_msg):
  global col_cstm_msgs
  connect_order_db()
  col_cstm_msgs.insert(order_entry_msg)
  return "Saved!!"


def get_custom_order_related_texts():
  global col_cstm_msgs
  connect_order_db()
  cstm_msg_data = col_cstm_msgs.find({},{"_id":0})
  return cstm_msg_data

def get_custom_order_related_texts_by_type(typ):
    global col_cstm_msgs
    connect_order_db()
    cstm_msg_data = col_cstm_msgs.find({"custom_message_type":str(typ)},{"_id":0})
    return cstm_msg_data

#==========================================================================================================================

def get_custom_order_related_texts_for_red_button_buffer_by_cst_type():
    print("---------------------------------INSIDE DB")
    print(session["bfr_cstm_type"])
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["bfr_cstm_type"]
    cstm_msg_data = col_cstm_msgs.find({"custom_message_type":str(ty_pe)},{"_id":0})
    return cstm_msg_data

def update_custom_red_button_buffertime_related_texts_by_type(order_entry_msg):
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["bfr_cstm_type"]
    col_cstm_msgs.update_one({"custom_message_type": str(ty_pe)}, {'$set' :{'create_order_text_box_1':order_entry_msg['create_order_text_box_1'],
                                                                'create_order_text_box_2':order_entry_msg['create_order_text_box_2'],
                                                                'create_order_text_box_3':order_entry_msg['create_order_text_box_3'],
                                                                'create_order_text_box_4':order_entry_msg['create_order_text_box_4'] }})
    return

#==========================================================================================================================

def get_custom_order_related_texts_for_consumer_review_by_cst_type():
    print("---------------------------------INSIDE DB")
    print(session["consumer_review_email_cstm_type"])
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["consumer_review_email_cstm_type"]
    cstm_msg_data = col_cstm_msgs.find({"custom_message_type":str(ty_pe)},{"_id":0})
    return cstm_msg_data

def update_custom_consumer_review_related_texts_by_type(order_entry_msg):
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["consumer_review_email_cstm_type"]
    col_cstm_msgs.update_one({"custom_message_type": str(ty_pe)}, {'$set' :{'create_order_text_box_1':order_entry_msg['create_order_text_box_1'],
                                                                'create_order_text_box_2':order_entry_msg['create_order_text_box_2'],
                                                                'create_order_text_box_3':order_entry_msg['create_order_text_box_3'] }})
    return

#==========================================================================================================================

def get_custom_order_related_texts_for_consumer_product_review_by_cst_type():
    print("---------------------------------INSIDE DB")
    print(session["consumer_product_review_email_cstm_type"])
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["consumer_product_review_email_cstm_type"]
    cstm_msg_data = col_cstm_msgs.find({"custom_message_type":str(ty_pe)},{"_id":0})
    return cstm_msg_data

def update_custom_consumer_product_review_related_texts_by_type(order_entry_msg):
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["consumer_product_review_email_cstm_type"]
    col_cstm_msgs.update_one({"custom_message_type": str(ty_pe)}, {'$set' :{'create_order_text_box_1':order_entry_msg['create_order_text_box_1'],
                                                                'create_order_text_box_2':order_entry_msg['create_order_text_box_2'],
                                                                'create_order_text_box_3':order_entry_msg['create_order_text_box_3'] }})
    return


#==========================================================================================================================

def get_custom_order_related_sms_for_consumer_review_by_cst_type():
    print("---------------------------------INSIDE DB")
    print(session["consumer_review_sms_cstm_type"])
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["consumer_review_sms_cstm_type"]
    cstm_msg_data = col_cstm_msgs.find({"custom_message_type":str(ty_pe)},{"_id":0})
    return cstm_msg_data

def update_custom_consumer_review_related_sms_by_type(order_entry_msg):
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["consumer_review_sms_cstm_type"]
    col_cstm_msgs.update_one({"custom_message_type": str(ty_pe)}, {'$set' :{'create_order_text_box_1':order_entry_msg['create_order_text_box_1'],
                                                                'create_order_text_box_2':order_entry_msg['create_order_text_box_2']}})
    return


#==========================================================================================================================

def get_custom_order_related_sms_for_consumer_product_review_by_cst_type():
    print("---------------------------------INSIDE DB")
    print(session["consumer_product_review_sms_cstm_type"])
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["consumer_product_review_sms_cstm_type"]
    cstm_msg_data = col_cstm_msgs.find({"custom_message_type":str(ty_pe)},{"_id":0})
    return cstm_msg_data

def update_custom_consumer_product_review_related_sms_by_type(order_entry_msg):
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["consumer_product_review_sms_cstm_type"]
    col_cstm_msgs.update_one({"custom_message_type": str(ty_pe)}, {'$set' :{'create_order_text_box_1':order_entry_msg['create_order_text_box_1'],
                                                                'create_order_text_box_2':order_entry_msg['create_order_text_box_2']}})
    return


#==========================================================================================================================

def get_custom_order_related_sms_for_red_button_buffer_by_cst_type():
    print("---------------------------------INSIDE DB")
    print(session["bfr_time_sms_cstm_type"])
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["bfr_time_sms_cstm_type"]
    cstm_msg_data = col_cstm_msgs.find({"custom_message_type":str(ty_pe)},{"_id":0})
    return cstm_msg_data

def update_custom_red_button_buffertime_related_sms_by_type(order_entry_msg):
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["bfr_time_sms_cstm_type"]
    col_cstm_msgs.update_one({"custom_message_type": str(ty_pe)}, {'$set' :{
                                                                'create_order_text_box_2':order_entry_msg['create_order_text_box_2'],
                                                                'create_order_text_box_3':order_entry_msg['create_order_text_box_3'],
                                                                'create_order_text_box_4':order_entry_msg['create_order_text_box_4'] }})
    return

#==================================================================================================================================

def get_custom_order_related_texts_for_red_button_lead_by_cst_type():
    print("---------------------------------INSIDE DB")
    print(session["ld_cstm_type"])
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["ld_cstm_type"]
    cstm_msg_data = col_cstm_msgs.find({"custom_message_type":str(ty_pe)},{"_id":0})
    return cstm_msg_data

def update_custom_red_button_leadtime_related_texts_by_type(order_entry_msg):
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["ld_cstm_type"]
    col_cstm_msgs.update_one({"custom_message_type": str(ty_pe)}, {'$set' :{'create_order_text_box_1':order_entry_msg['create_order_text_box_1'],
                                                                'create_order_text_box_2':order_entry_msg['create_order_text_box_2'],
                                                                'create_order_text_box_3':order_entry_msg['create_order_text_box_3'],
                                                                'create_order_text_box_4':order_entry_msg['create_order_text_box_4'] }})
    return

#==================================================================================================================================

def get_custom_order_related_sms_for_red_button_lead_by_cst_type():
    print("---------------------------------INSIDE DB")
    print(session["ld_time_sms_cstm_type"])
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["ld_time_sms_cstm_type"]
    cstm_msg_data = col_cstm_msgs.find({"custom_message_type":str(ty_pe)},{"_id":0})
    return cstm_msg_data

def update_custom_red_button_leadtime_related_sms_by_type(order_entry_msg):
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["ld_time_sms_cstm_type"]
    col_cstm_msgs.update_one({"custom_message_type": str(ty_pe)}, {'$set' :{
                                                                'create_order_text_box_2':order_entry_msg['create_order_text_box_2'],
                                                                'create_order_text_box_3':order_entry_msg['create_order_text_box_3'],
                                                                'create_order_text_box_4':order_entry_msg['create_order_text_box_4'] }})
    return


#===========================================================================================================
def get_custom_order_related_texts_for_progress_time_line_by_cst_type():
    print("---------------------------------INSIDE DB")
    print(session["pgrstmln_cstm_type"])
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["pgrstmln_cstm_type"]
    cstm_msg_data = col_cstm_msgs.find({"custom_message_type":str(ty_pe)},{"_id":0})
    return cstm_msg_data

def update_custom_progress_time_line_related_texts_by_type(order_entry_msg):
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["pgrstmln_cstm_type"]
    col_cstm_msgs.update_one({"custom_message_type": str(ty_pe)}, {'$set' :{'create_order_text_box_1':order_entry_msg['create_order_text_box_1'],
                                                                'create_order_text_box_2':order_entry_msg['create_order_text_box_2'],
                                                                'create_order_text_box_3':order_entry_msg['create_order_text_box_3'],
                                                                'create_order_text_box_4':order_entry_msg['create_order_text_box_4'] }})
    return

#===========================================================================================================
def get_custom_order_related_sms_for_progress_time_line_by_cst_type():
    print("---------------------------------INSIDE DB")
    print(session["prgs_time_line_sms_cstm_type"])
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["prgs_time_line_sms_cstm_type"]
    cstm_msg_data = col_cstm_msgs.find({"custom_message_type":str(ty_pe)},{"_id":0})
    return cstm_msg_data

def update_custom_progress_time_line_related_sms_by_type(order_entry_msg):
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["prgs_time_line_sms_cstm_type"]
    col_cstm_msgs.update_one({"custom_message_type": str(ty_pe)}, {'$set' :{'create_order_text_box_1':order_entry_msg['create_order_text_box_1'],
                                                                'create_order_text_box_2':order_entry_msg['create_order_text_box_2'],
                                                                'create_order_text_box_3':order_entry_msg['create_order_text_box_3']
                                                                 }})
    return

#===========================================================================================================
def get_custom_order_related_texts_for_order_buffer_by_cst_type():
    print("---------------------------------INSIDE DB")
    print(session["order_buffer_cstm_type"])
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["order_buffer_cstm_type"]
    cstm_msg_data = col_cstm_msgs.find({"custom_message_type":str(ty_pe)},{"_id":0})
    return cstm_msg_data

def update_custom_order_buffertime_related_texts_by_type(order_entry_msg):
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["order_buffer_cstm_type"]
    col_cstm_msgs.update_one({"custom_message_type": str(ty_pe)}, {'$set' :{'create_order_text_box_1':order_entry_msg['create_order_text_box_1'],
                                                                'create_order_text_box_2':order_entry_msg['create_order_text_box_2'],
                                                                'create_order_text_box_3':order_entry_msg['create_order_text_box_3'],
                                                                'create_order_text_box_4':order_entry_msg['create_order_text_box_4'] }})
    return

#===========================================================================================================
def get_custom_order_related_sms_for_order_buffer_by_cst_type():
    print("---------------------------------INSIDE DB")
    print(session["buffer_time_sms_cstm_type"])
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["buffer_time_sms_cstm_type"]
    cstm_msg_data = col_cstm_msgs.find({"custom_message_type":str(ty_pe)},{"_id":0})
    return cstm_msg_data

def update_custom_order_buffertime_related_sms_by_type(order_entry_msg):
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["buffer_time_sms_cstm_type"]
    col_cstm_msgs.update_one({"custom_message_type": str(ty_pe)}, {'$set' :{'create_order_text_box_1':order_entry_msg['create_order_text_box_1'],
                                                                'create_order_text_box_2':order_entry_msg['create_order_text_box_2'],
                                                                'create_order_text_box_3':order_entry_msg['create_order_text_box_3'],
                                                                'create_order_text_box_4':order_entry_msg['create_order_text_box_4'] }})
    return


#===========================================================================================================
def get_custom_order_related_texts_for_order_lead_time_by_cst_type():
    print("---------------------------------INSIDE DB")
    print(session["order_lead_cstm_type"])
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["order_lead_cstm_type"]
    cstm_msg_data = col_cstm_msgs.find({"custom_message_type":str(ty_pe)},{"_id":0})
    return cstm_msg_data

def update_custom_order_leadtime_related_texts_by_type(order_entry_msg):
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["order_lead_cstm_type"]
    col_cstm_msgs.update_one({"custom_message_type": str(ty_pe)}, {'$set' :{'create_order_text_box_1':order_entry_msg['create_order_text_box_1'],
                                                                'create_order_text_box_2':order_entry_msg['create_order_text_box_2'],
                                                                'create_order_text_box_3':order_entry_msg['create_order_text_box_3'],
                                                                'create_order_text_box_4':order_entry_msg['create_order_text_box_4'] }})
    return

#===========================================================================================================
def get_custom_order_related_sms_for_order_lead_time_by_cst_type():
    print("---------------------------------INSIDE DB")
    print(session["lead_time_sms_cstm_type"])
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["lead_time_sms_cstm_type"]
    cstm_msg_data = col_cstm_msgs.find({"custom_message_type":str(ty_pe)},{"_id":0})
    return cstm_msg_data

def update_custom_order_leadtime_related_sms_by_type(order_entry_msg):
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["lead_time_sms_cstm_type"]
    col_cstm_msgs.update_one({"custom_message_type": str(ty_pe)}, {'$set' :{'create_order_text_box_1':order_entry_msg['create_order_text_box_1'],
                                                                'create_order_text_box_2':order_entry_msg['create_order_text_box_2'],
                                                                'create_order_text_box_3':order_entry_msg['create_order_text_box_3'],
                                                                'create_order_text_box_4':order_entry_msg['create_order_text_box_4'] }})
    return


#===========================================================================================================
def get_custom_order_related_texts_for_order_edit_by_cst_type():
    print("---------------------------------INSIDE DB")
    print(session["order_edit_cstm_type"])
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["order_edit_cstm_type"]
    cstm_msg_data = col_cstm_msgs.find({"custom_message_type":str(ty_pe)},{"_id":0})
    return cstm_msg_data

def update_custom_order_edit_related_texts_by_type(order_entry_msg):
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["order_edit_cstm_type"]
    col_cstm_msgs.update_one({"custom_message_type": str(ty_pe)}, {'$set' :{'create_order_text_box_1':order_entry_msg['create_order_text_box_1'],
                                                                'create_order_text_box_2':order_entry_msg['create_order_text_box_2'],
                                                                'create_order_text_box_3':order_entry_msg['create_order_text_box_3'],
                                                                'create_order_text_box_4':order_entry_msg['create_order_text_box_4'] }})
    return

#===========================================================================================================
def get_custom_order_related_sms_for_order_edit_by_cst_type():
    print("---------------------------------INSIDE DB")
    print(session["order_edit_sms_cstm_type"])
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["order_edit_sms_cstm_type"]
    cstm_msg_data = col_cstm_msgs.find({"custom_message_type":str(ty_pe)},{"_id":0})
    return cstm_msg_data

def update_custom_order_edit_related_sms_by_type(order_entry_msg):
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["order_edit_sms_cstm_type"]
    col_cstm_msgs.update_one({"custom_message_type": str(ty_pe)}, {'$set' :{'create_order_text_box_1':order_entry_msg['create_order_text_box_1'],
                                                                'create_order_text_box_2':order_entry_msg['create_order_text_box_2'],
                                                                'create_order_text_box_3':order_entry_msg['create_order_text_box_3']
                                                                }})
    return


#===========================================================================================================
def get_custom_order_related_texts_for_order_entry_by_cst_type():
    print("---------------------------------INSIDE DB")
    print(session["order_entry_cstm_type"])
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["order_entry_cstm_type"]
    cstm_msg_data = col_cstm_msgs.find({"custom_message_type":str(ty_pe)},{"_id":0})
    return cstm_msg_data

def update_custom_order_entry_related_texts_by_type(order_entry_msg):
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["order_entry_cstm_type"]
    col_cstm_msgs.update_one({"custom_message_type": str(ty_pe)}, {'$set' :{'create_order_text_box_1':order_entry_msg['create_order_text_box_1'],
                                                                'create_order_text_box_2':order_entry_msg['create_order_text_box_2'],
                                                                'create_order_text_box_3':order_entry_msg['create_order_text_box_3'],
                                                                'create_order_text_box_4':order_entry_msg['create_order_text_box_4'] }})
    return

#===========================================================================================================
def get_custom_order_related_sms_for_order_entry_by_cst_type():
    print("---------------------------------INSIDE DB")
    print(session["order_entry_sms_cstm_type"])
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["order_entry_sms_cstm_type"]
    cstm_msg_data = col_cstm_msgs.find({"custom_message_type":str(ty_pe)},{"_id":0})
    return cstm_msg_data

def update_custom_order_entry_related_sms_by_type(order_entry_msg):
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["order_entry_sms_cstm_type"]
    col_cstm_msgs.update_one({"custom_message_type": str(ty_pe)}, {'$set' :{'create_order_text_box_1':order_entry_msg['create_order_text_box_1'],
                                                                'create_order_text_box_2':order_entry_msg['create_order_text_box_2'],
                                                                'create_order_text_box_3':order_entry_msg['create_order_text_box_3'],
                                                                'create_order_text_box_4':order_entry_msg['create_order_text_box_4'] }})
    return


#========================================================================================================
def get_custom_redbtn_related_texts_for_progress_time_line_by_cst_type():
    print("---------------------------------INSIDE DB of progress timeline-----------------")
    print(session["redbtn_pgrstmln_cstm_type"])
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["redbtn_pgrstmln_cstm_type"]
    cstm_msg_data = col_cstm_msgs.find({"custom_message_type":str(ty_pe)},{"_id":0})
    return cstm_msg_data

def update_custom_redbtn_progress_time_line_related_texts_by_type(order_entry_msg):
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["redbtn_pgrstmln_cstm_type"]
    col_cstm_msgs.update_one({"custom_message_type": str(ty_pe)}, {'$set' :{'create_order_text_box_1':order_entry_msg['create_order_text_box_1'],
                                                                'create_order_text_box_2':order_entry_msg['create_order_text_box_2'],
                                                                'create_order_text_box_3':order_entry_msg['create_order_text_box_3'],
                                                                'create_order_text_box_4':order_entry_msg['create_order_text_box_4'] }})
    return


#========================================================================================================
def get_custom_welcome_note_texts_by_cst_type():
    print("---------------------------------INSIDE DB")
    print(session["welcome_note_mail"])
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["welcome_note_mail"]
    cstm_msg_data = col_cstm_msgs.find({"custom_message_type":str(ty_pe)},{"_id":0})
    return cstm_msg_data

def update_custom_welcome_note_texts_by_type(order_entry_msg):
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["welcome_note_mail"]
    col_cstm_msgs.update_one({"custom_message_type": str(ty_pe)}, {'$set' :{'create_order_text_box_1':order_entry_msg['create_order_text_box_1'],
                                                                'create_order_text_box_2':order_entry_msg['create_order_text_box_2'] }})
    return


#===========================================================================================================
def get_custom_blk_related_sms_for_progress_time_line_by_cst_type():
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["blk_prgs_time_line_sms_cstm_type"]
    cstm_msg_data = col_cstm_msgs.find({"custom_message_type":str(ty_pe)},{"_id":0})
    return cstm_msg_data

def update_custom_blk_progress_time_line_related_sms_by_type(order_entry_msg):
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["blk_prgs_time_line_sms_cstm_type"]
    col_cstm_msgs.update_one({"custom_message_type": str(ty_pe)}, {'$set' :{'create_order_text_box_1':order_entry_msg['create_order_text_box_1'],
                                                                'create_order_text_box_2':order_entry_msg['create_order_text_box_2'],
                                                                'create_order_text_box_3':order_entry_msg['create_order_text_box_3'],
                                                                'create_order_text_box_4':order_entry_msg['create_order_text_box_4']
                                                                 }})
    return

#===========================================================================================================
def get_custom_welcome_note_sms_by_cst_type():
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["welcome_note"]
    cstm_msg_data = col_cstm_msgs.find({"custom_message_type":str(ty_pe)},{"_id":0})
    return cstm_msg_data

def update_custom_wecome_note_sms_by_type(order_entry_msg):
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["welcome_note"]
    col_cstm_msgs.update_one({"custom_message_type": str(ty_pe)}, {'$set' :{'create_order_text_box_1':order_entry_msg['create_order_text_box_1']
                                                                 }})
    return

#===========================================================================================================
def get_custom_review_page_details_by_cst_type():
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["review_page"]
    cstm_msg_data = col_cstm_msgs.find({"custom_message_type":str(ty_pe)},{"_id":0})
    return cstm_msg_data

def update_custom_review_page_details_by_type(review_data):
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["review_page"]
    col_cstm_msgs.update_one({"custom_message_type": str(ty_pe)}, {'$set' :{'create_order_text_box_1':review_data['create_order_text_box_1'],
                                                                'create_order_text_box_2':review_data['create_order_text_box_2']
                                                                 }})
    return


#===========================================================================================================
def get_custom_product_review_page_details_by_cst_type():
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["prod_review_page"]
    cstm_msg_data = col_cstm_msgs.find({"custom_message_type":str(ty_pe)},{"_id":0})
    return cstm_msg_data

def update_custom_product_review_page_details_by_type(review_data):
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["prod_review_page"]
    col_cstm_msgs.update_one({"custom_message_type": str(ty_pe)}, {'$set' :{'create_order_text_box_1':review_data['create_order_text_box_1'],
                                                                'create_order_text_box_2':review_data['create_order_text_box_2']
                                                                 }})
    return


#===========================================================================================================
def get_custom_feedback_review_page_details_by_cst_type():
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["feedback_review_page"]
    cstm_msg_data = col_cstm_msgs.find({"custom_message_type":str(ty_pe)},{"_id":0})
    return cstm_msg_data

def update_custom_feedback_review_page_details_by_type(feedback_data):
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["feedback_review_page"]
    col_cstm_msgs.update_one({"custom_message_type": str(ty_pe)}, {'$set' :{'create_order_text_box_1':feedback_data['create_order_text_box_1'],
                                                                'create_order_text_box_2':feedback_data['create_order_text_box_2']
                                                                 }})
    return


#===========================================================================================================
def get_custom_feedback_review_page_four_details_by_cst_type():
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["feedback_four_review_page"]
    cstm_msg_data = col_cstm_msgs.find({"custom_message_type":str(ty_pe)},{"_id":0})
    return cstm_msg_data

def update_custom_feedback_review_page_four_details_by_type(feedback_data):
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["feedback_four_review_page"]
    col_cstm_msgs.update_one({"custom_message_type": str(ty_pe)}, {'$set' :{'create_order_text_box_1':feedback_data['create_order_text_box_1'],
                                                                'create_order_text_box_2':feedback_data['create_order_text_box_2']
                                                                 }})
    return

#===========================================================================================================
def get_custom_coivid_precaution_details_by_cst_type():
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["covid_precautions"]
    cstm_msg_data = col_cstm_msgs.find({"custom_message_type":str(ty_pe)},{"_id":0})
    return cstm_msg_data

def update_custom_covide_precaution_by_type(covid_info):
    global col_cstm_msgs
    connect_order_db()
    ty_pe = session["covid_precautions"]
    col_cstm_msgs.update_one({"custom_message_type": str(ty_pe)}, {'$set' :{'create_order_text_box_1':covid_info['create_order_text_box_1'],
                                                                'create_order_text_box_2':covid_info['create_order_text_box_2']
                                                                 }})
    return


#------------------------------------------------Reviews Links and Info---------------------------------------------------------
def save_review_link_information(links_data):
  global col_review_links_info
  connect_order_db()
  col_review_links_info.insert(links_data)
  return "Saved!!"

def get_review_links_details():
    global col_review_links_info
    connect_order_db()
    link_recs = col_review_links_info.find({},{"_id":0})
    return link_recs

def get_review_links_details_by_review_id(link_id):
    global col_review_links_info
    connect_order_db()
    link_data = col_review_links_info.find({"review_link_id":str(link_id)},{"_id":0})
    return link_data

def update_review_link_data(r_id,review_link_disc):
    global col_review_links_info
    connect_order_db()
    col_review_links_info.update_one({"review_link_id": str(r_id)}, {'$set' :{'review_link_name':review_link_disc['review_link_name'],
                                                                              'review_link_url':review_link_disc['review_link_url'],
                                                                              'review_link_label':review_link_disc['review_link_label']
                                                                              }})
    return

def delete_a_review_link_using_link_id(r_id):
    global col_review_links_info
    connect_order_db()
    col_review_links_info.remove({"review_link_id": str(r_id)})
    return "Deleted successfully"
    








#=========================================================================================================
# login section
def connect_login_db():
    global con_login_dealer
    global db_login_dealer
    global col_login_dealer
    global col_login_consumer

    #auth = config['Authorization']['DB_NAME']
    #auth_col = config['Authorization']['COLLECTION_NAME_RETAILERS']
    ca = certifi.where()
    con_login_dealer = MongoClient('mongodb+srv://'+config['database']['USERNAME']+':'
                                            +config['database']['PASSWORD']+'@'
                                            +config['database']['HOST']+'/'
                                            +config['Authorization']['DB_NAME']
                                            +'?retryWrites=true&w=majority',tlsCAFile = ca)

    # con_login = MongoClient('mongodb+srv://Sourav:l9EG8ULwylphgjHS@nexusfieldservice.axvp7.mongodb.net/Authorization?retryWrites=true&w=majority')
    db_login_dealer = con_login_dealer.Authorization
    col_login_dealer = db_login_dealer.dealer_credentials
    col_login_consumer = db_login_dealer.consumer_creds


def search_authorization_by_id(u_id):
   global col_login_dealer
   connect_login_db()
   searched_data_list = []
   searched_data = col_login_dealer.find({'user_id':str(u_id)},{"_id":0})
   return searched_data

def update_one_password(email, check):
    global col_login_dealer
    connect_login_db()
    col_login_dealer.update_one({"user_id": str(email)}, {'$set' :{'password':check['password']} })
    return

def check_password(email):
    global col_login_dealer
    connect_login_db()
    searched_data = col_login_dealer.find({'user_id':str(email)},{"_id":0})
    return searched_data

# global con_authoisation
# global db_authorisation
# global col_authorisation

# def connect_consumer_creds_db():
#   global con_authoisation
#   global db_authorisation
#   global col_authorisation
#   con_authoisation = MongoClient('mongodb+srv://'+config['database']['USERNAME']+':'+config['database']['PASSWORD']+'@'+config['database']['HOST']+'/'+config['Authorization']['DB_NAME']+'?retryWrites=true&w=majority')
#   db_authorisation = con_authoisation.Authorization
#   col_authorisation = db_authorisation.consumer_creds

def save_consumer_credentials(conInfo):
  global col_login_consumer
  connect_login_db()
  col_login_consumer.insert(conInfo)
  return "saved Successfully"

def get_consumer_cred_by_ph_num(ph_num):
  global col_login_consumer
  connect_login_db()
  creds_data = col_login_consumer.find({'user_contact':str(ph_num)},{"_id":0})
  return creds_data

def delete_a_consumer_credentials(ph_num):
  global col_login_consumer
  connect_login_db()
  col_login_consumer.remove({"user_contact": str(ph_num)})
  return "Deleted successfully"



#=========================Consumer PO Matrix===============================================================================

global con_consumer_po
global db_consumer_po
global col_consumer_po

def connect_consumer_po_db():
    global con_consumer_po
    global db_consumer_po
    global col_consumer_po
    ca = certifi.where()
    con_consumer_po = MongoClient('mongodb+srv://'+
                        config['database']['USERNAME']+':'+
                        config['database']['PASSWORD']+'@'+
                        config['database']['HOST']+'/'+
                        config['cosumer_matrix_db']['DB_NAME']+
                        '?retryWrites=true&w=majority',tlsCAFile = ca)
    db_consumer_po = con_consumer_po.Customer_PO_Db
    col_consumer_po = db_consumer_po.phone_po_matrix

def get_po_phone_matrix_details(mobile_num):
  global col_consumer_po
  connect_consumer_po_db()
  phone_po_data = col_consumer_po.find({"consumer_mobile_number" : str(mobile_num)})
  return phone_po_data

def get_po_phone_matrix_details_by_ph_num(mobile_num):
  global col_consumer_po
  connect_consumer_po_db()
  phone_po_data = col_consumer_po.find({"consumer_mobile_number" : str(mobile_num)},{"_id":0, "country":0, "consumer_mobile_number":0})
  return phone_po_data

def save_consumer_po_data(consumer_po_dict):
    global col_consumer_po
    connect_consumer_po_db()
    col_consumer_po.insert(consumer_po_dict)
    return "saved!!"

def update_dealer_po_list(mobile_num,dealer_dics):
    global col_consumer_po
    connect_consumer_po_db()
    col_consumer_po.update_one({"consumer_mobile_number":str(mobile_num)}, {'$set' :{session['orgId_retailer']:dealer_dics[session['orgId_retailer']]} })
    return

def update_po_numbers_after_delete_an_order(mobile_num,con_po_Disc):
    global col_consumer_po
    connect_consumer_po_db()
    col_consumer_po.update_one({"consumer_mobile_number":str(mobile_num)}, {'$set' :{session['orgId_retailer']:con_po_Disc[session['orgId_retailer']]} })
    return


#==============================================Consumer message status summary=====================================================


def save_to_message_delivery_status_records(sms_logs):
    global col_consumer_sms_delvery_logs
    connect_order_db()
    col_consumer_sms_delvery_logs.insert(sms_logs)
    return 'saved'

def get_message_delivery_logs():
    global col_consumer_sms_delvery_logs
    connect_order_db()
    logs_from_db = col_consumer_sms_delvery_logs.find()
    return logs_from_db

def update_deliery_status(n_id,msg_status):
    global col_consumer_sms_delvery_logs
    connect_order_db()
    col_consumer_sms_delvery_logs.update_one({"nexus_id" : str(n_id)}, {'$set' : {"twilio_delivery_status" : msg_status}})
    return




#==========================================Work Flow Architecture===========================================================

def save_workflow_structure(wrk_flowInfo):
    global col_work_flow_unit
    connect_order_db()
    col_work_flow_unit.insert(wrk_flowInfo)
    return "Saved Successfully"


def get_work_flow_data():
    global col_work_flow_unit
    connect_order_db()
    wrk_flw_data = col_work_flow_unit.find({"work_flow_name_disable" : False},{'_id':0})
    return wrk_flw_data

def get_all_work_flow_data():
    global col_work_flow_unit
    connect_order_db()
    wrk_flw_data = col_work_flow_unit.find({},{'_id':0})
    return wrk_flw_data

def get_workflow_data_by_one_wrkflw_id(wf_id):
    global col_work_flow_unit
    connect_order_db()
    wrk_flw_data = col_work_flow_unit.find({'work_flow_id':str(wf_id)}, {"_id":0})
    return wrk_flw_data

def update_workflow_name(wf_ID,work_flow_name):
    global col_work_flow_unit
    connect_order_db()
    col_work_flow_unit.update_one({"work_flow_id":str(wf_ID)}, {'$set' :{"work_flow_name":work_flow_name} })
    return

def update_stages_to_workflow(wf_ID,wf_Disc):
    global col_work_flow_unit
    connect_order_db()
    col_work_flow_unit.update_one({"work_flow_id":str(wf_ID)}, {'$set' :{"work_flow_stages":wf_Disc['work_flow_stages'],
                                                                         "work_flow_name_disable":wf_Disc['work_flow_name_disable']    } })
    return

def update_stages_to_workflow_after_delete(wf_ID,wf_Disc):
    global col_work_flow_unit
    connect_order_db()
    col_work_flow_unit.update_one({"work_flow_id":str(wf_ID)}, {'$set' :{"work_flow_stages":wf_Disc['work_flow_stages']} })
    return


def update_disable_field_to_workflow_after_delete(wf_ID,wf_Disc_disable):
    global col_work_flow_unit
    connect_order_db()
    col_work_flow_unit.update_one({"work_flow_id":str(wf_ID)}, {'$set' :{"work_flow_name_disable":wf_Disc_disable['work_flow_name_disable']} })
    return

def delete_a_workflow(wf_ID):
  global col_work_flow_unit
  connect_order_db()
  col_work_flow_unit.remove({"work_flow_id": str(wf_ID)})
  return "Deleted Successfully"



#=========================================================================================================================================================

def save_empty_keys_to_db(order_empinfo):
    global emp_keys
    connect_order_db()
    emp_keys.insert(order_empinfo)
    return "saved"

def get_empty_keys_from_db():
    global emp_keys
    connect_order_db()
    order_from_db = emp_keys.find({},{'_id':0})
    return order_from_db

def update_custom_choice_values_to_db(deal_id,order_vals):
    global emp_keys
    connect_order_db()
    emp_keys.update_one({"dealer_id":str(deal_id)}, {'$set' :{"order_id":order_vals['order_id'],
                                                              "po_number":order_vals['po_number'],
                                                            "order_date":order_vals['order_date'],
                                                            "work_flow_name":order_vals['work_flow_name'],
                                                            "order_value":order_vals['order_value'],
                                                            "order_cost":order_vals['order_cost'],
                                                            "model":order_vals['model'],
                                                            "size":order_vals['size'],
                                                            "user_type":order_vals['user_type'],
                                                            "job_name":order_vals['job_name'],
                                                            "consumer_first_name":order_vals['consumer_first_name'],
                                                            "consumer_last_name":order_vals['consumer_last_name'],
                                                            "consumer_mobile_number":order_vals['consumer_mobile_number'],
                                                            "consumer_email":order_vals['consumer_email'],
                                                            "country":order_vals['country'],
                                                            "state":order_vals['state'],
                                                            "address":order_vals['address'],
                                                            "city":order_vals['city'],
                                                            "brand":order_vals['brand'],
                                                            "total_lead_time":order_vals['total_lead_time'],
                                                            "dealer_buffer_time":order_vals['dealer_buffer_time'],
                                                            "est_deliver_time":order_vals['est_deliver_time'],
                                                            "lead_time_parameter":order_vals['lead_time_parameter'],
                                                            "buffer_time_parameter":order_vals['buffer_time_parameter'],
                                                            "progress_timeline":order_vals['progress_timeline'],
                                                            "preference_reply_back":order_vals['preference_reply_back'],
                                                            "order_notes":order_vals['order_notes'],
                                                            "last_activity":order_vals['last_activity'],
                                                            "order_completion_date":order_vals['order_completion_date'],} })
    return

#================================================Dealer Account===============================================================================
#=========================================================================================================
global con_dealer_account
global db_dealer_account
global col_dealer_account
global col_employee_info
global col_terms_n_co


def connect_account_db():
    global con_dealer_account
    global db_dealer_account
    global col_dealer_account
    global col_employee_info
    global col_terms_n_co

    ca = certifi.where()
    con_dealer_account = MongoClient('mongodb+srv://'+config['database']['USERNAME']+':'
                                            +config['database']['PASSWORD']+'@'
                                            +config['database']['HOST']+'/'
                                            +config['Dealer_Account']['DB_NAME']
                                            +'?retryWrites=true&w=majority',tlsCAFile = ca)
    db_dealer_account = con_dealer_account.Dealer_account_DB
    col_dealer_account = db_dealer_account.basic_details
    col_employee_info = db_dealer_account.employee_info
    col_terms_n_co = db_dealer_account.text_asset

def get_dealer_basic_details_from_dealer_account():
    global col_dealer_account
    connect_account_db()
    org_id = session['orgId_retailer']
    dealer_data = col_dealer_account.find({"dealer_id": str(org_id)},{"_id":0})
    return dealer_data

def get_dealer_basic_details_from_employee_account():
    global col_employee_info
    connect_account_db()
    org_id = session['orgId_retailer']
    emp_data = col_employee_info.find({"dealer_id": str(org_id)},{"_id":0})
    return emp_data


def get_account_activation_status_details(org_id):
    global col_dealer_account
    connect_account_db()
    dealer_data = col_dealer_account.find( {'$and': [{"dealer_id" : str(org_id) },{"dealer_activation_status" : True} ]},{"_id":0})
    return dealer_data

def get_dealer_basic_details_from_dealer_account_by_phone_num(phone_num):
    global col_dealer_account
    connect_account_db()
    dealer_data = col_dealer_account.find({"contact_number": str(phone_num)},{"_id":0})
    return dealer_data

def get_terms_and_condition_details():
  global col_terms_n_co
  connect_account_db()
  dealer_data = col_terms_n_co.find({},{"_id":0})
  return dealer_data

#================================================Dealer Account===============================================================================
#=========================================================================================================
global con_announcement
global db_announcement
global col_announcement


def connect_announcement_db():
    global con_announcement
    global db_announcement
    global col_announcement

    ca = certifi.where()
    con_announcement = MongoClient('mongodb+srv://'+config['database']['USERNAME']+':'
                                            +config['database']['PASSWORD']+'@'
                                            +config['database']['HOST']+'/'
                                            +config['Announcement']['DB_NAME']
                                            +'?retryWrites=true&w=majority',tlsCAFile = ca)
    db_announcement = con_announcement.Nexus_Superapp_Marketing_siteDB
    col_announcement = db_announcement.Announcements_Col

def get_all_announcements_for_dealers():
    global col_announcement
    connect_announcement_db()
    announcemet_data = col_announcement.find({},{"_id":0})
    return announcemet_data




#==========================================================================================
global con_reviews
global db_reviews
global col_reviews

def connect_reviews_db():
    global con_reviews
    global db_reviews
    global col_reviews
    
    ca = certifi.where()
    con_reviews = MongoClient('mongodb+srv://'+
                        config['database']['USERNAME']+':'+
                        config['database']['PASSWORD']+'@'+
                        config['database']['HOST']+'/'+
                        config['cosumer_matrix_db']['DB_NAME']+
                        '?retryWrites=true&w=majority',tlsCAFile = ca)
    db_reviews = con_reviews.Dealer_Consumer_Reviews_Db
    col_reviews = db_reviews.reviews_info



def save_review_process_information(review_info):
    global col_reviews
    connect_reviews_db()
    col_reviews.insert(review_info)
    return


def get_review_data_for_the_dealer():
    global col_reviews
    connect_reviews_db()
    org_id = session['orgId_retailer']
    review_data = col_reviews.find({"dealer_id":str(org_id)},{"_id":0})
    return review_data


def get_review_data_by_review_id(r_id):
    global col_reviews
    connect_reviews_db()
    review_data = col_reviews.find({"review_id":r_id},{"_id":0})
    return review_data

def update_product_review_update_date_time(r_id,dynamic_url,prod_activation_token,prod_activation_date_time,prod_activation_state):
  global col_reviews
  connect_reviews_db()
  col_reviews.update_one({"review_id": str(r_id)}, {'$set' :{'product_review_activate_token':prod_activation_token,
                                                                 'product_review_activation_date_time':prod_activation_date_time,
                                                                 'product_review_activation_state' :prod_activation_state,
                                                                 'product_review_dynamic_url' :dynamic_url} })
  return

def update_product_review_update_date_time_with_activation_token(r_id,prod_activation_token,prod_activation_date_time,prod_activation_state,dynamic_url):
    print("===================================update product review token")
    print(r_id)
    global col_reviews
    connect_reviews_db()
    col_reviews.update_one({"review_id": str(r_id)},{'$set' :
                                                    {'product_review_activate_token':prod_activation_token,
                                                     'product_review_activation_date_time':prod_activation_date_time,
                                                     'product_review_activation_state':prod_activation_state,
                                                     'product_review_dynamic_url':dynamic_url
                               }})
    return
