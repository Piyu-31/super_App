from flask import Flask, render_template, redirect, request, flash, g, session, url_for, jsonify
import random
import string

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, BooleanField, TextAreaField, SelectMultipleField,HiddenField,DecimalField
from wtforms.fields.html5 import DateField, EmailField
from wtforms.validators import InputRequired,Length
from flask_wtf.file import FileField, FileRequired
from wtforms import widgets
#from wtforms.widgets import ListWidget,html_params
from werkzeug.utils import secure_filename

import xlrd
import datetime
import time
from datetime import datetime
from datetime import timedelta
from passlib.hash import sha256_crypt
from functools import wraps
#from datetime import date
import sys
import pytz
import sendSms
import sendMail
import sensitive_wordsOrc


import json

import pprint

import flask

#from passlib.hash import sha256_crypt
import string
import random

import operator
import configparser

import DOL_DB
import DOL_info
import sensitive_Info_db

config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)

app = flask.Flask('env')

app.secret_key = 'rgd47dghd678'

app.jinja_env.add_extension('jinja2.ext.loopcontrols')

#---------------------------------------------------------------------------------------------------------------------

class OrderLoginForm(FlaskForm):
    e_mail = EmailField('Email', validators=[InputRequired()], render_kw={"placeholder": "Email"})
    pass_word = StringField('Password',validators=[InputRequired()], render_kw={"placeholder": "Password"})

#---------------------------------------------------------------------------------------------------------------------

class ResetPasswordForm(FlaskForm):
    reset_email = EmailField('Email', validators=[InputRequired()], render_kw={"placeholder": "Username"})
    phone_num = IntegerField('Mobile #', validators=[InputRequired()], render_kw={"placeholder": "Mobile number"})


#=============================================One on One Communication=================================================================================
class WF_OneOnOneCommunication(FlaskForm):
    subject = SelectField('Subject',  choices=[], validators=[InputRequired()])
    send_type = SelectField('Type', choices=[('SMS', 'SMS'), ('Email & SMS', 'Email & SMS')], validators=[InputRequired()])
    msg = TextAreaField('Message',validators=[InputRequired()], render_kw={"placeholder": "Message"})

#==========================================Work Flow============================================================================
class WorkFlowCreate(FlaskForm):
    send_review_link = SelectField('Type', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[InputRequired()])
    wrk_flw = StringField('Workflow', validators=[InputRequired()], render_kw={"placeholder": "Workflow"})

class WorkFlowNameEdit(FlaskForm):
    wrk_flw = StringField('Workflow', validators=[InputRequired()], render_kw={"placeholder": "Workflow"})

class WorkFlowEdit(FlaskForm):
    sta_ges = StringField('Stages', validators=[InputRequired(), Length(min=1, max=40)], render_kw={"placeholder": "Stages"})


#=============================================Work Flow Order Entry==========================================================================
class WFOrderForm(FlaskForm):
    provinces_canada_list_of_tuples = []
    provinces_canada_list_of_tuples.append(('' , 'Select Province'))
    
    states_us_list_of_tuples = []
    states_us_list_of_tuples.append(('', 'Select State'))

    
    po_no = StringField('PO #', validators=[InputRequired()], render_kw={"placeholder": "PO #"})
    or_date = DateField("Date",validators=[InputRequired()], render_kw={"placeholder": "Order date"})
    
    wf_type = SelectField('WorkFlow Type', choices=[], validators=[InputRequired()])
    
    or_price = DecimalField('Order Value', places=2,rounding=None, use_locale=False, number_format=None, validators=[InputRequired()], render_kw={"placeholder": "Sales Order Revenue (in USD $)"})
    or_cost = DecimalField('Order Cost', places=2,rounding=None, use_locale=False, number_format=None, validators=[InputRequired()], render_kw={"placeholder": "Sales Order Cost (in USD $)"})
    mdl = StringField('Model',validators=[InputRequired()], render_kw={"placeholder": "Model"})
    siz = StringField('Size',validators=[InputRequired()], render_kw={"placeholder": "Size"})
    user_type = SelectField('user Type', choices=[('Consumer', 'Consumer'), ('Business', 'Business')], validators=[InputRequired()])
    j_name = StringField('Job Name',validators=[InputRequired()], render_kw={"placeholder": "Job Name"})
    co_fname = StringField('First Name',validators=[InputRequired()], render_kw={"placeholder": "First Name/Company"})
    co_lname = StringField('Last Name', render_kw={"placeholder": "Last Name (Optional)"})
    co_mo_num = IntegerField('Mobile #', validators=[InputRequired()], render_kw={"placeholder": "Mobile Number"})
    co_email = EmailField('Email', validators=[InputRequired()], render_kw={"placeholder": "Email"})
    address = StringField('Address',validators=[InputRequired()], render_kw={"placeholder": "Address"})
    ci_ty = StringField('City',validators=[InputRequired()], render_kw={"placeholder": "City"})
    
    
    provinces_canada = config['states']['CANADA'].split(', ')
    for i in provinces_canada:
        single_province_tuple = (i,i)
        provinces_canada_list_of_tuples.append(single_province_tuple)

    ca_States = SelectField('Select Province', choices=provinces_canada_list_of_tuples)

    states_us = config['states']['US'].split(', ')
    for s in states_us:
        single_state_tuple = (s,s)
        states_us_list_of_tuples.append(single_state_tuple)

    us_States = SelectField('Select State', choices=states_us_list_of_tuples)

    emp_fld = SelectField('Select', choices=[('' , 'Select')])

    country_1 = BooleanField('Canada')
    country_2 = BooleanField('US')
    #br_and = StringField('Brand',validators=[InputRequired()], render_kw={"placeholder": "Brand"})
    br_and = SelectField('Brand', choices=[], validators=[InputRequired()])
    totl_lt = IntegerField('Total Lead Time', validators=[InputRequired()], render_kw={"placeholder": "Lead Time (in weeks)"})
    delr_bfr_tm = IntegerField('Dealer Buffer Time', validators=[InputRequired()], render_kw={"placeholder": "Buffer Time (in weeks)"})
    o_notes = TextAreaField('Notes', render_kw={"placeholder": "Notes"})
    zip_code = StringField('Zipcode',validators=[InputRequired()], render_kw={"placeholder": "Zip Code"})


class WFOrderEditForm(FlaskForm):
    provinces_canada_list_of_tuples = []
    provinces_canada_list_of_tuples.append(('' , 'Select Province'))
    
    states_us_list_of_tuples = []
    states_us_list_of_tuples.append(('', 'Select State'))

    
    po_no = StringField('PO #', validators=[InputRequired()], render_kw={"placeholder": "PO #"})
    or_date = DateField("Date", render_kw={'readonly': True})
    
    #wf_type = SelectField('WorkFlow Type',validators=[InputRequired()], render_kw={'disabled':'disabled'})
    wf_type = StringField('WorkFlow Type', render_kw={'disabled':'disabled'})
    
    or_price = IntegerField('Order Value', validators=[InputRequired()], render_kw={"placeholder": "Sales Order Revenue (in USD $)"})
    or_cost = IntegerField('Order Cost', validators=[InputRequired()], render_kw={"placeholder": "Sales Order Cost (in USD $)"})
    mdl = StringField('Model',validators=[InputRequired()], render_kw={"placeholder": "Model"})
    siz = StringField('Size',validators=[InputRequired()], render_kw={"placeholder": "Size"})
    user_type = SelectField('user Type', choices=[('Consumer', 'Consumer'), ('Business', 'Business')], validators=[InputRequired()])
    j_name = StringField('Job Name',validators=[InputRequired()], render_kw={"placeholder": "Job Name"})
    co_fname = StringField('First Name',validators=[InputRequired()], render_kw={"placeholder": "First Name/Company"})
    co_lname = StringField('Last Name', render_kw={"placeholder": "Last Name (Optional)"})
    co_mo_num = IntegerField('Mobile #', validators=[InputRequired()], render_kw={"placeholder": "Mobile Number"})
    co_email = EmailField('Email', validators=[InputRequired()], render_kw={"placeholder": "Email"})
    co_dob = DateField('Date of Birth', render_kw={"placeholder": "Date of Birth (Optional)"})
    address = StringField('Address',validators=[InputRequired()], render_kw={"placeholder": "Address"})
    ci_ty = StringField('City',validators=[InputRequired()], render_kw={"placeholder": "City"})
    zip_code = StringField('Zipcode',validators=[InputRequired()], render_kw={"placeholder": "Zip Code"})
    
    
    provinces_canada = config['states']['CANADA'].split(', ')
    for i in provinces_canada:
        single_province_tuple = (i,i)
        provinces_canada_list_of_tuples.append(single_province_tuple)

    ca_States = SelectField('Select Province', choices=provinces_canada_list_of_tuples)

    states_us = config['states']['US'].split(', ')
    for s in states_us:
        single_state_tuple = (s,s)
        states_us_list_of_tuples.append(single_state_tuple)

    us_States = SelectField('Select State', choices=states_us_list_of_tuples)

    country_1 = BooleanField('Canada', render_kw={'value': 'Canada'})
    country_2 = BooleanField('US', render_kw={'value': 'US'})
    br_and = SelectField('Brand', choices = [],validators=[InputRequired()])
    totl_lt = IntegerField('Total Lead Time', validators=[InputRequired()], render_kw={"placeholder": "Lead Time (in weeks)"})
    delr_bfr_tm = IntegerField('Dealer Buffer Time', validators=[InputRequired()], render_kw={"placeholder": "Buffer Time (in weeks)"})
    o_notes = TextAreaField('Notes', render_kw={"placeholder": "Notes"})
    cal_wflead_type = SelectField('Calculation Lead Type', choices=[('increase', 'increase'), ('decrease', 'decrease')], validators=[InputRequired()])
    cal_WFbuffer_type = SelectField('Calculation Buffer Type', choices=[('increase', 'increase'), ('decrease', 'decrease')], validators=[InputRequired()])
    pgrs_stage_name = SelectField('progress', choices=[], validators=[InputRequired()])
    pre_ference = SelectField('Reply Back Preference', choices=[('SMS', 'SMS'), ('Email N SMS', 'Email & SMS')], validators=[InputRequired()])
    leadtm_reason = TextAreaField('Reason',validators=[InputRequired()], render_kw={"placeholder": "Reason"})
    bfrtm_reason = TextAreaField('Reason',validators=[InputRequired()], render_kw={"placeholder": "Reason"})

class WFOrderUpdateEditForm(FlaskForm):
    provinces_canada_list_of_tuples = []
    provinces_canada_list_of_tuples.append(('' , 'Select Province'))

    states_us_list_of_tuples = []
    states_us_list_of_tuples.append(('', 'Select State'))

    po_no = StringField('PO #', validators=[InputRequired()], render_kw={"placeholder": "PO #"})
    or_date = DateField("Date", render_kw={'readonly': True})
    or_price = DecimalField('Order Value', places=2,rounding=None, use_locale=False, number_format=None, validators=[InputRequired()], render_kw={"placeholder": "Sales Order Revenue (in USD $)"})
    or_cost = DecimalField('Order Cost', places=2,rounding=None, use_locale=False, number_format=None, validators=[InputRequired()], render_kw={"placeholder": "Sales Order Cost (in USD $)"})
    mdl = StringField('Model',validators=[InputRequired()], render_kw={"placeholder": "Model"})
    siz = StringField('Size',validators=[InputRequired()], render_kw={"placeholder": "Size"})
    user_type = SelectField('user Type', choices=[('Consumer', 'Consumer'), ('Business', 'Business')], validators=[InputRequired()])
    j_name = StringField('Job Name',validators=[InputRequired()], render_kw={"placeholder": "Job Name"})
    co_fname = StringField('First Name',validators=[InputRequired()], render_kw={"placeholder": "First Name/Company"})
    co_lname = StringField('Last Name', render_kw={"placeholder": "Last Name (Optional)"})
    co_mo_num = IntegerField('Mobile #', validators=[InputRequired()], render_kw={"placeholder": "Mobile Number"})
    co_email = EmailField('Email', validators=[InputRequired()], render_kw={"placeholder": "Email"})
    co_dob = DateField('Date of Birth', render_kw={"placeholder": "Date of Birth (Optional)"})
    address = StringField('Address',validators=[InputRequired()], render_kw={"placeholder": "Address"})
    ci_ty = StringField('City',validators=[InputRequired()], render_kw={"placeholder": "City"})

    provinces_canada = config['states']['CANADA'].split(', ')
    for i in provinces_canada:
        single_province_tuple = (i,i)
        provinces_canada_list_of_tuples.append(single_province_tuple)
    ca_States = SelectField('Select Province', choices=provinces_canada_list_of_tuples)

    states_us = config['states']['US'].split(', ')
    for s in states_us:
        single_state_tuple = (s,s)
        states_us_list_of_tuples.append(single_state_tuple)
    us_States = SelectField('Select State', choices=states_us_list_of_tuples)
    country_1 = BooleanField('Canada')
    country_2 = BooleanField('US')
    br_and = SelectField('Brand', choices = [],validators=[InputRequired()])
    o_notes = TextAreaField('Notes', render_kw={"placeholder": "Notes"})
    #br_and = StringField('Brand',validators=[InputRequired()], render_kw={"placeholder": "Brand"})
    zip_code = StringField('Zipcode',validators=[InputRequired()], render_kw={"placeholder": "Zipcode"})





class WFOrderUpdateLeadTimeForm(FlaskForm):
    cal_wflead_type = SelectField('Calculation Lead Type', choices=[('increase', 'increase'), ('decrease', 'decrease')], validators=[InputRequired()])
    totl_lt = IntegerField('Total Lead Time', validators=[InputRequired()], render_kw={"placeholder": "Lead Time (in weeks)"})
    leadtm_reason = TextAreaField('Reason',validators=[InputRequired()], render_kw={"placeholder": "Reason"})

class WFOrderUpdateBufferTimeForm(FlaskForm):
    cal_WFbuffer_type = SelectField('Calculation Buffer Type', choices=[('increase', 'increase'), ('decrease', 'decrease')], validators=[InputRequired()])
    delr_bfr_tm = IntegerField('Dealer Buffer Time', validators=[InputRequired()], render_kw={"placeholder": "Buffer Time (in weeks)"})
    bfrtm_reason = TextAreaField('Reason',validators=[InputRequired()], render_kw={"placeholder": "Reason"})


class WFOrderUpdateProgressTimeLineForm(FlaskForm):
	pgrs_stage_name = SelectField('Progress', choices=[], validators=[InputRequired()])

    # def set_Context(self, pgrs_stage_choices):
    #     self.pgrs_stage_name.choices = pgrs_stage_choices

class WFOrderUpdateReplyPreferenceForm(FlaskForm):
	pre_ference = SelectField('Reply Back Preference', choices=[('SMS', 'SMS'), ('Email N SMS', 'Email & SMS')], validators=[InputRequired()])


#==================================Workflow Search Form Class==========================================================================
class SearchWFOrderFormByPO(FlaskForm):
    searchbyPonumber = IntegerField('PO #', validators=[InputRequired()], render_kw={"placeholder": "PO #"})

class SearchWFOrderFormByCity(FlaskForm):
    searchbyCity = StringField('City', validators=[InputRequired()], render_kw={"placeholder": "City"})

class SearchWFOrderFormByWFType(FlaskForm):
    searchbyWfType = StringField('Workflow Type', validators=[InputRequired()], render_kw={"placeholder": "Workflow Type"})


class SearchWFOrderFormByState(FlaskForm):
    provinces_canada_list_of_tuples = []
    provinces_canada_list_of_tuples.append(('' , 'Select Province'))

    states_us_list_of_tuples = []
    states_us_list_of_tuples.append(('', 'Select State'))

    all_states_and_provinces = []

    

    # searchbyState = SelectField('Select Province', choices=provinces_canada_list_of_tuples)

    states_us = config['states']['US'].split(', ')
    for s in states_us:
        single_state_tuple = (s,s)
        states_us_list_of_tuples.append(single_state_tuple)
        all_states_and_provinces.append(s)

    provinces_canada = config['states']['CANADA'].split(', ')
    for i in provinces_canada:
        single_province_tuple = (i,i)
        provinces_canada_list_of_tuples.append(single_province_tuple)
        all_states_and_provinces.append(i)

    #searchbyState = SelectField('Select State', choices=all_states_and_provinces)
    searchbyState = SelectField('Select State', choices=states_us_list_of_tuples)

class SearchWFOrderFormByDateRange(FlaskForm):
    searchbyFromdate = DateField("Date",validators=[InputRequired()], render_kw={"placeholder": "From date"})
    searchbyTodate = DateField("Date",validators=[InputRequired()], render_kw={"placeholder": "To date"})

class SearchWFOrderFormByJobName(FlaskForm):
    searchbyJobname = StringField('Job name', validators=[InputRequired()], render_kw={"placeholder": "Job Name"})

class SearchWFOrderFormByFirstName(FlaskForm):
    searchbyFname = StringField('Firstname', validators=[InputRequired()], render_kw={"placeholder": "First Name/Company"})

class SearchWFOrderFormByLastName(FlaskForm):
    searchbyLname = StringField('Lastname', validators=[InputRequired()], render_kw={"placeholder": "Last Name"})

#===========================================Custom Order Viewer=============================================================================

class OrderCustomViewerForm(FlaskForm):
    order_id = SelectField('Nexus Id', choices=[('True', 'True'), ('False', 'False')], validate_choice=False)
    po_number = SelectField('PO#', choices=[('True', 'True'), ('False', 'False')], validate_choice=False)
    order_date = SelectField('Date', choices=[('True', 'True'), ('False', 'False')], validate_choice=False)
    work_flow_name = SelectField('Name', choices=[('True', 'True'), ('False', 'False')], validate_choice=False)
    order_value = SelectField('Price', choices=[('True', 'True'), ('False', 'False')], validate_choice=False)
    order_cost = SelectField('Cost', choices=[('True', 'True'), ('False', 'False')], validate_choice=False)
    model = SelectField('Model', choices=[('True', 'True'), ('False', 'False')], validate_choice=False)
    size = SelectField('Size', choices=[('True', 'True'), ('False', 'False')], validate_choice=False)
    user_type = SelectField('User Type', choices=[('True', 'True'), ('False', 'False')], validate_choice=False)
    job_name = SelectField('Job Name', choices=[('True', 'True'), ('False', 'False')], validate_choice=False)
    consumer_first_name = SelectField('First Name', choices=[('True', 'True'), ('False', 'False')], validate_choice=False)
    consumer_last_name = SelectField('Last Name', choices=[('True', 'True'), ('False', 'False')], validate_choice=False)
    consumer_mobile_number = SelectField('Mobile #', choices=[('True', 'True'), ('False', 'False')], validate_choice=False)
    consumer_email = SelectField('Email', choices=[('True', 'True'), ('False', 'False')], validate_choice=False)
    zip_code = SelectField('Zipcode', choices=[('True', 'True'), ('False', 'False')], validate_choice=False)
    country = SelectField('Country', choices=[('True', 'True'), ('False', 'False')], validate_choice=False)
    state = SelectField('State', choices=[('True', 'True'), ('False', 'False')], validate_choice=False)
    address = SelectField('Address', choices=[('True', 'True'), ('False', 'False')], validate_choice=False)
    city = SelectField('City', choices=[('True', 'True'), ('False', 'False')], validate_choice=False)
    brand = SelectField('Brand', choices=[('True', 'True'), ('False', 'False')], validate_choice=False)
    total_lead_time = SelectField('Total Lead Time', choices=[('True', 'True'), ('False', 'False')], validate_choice=False)
    dealer_buffer_time = SelectField('Dealer Buffer Time', choices=[('True', 'True'), ('False', 'False')], validate_choice=False)
    est_deliver_time = SelectField('Estimated Delivery Time', choices=[('True', 'True'), ('False', 'False')], validate_choice=False)
    lead_time_parameter = SelectField('Lead Time Parameter', choices=[('True', 'True'), ('False', 'False')], validate_choice=False)
    buffer_time_parameter = SelectField('Buffer Time Parameter', choices=[('True', 'True'), ('False', 'False')], validate_choice=False)
    progress_timeline = SelectField('Progress', choices=[('True', 'True'), ('False', 'False')], validate_choice=False)
    preference_reply_back = SelectField('Reply Back', choices=[('True', 'True'), ('False', 'False')], validate_choice=False)
    order_notes = SelectField('Order Notes', choices=[('True', 'True'), ('False', 'False')], validate_choice=False)
    last_activity = SelectField('Last Activity', choices=[('True', 'True'), ('False', 'False')], validate_choice=False)
    order_completion_date = SelectField('Order Completion Date', choices=[('True', 'True'), ('False', 'False')], validate_choice=False)


#=====================================================Excel Uploader=======================================================
class excelFile(FlaskForm):
    excelip = FileField(validators=[FileRequired()])

#==================================Review Stars============================================================
class reviewStars(FlaskForm):
    num_of_stars = SelectField('Review', choices=[('0.5', '0.5'), ('1', '1'), ('1.5', '1.5'), ('2', '2'), ('2.5', '2.5'), ('3', '3'), ('3.5', '3.5'), ('4', '4'), ('4.5', '4.5'), ('5', '5')], validators=[InputRequired()])

#====================================================================================================================
class ConsumerFeedbackForm(FlaskForm):
    cust_feedback = TextAreaField('Text Area',render_kw={"placeholder": "Text Area"})
    option_1 = SelectField('option_1', choices=[('True', 'Yes'), ('False', 'No')], validate_choice=False)
    option_2 = SelectField('option_2', choices=[('True', 'Yes'), ('False', 'No')], validate_choice=False)
    option_3 = SelectField('option_3', choices=[('True', 'Yes'), ('False', 'No')], validate_choice=False)
    option_4 = SelectField('option_4', choices=[('True', 'Yes'), ('False', 'No')], validate_choice=False)
    option_5 = SelectField('option_5', choices=[('True', 'Yes'), ('False', 'No')], validate_choice=False)
#====================================================================================================================
class ReviewLinksSettingForm(FlaskForm):
    rw_link_name = StringField('Name',validators=[InputRequired()], render_kw={"placeholder": "Name"})
    rw_link_url = StringField('URL',validators=[InputRequired()], render_kw={"placeholder": "URL"})
    rw_link_label = StringField('Label',validators=[InputRequired()], render_kw={"placeholder": "Label"})

class reviewProductStars(FlaskForm):
    product_num_of_stars = SelectField('Review', choices=[('0.5', '0.5'), ('1', '1'), ('1.5', '1.5'), ('2', '2'), ('2.5', '2.5'), ('3', '3'), ('3.5', '3.5'), ('4', '4'), ('4.5', '4.5'), ('5', '5')], validators=[InputRequired()])
    opt_1 = SelectField('option_1', choices=[('True', 'Yes'), ('False', 'No')], validate_choice=False)
    opt_2 = SelectField('option_2', choices=[('True', 'Yes'), ('False', 'No')], validate_choice=False)
    opt_3 = SelectField('option_3', choices=[('True', 'Yes'), ('False', 'No')], validate_choice=False)
    opt_4 = SelectField('option_4', choices=[('True', 'Yes'), ('False', 'No')], validate_choice=False)
    opt_5 = SelectField('option_5', choices=[('True', 'Yes'), ('False', 'No')], validate_choice=False)
    opt_6 = SelectField('option_6', choices=[('True', 'Yes'), ('False', 'No')], validate_choice=False)
    opt_7 = SelectField('option_7', choices=[('True', 'Yes'), ('False', 'No')], validate_choice=False)
    opt_8 = SelectField('option_8', choices=[('True', 'Yes'), ('False', 'No')], validate_choice=False)
    prd_cmnts = TextAreaField('Feedback',validators=[InputRequired()], render_kw={"placeholder": "Feedback"})




#=================================================================================================================
class VendorInfoForm(FlaskForm):
    v_name = StringField('Name',validators=[InputRequired()], render_kw={"placeholder": "Supplier Name"})
    v_inds = StringField('Industry',validators=[InputRequired()], render_kw={"placeholder": "Industry"})
    v_cnumber = IntegerField('Mobile #', validators=[InputRequired()], render_kw={"placeholder": "Mobile Number"})
    v_email = EmailField('Email', validators=[InputRequired()], render_kw={"placeholder": "Email"})
    v_city = StringField('City',validators=[InputRequired()], render_kw={"placeholder": "City"})
    v_addrs = StringField('Address',validators=[InputRequired()], render_kw={"placeholder": "Address"})
    v_con = StringField('Country',validators=[InputRequired()], render_kw={"placeholder": "Country"})
    v_cname = StringField('Contact Name',validators=[InputRequired()], render_kw={"placeholder": "Contact Name"})
    v_zip = StringField('Zip Code', validators=[InputRequired()], render_kw={"placeholder": "Zip Code"})
    v_desc = TextAreaField('Description',validators=[InputRequired()], render_kw={"placeholder": "Description"})


class VendorEditInfoForm(FlaskForm):
    v_name = StringField('Name',validators=[InputRequired()], render_kw={"placeholder": "Supplier Name"})
    v_inds = StringField('Industry',validators=[InputRequired()], render_kw={"placeholder": "Industry"})
    v_cnumber = IntegerField('Mobile #', validators=[InputRequired()], render_kw={"placeholder": "Mobile Number"})
    v_email = EmailField('Email', validators=[InputRequired()], render_kw={"placeholder": "Email"})
    v_city = StringField('City',validators=[InputRequired()], render_kw={"placeholder": "City"})
    v_addrs = StringField('Address',validators=[InputRequired()], render_kw={"placeholder": "Address"})
    v_con = StringField('Country',validators=[InputRequired()], render_kw={"placeholder": "Country"})
    v_cname = StringField('Contact Name',validators=[InputRequired()], render_kw={"placeholder": "Contact Name"})
    v_zip = StringField('Zip Code', validators=[InputRequired()], render_kw={"placeholder": "Zip Code"})
    v_desc = TextAreaField('Description',validators=[InputRequired()], render_kw={"placeholder": "Description"})

class VendorUpdateInfoForm(FlaskForm):
    v_name = StringField('Name',validators=[InputRequired()], render_kw={"placeholder": "Supplier Name"})
    v_inds = StringField('Industry',validators=[InputRequired()], render_kw={"placeholder": "Industry"})
    v_cnumber = IntegerField('Mobile #', validators=[InputRequired()], render_kw={"placeholder": "Mobile Number"})
    v_email = EmailField('Email', validators=[InputRequired()], render_kw={"placeholder": "Email"})
    v_city = StringField('City',validators=[InputRequired()], render_kw={"placeholder": "City"})
    v_addrs = StringField('Address',validators=[InputRequired()], render_kw={"placeholder": "Address"})
    v_con = StringField('Country',validators=[InputRequired()], render_kw={"placeholder": "Country"})
    v_cname = StringField('Contact Name',validators=[InputRequired()], render_kw={"placeholder": "Contact Name"})
    v_zip = StringField('Zip Code', validators=[InputRequired()], render_kw={"placeholder": "Zip Code"})
    v_desc = TextAreaField('Description',validators=[InputRequired()], render_kw={"placeholder": "Description"})


class SearchVendorFormByCity(FlaskForm):
    searchbyCity = StringField('City', validators=[InputRequired()], render_kw={"placeholder": "City"})


class SearchVendorFormByConName(FlaskForm):
    searchbyCname = StringField('Contact Name', validators=[InputRequired()], render_kw={"placeholder": "Contact Name"})


class SearchVendorFormByConNumber(FlaskForm):
    searchbyCnum = IntegerField('Contact Number', validators=[InputRequired()], render_kw={"placeholder": "Contact Number"})

class SearchVendorFormByName(FlaskForm):
    searchbyName = StringField('Name', validators=[InputRequired()], render_kw={"placeholder": "Supplier Name"})

#===============================================Consumers========================================================================================
class ConsumerInfoForm(FlaskForm):
    c_fname = StringField('First Name',validators=[InputRequired()], render_kw={"placeholder": "First Name"})
    c_lname = StringField('Last Name', render_kw={"placeholder": "Last Name (Optional)"})
    c_mobile = IntegerField('Mobile #', validators=[InputRequired()], render_kw={"placeholder": "Mobile Number"})
    c_email = EmailField('Email', validators=[InputRequired()], render_kw={"placeholder": "Email"})
    c_dob = StringField('Date of Birth', render_kw={"placeholder": "Date of Birth (Optional)"})
    c_addrs = StringField('Address',validators=[InputRequired()], render_kw={"placeholder": "Address"})
    c_city = StringField('City',validators=[InputRequired()], render_kw={"placeholder": "City"})
    c_con = StringField('Country',validators=[InputRequired()], render_kw={"placeholder": "Country"})
    c_state = StringField('State',validators=[InputRequired()], render_kw={"placeholder": "State"})
    c_zip_code = StringField('Zipcode',validators=[InputRequired()], render_kw={"placeholder": "Zip Code"})
    c_user_type = SelectField('User Type', choices=[('Consumer', 'Consumer'), ('Business', 'Business')], validators=[InputRequired()])


class ConsumerInfoEditForm(FlaskForm):
    c_fname = StringField('First Name',validators=[InputRequired()], render_kw={"placeholder": "First Name"})
    c_lname = StringField('Last Name', render_kw={"placeholder": "Last Name (Optional)"})
    c_mobile = IntegerField('Mobile #', validators=[InputRequired()], render_kw={"placeholder": "Mobile Number"})
    c_email = EmailField('Email', validators=[InputRequired()], render_kw={"placeholder": "Email"})
    c_dob = StringField('Date of Birth', render_kw={"placeholder": "Date of Birth (Optional)"})
    c_addrs = StringField('Address',validators=[InputRequired()], render_kw={"placeholder": "Address"})
    c_city = StringField('City',validators=[InputRequired()], render_kw={"placeholder": "City"})
    c_con = StringField('Country',validators=[InputRequired()], render_kw={"placeholder": "Country"})
    c_state = StringField('State',validators=[InputRequired()], render_kw={"placeholder": "State"})
    c_zip_code = StringField('Zipcode',validators=[InputRequired()], render_kw={"placeholder": "Zip Code"})
    c_user_type = SelectField('User Type', choices=[('Consumer', 'Consumer'), ('Business', 'Business')], validators=[InputRequired()])

class ConsumerInfoUpdateForm(FlaskForm):
    c_fname = StringField('First Name',validators=[InputRequired()], render_kw={"placeholder": "First Name"})
    c_lname = StringField('Last Name', render_kw={"placeholder": "Last Name (Optional)"})
    c_mobile = IntegerField('Mobile #', validators=[InputRequired()], render_kw={"placeholder": "Mobile Number"})
    c_email = EmailField('Email', validators=[InputRequired()], render_kw={"placeholder": "Email"})
    c_dob = StringField('Date of Birth', render_kw={"placeholder": "Date of Birth (Optional)"})
    c_addrs = StringField('Address',validators=[InputRequired()], render_kw={"placeholder": "Address"})
    c_city = StringField('City',validators=[InputRequired()], render_kw={"placeholder": "City"})
    c_con = StringField('Country',validators=[InputRequired()], render_kw={"placeholder": "Country"})
    c_state = StringField('State',validators=[InputRequired()], render_kw={"placeholder": "State"})
    c_zip_code = StringField('Zipcode',validators=[InputRequired()], render_kw={"placeholder": "Zip Code"})
    c_user_type = SelectField('User Type', choices=[('Consumer', 'Consumer'), ('Business', 'Business')], validators=[InputRequired()])

class consumerexcelFile(FlaskForm):
    excelip = FileField(validators=[FileRequired()])


class SearchConsumerFormByCity(FlaskForm):
    searchbyCity = StringField('City', validators=[InputRequired()], render_kw={"placeholder": "City"})


class SearchConsumerFormByState(FlaskForm):
    searchbyState = StringField('State', validators=[InputRequired()], render_kw={"placeholder": "State"})


class SearchConsumerFormByMobile(FlaskForm):
    searchbyMobile = IntegerField('Mobile #', validators=[InputRequired()], render_kw={"placeholder": "Mobile Number"})

class SearchConsumerFormByFName(FlaskForm):
    searchbyFName = StringField('First Name', validators=[InputRequired()], render_kw={"placeholder": "First Name"})



#=========================================Contractors========================================================================================

class ContractorsInfoForm(FlaskForm):
    cont_fname = StringField('First Name',validators=[InputRequired()], render_kw={"placeholder": "First Name"})
    cont_lname = StringField('Last Name',validators=[InputRequired()], render_kw={"placeholder": "Last Name"})
    cont_mobile = IntegerField('Mobile #', validators=[InputRequired()], render_kw={"placeholder": "Mobile Number"})
    cont_email = EmailField('Email', validators=[InputRequired()], render_kw={"placeholder": "Email"})
    cont_addrs = StringField('Address',validators=[InputRequired()], render_kw={"placeholder": "Address"})
    cont_city = StringField('City',validators=[InputRequired()], render_kw={"placeholder": "City"})
    cont_con = StringField('Country',validators=[InputRequired()], render_kw={"placeholder": "Country"})
    cont_state = StringField('State',validators=[InputRequired()], render_kw={"placeholder": "State"})
    cont_zip = StringField('Zip Code', validators=[InputRequired()], render_kw={"placeholder": "Zip Code"})

class ContractorsInfoEditForm(FlaskForm):
    cont_fname = StringField('First Name',validators=[InputRequired()], render_kw={"placeholder": "First Name"})
    cont_lname = StringField('Last Name',validators=[InputRequired()], render_kw={"placeholder": "Last Name"})
    cont_mobile = IntegerField('Mobile #', validators=[InputRequired()], render_kw={"placeholder": "Mobile Number"})
    cont_email = EmailField('Email', validators=[InputRequired()], render_kw={"placeholder": "Email"})
    cont_addrs = StringField('Address',validators=[InputRequired()], render_kw={"placeholder": "Address"})
    cont_city = StringField('City',validators=[InputRequired()], render_kw={"placeholder": "City"})
    cont_con = StringField('Country',validators=[InputRequired()], render_kw={"placeholder": "Country"})
    cont_state = StringField('State',validators=[InputRequired()], render_kw={"placeholder": "State"})
    cont_zip = StringField('Zip Code', validators=[InputRequired()], render_kw={"placeholder": "Zip Code"})

class ContractorsInfoUpdateForm(FlaskForm):
    cont_fname = StringField('First Name',validators=[InputRequired()], render_kw={"placeholder": "First Name"})
    cont_lname = StringField('Last Name',validators=[InputRequired()], render_kw={"placeholder": "Last Name"})
    cont_mobile = IntegerField('Mobile #', validators=[InputRequired()], render_kw={"placeholder": "Mobile Number"})
    cont_email = EmailField('Email', validators=[InputRequired()], render_kw={"placeholder": "Email"})
    cont_addrs = StringField('Address',validators=[InputRequired()], render_kw={"placeholder": "Address"})
    cont_city = StringField('City',validators=[InputRequired()], render_kw={"placeholder": "City"})
    cont_con = StringField('Country',validators=[InputRequired()], render_kw={"placeholder": "Country"})
    cont_state = StringField('State',validators=[InputRequired()], render_kw={"placeholder": "State"})
    cont_zip = StringField('Zip Code', validators=[InputRequired()], render_kw={"placeholder": "Zip Code"})


class SearchContractorsFormByCity(FlaskForm):
    searchbyCity = StringField('City', validators=[InputRequired()], render_kw={"placeholder": "City"})


class SearchContractorsFormByState(FlaskForm):
    searchbyState = StringField('State', validators=[InputRequired()], render_kw={"placeholder": "State"})


class SearchContractorsFormByMobile(FlaskForm):
    searchbyMobile = IntegerField('Mobile #', validators=[InputRequired()], render_kw={"placeholder": "Mobile Number"})

class SearchContractorsFormByFName(FlaskForm):
    searchbyFName = StringField('First Name', validators=[InputRequired()], render_kw={"placeholder": "First Name"})


#================================================Custom Message for all sms services=================================================================================
class CustomOrdeEntryrMsg(FlaskForm):
    crt_odr_tb_1 = StringField('Enter Text', render_kw={"placeholder": "Text Box 1"})
    crt_odr_tb_2 = StringField('Enter Text', render_kw={"placeholder": "Text Box 2"})
    crt_odr_tb_3 = StringField('Enter Text', render_kw={"placeholder": "Text Box 3"})
    crt_odr_tb_4 = StringField('Enter Text', render_kw={"placeholder": "Text Box 4"})


class CustomOrdeEditingMsg(FlaskForm):
    crt_odr_ed_tb_1 = StringField('Enter Text', render_kw={"placeholder": "Text Box 1"})
    crt_odr_ed_tb_2 = StringField('Enter Text', render_kw={"placeholder": "Text Box 2"})
    crt_odr_ed_tb_3 = StringField('Enter Text', render_kw={"placeholder": "Text Box 3"})

class CustomOrdeLeadTimeChangeMsg(FlaskForm):
    crt_odr_ld_tb_1 = StringField('Enter Text', render_kw={"placeholder": "Text Box 1"})
    crt_odr_ld_tb_2 = StringField('Enter Text', render_kw={"placeholder": "Text Box 2"})
    crt_odr_ld_tb_3 = StringField('Enter Text', render_kw={"placeholder": "Text Box 3"})
    crt_odr_ld_tb_4 = StringField('Enter Text', render_kw={"placeholder": "Text Box 4"})

class CustomOrdeBufferTimeChangeMsg(FlaskForm):
    crt_odr_bf_tb_1 = StringField('Enter Text', render_kw={"placeholder": "Text Box 1"})
    crt_odr_bf_tb_2 = StringField('Enter Text', render_kw={"placeholder": "Text Box 2"})
    crt_odr_bf_tb_3 = StringField('Enter Text', render_kw={"placeholder": "Text Box 3"})
    crt_odr_bf_tb_4 = StringField('Enter Text', render_kw={"placeholder": "Text Box 4"})

class CustomOrdeProgressTimeLineChangeMsg(FlaskForm):
    crt_odr_pglt_tb_1 = StringField('Enter Text', render_kw={"placeholder": "Text Box 1"})
    crt_odr_pglt_tb_2 = StringField('Enter Text', render_kw={"placeholder": "Text Box 2"})
    crt_odr_pglt_tb_3 = StringField('Enter Text', render_kw={"placeholder": "Text Box 3"})

class CustomRedButtonLeadTimeChangeMsg(FlaskForm):
    crt_rbtnld_tb_2 = StringField('Enter Text', render_kw={"placeholder": "Text Box 1"})
    crt_rbtnld_tb_3 = StringField('Enter Text', render_kw={"placeholder": "Text Box 2"})
    crt_rbtnld_tb_4 = StringField('Enter Text', render_kw={"placeholder": "Text Box 3"})

class CustomRedButtonBufferTimeChangeMsg(FlaskForm):
    crt_rbtnlbfrd_tb_2 = StringField('Enter Text', render_kw={"placeholder": "Text Box 1"})
    crt_rbtnlbfrd_tb_3 = StringField('Enter Text', render_kw={"placeholder": "Text Box 2"})
    crt_rbtnlbfrd_tb_4 = StringField('Enter Text', render_kw={"placeholder": "Text Box 3"})

class CustomConsumerReviewMsg(FlaskForm):
    crt_cstnreview_tb_1 = StringField('Enter Text', render_kw={"placeholder": "Text Box 1"})
    crt_cstnreview_tb_2 = StringField('Enter Text', render_kw={"placeholder": "Text Box 2"})

class CustomConsumerProductReviewMsg(FlaskForm):
    crt_cstn_prodreview_tb_1 = StringField('Enter Text', render_kw={"placeholder": "Text Box 1"})
    crt_cstn_prodreview_tb_2 = StringField('Enter Text', render_kw={"placeholder": "Text Box 2"})

class CustomRedbtnProgressTimeLineChangeMsg(FlaskForm):
    crt_redbtn_pglt_tb_1 = StringField('Enter Text', render_kw={"placeholder": "Text Box 1"})
    crt_redbtn_pglt_tb_2 = StringField('Enter Text', render_kw={"placeholder": "Text Box 2"})
    crt_redbtn_pglt_tb_3 = StringField('Enter Text', render_kw={"placeholder": "Text Box 3"})
    crt_redbtn_pglt_tb_4 = StringField('Enter Text', render_kw={"placeholder": "Text Box 4"})

class CustomWelcomeMessageMsg(FlaskForm):
    crt_wlcmmsg_tb_1 = TextAreaField('Enter Text', render_kw={"placeholder": "Message"})

#==================================================Custom Message for all Email services===========================================================================================

class CustomOrdeEntryrMail(FlaskForm):
    crt_odr_mail_tb_1 = StringField('Enter Text', render_kw={"placeholder": "Subject"})
    crt_odr_mail_tb_2 = StringField('Enter Text', render_kw={"placeholder": "Salutaion"})
    crt_odr_mail_tb_3 = StringField('Enter Text', render_kw={"placeholder": "Message"})
    crt_odr_mail_tb_4 = StringField('Enter Text', render_kw={"placeholder": "Regards"})


class CustomOrdeEditingMail(FlaskForm):
    crt_odr_mail_ed_tb_1 = StringField('Enter Text', render_kw={"placeholder": "Subject"})
    crt_odr_mail_ed_tb_2 = StringField('Enter Text', render_kw={"placeholder": "Salutaion"})
    crt_odr_mail_ed_tb_3 = StringField('Enter Text', render_kw={"placeholder": "Message"})
    crt_odr_mail_ed_tb_4 = StringField('Enter Text', render_kw={"placeholder": "Regards"})

class CustomOrdeLeadTimeChangeMail(FlaskForm):
    crt_odr_mail_ld_tb_1 = StringField('Enter Text', render_kw={"placeholder": "Subject"})
    crt_odr_mail_ld_tb_2 = StringField('Enter Text', render_kw={"placeholder": "Salutaion"})
    crt_odr_mail_ld_tb_3 = StringField('Enter Text', render_kw={"placeholder": "Message"})
    crt_odr_mail_ld_tb_4 = StringField('Enter Text', render_kw={"placeholder": "Regards"})

class CustomOrdeBufferTimeChangeMail(FlaskForm):
    crt_odr_mail_bf_tb_1 = StringField('Enter Text', render_kw={"placeholder": "Subject"})
    crt_odr_mail_bf_tb_2 = StringField('Enter Text', render_kw={"placeholder": "Salutaion"})
    crt_odr_mail_bf_tb_3 = StringField('Enter Text', render_kw={"placeholder": "Message"})
    crt_odr_mail_bf_tb_4 = StringField('Enter Text', render_kw={"placeholder": "Regards"})

class CustomOrdeProgressTimeLineChangeMail(FlaskForm):
    crt_odr_mail_pglt_tb_1 = StringField('Enter Text', render_kw={"placeholder": "Subject"})
    crt_odr_mail_pglt_tb_2 = StringField('Enter Text', render_kw={"placeholder": "Salutaion"})
    crt_odr_mail_pglt_tb_3 = StringField('Enter Text', render_kw={"placeholder": "Message"})
    crt_odr_mail_pglt_tb_4 = StringField('Enter Text', render_kw={"placeholder": "Regards"})


class CustomRedButtonLeadTimeChangeMail(FlaskForm):
    crt_rbtnld_mail_tb_1 = StringField('Enter Text', render_kw={"placeholder": "Subject"})
    crt_rbtnld_mail_tb_2 = StringField('Enter Text', render_kw={"placeholder": "Salutaion"})
    crt_rbtnld_mail_tb_3 = StringField('Enter Text', render_kw={"placeholder": "Message"})
    crt_rbtnld_mail_tb_4 = StringField('Enter Text', render_kw={"placeholder": "Regards"})

class CustomRedButtonBufferTimeChangeMail(FlaskForm):
    crt_rbtnlbfrd_mail_tb_1 = StringField('Enter Text', render_kw={"placeholder": "Subject"})
    crt_rbtnlbfrd_mail_tb_2 = StringField('Enter Text', render_kw={"placeholder": "Salutaion"})
    crt_rbtnlbfrd_mail_tb_3 = StringField('Enter Text', render_kw={"placeholder": "Message"})
    crt_rbtnlbfrd_mail_tb_4 = StringField('Enter Text', render_kw={"placeholder": "Regards"})

class CustomConsumerReviewMail(FlaskForm):
    crt_cstnreview_mail_tb_1 = StringField('Enter Text', render_kw={"placeholder": "Subject"})
    crt_cstnreview_mail_tb_2 = StringField('Enter Text', render_kw={"placeholder": "Salutaion"})
    crt_cstnreview_mail_tb_3 = StringField('Enter Text', render_kw={"placeholder": "Message"})

class CustomConsumerProductReviewMail(FlaskForm):
    crt_cstn_prodreview_mail_tb_1 = StringField('Enter Text', render_kw={"placeholder": "Subject"})
    crt_cstn_prodreview_mail_tb_2 = StringField('Enter Text', render_kw={"placeholder": "Salutaion"})
    crt_cstn_prodreview_mail_tb_3 = StringField('Enter Text', render_kw={"placeholder": "Message"})

class CustomRedbtnProgressTimeLineChangeMail(FlaskForm):
    crt_rbtnpglt_mail_tb_1 = StringField('Enter Text', render_kw={"placeholder": "Subject"})
    crt_rbtnpglt_mail_tb_2 = StringField('Enter Text', render_kw={"placeholder": "Salutaion"})
    crt_rbtnpglt_mail_tb_3 = StringField('Enter Text', render_kw={"placeholder": "Message"})
    crt_rbtnpglt_mail_tb_4 = StringField('Enter Text', render_kw={"placeholder": "Regards"})

class CustomWelcomeMessageMail(FlaskForm):
    crt_wlcmmsg_mail_tb_1 = StringField('Enter Text', render_kw={"placeholder": "Subject"})
    crt_wlcmmsg_mail_tb_2 = TextAreaField('Enter Text', render_kw={"placeholder": "Message"})

#================================================redbutton in WForder=================================================================================
class RedButtonWFOrderForm(FlaskForm):
    cstm_msg_ids = StringField('Order IDs', render_kw={"placeholder": "Order IDs"})
    mail_subject = StringField('Subject', validators=[InputRequired()], render_kw={"placeholder": "Subject"})
    sub_ject = SelectField('Subject', choices=[('Related to Manufacturing', 'Related to Manufacturing'), ('Related to Site-Check', 'Related to Site-Check'), ('Related to Dealer', 'Related to Dealer'), ('Related to Consumer', 'Related to Consumer'), ('Related to Delivery', 'Related to Delivery')], validators=[InputRequired()])
    send_type = SelectField('', choices=[('SMS', 'SMS'), ('Email & SMS', 'Email & SMS')], validators=[InputRequired()])
    msg = TextAreaField('Message',validators=[InputRequired()], render_kw={"placeholder": "Message"})

class RedButtonWFLeadTime(FlaskForm):
    cst_leadtm_ids = StringField('Order IDs', validators=[InputRequired()], render_kw={"placeholder": "Order IDs"})
    cal_lead_type = SelectField('Lead Type', choices=[('increase', 'increase'), ('decrease', 'decrease')], validators=[InputRequired()])
    ttl_lt = IntegerField('Lead Time', validators=[InputRequired()], render_kw={"placeholder": "Lead Time (in weeks)"})
    cst_leadtm_reason = TextAreaField('Reason',validators=[InputRequired()], render_kw={"placeholder": "Reason"})


class RedButtonWFBufferTime(FlaskForm):
    cstm_bfrtm_ids = StringField('Order IDs', validators=[InputRequired()], render_kw={"placeholder": "Order IDs"})
    cal_buffer_type = SelectField('Buffer Type', choices=[('increase', 'increase'), ('decrease', 'decrease')], validators=[InputRequired()])
    dlr_bfr_tm = IntegerField('Buffer Time', validators=[InputRequired()], render_kw={"placeholder": "Buffer Time (in weeks)"})
    cst_bfrtm_reason = TextAreaField('Reason',validators=[InputRequired()], render_kw={"placeholder": "Reason"})

#================================================================================================================
class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class CheckboxForRedBtn(FlaskForm):
    nexus_id_checkbox = MultiCheckboxField("Order IDs")

class CheckboxForBulkPgrstimeline(FlaskForm):
    nexus_id_cbox = MultiCheckboxField("Order IDs")
#----------------------------------------------------------------------------------------------------------
class RedButtonWFOrderpgrogressTimelineForm(FlaskForm):
    cstm_nex_ids = StringField('Order IDs', render_kw={"placeholder": "Order IDs"})
    pgrs_stage_name = SelectField('progress', choices=[], validators=[InputRequired()])

#========================================================================================================
class ReviewPageCutomization(FlaskForm):
    review_page_heading = StringField('Review Heading',render_kw={"placeholder": "Header"})
    review_page_textarea = TextAreaField('Text Area',render_kw={"placeholder": "Text Area"})

#========================================================================================================
class ProductReviewPageCutomization(FlaskForm):
    product_review_page_heading = StringField('Review Heading',render_kw={"placeholder": "Header"})
    product_review_page_textarea = TextAreaField('Text Area',render_kw={"placeholder": "Text Area"})

#====================================================================================================================
class ReviewConsumerFeedbackPageCutomization(FlaskForm):
    feedbak_page_heading = StringField('Review Heading',render_kw={"placeholder": "Header"})
    feedback_page_textarea = TextAreaField('Text Area',render_kw={"placeholder": "Text Area"})

#====================================================================================================================
class ReviewConsumerFeedbackPageCutomizationForFourandMore(FlaskForm):
    fdbk_page_heading = StringField('Review Heading',render_kw={"placeholder": "Header"})
    fdbk_page_textarea = TextAreaField('Text Area',render_kw={"placeholder": "Text Area"})

#====================================================================================================================
class CovidPrecautionaryMessageForm(FlaskForm):
    covd_page_heading = StringField('Header',render_kw={"placeholder": "Header"})
    covd_page_textarea = TextAreaField('Text Area',render_kw={"placeholder": "Description"})

#==================================================================================================================

# Login required
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username_retailer' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap


@app.route("/logout/")
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))


# Login Section
@app.route("/login/")
def login():
    user_exists_flag = False
    if 'username_retailer' in session:
        user_exists_flag = True
        session['rPerPage'] = config['page_count']['RECORDS_PER_PAGE']
        session['defaultPage'] = config['page_count']['DEFAULT_PAGE']
        session['totalPages'] = 0

        session['search_activated_Wfdol'] = False
        session['Wfdol_records'] = []
        session['searched_wfdol_page_no'] = ''
        session['searched_wfdol_page_term'] = ''
        session['count_dolwfUser'] = 0
        session['job_name'] = ''
        session['wf_first_name'] = ''
        session['wf_last_name'] = ''
        session['wfcity'] = ''
        session['wfcity'] = ''
        session['wfstate'] = ''
        session['wf_type'] = ''

        session['search_activated_consumer'] = False
        session['consumer_records'] = []
        session['searched_consumer_page_no'] = ''
        session['searched_consumer_page_term'] = ''
        session['count_Users'] = 0
        session['consumer_monum'] = 0
        session['consumer_city'] = ''
        session['consumer_state'] = ''
        session['consumer_fname'] = ''

        session['search_activated_contractor'] = False
        session['contractor_records'] = []
        session['searched_contractor_page_no'] = ''
        session['searched_contractor_page_term'] = ''
        session['count_contractor'] = 0
        session['contractor_monum'] = 0
        session['contractor_city'] = ''
        session['contractor_state'] = ''
        session['contractor_fname'] = ''

        session['search_activated_vendor'] = False
        session['vendor_records'] = []
        session['searched_vendor_page_no'] = ''
        session['searched_vendor_page_term'] = ''
        session['count_vendor'] = 0
        session['vendor_monum'] = 0
        session['vendor_city'] = ''
        session['vendor_state'] = ''
        session['vendor_fname'] = ''
        return redirect(url_for('WF_orderWrapper'))
    else:
        return render_template('login.html', user = '', user_exists = user_exists_flag)


@app.route("/login/attempt", methods=['POST'])
def login_attempt():
    db_id = ''
    db_pass = ''
    retailer_db = ''
    db_auth_data = {}
    active_list = []
    incorrect_pass_flag = False

    login_id = request.form['e_mail'].strip()
    print(login_id)
    login_pass = request.form['pass_word'].strip()
    print(login_pass)
    print("=============================================================")
    
    cursor = DOL_DB.search_authorization_by_id(login_id)
    for c in cursor:
        db_auth_data = c

    dealer_id = db_auth_data["org_id"]
    active_cur = DOL_DB.get_account_activation_status_details(dealer_id)
    for d in active_cur:
        active_list.append(d)
    print("-----------------------------active list: ",active_list)

    if db_auth_data:
        print("------------------------------True")
        if sha256_crypt.verify(login_pass, db_auth_data['password']):
            if active_list:
                print("-----------------------------------------active ture")
                session['username_retailer'] = db_auth_data['first_name']
                print(session['username_retailer'])
                session['fullname_retailer'] = db_auth_data['first_name'] + " " + db_auth_data['last_name']
                session['org_retailer'] = db_auth_data['org_name']
                session['email_retailer'] = db_auth_data['user_email']
                session['userId_retailer'] = db_auth_data['user_id']
                session['userType_retailer'] = db_auth_data['user_type']
                session['orgId_retailer'] = db_auth_data['org_id']
                session['phonenum_retailer'] = db_auth_data['user_contact']
                session.pop('_flashes', None)
            else:
                incorrect_pass_flag = True
                return render_template('login.html', incorrect_pass_flag = incorrect_pass_flag)
        else:
            incorrect_pass_flag = True
            return render_template('login.html', incorrect_pass_flag = incorrect_pass_flag)
    else:
        incorrect_pass_flag = True
        return render_template('login.html', incorrect_pass_flag = incorrect_pass_flag)
    return redirect(url_for('login'))

@app.route("/reset_form", methods=['GET'])
def resetWrapper():
    print("========================inside reset wrapper")
    form = ResetPasswordForm()
    return render_template('resetpassword_form.html',
                            form = form,
                            formclass = 'form-control')


@app.route('/reset_password', methods=['POST'])
def reset_password():
    checkForMail = []
    check=[]
    incorrect_credentials_flag = False
    email = request.form['reset_email'].strip()
    phone = request.form['phone_num'].strip()
    check_for_pw = DOL_DB.check_password(email)

    for c in check_for_pw:
        checkForMail.append(c)
    print(checkForMail)

    if checkForMail :
        if checkForMail[0]['user_contact'] == phone:
            newPass = generate_id(4, 2)
            newPass_en = sha_encryption(newPass)
            for check in checkForMail:
                check['password']  = newPass_en

            org = checkForMail[0]['first_name']
            phone_num = checkForMail[0]['user_contact']
            print("===============================================")
            print(phone_num)
            print("===============================================")
            DOL_DB.update_one_password(email, check)
            #send_to_sms(newPass, newPass, org)
            sendSms.send_consumer_new_reset_creds_by_msg(newPass,phone_num,org)
            sendMail.send_consumer_new_reset_creds_by_mail(newPass,email,org)
            flash('Successfully reset the password')
        else:
            print("```````````````````````````````````````````````")
            incorrect_credentials_flag = True
            return render_template('login.html', incorrect_pass_flag = incorrect_credentials_flag)

    else:
        print("**********************************************")
        incorrect_credentials_flag = True
        return render_template('login.html', incorrect_pass_flag = incorrect_credentials_flag)
    return redirect(url_for('login'))



#=================================================================================================================================================================
def generate_id(letters_count, digits_count):
	sample_str = ''.join((random.choice(string.ascii_letters) for i in range(letters_count)))
	sample_str += ''.join((random.choice(string.digits) for i in range(digits_count)))
	sample_list = list(sample_str)
	final_string = ''.join(sample_list)
	return final_string

def generate_workflow_id(letters_count, digits_count):
    sample_str = ''.join((random.choice(string.ascii_uppercase) for i in range(letters_count)))
    sample_str += ''.join((random.choice(string.digits) for i in range(digits_count)))
    sample_list = list(sample_str)
    final_string = ''.join(sample_list)
    return final_string

#Password Encryption
def sha_encryption(un_encrypted_password):
	encrypted_password = sha256_crypt.encrypt(un_encrypted_password)
	return encrypted_password

def generate_activation_token(letters_count, digits_count):
  sample_str = ''.join((random.choice(string.ascii_letters) for i in range(letters_count)))
  sample_str += ''.join((random.choice(string.digits) for i in range(digits_count)))
  sample_list = list(sample_str)
  final_string = ''.join(sample_list)

  return final_string


# def send_to_sms(password,phone, org):
# 	message_info = {}
# 	message_info['number'] = phone
# 	message_info['message'] = "Welcome to " + org + ", Your password is : " + password
# 	sendSms.send_msg(message_info)
# 	return

#================================================================================================================
# @app.route("/index")
# @login_required
# def index():
# 	garage_door_designer = True
# 	return render_template('DOL_orderform_workflow.html',
# 							garage_door_designer = garage_door_designer)

@app.route("/index")
@login_required
def index():
    now = datetime.today()
    new_date = []
    final_stage_list = []
    progs_time_line_list = []
    order_value_list = []
    order_cost_list = []
    sum_of_all_price = 0.00

    email_list = []
    order_date_list = []
    open_orders_list = []

    sum_of_order_completed_prices_today = 0.00
    sum_of_order_completed_prices_month = 0.00
    sum_of_order_completed_prices_year = 0.00
    sum_of_order_entered_prices_today = 0.00


    order_completion_date_list = []
    order_val_list = []
    order_val_list_for_a_month = []
    order_val_list_for_a_year = []
    order_val_list_entered_today = []

    d = now.strftime("%Y, %b, %d")
    
    new_date = d.split(',')
    year = new_date[0].strip()
    month = new_date[1].strip()

    open_orders_count = 0
    open_orders_cursor = ''
    order_val_cur = ''
    order_val_cur_per_month = ''
    order_val_cur_per_year = ''
    order_val_cur_entred_today = ''
    order_val_cur_entred_today_count = 0

    orders_count = DOL_DB.get_wforder_count()
    emails_count = DOL_DB.get_dealer_email_logs_per_month(year,month)
    sms_count = DOL_DB.get_dealer_sms_logs_per_month(year,month)
    total_logs_count = DOL_DB.get_dealer_logs_per_month(year,month)
    print("total_logs_count: ",total_logs_count)

    order_cusr = DOL_DB.get_wforder_details()
    for i in order_cusr:
        progs_time_line_list.append(i['progress_timeline'])
        order_date_list.append(i['order_date'])

        if i['final_work_flow_stages']:
            final_stage_list.append(i['final_work_flow_stages'])
        if i['order_completion_date']:
            order_completion_date_list.append(i['order_completion_date'])


    for p, f in zip(progs_time_line_list,final_stage_list):
        if p!=f:
            open_orders_count = DOL_DB.get_wforder_open_orders_using_p(p)
            open_orders_cursor = DOL_DB.get_wforder_details_using_p(p)



    # for o in order_completion_date_list:
    #     if not o:
    #         open_orders_count = DOL_DB.get_wforder_count_using_o(o)

    #         #pass
    #     else:
    #         open_orders_count = DOL_DB.get_wforder_count_using_o(o)

    # for x in open_orders_cursor:
    #     open_orders_list.append(x)
    
    # length_open_orders = len(open_orders_list)
    
    # print("o else oooooooooooooooooooooooooooooooooooooooooooooooooooooo: ",length_open_orders)
    #         #open_orders_cursor = DOL_DB.get_wforder_details_using_o(o)

    for ords in open_orders_cursor:
        order_value_list.append(ords['order_price'])

    print("======================order_value_list: ",order_value_list)

    for x in order_value_list:
        sum_of_all_price = sum_of_all_price + float(x)

    new_now = now.strftime("%Y %b %d")
    new_now_date = now.strftime("%m-%d-%Y")

    new_now_list = new_now.split(' ')
    curr_year = new_now_list[0]
    curr_month = new_now_list[1]

    if order_completion_date_list:
        for dt in order_completion_date_list:
            if dt:
                new_dt = dt.split(' ')
                cur_year = new_dt[0]
                cur_mon = new_dt[1]

                if dt == new_now:
                    order_val_cur = DOL_DB.get_wforder_details_using_todays_date(dt)

                if cur_mon == curr_month:
                    order_val_cur_per_month = DOL_DB.get_wforder_details_using_current_month(cur_mon)

                if cur_year == curr_year:
                    order_val_cur_per_year = DOL_DB.get_wforder_details_using_current_year(cur_year)

    
        for dat in order_val_cur:
            order_val_list.append(float(dat['order_price']))

        for sm in order_val_list:
            sum_of_order_completed_prices_today = sum_of_order_completed_prices_today + sm


        for val in order_val_cur_per_month:
            order_val_list_for_a_month.append(float(val['order_price']))

        for sm_month in order_val_list_for_a_month:
            sum_of_order_completed_prices_month = sum_of_order_completed_prices_month + sm_month


    for yr_val in order_val_cur_per_year:
        order_val_list_for_a_year.append(float(yr_val['order_price']))

    for sm_year in order_val_list_for_a_year:
        sum_of_order_completed_prices_year = sum_of_order_completed_prices_year + sm_year



    for or_date in order_date_list:
        if or_date == new_now_date:
            order_val_cur_entred_today = DOL_DB.get_wforder_details_todays_date(or_date)
            order_val_cur_entred_today_count = DOL_DB.get_wforder_details_todays_date_count(or_date)


    for od_pc in order_val_cur_entred_today:
        order_val_list_entered_today.append(float(od_pc['order_price']))

    for or_sm_val in order_val_list_entered_today:
        sum_of_order_entered_prices_today = sum_of_order_entered_prices_today + or_sm_val


    return render_template('home.html',
                            orders_count = orders_count,
                            emails_count = emails_count,
                            total_logs_count = total_logs_count,
                            sms_count = sms_count,
                            email_list = email_list,
                            sum_of_all_price = sum_of_all_price,
                            open_orders_count = open_orders_count,
                            sum_of_order_completed_prices_today = sum_of_order_completed_prices_today,
                            sum_of_order_completed_prices_month = sum_of_order_completed_prices_month,
                            sum_of_order_completed_prices_year = sum_of_order_completed_prices_year,
                            sum_of_order_entered_prices_today = sum_of_order_entered_prices_today,
                            order_val_cur_entred_today_count = order_val_cur_entred_today_count
                            )


#===================================Workflow One On One Communication======================================================================
@app.route("/wf_communication_log/<url_params>", methods=['GET'])
@login_required
def workflow_one_on_one_communication(url_params):
    form_wf_comm = WF_OneOnOneCommunication()
    formclass = 'form-control'

    #wrkflw_stage_names = []
    wf_orders_list = []

    parameters = url_params.split('_')
    n_id = parameters[0]
    po_no = parameters[1]
    wf_type = parameters[2]

    wrkfl_cursor = DOL_DB.get_workflow_stage_from_order(wf_type)
    for k in wrkfl_cursor:
        wf_orders_list.append(k)

    wrkflw_stage_names = wf_orders_list[0]["work_flow_stages"]
    

    print("wrkflw_stage_names---- : ",wrkflw_stage_names)

    form_wf_comm.subject.choices = wrkflw_stage_names
    print("form_wf_comm.subject.choices---- : ",form_wf_comm.subject.choices)



    log_recs = []
    log_cur = DOL_DB.get_all_logs_for_specific_po(n_id)
    for l in log_cur:
        log_recs.append(l)
    print(log_recs)
    return render_template('wf_communication_form.html',
                            form_wf_comm = form_wf_comm,
                            formclass = formclass,
                            log_recs=log_recs,
                            n_id = n_id,
                            po_no = po_no,
                            wf_type = wf_type,
                            user = session['username_retailer'],
                            org = session['org_retailer'])

@app.route("/wf_save_logs/<nid>/<po_no>/<wf_type>", methods=['POST'])
def wf_save_communication_logs(nid,po_no,wf_type):
    print("INSIDE SAVE ONE ONE ONE")
    form_wf_comm = WF_OneOnOneCommunication()
    formclass = 'form-control'
    communication_Info = {}
    communication_Info_Email = {}
    order_list = []
    wf_orders_list = []

    last_acti_list = []

    url_params = nid + '_' + po_no + '_' + wf_type
    print("--------url_params : ",url_params)

    wrkfl_cursor = DOL_DB.get_workflow_stage_from_order(wf_type)
    for k in wrkfl_cursor:
        wf_orders_list.append(k)

    wrkflw_stage_names = wf_orders_list[0]["work_flow_stages"]
    

    print("wrkflw_stage_names---- : ",wrkflw_stage_names)

    form_wf_comm.subject.choices = wrkflw_stage_names
    print("form_wf_comm.subject.choices---- : ",form_wf_comm.subject.choices)

    if form_wf_comm.validate_on_submit():
        print("Inside if")
        order_cur = DOL_DB.get_one_wforder_detail(nid)

        for o in order_cur:
            order_list.append(o)
        print(order_list)
        
        consumer_phone = order_list[0]['consumer_mobile_number']
        consumer_email = order_list[0]['consumer_email']
        communication_log_id = generate_id(4,2)
        currentDT = datetime.today()
        current_log_datetime = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")

        subject = request.form.get('subject')
        sending_mode = request.form.get('send_type')
        message_plain_text = request.form['msg']

        communication_Info['communication_log_id'] = communication_log_id.strip()
        communication_Info['nexus_id'] = nid.strip()
        communication_Info['po_number'] = po_no.strip()
        communication_Info['logger_id'] = session['orgId_retailer']
        communication_Info['logger_name'] = session['fullname_retailer']
        communication_Info['logger_type'] = "Dealer".strip()
        communication_Info['subject'] = subject
        communication_Info['sending_mode'] = "SMS".strip()
        communication_Info['message_plain_text'] = message_plain_text
        communication_Info['current_log_datetime'] = current_log_datetime.strip()
        communication_Info['action_taken'] = "".strip()


        communication_Info_Email['communication_log_id'] = communication_log_id.strip()
        communication_Info_Email['nexus_id'] = nid.strip()
        communication_Info_Email['po_number'] = po_no.strip()
        communication_Info_Email['logger_id'] = session['orgId_retailer']
        communication_Info_Email['logger_name'] = session['fullname_retailer']
        communication_Info_Email['logger_type'] = "Dealer".strip()
        communication_Info_Email['subject'] = subject
        communication_Info_Email['sending_mode'] = "Email".strip()
        communication_Info_Email['message_plain_text'] = message_plain_text
        communication_Info_Email['current_log_datetime'] = current_log_datetime.strip()
        communication_Info_Email['action_taken'] = "".strip()

        print('===================================================')
        print(communication_Info)

        if sending_mode == 'SMS':
            sendSms.send_log_msg(consumer_phone,communication_Info)
            DOL_DB.save_communication_logs(communication_Info)
        else:
            sendSms.send_log_msg(consumer_phone,communication_Info)
            DOL_DB.save_communication_logs(communication_Info)
            sendMail.send_to_mail(consumer_email,communication_Info)
            DOL_DB.save_communication_logs(communication_Info_Email)
        

        currentDT = datetime.today()
        current_datetime_for_last_activity = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")

        last_acti_cur = DOL_DB.get_one_wforder_detail(nid)
        for la in last_acti_cur:
            last_acti_list.append(la)

        last_activity = last_acti_list[0]['last_activity']

        print("==================================================")
        print(last_activity)
        print("==================================================")

        last_activity = current_datetime_for_last_activity
        print(last_activity)

        DOL_DB.update_last_activity_of_an_order_change(nid,last_activity)
    print(form_wf_comm.errors)
    return redirect(url_for('workflow_one_on_one_communication',url_params = url_params))


#===========================================Work Flow ===============================================================================


@app.route("/save_workflow_logs", methods=['POST'])
@login_required
def save_workflow_records():
    form_wrkflw = WorkFlowCreate()
    formclass = 'form-control'
    wrk_flowInfo = {}

    if form_wrkflw.validate_on_submit():
        work_flow_id = generate_workflow_id(4,3)
        currentDT = datetime.today()
        date_time = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")
        request_automated_reviews = request.form['send_review_link']
        work_flow_name = request.form['wrk_flw'].strip()
        work_flow_name_disable = True
        work_flow_stage_list = []

        wrk_flowInfo['work_flow_id'] = work_flow_id.strip()
        wrk_flowInfo['request_automated_reviews'] = request_automated_reviews.strip()
        wrk_flowInfo['work_flow_name'] = work_flow_name.strip()
        wrk_flowInfo['work_flow_stages'] = work_flow_stage_list
        wrk_flowInfo['work_flow_name_disable'] = work_flow_name_disable
        wrk_flowInfo['work_flow_name_identity_parameter'] = "Original".strip()
        wrk_flowInfo['work_flow_created_by'] = session['fullname_retailer'].strip()
        wrk_flowInfo['work_flow_created_time'] = date_time.strip()
        print(wrk_flowInfo)
        DOL_DB.save_workflow_structure(wrk_flowInfo)
    print(form_wrkflw.errors)
    return redirect(url_for('custom_viewWrapper'))


@app.route("/edit_workflow/<wf_id>", methods=['POST','GET'])
@login_required
def edit_work_flow_records(wf_id):
    form_wrkflow_name_Edit = WorkFlowNameEdit()
    form_wrkflw_Edit = WorkFlowEdit()
    formclass = 'form-control'
    wf_stage_list = []
    wfs_cursor = DOL_DB.get_workflow_data_by_one_wrkflw_id(wf_id)
    for s in wfs_cursor:
        wf_stage_list.append(s)
    
    form_wrkflow_name_Edit.wrk_flw.data = wf_stage_list[0]['work_flow_name']
    #wrkflw_name = wf_stage_list[0]['work_flow_name']
    stage_name = wf_stage_list[0]['work_flow_stages']
    work_flow_name_identity_parameter = wf_stage_list[0]['work_flow_name_identity_parameter']
    return render_template('workflow_edit.html',
                            wf_ID = wf_id,
                            #wrkflw_name = wrkflw_name,
                            form_wrkflw_Edit = form_wrkflw_Edit,
                            form_wrkflow_name_Edit = form_wrkflow_name_Edit,
                            work_flow_name_identity_parameter = work_flow_name_identity_parameter,
                            formclass = formclass,
                            stageName = stage_name)


@app.route("/update_wrkflw_name/<wf_ID>", methods=['POST'])
@login_required
def update_work_flow_name(wf_ID):
    form_wrkflow_name_Edit = WorkFlowNameEdit()
    formclass = 'form-control'

    if form_wrkflow_name_Edit.validate_on_submit():
        work_flow_name = request.form['wrk_flw'].strip()
        DOL_DB.update_workflow_name(wf_ID,work_flow_name)
    return redirect(url_for('edit_work_flow_records',wf_id = wf_ID))




@app.route("/add_stages/<wf_ID>", methods=['POST'])
@login_required
def update_work_flow_stage(wf_ID):
    form_wrkflw_Edit = WorkFlowEdit()
    formclass = 'form-control'
    wf_list = []
    wf_Disc = {}

    if form_wrkflw_Edit.validate_on_submit():
        stage_name = request.form['sta_ges'].strip()
        print(stage_name)

        wf_cursor = DOL_DB.get_workflow_data_by_one_wrkflw_id(wf_ID)
        for k in wf_cursor:
            wf_list.append(k)
        
        wrkflw_disable = wf_list[0]['work_flow_name_disable']
        print("--------Before-----------wrkflw_disable : ",wrkflw_disable)

        wrkflw_disable = False
        print("---------After----------wrkflw_disable : ",wrkflw_disable)

        
        print(wf_list[0]['work_flow_stages'])
        wf_stages = wf_list[0]['work_flow_stages']
        wf_stages.append(stage_name)
        print('------------------------')
        print(wf_stages)
        
        wf_Disc['work_flow_stages'] = wf_stages
        wf_Disc['work_flow_name_disable'] = wrkflw_disable
        print("---------------------wf_Disc : ", wf_Disc)
        DOL_DB.update_stages_to_workflow(wf_ID,wf_Disc)
    return redirect(url_for('edit_work_flow_records',wf_id = wf_ID))


@app.route("/duplicate_workflow/<wf_id>", methods=['POST','GET'])
@login_required
def duplicate_work_flow_records(wf_id):
    wf_duplicate_disc = {}
    wf_duplicate_list = []
    
    wfd_cursor = DOL_DB.get_workflow_data_by_one_wrkflw_id(wf_id)
    for d in wfd_cursor:
        wf_duplicate_list.append(d)
    
    auto_reviews = wf_duplicate_list[0]['request_automated_reviews']
    wrkflw_name = wf_duplicate_list[0]['work_flow_name']
    wf_stages = wf_duplicate_list[0]['work_flow_stages']
    print("-----------------------wf_duplicate_list :",wf_duplicate_list)
    print("-----------------------auto_reviews :",auto_reviews)
    print("-----------------------wrkflw_name :",wrkflw_name)
    print("-----------------------wf_stages :",wf_stages)

    work_flow_id = generate_workflow_id(4,3)
    work_flow_name_disable = True
    currentDT = datetime.today()
    date_time = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")

    wf_duplicate_disc['work_flow_id'] = work_flow_id.strip()
    wf_duplicate_disc['request_automated_reviews'] = auto_reviews.strip()
    wf_duplicate_disc['work_flow_name'] = wrkflw_name.strip()
    wf_duplicate_disc['work_flow_stages'] = wf_stages
    wf_duplicate_disc['work_flow_name_disable'] = work_flow_name_disable
    wf_duplicate_disc['work_flow_name_identity_parameter'] = "Copy".strip()
    wf_duplicate_disc['work_flow_created_by'] = session['fullname_retailer'].strip()
    wf_duplicate_disc['work_flow_created_time'] = date_time.strip()
    print(wf_duplicate_disc)
    DOL_DB.save_workflow_structure(wf_duplicate_disc)
    return redirect(url_for('custom_viewWrapper'))

@app.route("/deleteWrkflow/<wf_ID>", methods=['GET'])
@login_required
def delete_workflow(wf_ID):
    DOL_DB.delete_a_workflow(wf_ID)
    return redirect(url_for('custom_viewWrapper'))


@app.route("/delete_stage_name/<stage_nkey>/<wf_ID>", methods=['POST'])
@login_required
def delete_a_stage_name(stage_nkey,wf_ID):
    form_wrkflw_Edit = WorkFlowEdit()
    formclass = 'form-control'
    wf_stage_list = []
    wf_Disc = {}
    wf_Disc_disable = {}
    wf_list = []

    wfs_cursor = DOL_DB.get_workflow_data_by_one_wrkflw_id(wf_ID)
    for s in wfs_cursor:
        wf_stage_list.append(s)

    stage_name = wf_stage_list[0]['work_flow_stages']
    print('--------------------------------before-----',stage_name)
    print("--------------------------------before length : ", len(stage_name))

    del stage_name[int(stage_nkey)]
    print('----------------------------after----',stage_name)

    wf_Disc['work_flow_stages'] = stage_name
    DOL_DB.update_stages_to_workflow_after_delete(wf_ID,wf_Disc)

    wf_cursor = DOL_DB.get_workflow_data_by_one_wrkflw_id(wf_ID)
    for k in wf_cursor:
        wf_list.append(k)

    print(wf_list[0]['work_flow_stages'])
    wf_stages = wf_list[0]['work_flow_stages']
    wrkflw_disable = wf_list[0]['work_flow_name_disable']
    
    print("-----after delete--------------length : ",len(wf_stages))
    length_of_wf_stages = len(wf_stages)

    if length_of_wf_stages == 0:
        print("ZERO")
        print("Inside IF")
        print("-----------------length_of_wf_stages : ", length_of_wf_stages)
        wrkflw_disable = True
        print("-----------------wrkflw_disable : ", wrkflw_disable)

        wf_Disc_disable['work_flow_name_disable'] = wrkflw_disable
        DOL_DB.update_disable_field_to_workflow_after_delete(wf_ID,wf_Disc_disable)
    
    else:
        print('Inside else')
        print("-----------------length_of_wf_stages : ", length_of_wf_stages)
        print("---------After----------wrkflw_disable : ",wrkflw_disable)
        pass

    return redirect(url_for('edit_work_flow_records',wf_id = wf_ID))


#=====================================Work Flow Order Entry====================================================================
@app.route("/")
@login_required
def WF_orderWrapper():
    form_wrk_flw_order = WFOrderForm()
    form_po = SearchWFOrderFormByPO()
    form_city = SearchWFOrderFormByCity()
    form_wftype = SearchWFOrderFormByWFType()
    form_state = SearchWFOrderFormByState()
    form_daterange = SearchWFOrderFormByDateRange()
    form_jobname = SearchWFOrderFormByJobName()
    form_fname = SearchWFOrderFormByFirstName()
    form_lname = SearchWFOrderFormByLastName()
    form_redbtn = RedButtonWFOrderForm()
    form_rbtnleadtime = RedButtonWFLeadTime()
    form_rbtnbuffertime = RedButtonWFBufferTime()
    form_checkbox = CheckboxForRedBtn()
    form_excel = excelFile()
    formclass = 'form-control'
    work_flow_list = []
    work_flow_drop_down_list = []
    wf_dol_list = []
    vendor_name_list = []
    emp_dol_list = []
    form_checkbox.nexus_id_checkbox.choices = []
    cst_mgs_type_list = []
    entry_msg_list = []
    entry_email_list = []
    redbtn_list = []

    search_page_code = ''
    search_page_term = ''

    print(session['defaultPage'])
    print(session['rPerPage'])

    if session['search_activated_Wfdol']:
        wf_dol_list = session['Wfdol_records']
        search_page_code = session['searched_wfdol_page_no']
        search_page_term = session['searched_wfdol_page_term']

    else:
        wf_dol_cur = DOL_DB.get_wforder_details_paginated(int(session['defaultPage']),int(session['rPerPage']))
        session['recordsPerPage'] = int(wf_dol_cur[1])
        session['count_dolwfUser'] = int(wf_dol_cur[2])
        session['totalPages'] = int(wf_dol_cur[3])
        search_page_code = '0'
        search_page_term = 'all'
        
        for u in wf_dol_cur[0]:
            wf_dol_list.append(u)
            form_checkbox.nexus_id_checkbox.choices.append((u['nexus_id'],u['nexus_id']))


    work_flow_drop_down_list.append(('' , 'Select Workflow'))
    wrk_flw_cur = DOL_DB.get_work_flow_data()
    for r in wrk_flw_cur:
        work_flow_list.append(r)
        work_flow_drop_down_list.append((r['work_flow_id'],r['work_flow_name']))
    print("--------------------------work_flow_list: ",work_flow_list)   

    form_wrk_flw_order.wf_type.choices = work_flow_drop_down_list
    
    emp_DolCur = DOL_DB.get_empty_keys_from_db()
    for k in emp_DolCur:
        emp_dol_list.append(k)

    vendor_cur = DOL_DB.get_vendor_data()
    for d in vendor_cur:
        vendor_name_list.append((d['vendor_name'],d['vendor_name']))

    form_wrk_flw_order.br_and.choices = vendor_name_list

    form_info = zip(wf_dol_list,form_checkbox.nexus_id_checkbox)

    entry_msg_cur = DOL_DB.get_custom_order_related_texts()
    for e in entry_msg_cur:
       cst_mgs_type_list.append(e['custom_message_type'])

    for typ in cst_mgs_type_list:
        
        if typ == 'Order Entry':
            typ_cur = DOL_DB.get_custom_order_related_texts_by_type(typ)
            for t in typ_cur:
                entry_msg_list.append(t)
        
        elif typ == 'Order Entry Email':
            typ_cur = DOL_DB.get_custom_order_related_texts_by_type(typ)
            for t in typ_cur:
                entry_email_list.append(t)


    phone_num = session['phonenum_retailer']
    redbtn_cur = DOL_DB.get_dealer_basic_details_from_dealer_account_by_phone_num(phone_num)
    for d in redbtn_cur:
       redbtn_list.append(d)
    redbtn = redbtn_list[0]['redbutton_feature']
    blk_upload = redbtn_list[0]['bulkorder_upload']
    print("-----------------------------redbtn_list: ",redbtn_list)
    print("-------------------------------: ",redbtn)
    print("----------------blk_upload---------------: ",blk_upload)

    session['search_activated_Wfdol'] = False
    return render_template('DOL_orderform_workflow.html',
                          workFlowList=work_flow_list,
                          wfDol_list = wf_dol_list,
                          form_wrk_flw_order = form_wrk_flw_order,
                          form_po = form_po,
                          form_city = form_city,
                          form_wftype = form_wftype,
                          form_state = form_state,
                          form_daterange = form_daterange,
                          form_jobname = form_jobname,
                          form_fname = form_fname,
                          form_lname = form_lname,
                          form_redbtn = form_redbtn,
                          form_rbtnleadtime = form_rbtnleadtime,                      
                          form_rbtnbuffertime = form_rbtnbuffertime,
                          form_checkbox = form_checkbox,
                          formclass = formclass,
                          form_info = form_info,
                          empList = emp_dol_list,
                          form_excel = form_excel,
                          entry_msg_list = entry_msg_list,
                          user = session['username_retailer'],
                          org = session['org_retailer'],
                          totalPages = session['totalPages'],
                          records_pages = session['recordsPerPage'],
                          count_user = session['count_dolwfUser'],
                          redbtn = redbtn,
                          blk_upload = blk_upload,
                          search_code = search_page_code,
                          search_term = search_page_term)

@app.route("/WForders_page/<pagenum>/<records_pages>/<search_code>/<search_term>", methods = ['GET'])
@login_required
def WF_orderWrapper_paginated(pagenum,records_pages,search_code,search_term):
    form_wrk_flw_order = WFOrderForm()
    form_po = SearchWFOrderFormByPO()
    form_city = SearchWFOrderFormByCity()
    form_wftype = SearchWFOrderFormByWFType()
    form_state = SearchWFOrderFormByState()
    form_daterange = SearchWFOrderFormByDateRange()
    form_jobname = SearchWFOrderFormByJobName()
    form_fname = SearchWFOrderFormByFirstName()
    form_lname = SearchWFOrderFormByLastName()
    form_redbtn = RedButtonWFOrderForm()
    form_rbtnleadtime = RedButtonWFLeadTime()
    form_rbtnbuffertime = RedButtonWFBufferTime()
    form_checkbox = CheckboxForRedBtn()
    form_excel = excelFile()
    formclass = 'form-control'
    work_flow_list = []
    work_flow_drop_down_list = []
    wf_dol_list = []
    vendor_name_list = []
    emp_dol_list = []
    form_checkbox.nexus_id_checkbox.choices = []
    cst_mgs_type_list = []
    entry_msg_list = []
    entry_email_list = []
    redbtn_list = []
    
    wforders_info = []

    search_page_code = ''
    search_page_term = ''

    if search_code == '0':
        wf_dol_cur = DOL_DB.get_wforder_details_paginated(int(pagenum),int(records_pages))
        wforders_info = session['Wfdol_records']
        search_page_code = session['searched_wfdol_page_no']
        search_page_term = session['searched_wfdol_page_term']
        session['search_activated_Wfdol'] = False

    elif search_code == '1':
        wf_dol_cur = DOL_DB.search_by_job_name(search_term,int(pagenum),int(records_pages))
        session['Wfdol_records'] = wf_dol_cur
        session['searched_wfdol_page_no'] = '1'
        session['searched_wfdol_page_term'] = search_term
        session['search_activated_Wfdol'] = True

    elif search_code == '2':
        wf_dol_cur = DOL_DB.search_by_cons_first_name(search_term,int(pagenum),int(records_pages))
        session['Wfdol_records'] = wf_dol_cur
        session['searched_wfdol_page_no'] = '2'
        session['searched_wfdol_page_term'] = search_term
        session['search_activated_Wfdol'] = True

    elif search_code == '3':
        wf_dol_cur = DOL_DB.search_by_cons_last_name(search_term,int(pagenum),int(records_pages))
        session['Wfdol_records'] = wf_dol_cur
        session['searched_wfdol_page_no'] = '3'
        session['searched_wfdol_page_term'] = search_term
        session['search_activated_Wfdol'] = True

    elif search_code == '4':
        wf_dol_cur = DOL_DB.search_by_WFpo_number(search_term,int(pagenum),int(records_pages))
        session['Wfdol_records'] = wf_dol_cur
        session['searched_wfdol_page_no'] = '4'
        session['searched_wfdol_page_term'] = search_term
        session['search_activated_Wfdol'] = True

    elif search_code == '5':
        wf_dol_cur = DOL_DB.search_by_WFcity(search_term,int(pagenum),int(records_pages))
        session['Wfdol_records'] = wf_dol_cur
        session['searched_wfdol_page_no'] = '5'
        session['searched_wfdol_page_term'] = search_term
        session['search_activated_Wfdol'] = True

    elif search_code == '6':
        wf_dol_cur = DOL_DB.search_by_WF_type(search_term,int(pagenum),int(records_pages))
        session['Wfdol_records'] = wf_dol_cur
        session['searched_wfdol_page_no'] = '6'
        session['searched_wfdol_page_term'] = search_term
        session['search_activated_Wfdol'] = True

    elif search_code == '7':
        wf_dol_cur = DOL_DB.search_by_WFstate(search_term,int(pagenum),int(records_pages))
        session['Wfdol_records'] = wf_dol_cur
        session['searched_wfdol_page_no'] = '7'
        session['searched_wfdol_page_term'] = search_term
        session['search_activated_Wfdol'] = True

    elif search_code == '8':
        wf_dol_cur = DOL_DB.get_wforder_details_paginated(int(pagenum),int(records_pages))
        session['Wfdol_records'] = wf_dol_cur
        session['searched_wfdol_page_no'] = '8'
        session['searched_wfdol_page_term'] = search_term
        session['search_activated_Wfdol'] = True

    elif search_code == '9':
        wf_dol_cur = DOL_DB.get_wforder_details_paginated(int(pagenum),int(records_pages))
        session['Wfdol_records'] = wf_dol_cur
        session['searched_wfdol_page_no'] = '9'
        session['searched_wfdol_page_term'] = search_term
        session['search_activated_Wfdol'] = True

    session['recordsPerPage'] = int(wf_dol_cur[1])
    session['count_dolwfUser'] = int(wf_dol_cur[2])
    session['totalPages'] = int(wf_dol_cur[3])
    search_page_code = session['searched_wfdol_page_no']
    search_page_term = session['searched_wfdol_page_term']
        
    for u in wf_dol_cur[0]:
        wf_dol_list.append(u)
        form_checkbox.nexus_id_checkbox.choices.append((u['nexus_id'],u['nexus_id']))

    
    work_flow_drop_down_list.append(('' , 'Select Workflow'))
    wrk_flw_cur = DOL_DB.get_work_flow_data()
    for r in wrk_flw_cur:
        work_flow_list.append(r)
        work_flow_drop_down_list.append((r['work_flow_id'],r['work_flow_name']))

    form_wrk_flw_order.wf_type.choices = work_flow_drop_down_list
    
    emp_DolCur = DOL_DB.get_empty_keys_from_db()
    for k in emp_DolCur:
        emp_dol_list.append(k)

    vendor_cur = DOL_DB.get_vendor_data()
    for d in vendor_cur:
        vendor_name_list.append((d['vendor_name'],d['vendor_name']))

    form_wrk_flw_order.br_and.choices = vendor_name_list

    form_info = zip(wf_dol_list,form_checkbox.nexus_id_checkbox)

    entry_msg_cur = DOL_DB.get_custom_order_related_texts()
    for e in entry_msg_cur:
       cst_mgs_type_list.append(e['custom_message_type'])

    for typ in cst_mgs_type_list:
        
        if typ == 'Order Entry':
            typ_cur = DOL_DB.get_custom_order_related_texts_by_type(typ)
            for t in typ_cur:
                entry_msg_list.append(t)
        
        elif typ == 'Order Entry Email':
            typ_cur = DOL_DB.get_custom_order_related_texts_by_type(typ)
            for t in typ_cur:
                entry_email_list.append(t)

    phone_num = session['phonenum_retailer']
    redbtn_cur = DOL_DB.get_dealer_basic_details_from_dealer_account_by_phone_num(phone_num)
    for d in redbtn_cur:
       redbtn_list.append(d)
    redbtn = redbtn_list[0]['redbutton_feature']
    blk_upload = redbtn_list[0]['bulkorder_upload']
    print("-----------------------------redbtn_list: ",redbtn_list)
    print("-------------------------------: ",redbtn)

    session['search_activated_Wfdol'] = False
    return render_template('DOL_orderform_workflow.html',
                          workFlowList=work_flow_list,
                          wfDol_list = wf_dol_list,
                          form_wrk_flw_order = form_wrk_flw_order,
                          form_po = form_po,
                          form_city = form_city,
                          form_wftype = form_wftype,
                          form_state = form_state,
                          form_daterange = form_daterange,
                          form_jobname = form_jobname,
                          form_fname = form_fname,
                          form_lname = form_lname,
                          form_redbtn = form_redbtn,
                          form_rbtnleadtime = form_rbtnleadtime,                      
                          form_rbtnbuffertime = form_rbtnbuffertime,
                          form_checkbox = form_checkbox,
                          formclass = formclass,
                          form_info = form_info,
                          empList = emp_dol_list,
                          form_excel = form_excel,
                          entry_msg_list = entry_msg_list,
                          user = session['username_retailer'],
                          org = session['org_retailer'],
                          totalPages = session['totalPages'], 
                          records_pages = session['recordsPerPage'],
                          count_user = session['count_dolwfUser'],
                          redbtn = redbtn,
                          blk_upload = blk_upload,
                          search_code = search_page_code,
                          search_term = search_page_term)




@app.route('/search_WForder_records/<search_code>', methods=['POST'])
@login_required
def search_WForder_Records(search_code):
    print("Inside WF search")
    form_wrk_flw_order = WFOrderForm()
    form_po = SearchWFOrderFormByPO()
    form_city = SearchWFOrderFormByCity()
    form_wftype = SearchWFOrderFormByWFType()
    form_state = SearchWFOrderFormByState()
    form_daterange = SearchWFOrderFormByDateRange()
    form_jobname = SearchWFOrderFormByJobName()
    form_fname = SearchWFOrderFormByFirstName()
    form_lname = SearchWFOrderFormByLastName()
    form_redbtn = RedButtonWFOrderForm()
    form_rbtnleadtime = RedButtonWFLeadTime()
    form_rbtnbuffertime = RedButtonWFBufferTime()
    form_checkbox = CheckboxForRedBtn()
    form_excel = excelFile()
    formclass = 'form-control'

    date_range_filtered_WForders = []
    work_flow_list = []
    work_flow_drop_down_list = []
    work_flow_drop_down_namelist = []
    wf_dol_list = []
    order_list = []
    vendor_name_list = []
    form_checkbox.nexus_id_checkbox.choices = []
    emp_dol_list = []
    redbtn_list = []
    
    search_page_code = ''
    search_page_term = ''

    # wf_dol_cur = DOL_DB.get_wforder_details()
    # for u in wf_dol_cur:
    #     wf_dol_list.append(u)
    #     form_checkbox.nexus_id_checkbox.choices.append((u['nexus_id'],u['nexus_id']))

    if int(search_code) == 1:
        if form_jobname.validate_on_submit():
            session['job_name'] = request.form['searchbyJobname'].strip()
            print(session['job_name'])
            WF_cursor = DOL_DB.search_by_job_name(session['job_name'], int(session['defaultPage']), int(session['rPerPage']))
            for o in WF_cursor[0]:
                wf_dol_list.append(o)
                form_checkbox.nexus_id_checkbox.choices.append((o['nexus_id'],o['nexus_id']))
            form_info = zip(wf_dol_list,form_checkbox.nexus_id_checkbox)
            print("------------------------------------wf_dol_list of Search----------")
            print(wf_dol_list)
            session['searched_wfdol_page_no'] = '1'
            session['searched_wfdol_page_term'] = session['job_name']
            session['recordsPerPage'] = int(WF_cursor[1])
            session['count_dolwfUser'] = int(WF_cursor[2])
            session['totalPages'] = int(WF_cursor[3])

    elif int(search_code) == 2:
        if form_fname.validate_on_submit():
            session['wf_first_name'] = request.form['searchbyFname'].strip()
            print(session['wf_first_name'])
            WF_cursor = DOL_DB.search_by_cons_first_name(session['wf_first_name'], int(session['defaultPage']), int(session['rPerPage']))
            for o in WF_cursor[0]:
                wf_dol_list.append(o)
                form_checkbox.nexus_id_checkbox.choices.append((o['nexus_id'],o['nexus_id']))
            form_info = zip(wf_dol_list,form_checkbox.nexus_id_checkbox)
            print("------------------------------------wf_dol_list of Search----------")
            print(wf_dol_list)
            session['searched_wfdol_page_no'] = '2'
            session['searched_wfdol_page_term'] = session['wf_first_name']
            session['recordsPerPage'] = int(WF_cursor[1])
            session['count_dolwfUser'] = int(WF_cursor[2])
            session['totalPages'] = int(WF_cursor[3])

    elif int(search_code) == 3:
        if form_lname.validate_on_submit():
            session['wf_last_name'] = request.form['searchbyLname'].strip()
            print(session['wf_last_name'])
            WF_cursor = DOL_DB.search_by_cons_last_name(session['wf_last_name'], int(session['defaultPage']), int(session['rPerPage']))
            for o in WF_cursor[0]:
                wf_dol_list.append(o)
                form_checkbox.nexus_id_checkbox.choices.append((o['nexus_id'],o['nexus_id']))
            form_info = zip(wf_dol_list,form_checkbox.nexus_id_checkbox)
            print("------------------------------------wf_dol_list of Search----------")
            print(wf_dol_list)
            session['searched_wfdol_page_no'] = '3'
            session['searched_wfdol_page_term'] = session['wf_last_name']
            session['recordsPerPage'] = int(WF_cursor[1])
            session['count_dolwfUser'] = int(WF_cursor[2])
            session['totalPages'] = int(WF_cursor[3])


    elif int(search_code) == 4:
        if form_po.validate_on_submit():
            session['wfpo_num'] = request.form['searchbyPonumber'].strip()
            WF_cursor = DOL_DB.search_by_WFpo_number(session['wfpo_num'], int(session['defaultPage']), int(session['rPerPage']))
            for o in WF_cursor[0]:
                wf_dol_list.append(o)
                form_checkbox.nexus_id_checkbox.choices.append((o['nexus_id'],o['nexus_id']))
            form_info = zip(wf_dol_list,form_checkbox.nexus_id_checkbox)
            print("------------------------------------wf_dol_list of Search----------")
            print(wf_dol_list)
            session['searched_wfdol_page_no'] = '4'
            session['searched_wfdol_page_term'] = session['wfpo_num']
            session['recordsPerPage'] = int(WF_cursor[1])
            session['count_dolwfUser'] = int(WF_cursor[2])
            session['totalPages'] = int(WF_cursor[3])

    elif int(search_code) == 5:
        if form_city.validate_on_submit():
            session['wfcity'] = request.form['searchbyCity'].strip()
            WF_cursor = DOL_DB.search_by_WFcity(session['wfcity'], int(session['defaultPage']), int(session['rPerPage']))
            for o in WF_cursor[0]:
                wf_dol_list.append(o)
                form_checkbox.nexus_id_checkbox.choices.append((o['nexus_id'],o['nexus_id']))
            form_info = zip(wf_dol_list,form_checkbox.nexus_id_checkbox)
            session['searched_wfdol_page_no'] = '5'
            session['searched_wfdol_page_term'] = session['wfcity']
            session['recordsPerPage'] = int(WF_cursor[1])
            session['count_dolwfUser'] = int(WF_cursor[2])
            session['totalPages'] = int(WF_cursor[3])

    elif int(search_code) == 6:
        if form_wftype.validate_on_submit():
            session['wf_type'] = request.form['searchbyWfType'].strip()
            WF_cursor = DOL_DB.search_by_WF_type(session['wf_type'], int(session['defaultPage']), int(session['rPerPage']))
            for o in WF_cursor[0]:
                wf_dol_list.append(o)
                form_checkbox.nexus_id_checkbox.choices.append((o['nexus_id'],o['nexus_id']))
            form_info = zip(wf_dol_list,form_checkbox.nexus_id_checkbox)
            print('=======================wf_dol_list=============================================')
            print(wf_dol_list)
            session['searched_wfdol_page_no'] = '6'
            session['searched_wfdol_page_term'] = session['wf_type']
            session['recordsPerPage'] = int(WF_cursor[1])
            session['count_dolwfUser'] = int(WF_cursor[2])
            session['totalPages'] = int(WF_cursor[3])

    elif int(search_code) == 7:
        if form_state.validate_on_submit():
            session['wfstate'] = request.form['searchbyState'].strip()
            WF_cursor = DOL_DB.search_by_WFstate(session['wfstate'], int(session['defaultPage']), int(session['rPerPage']))
            for o in WF_cursor[0]:
                wf_dol_list.append(o)
                form_checkbox.nexus_id_checkbox.choices.append((o['nexus_id'],o['nexus_id']))
            form_info = zip(wf_dol_list,form_checkbox.nexus_id_checkbox)
            session['searched_wfdol_page_no'] = '7'
            session['searched_wfdol_page_term'] = session['wfstate']
            session['recordsPerPage'] = int(WF_cursor[1])
            session['count_dolwfUser'] = int(WF_cursor[2])
            session['totalPages'] = int(WF_cursor[3])

    elif int(search_code) == 8:
        if form_daterange.validate_on_submit():
            from_date = request.form['searchbyFromdate'].strip()
            from_date_to_date_obj = datetime.strptime(from_date,'%Y-%m-%d')
            #from_date_to_date_obj_str = datetime_object_from_date.strftime("%m-%d-%Y")
            #from_date_to_date_obj = datetime.strptime(from_date_to_date_obj_str,'%m-%d-%Y')
            print(from_date_to_date_obj)

            

            to_date = request.form['searchbyTodate'].strip()
            print("=================================to_date : ",to_date)
            to_date_to_date_obj = datetime.strptime(to_date,'%Y-%m-%d')
            #to_date_to_date_obj_str = datetime_object_to_date.strftime("%m-%d-%Y")
            #to_date_to_date_obj = datetime.strptime(to_date_to_date_obj_str,'%m-%d-%Y')
            print(to_date_to_date_obj)
            
            all_order_cursor = DOL_DB.get_wforder_details_paginated(int(session['defaultPage']),int(session['rPerPage']))
            for od in all_order_cursor[0]:
                order_list.append(od)
                form_checkbox.nexus_id_checkbox.choices.append((od['nexus_id'],od['nexus_id']))

            for order in order_list:
                o_date = order['order_date']
                o_date_str_to_date = datetime.strptime(o_date,'%m-%d-%Y')

                print("=============================o_date_str_to_date : ",o_date_str_to_date)

                if (o_date_str_to_date >= from_date_to_date_obj and o_date_str_to_date <= to_date_to_date_obj):
                    date_range_filtered_WForders.append(order)

            print(date_range_filtered_WForders)

            wf_dol_list = date_range_filtered_WForders
            form_info = zip(wf_dol_list,form_checkbox.nexus_id_checkbox)

    elif int(search_code) == 9:
        WF_cursor = DOL_DB.get_wforder_details_paginated(int(session['defaultPage']),int(session['rPerPage']))
        for o in WF_cursor[0]:
            wf_dol_list.append(o)
            form_checkbox.nexus_id_checkbox.choices.append((o['nexus_id'],o['nexus_id']))
        form_info = zip(wf_dol_list,form_checkbox.nexus_id_checkbox)
        print('=======================wf_dol_list=============================================')
        print(wf_dol_list)
        session['searched_wfdol_page_no'] = '9'
        session['searched_wfdol_page_term'] = session['wf_type']
        session['recordsPerPage'] = int(WF_cursor[1])
        session['count_dolwfUser'] = int(WF_cursor[2])
        session['totalPages'] = int(WF_cursor[3])


    work_flow_drop_down_list.append(('' , 'Select Workflow'))
    wrk_flw_cur = DOL_DB.get_work_flow_data()
    for r in wrk_flw_cur:
        work_flow_list.append(r)
        work_flow_drop_down_list.append((r['work_flow_id'],r['work_flow_name']))
        work_flow_drop_down_namelist.append((r['work_flow_name'],r['work_flow_name']))


    form_wrk_flw_order.wf_type.choices = work_flow_drop_down_list

    vendor_cur = DOL_DB.get_vendor_data()
    for d in vendor_cur:
        vendor_name_list.append((d['vendor_name'],d['vendor_name']))
    print(vendor_name_list)

    form_wrk_flw_order.br_and.choices = vendor_name_list

    emp_DolCur = DOL_DB.get_empty_keys_from_db()
    for k in emp_DolCur:
        emp_dol_list.append(k)

    phone_num = session['phonenum_retailer']
    redbtn_cur = DOL_DB.get_dealer_basic_details_from_dealer_account_by_phone_num(phone_num)
    for d in redbtn_cur:
       redbtn_list.append(d)
    redbtn = redbtn_list[0]['redbutton_feature']
    blk_upload = redbtn_list[0]['bulkorder_upload']
    print("-----------------------------redbtn_list: ",redbtn_list)
    print("-------------------------------: ",redbtn)
    
    print(form_wftype.errors)
    session['search_activated_Wfdol'] = True
    return render_template('DOL_orderform_workflow.html',
                          workFlowList=work_flow_list,
                          wfDol_list = wf_dol_list,
                          form_wrk_flw_order = form_wrk_flw_order,
                          form_po = form_po,
                          form_city = form_city,
                          form_wftype = form_wftype,
                          form_state = form_state,
                          form_daterange = form_daterange,
                          form_jobname = form_jobname,
                          form_fname = form_fname,
                          form_lname = form_lname,
                          form_redbtn = form_redbtn,
                          form_rbtnleadtime = form_rbtnleadtime,                      
                          form_rbtnbuffertime = form_rbtnbuffertime,
                          form_checkbox = form_checkbox,
                          formclass = formclass,
                          form_info = form_info,
                          empList = emp_dol_list,
                          form_excel = form_excel,
                          user = session['username_retailer'],
                          org = session['org_retailer'],
                          totalPages = session['totalPages'],
                          records_pages = session['recordsPerPage'],
                          count_user = session['count_dolwfUser'],
                          redbtn = redbtn,
                          blk_upload =blk_upload,
                          search_code = search_page_code,
                          search_term = search_page_term)

@app.route("/wf_saveorder", methods=['POST'])
@login_required
def save_work_flow_order_records():
    session['search_activated_Wfdol'] = False
    form_wrk_flw_order = WFOrderForm()
    formclass = 'form-control'
    consumer_nid_list = []
    consumer_po_dict = {}
    communication_Info = {}
    nex_id_list = []
    work_flow_list = []
    work_flow_drop_down_list = []
    wftype_list = []
    vendor_name_list = []
    consumer_info_list = []
    consumer_cred_list = []
    consumer_info_list_after_save = []
    conInfo = {}
    consumer_info = {}
    cstm_type_list = []
    
    type_list = []
    type_list_email = []
    #workflow_stages_list = []

    welcome_type_list = []
    welcome_type_list_email = []

    last_acti_list = []
    
    text_message_1 = ''
    text_message_2 = ''
    
    session['sub_1'] = ''
    session['salutaion_1'] = ''
    session['text_body_1'] = ''
    session['conclusion_1'] = ''

    session['sub_2'] = ''
    session['salutaion_2'] = ''
    session['text_body_2'] = ''
    session['conclusion_2'] = ''

    session['welcome_msg_sms'] = ''
    
    session['welcome_sub_email'] = ''
    session['welcome_msg_email'] = ''

    communication_Info_Email = {}

    work_flow_drop_down_list.append(('' , 'Select Workflow'))
    wrk_flw_cur = DOL_DB.get_work_flow_data()
    for r in wrk_flw_cur:
        work_flow_list.append(r)
        workflow_stages_list = r['work_flow_stages']
        work_flow_drop_down_list.append((r['work_flow_id'],r['work_flow_name']))

    form_wrk_flw_order.wf_type.choices = work_flow_drop_down_list

    vendor_cur = DOL_DB.get_vendor_data()
    for d in vendor_cur:
        vendor_name_list.append((d['vendor_name'],d['vendor_name']))

    form_wrk_flw_order.br_and.choices = vendor_name_list

    cstm_msg_cursor = DOL_DB.get_custom_order_related_texts()
    for cst in cstm_msg_cursor:
        cstm_type_list.append(cst['custom_message_type'])

    if form_wrk_flw_order.validate_on_submit():
        order_info = DOL_info.setWF_OrderData()
        
        mobile_num = order_info['consumer_mobile_number']
        email = order_info['consumer_email']
        
        first_name = order_info['consumer_first_name']
        last_name = order_info['consumer_last_name']

        
        po_num = order_info['po_number']
        nx_id = order_info['nexus_id']

        wf_type_id = request.form['wf_type']

        od_date = order_info['order_date']

        est_date = order_info['est_deliver_time']

        order_info['progress_timeline'] = workflow_stages_list[0]
        print("===========================================================================")
        print(workflow_stages_list)
        print(order_info['progress_timeline'])
        print("===========================================================================")


        consumer_cursor = DOL_DB.get_consumer_data_by_phone(mobile_num)
        for c in consumer_cursor:
            consumer_info_list.append(c)

        if consumer_info_list:
            consumer_cred_cur = DOL_DB.get_consumer_cred_by_ph_num(mobile_num)
            
            for cr in consumer_cred_cur:
                consumer_cred_list.append(cr)

            if consumer_cred_list:
                print("User Exist--------------------")

            else:
                print("Only Consumer creds does not exits")
                consumer_user_id = generate_id(6,4)

                password_Un = generate_id(4,2)
                print('--------------------------password_Un : ', password_Un)
                password_Encrypt = sha_encryption(password_Un)
                currentDT = datetime.today()
                date_time = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")

                new_password_Un = sensitive_wordsOrc.setWFpass_words(password_Un)
                print("======================new_password_Un: ",new_password_Un)

                conInfo["org_name"]="Consumer".strip()
                conInfo["first_name"]=first_name.strip()
                conInfo["last_name"]=last_name.strip()
                conInfo["user_contact"]=mobile_num.strip()
                conInfo["email"]=email.strip()
                conInfo["user_type"]="Consumer".strip()
                conInfo["user_id"] = consumer_user_id.strip()
                conInfo["password"]=password_Encrypt.strip()
                conInfo["created_date"] = date_time.strip()

                print(conInfo)
                DOL_DB.save_consumer_credentials(conInfo)

                password = new_password_Un
                phone = conInfo['user_contact']
                user_id = conInfo['user_id']
                first_name = conInfo["first_name"]
                org_name = conInfo["org_name"]
                email = conInfo["email"]

                if cstm_type_list:
                    for typ in cstm_type_list:

                        if typ == "Welcome Note Change":
                            print("=====================================TRUE")
                            
                            typ_cursor = DOL_DB.get_custom_order_related_texts_by_type(typ)
                            for t in typ_cursor:
                                welcome_type_list.append(t)

                    
                            session['welcome_msg_sms'] = welcome_type_list[0]['create_order_text_box_1']

                            text_message_1 = session['welcome_msg_sms'] + config['consumer_portal_url']['CUST_URL']

                        if  typ == "Welcome Note Change Email":
                            print("===================EMAIL==================TRUE")
                            typ_cursor_email = DOL_DB.get_custom_order_related_texts_by_type(typ)
                            for t in typ_cursor_email:
                                welcome_type_list_email.append(t)
                            session['welcome_sub_email'] = welcome_type_list_email[0]['create_order_text_box_1']
                            session['welcome_msg_email'] = welcome_type_list_email[0]['create_order_text_box_2']


                            text_message_2 = session['welcome_sub_email'] + session['welcome_msg_email'] + config['consumer_portal_url']['CUST_URL']

                    communication_log_id = generate_id(4,2)
                    currentDT = datetime.today()
                    current_log_datetime = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")

                    communication_Info['communication_log_id'] = communication_log_id.strip()
                    communication_Info['nexus_id'] = order_info['nexus_id'].strip()
                    communication_Info['po_number'] = order_info['po_number'].strip()
                    communication_Info['logger_id'] = session['orgId_retailer']
                    communication_Info['logger_name'] = session['fullname_retailer']
                    communication_Info['logger_type'] = "Dealer".strip()
                    communication_Info['subject'] = "Welcome Note SMS"
                    communication_Info['sending_mode'] = "SMS".strip()
                    communication_Info['message_plain_text'] = text_message_1
                    communication_Info['current_log_datetime'] = current_log_datetime.strip()
                    communication_Info['action_taken'] = "".strip()

                    communication_Info_Email['communication_log_id'] = communication_log_id.strip()
                    communication_Info_Email['nexus_id'] = order_info['nexus_id'].strip()
                    communication_Info_Email['po_number'] = order_info['po_number'].strip()
                    communication_Info_Email['logger_id'] = session['orgId_retailer']
                    communication_Info_Email['logger_name'] = session['fullname_retailer']
                    communication_Info_Email['logger_type'] = "Dealer".strip()
                    communication_Info_Email['subject'] = session['welcome_sub_email']
                    communication_Info_Email['sending_mode'] = "Email".strip()
                    communication_Info_Email['message_plain_text'] = text_message_2
                    communication_Info_Email['current_log_datetime'] = current_log_datetime.strip()
                    communication_Info_Email['action_taken'] = "".strip()

                    if consumer_info_list[0]['welcome_email']==True:

                        if consumer_info_list[0]['receive_sms_notification']==True and consumer_info_list[0]['receive_mail_notification']==False:
                            print("Sms true")
                            #sendSms.send_consumer_welcome_note_by_msg(phone,communication_Info)
                        elif consumer_info_list[0]['receive_mail_notification']==True and consumer_info_list[0]['receive_sms_notification']==False:
                            print("Emal true")
                            sendMail.send_consumer_welcome_note_by_mail(email,communication_Info_Email)
                        
                        elif consumer_info_list[0]['receive_mail_notification']==True and consumer_info_list[0]['receive_sms_notification']==True:
                            print("Both true")
                            #sendSms.send_consumer_welcome_note_by_msg(phone,communication_Info)
                            sendMail.send_consumer_welcome_note_by_mail(email,communication_Info_Email)
                        else:
                            print("No action")


                        if consumer_info_list[0]['receive_sms_notification']==True and consumer_info_list[0]['receive_mail_notification']==False:
                            print("Sms true")
                            sendSms.send_consumer_creds_by_msg(password,phone,user_id,first_name,org_name)
                        elif consumer_info_list[0]['receive_mail_notification']==True and consumer_info_list[0]['receive_sms_notification']==False:
                            print("Emal true")
                            sendMail.send_consumer_creds_by_mail(password,phone,email,user_id,first_name,org_name)
                        
                        elif consumer_info_list[0]['receive_mail_notification']==True and consumer_info_list[0]['receive_sms_notification']==True:
                            print("Both true")
                            sendSms.send_consumer_creds_by_msg(password,phone,user_id,first_name,org_name)
                            sendMail.send_consumer_creds_by_mail(password,phone,email,user_id,first_name,org_name)
                        else:
                            print("No action")

                    else:
                        print("No welcome message, no email, no credentials")
                        pass

        else:
            consumer_cred_cur = DOL_DB.get_consumer_cred_by_ph_num(mobile_num)
            for cr in consumer_cred_cur:
                consumer_cred_list.append(cr)
            print(consumer_cred_list)

            currentDT = datetime.today()
            current_welcome_datetime = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")
            welcome_datetime = current_welcome_datetime
            cons_datetime = current_welcome_datetime

            if consumer_cred_list:
                print("Consuemr exits!!! No creds")
                consumer_info['consumer_id'] = order_info['relationship_number']
                consumer_info['consumer_first_name'] = order_info['consumer_first_name']
                consumer_info['consumer_last_name'] = order_info['consumer_last_name'].strip()
                consumer_info['consumer_mobile_number'] = order_info['consumer_mobile_number'].strip()
                consumer_info['consumer_email'] = order_info['consumer_email'].strip()
                consumer_info['consumer_date_of_birth'] = "".strip()
                consumer_info['consumer_address'] = order_info['address'].strip()
                consumer_info['consumer_city'] = order_info['city'].strip()
                consumer_info['consumer_country'] = order_info['country'].strip()
                state = order_info['state'].split('- ')
                consumer_info['consumer_state'] = state[0].strip()
                consumer_info['consumer_zip_code'] = order_info['consumer_zip_code'].strip()
                consumer_info['user_type'] = order_info['user_type'].strip()
                consumer_info['welcome_email'] = True
                consumer_info['welcome_email_datetime'] = welcome_datetime
                consumer_info['consumer_origin'] = "Single Order Entry"
                consumer_info['receive_mail_notification'] = True
                consumer_info['receive_sms_notification'] = True
                consumer_info['excel_upload'] = "Nexus"
                consumer_info['consumer_datetime'] = cons_datetime

                
                DOL_DB.save_consumer_informaton(consumer_info)

            else:
                consumer_info['consumer_id'] = order_info['relationship_number']
                consumer_info['consumer_first_name'] = order_info['consumer_first_name']
                consumer_info['consumer_last_name'] = order_info['consumer_last_name'].strip()
                consumer_info['consumer_mobile_number'] = order_info['consumer_mobile_number'].strip()
                consumer_info['consumer_email'] = order_info['consumer_email'].strip()
                consumer_info['consumer_date_of_birth'] = "".strip()
                consumer_info['consumer_address'] = order_info['address'].strip()
                consumer_info['consumer_city'] = order_info['city'].strip()
                consumer_info['consumer_country'] = order_info['country'].strip()
                state = order_info['state'].split('- ')
                consumer_info['consumer_state'] = state[0].strip()
                consumer_info['consumer_zip_code'] = order_info['consumer_zip_code'].strip()
                consumer_info['user_type'] = order_info['user_type']
                consumer_info['welcome_email'] = True
                consumer_info['welcome_email_datetime'] = welcome_datetime
                consumer_info['consumer_origin'] = "Single Order Entry"
                consumer_info['receive_mail_notification'] = True
                consumer_info['receive_sms_notification'] = True
                consumer_info['excel_upload'] = "Nexus"
                consumer_info['consumer_datetime'] = cons_datetime
                
                DOL_DB.save_consumer_informaton(consumer_info)
                

                consumer_user_id = generate_id(6,4)
                print("==================================nexus_consumer_id : ", consumer_user_id)

                password_Un = generate_id(4,2)
                print('--------------------------password_Un : ', password_Un)
                password_Encrypt = sha_encryption(password_Un)
                currentDT = datetime.today()
                date_time = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")

                new_password_Un = sensitive_wordsOrc.setWFpass_words(password_Un)
                print("======================new_password_Un: ",new_password_Un)

                conInfo["org_name"]="Consumer".strip()
                conInfo["first_name"]=first_name.strip()
                conInfo["last_name"]=last_name.strip()
                conInfo["user_contact"]=mobile_num.strip()
                conInfo["email"]=email.strip()
                conInfo["user_type"]="Consumer".strip()
                conInfo["user_id"] = consumer_user_id.strip()
                conInfo["password"]=password_Encrypt.strip()
                conInfo["created_date"] = date_time.strip()

                DOL_DB.save_consumer_credentials(conInfo)

                password = new_password_Un
                phone = conInfo['user_contact']
                user_id = conInfo['user_id']
                first_name = conInfo["first_name"]
                org_name = conInfo["org_name"]
                email = conInfo["email"]


                if cstm_type_list:
                    for typ in cstm_type_list:

                        if typ == "Welcome Note Change":
                            print("=====================================TRUE")
                            
                            typ_cursor = DOL_DB.get_custom_order_related_texts_by_type(typ)
                            for t in typ_cursor:
                                welcome_type_list.append(t)


                    
                            session['welcome_msg_sms'] = welcome_type_list[0]['create_order_text_box_1']

                            text_message_1 = session['welcome_msg_sms'] + config['consumer_portal_url']['CUST_URL']



                        if  typ == "Welcome Note Change Email":
                            print("===================EMAIL==================TRUE")
                            typ_cursor_email = DOL_DB.get_custom_order_related_texts_by_type(typ)
                            for t in typ_cursor_email:
                                welcome_type_list_email.append(t)

                            session['welcome_sub_email'] = welcome_type_list_email[0]['create_order_text_box_1']
                            session['welcome_msg_email'] = welcome_type_list_email[0]['create_order_text_box_2']


                            text_message_2 = session['welcome_sub_email'] + session['welcome_msg_email'] + config['consumer_portal_url']['CUST_URL']


                    communication_log_id = generate_id(4,2)
                    currentDT = datetime.today()
                    current_log_datetime = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")

                    communication_Info['communication_log_id'] = communication_log_id.strip()
                    communication_Info['nexus_id'] = order_info['nexus_id'].strip()
                    communication_Info['po_number'] = order_info['po_number'].strip()
                    communication_Info['logger_id'] = session['orgId_retailer']
                    communication_Info['logger_name'] = session['fullname_retailer']
                    communication_Info['logger_type'] = "Dealer".strip()
                    communication_Info['subject'] = "Welcome Note SMS"
                    communication_Info['sending_mode'] = "SMS".strip()
                    communication_Info['message_plain_text'] = text_message_1
                    communication_Info['current_log_datetime'] = current_log_datetime.strip()
                    communication_Info['action_taken'] = "".strip()

                    communication_Info_Email['communication_log_id'] = communication_log_id.strip()
                    communication_Info_Email['nexus_id'] = order_info['nexus_id'].strip()
                    communication_Info_Email['po_number'] = order_info['po_number'].strip()
                    communication_Info_Email['logger_id'] = session['orgId_retailer']
                    communication_Info_Email['logger_name'] = session['fullname_retailer']
                    communication_Info_Email['logger_type'] = "Dealer".strip()
                    communication_Info_Email['subject'] = session['welcome_sub_email']
                    communication_Info_Email['sending_mode'] = "Email".strip()
                    communication_Info_Email['message_plain_text'] = text_message_2
                    communication_Info_Email['current_log_datetime'] = current_log_datetime.strip()
                    communication_Info_Email['action_taken'] = "".strip()

                    #sendSms.send_consumer_welcome_note_by_msg(phone,communication_Info)
                    #sendMail.send_consumer_welcome_note_by_mail(email,communication_Info_Email)
                
                sendSms.send_consumer_creds_by_msg(password,phone,user_id,first_name,org_name)
                sendMail.send_consumer_creds_by_mail(password,phone,email,user_id,first_name,org_name)

        con_po_cursor = DOL_DB.get_po_phone_matrix_details(mobile_num)
        for c in con_po_cursor:
            consumer_nid_list.append(c)
        print(consumer_nid_list)

        if consumer_nid_list:
            print('exist')
            print("-----------------------------nex_id_list")
            if session['orgId_retailer'] in consumer_nid_list[0]:
                nex_id_list = consumer_nid_list[0][session['orgId_retailer']]

                if nx_id in nex_id_list:
                    pass
                else:
                    print(nex_id_list)
                    dealer_dics = {}
                    nex_id_list.append(nx_id)
                    dealer_dics[session['orgId_retailer']] = nex_id_list
                    print("===================else===============nex_id_list")
                    print(nex_id_list)
                    DOL_DB.update_dealer_po_list(mobile_num,dealer_dics)

            else:
                dealer_dics = {}
                nex_id_list.append(nx_id)
                dealer_dics[session['orgId_retailer']] = nex_id_list
                print('=============================dealer_dics')
                print(dealer_dics)
                DOL_DB.update_dealer_po_list(mobile_num,dealer_dics)
        else:
            consumer_po_dict['consumer_mobile_number'] = mobile_num
            consumer_po_dict['country'] = order_info['country']
            consumer_po_dict[session['orgId_retailer']] = [nx_id]
            DOL_DB.save_consumer_po_data(consumer_po_dict)

        wftype_cursor = DOL_DB.get_workflow_data_by_one_wrkflw_id(wf_type_id)
        for i in wftype_cursor:
            wftype_list.append(i)

        order_info['work_flow_id'] = wf_type_id
        order_info['request_automated_reviews'] = wftype_list[0]['request_automated_reviews']
        order_info['work_flow_name'] = wftype_list[0]['work_flow_name']
        order_info['work_flow_stages'] = wftype_list[0]['work_flow_stages']
        order_info['final_work_flow_stages'] = order_info['work_flow_stages'][-1]

        DOL_DB.save_wforder_details(order_info)

        

        if cstm_type_list:
            for typ in cstm_type_list:

                if typ == "Order Entry":
                    print("=====================================TRUE")
                    
                    typ_cursor = DOL_DB.get_custom_order_related_texts_by_type(typ)
                    for t in typ_cursor:
                        type_list.append(t)

            
                    session['sub_1'] = type_list[0]['create_order_text_box_1']
                    session['salutaion_1'] = type_list[0]['create_order_text_box_2']
                    session['text_body_1'] = type_list[0]['create_order_text_box_3']
                    session['conclusion_1'] = type_list[0]['create_order_text_box_4']

                    text_message_1 = session['sub_1'] + order_info['nexus_id'] + session['salutaion_1'] + order_info['est_deliver_time'] + session['text_body_1'] + config['consumer_portal_url']['CUST_URL'] + session['conclusion_1']



                if  typ == "Order Entry Email":
                    print("===================EMAIL==================TRUE")
                    typ_cursor_email = DOL_DB.get_custom_order_related_texts_by_type(typ)
                    for t in typ_cursor_email:
                        type_list_email.append(t)

                    session['sub_2'] = type_list_email[0]['create_order_text_box_1']
                    session['salutaion_2'] = type_list_email[0]['create_order_text_box_2']
                    session['text_body_2'] = type_list_email[0]['create_order_text_box_3']
                    session['conclusion_2'] = type_list_email[0]['create_order_text_box_4']


                    text_message_2 = session['salutaion_2'] + order_info['nexus_id'] + session['text_body_2'] + order_info['est_deliver_time'] + session['conclusion_2'] + config['consumer_portal_url']['CUST_URL']


            communication_log_id = generate_id(4,2)
            currentDT = datetime.today()
            current_log_datetime = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")

            communication_Info['communication_log_id'] = communication_log_id.strip()
            communication_Info['nexus_id'] = order_info['nexus_id'].strip()
            communication_Info['po_number'] = order_info['po_number'].strip()
            communication_Info['logger_id'] = session['orgId_retailer']
            communication_Info['logger_name'] = session['fullname_retailer']
            communication_Info['logger_type'] = "Dealer".strip()
            communication_Info['subject'] = session['sub_1']
            communication_Info['sending_mode'] = "SMS".strip()
            communication_Info['message_plain_text'] = text_message_1
            communication_Info['current_log_datetime'] = current_log_datetime.strip()
            communication_Info['action_taken'] = "".strip()

            communication_Info_Email['communication_log_id'] = communication_log_id.strip()
            communication_Info_Email['nexus_id'] = order_info['nexus_id'].strip()
            communication_Info_Email['po_number'] = order_info['po_number'].strip()
            communication_Info_Email['logger_id'] = session['orgId_retailer']
            communication_Info_Email['logger_name'] = session['fullname_retailer']
            communication_Info_Email['logger_type'] = "Dealer".strip()
            communication_Info_Email['subject'] = session['sub_2']
            communication_Info_Email['sending_mode'] = "Email".strip()
            communication_Info_Email['message_plain_text'] = text_message_2
            communication_Info_Email['current_log_datetime'] = current_log_datetime.strip()
            communication_Info_Email['action_taken'] = "".strip()

            consumer_cursor = DOL_DB.get_consumer_data_by_phone(mobile_num)
            for c in consumer_cursor:
                consumer_info_list_after_save.append(c)

            if consumer_info_list_after_save:
                if consumer_info_list_after_save[0]['receive_sms_notification']==True and consumer_info_list_after_save[0]['receive_mail_notification']==False:
                    print("SMS True")
                    sendSms.send_order_entry_log_msg(mobile_num,communication_Info)
                    DOL_DB.save_communication_logs(communication_Info)

                elif consumer_info_list_after_save[0]['receive_mail_notification']==True and consumer_info_list_after_save[0]['receive_sms_notification']==False:
                    print("Email True")
                    sendMail.send_order_entry_to_mail(email,communication_Info_Email)
                    DOL_DB.save_communication_logs(communication_Info_Email)

                elif consumer_info_list_after_save[0]['receive_mail_notification']==True and consumer_info_list_after_save[0]['receive_sms_notification']==True:
                    print("Both True")
                    sendSms.send_order_entry_log_msg(mobile_num,communication_Info)
                    DOL_DB.save_communication_logs(communication_Info)
                    sendMail.send_order_entry_to_mail(email,communication_Info_Email)
                    DOL_DB.save_communication_logs(communication_Info_Email)
                else:
                    print("No action")

            else:
                print("consumer does not exit both send")
                sendSms.send_order_entry_log_msg(mobile_num,communication_Info)
                DOL_DB.save_communication_logs(communication_Info)
                sendMail.send_order_entry_to_mail(email,communication_Info_Email)
                DOL_DB.save_communication_logs(communication_Info_Email)

        currentDT = datetime.today()
        current_datetime_for_last_activity = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")

        last_acti_cur = DOL_DB.get_one_wforder_detail(nx_id)
        for la in last_acti_cur:
            last_acti_list.append(la)

        last_activity = last_acti_list[0]['last_activity']

        print("==================================================")
        print(last_activity)
        print("==================================================")

        last_activity = current_datetime_for_last_activity
        print(last_activity)

        DOL_DB.update_last_activity_of_an_order_change(nx_id,last_activity)
    print(form_wrk_flw_order.errors)
    return redirect(url_for('WF_orderWrapper'))

@app.route("/editWForder/<nid>", methods=['POST','GET'])
@login_required
def edit_work_flow_order_records(nid):
    print("Inside edit")
    form = WFOrderEditForm()
    formclass = 'form-control'
    order_Records = []
    progress_stages_color_codes = []
    progress_stages_badge_index = []
    progress_stages_dynamic = []
    progress_stages = []
    wfl_stages_list = []
    work_flow_list = []
    work_flow_drop_down_list = []
    vendor_name_list = []
    progress_stage_number = 0

    vendor_cur = DOL_DB.get_vendor_data()
    for d in vendor_cur:
        vendor_name_list.append((d['vendor_name'],d['vendor_name']))

    form.br_and.choices = vendor_name_list

    or_cur = DOL_DB.get_one_wforder_detail(nid)

    for o in or_cur:
        order_Records.append(o)
    print(order_Records)

    wrk_flw_name = order_Records[0]['work_flow_name']

    form.user_type.default = order_Records[0]['user_type']

    form.wf_type.default = order_Records[0]['work_flow_name']

    if order_Records[0]['country']=='Canada':
        form.country_1.default = order_Records[0]['country']
        form.ca_States.default = order_Records[0]['state']

    elif order_Records[0]['country']=='US':
        form.country_2.default = order_Records[0]['country']
        form.us_States.default = order_Records[0]['state']
    form.process()

    form.po_no.data = order_Records[0]['po_number']

    order_date_db = order_Records[0]['order_date']
    order_date_db_str_to_date = datetime.strptime(order_date_db, "%m-%d-%Y")

    
    form.or_date.data = order_date_db_str_to_date

    form.or_price.data = order_Records[0]['order_price']
    form.or_cost.data = order_Records[0]['order_cost']
    form.mdl.data = order_Records[0]['model']
    form.siz.data = order_Records[0]['size']
    form.j_name.data = order_Records[0]['job_name']
    form.co_fname.data = order_Records[0]['consumer_first_name']
    form.co_lname.data = order_Records[0]['consumer_last_name']
    form.co_mo_num.data = order_Records[0]['consumer_mobile_number']
    form.co_email.data = order_Records[0]['consumer_email']
    form.co_dob.data = order_Records[0]['consumer_date_of_birth']
    form.address.data = order_Records[0]['address']
    form.ci_ty.data = order_Records[0]['city']
    form.zip_code.data = order_Records[0]['consumer_zip_code']
    form.o_notes.data = order_Records[0]['order_notes']


    nexusId = order_Records[0]['nexus_id']
    orderDate = order_Records[0]['order_date']
    leadTme = order_Records[0]['total_lead_time']
    bufferTime = order_Records[0]['dealer_buffer_time']
    workfl_name = order_Records[0]['work_flow_name']
    po_no = order_Records[0]['po_number']
    brand = order_Records[0]['brand']
    price = order_Records[0]['order_price']
    est_dlvry = order_Records[0]['est_deliver_time']
    country = order_Records[0]['country']

    wfl_stages = order_Records[0]['work_flow_stages']
    final_stage = order_Records[0]['final_work_flow_stages']


    #-------------------------------------------------------------------------------------

    now = datetime.today()

    delta = now - order_date_db_str_to_date
    delta_object_today = delta.days

    #leadTme = order_list[0]['total_lead_time']
    lead_time_int = int(leadTme)
    lead_time_weeks_to_days = lead_time_int*7
    lead_time_in_days = timedelta(days=lead_time_weeks_to_days)

    #bufferTime = order_list[0]['dealer_buffer_time']
    buffer_time_int = int(bufferTime)
    buffer_time_weeks_to_days = buffer_time_int*7
    buffer_time_in_days = timedelta(days=buffer_time_weeks_to_days)

    est_deliver_time_today_raw = (((lead_time_weeks_to_days + buffer_time_weeks_to_days) - delta_object_today)/(lead_time_weeks_to_days + buffer_time_weeks_to_days))*100
    est_deliver_time_today = round((((lead_time_weeks_to_days + buffer_time_weeks_to_days) - delta_object_today)/(lead_time_weeks_to_days + buffer_time_weeks_to_days))*100)


    remaining_time_in_days = (lead_time_weeks_to_days + buffer_time_weeks_to_days) - delta_object_today

    result_days_to_weeks = round(remaining_time_in_days/7)

    #------------------------------------------------------------------------------
    form.pgrs_stage_name.choices = [(s, s)for s in wfl_stages]


    prgrs_tmln = order_Records[0]['progress_timeline']

    if prgrs_tmln:
        progress_stage_number = order_Records[0]['progress_stage_number']

    order_count = DOL_DB.get_count_of_orders_associated_by_po(po_no)
    return render_template('DOL_orderedit_workflow.html', 
                        orRecs = order_Records,
                        NexusId = nexusId,
                        workfl_name = workfl_name,
                        progress_stage_number = progress_stage_number,
                        prgrs_tmln = prgrs_tmln,
                        po_no = po_no,
                        order_count =order_count,
                        OrderDate = orderDate,
                        country = country,
                        LeadTme = leadTme,
                        BufferTime = bufferTime,
                        wfl_stages = wfl_stages,
                        brand = brand,
                        price = price,
                        est_dlvry = est_dlvry,
                        final_stage = final_stage,
                        form = form,
                        formclass = formclass,
                        progress_stages_color_codes = progress_stages_color_codes,
                        progress_stages_badge_index= progress_stages_badge_index,
                        progress_stages_dynamic = progress_stages_dynamic,
                        remaining_time_in_days = result_days_to_weeks,
                        est_deliver_time_today = est_deliver_time_today,
                        user = session['username_retailer'],
                        org = session['org_retailer'])



@app.route("/update_WForder/<NexusId>", methods=['POST'])
@login_required
def update_work_flow_orders_records(NexusId):
    form = WFOrderUpdateEditForm()
    nid = NexusId
    order_info = {}
    order_before_list = []
    order_after_list = []
    vendor_name_list = []
    consumer_info_list = []
    communication_Info = {}
    type_list = []
    cstm_type_list = []
    type_list_email = []

    last_acti_list = []
    
    session['sub_1'] = ''
    session['salutaion_1'] = ''
    session['text_body_1'] = ''
    session['conclusion_1'] = ''

    session['sub_2'] = ''
    session['salutaion_2'] = ''
    session['text_body_2'] = ''
    session['conclusion_2'] = ''

    communication_Info_Email = {}

    vendor_cur = DOL_DB.get_vendor_data()
    for d in vendor_cur:
        vendor_name_list.append((d['vendor_name'],d['vendor_name']))
        print(vendor_name_list)

    form.br_and.choices = vendor_name_list
    print('``````````````````````')
    print(form.br_and.choices)

    if form.validate_on_submit():
        order_before_editing_cur = DOL_DB.get_one_wforder_detail(nid)

        for l in order_before_editing_cur:
            order_before_list.append(l)
        print("==================order_before_list=========================================")
        print(order_before_list)

        po_number = request.form['po_no']
        order_price = request.form['or_price']
        order_cost = request.form['or_cost']
        model = request.form['mdl']
        size = request.form['siz']
        user_type = request.form['user_type']
        job_name = request.form['j_name']
        consumer_first_name = request.form['co_fname']
        consumer_last_name = request.form['co_lname']
        consumer_mobile_number = request.form['co_mo_num']
        consumer_email = request.form['co_email']

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

        address = request.form['address']
        city = request.form['ci_ty']
        consumer_zip_code = request.form['zip_code']
        brand = request.form['br_and']
        order_notes = request.form['o_notes']

        order_info['po_number'] = po_number.strip()
        order_info['order_price'] = order_price.strip()
        order_info['order_cost'] = order_cost.strip()
        order_info['model'] = model.strip()
        order_info['size'] = size.strip()
        order_info['user_type'] = user_type.strip()
        order_info['job_name'] = job_name.strip()
        order_info['consumer_first_name'] = consumer_first_name.strip()
        order_info['consumer_last_name'] = consumer_last_name.strip()
        order_info['consumer_mobile_number'] = consumer_mobile_number.strip()
        order_info['consumer_email'] = consumer_email.strip()
        order_info['country'] = Country.strip()
        order_info['state'] = State.strip()
        order_info['address'] = address.strip()
        order_info['city'] = city.strip()
        order_info['consumer_zip_code'] = consumer_zip_code.strip()
        order_info['brand'] = brand.strip()
        order_info['order_notes'] = order_notes.strip()

        DOL_DB.update_one_wforder_record(nid, order_info)

        order_after_editing_cur = DOL_DB.get_one_wforder_detail(nid)

        for h in order_after_editing_cur:
            order_after_list.append(h)
        print("==================order_after_list=========================================")
        print(order_after_list)

        cstm_msg_cursor = DOL_DB.get_custom_order_related_texts()
        for cst in cstm_msg_cursor:
            cstm_type_list.append(cst['custom_message_type'])
        print("----------------------Custom Type-----------------------------------------------")
        print(cstm_type_list)

        if cstm_type_list:
            for typ in cstm_type_list:

                if typ == "Order Editing":
                    print("=====================================TRUE")
                    
                    typ_cursor = DOL_DB.get_custom_order_related_texts_by_type(typ)
                    for t in typ_cursor:
                        type_list.append(t)
                    print("-------------------------------------------------------",type_list)
                    print(type_list)

            
                    session['sub_1'] = type_list[0]['create_order_text_box_1']
                    session['salutaion_1'] = type_list[0]['create_order_text_box_2']
                    session['text_body_1'] = type_list[0]['create_order_text_box_3']
                    #session['conclusion_1'] = type_list[0]['create_order_text_box_4']

                    text_message_1 = session['sub_1'] + NexusId + session['salutaion_1'] + config['consumer_portal_url']['CUST_URL'] + session['text_body_1']
                    print("------------------------------------------------------------text_message_1")
                    print(text_message_1)

                if  typ == "Order Editing Email":
                    print("===================EMAIL==================TRUE")
                    typ_cursor_email = DOL_DB.get_custom_order_related_texts_by_type(typ)
                    for t in typ_cursor_email:
                        type_list_email.append(t)
                    print("-----------------------------------------type_list_email--------------")
                    print(type_list_email)

                    session['sub_2'] = type_list_email[0]['create_order_text_box_1']
                    session['salutaion_2'] = type_list_email[0]['create_order_text_box_2']
                    session['text_body_2'] = type_list_email[0]['create_order_text_box_3']
                    session['conclusion_2'] = type_list_email[0]['create_order_text_box_4']
                    
                    text_message_2 = session['salutaion_2'] + NexusId + session['text_body_2'] + config['consumer_portal_url']['CUST_URL'] + session['conclusion_2']
                    print("text_message_2-----------------------------------------------------------------text_message_2")
                    print(text_message_2)
            

                    #text_message = "A change has been made to your order details with PO #" + order_info['po_number'] + "."
            communication_log_id = generate_id(4,2)
            currentDT = datetime.today()
            current_log_datetime = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")

            communication_Info['communication_log_id'] = communication_log_id.strip()
            communication_Info['nexus_id'] = nid.strip()
            communication_Info['po_number'] = order_info['po_number'].strip()
            communication_Info['logger_id'] = session['orgId_retailer']
            communication_Info['logger_name'] = session['fullname_retailer']
            communication_Info['logger_type'] = "Dealer".strip()
            communication_Info['orders_before_edit'] = order_before_list
            communication_Info['orders_after_edit'] = order_after_list
            communication_Info['subject'] = session['sub_1']
            communication_Info['sending_mode'] = "SMS".strip()
            communication_Info['message_plain_text'] = text_message_1
            communication_Info['current_log_datetime'] = current_log_datetime.strip()
            communication_Info['action_taken'] = "".strip()

            communication_Info_Email['communication_log_id'] = communication_log_id.strip()
            communication_Info_Email['nexus_id'] = nid.strip()
            communication_Info_Email['po_number'] = order_info['po_number'].strip()
            communication_Info_Email['logger_id'] = session['orgId_retailer']
            communication_Info_Email['logger_name'] = session['fullname_retailer']
            communication_Info_Email['logger_type'] = "Dealer".strip()
            communication_Info_Email['orders_before_edit'] = order_before_list
            communication_Info_Email['orders_after_edit'] = order_after_list
            communication_Info_Email['subject'] = session['sub_2']
            communication_Info_Email['sending_mode'] = "Email".strip()
            communication_Info_Email['message_plain_text'] = text_message_2
            communication_Info_Email['current_log_datetime'] = current_log_datetime.strip()
            communication_Info_Email['action_taken'] = "".strip()

            print("--------------communication_Info-----------------------------------------------")
            print(communication_Info)

            consumer_cursor = DOL_DB.get_consumer_data_by_phone(consumer_mobile_number)
            for c in consumer_cursor:
                consumer_info_list.append(c)
            print("---------------------------------------------consumer_info_list")
            print("Consumer Database------------ : ",consumer_info_list)

            if consumer_info_list:
                if consumer_info_list[0]['receive_sms_notification']==True and consumer_info_list[0]['receive_mail_notification']==False:
                    sendSms.send_order_entry_log_msg(consumer_mobile_number,communication_Info)
                    DOL_DB.save_communication_logs(communication_Info)

                elif consumer_info_list[0]['receive_mail_notification']==True and consumer_info_list[0]['receive_sms_notification']==False:
                    sendMail.send_order_entry_to_mail(consumer_email,communication_Info_Email)
                    DOL_DB.save_communication_logs(communication_Info_Email)

                elif consumer_info_list[0]['receive_mail_notification']==True and consumer_info_list[0]['receive_sms_notification']==True:
                    sendSms.send_order_entry_log_msg(consumer_mobile_number,communication_Info)
                    DOL_DB.save_communication_logs(communication_Info)
                    sendMail.send_order_entry_to_mail(consumer_email,communication_Info_Email)
                    DOL_DB.save_communication_logs(communication_Info_Email)

                else:
                    print("No action")

            else:
                sendSms.send_order_entry_log_msg(consumer_mobile_number,communication_Info)
                DOL_DB.save_communication_logs(communication_Info)
                sendMail.send_order_entry_to_mail(consumer_email,communication_Info_Email)
                DOL_DB.save_communication_logs(communication_Info_Email)
            
        currentDT = datetime.today()
        current_datetime_for_last_activity = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")

        last_acti_cur = DOL_DB.get_one_wforder_detail(nid)
        for la in last_acti_cur:
            last_acti_list.append(la)

        last_activity = last_acti_list[0]['last_activity']

        print("==================================================")
        print(last_activity)
        print("==================================================")

        last_activity = current_datetime_for_last_activity
        print(last_activity)

        DOL_DB.update_last_activity_of_an_order_change(nid,last_activity)
    print("===================================================================")
    print(form.errors)
    print("========================================================================")
    return redirect(url_for('edit_work_flow_order_records',nid=NexusId))


@app.route("/update_wflead/<NexusId>/<OrderDate>/<BufferTime>/<LeadTime>", methods=['POST'])
@login_required
def update_workflow_lead_records(NexusId,OrderDate,BufferTime,LeadTime):
    print("Inside Lead time Update----------------------------------")
    form = WFOrderUpdateLeadTimeForm()
    print("==================================================inside")
    if form.validate_on_submit():
        lTime_info = {}
        lTime_logs = {}
        order_List = []
        est_deliver_time = ''

        nid = NexusId

        order_cur = DOL_DB.get_one_wforder_detail(nid)
        for o in order_cur:
            order_List.append(o)

        consumer_phone = order_List[0]['consumer_mobile_number']
        consumer_email = order_List[0]['consumer_email']
        po_no = order_List[0]['po_number']
        original_est_dlr_date = order_List[0]['est_deliver_time']

        print("--------------------original_est_dlr_date : ", original_est_dlr_date)

        old_lead_time_int = int(LeadTime)
        old_lead_time_weeks_to_days = old_lead_time_int*7
        old_lead_time_in_days = timedelta(days=old_lead_time_weeks_to_days)

        order_date = OrderDate
        print(order_date)
        date_object = datetime.strptime(order_date,'%m-%d-%Y')
        datetime_object = date_object.date()

        lead_time_parameter = request.form['cal_wflead_type']
        total_lead_time = request.form['totl_lt']
        lead_time_reason = request.form['leadtm_reason']
        print(total_lead_time)

        lead_time_int = int(total_lead_time)
        new_lead_time_weeks_to_days = lead_time_int*7
        new_lead_time_in_days = timedelta(days=new_lead_time_weeks_to_days)

        dealer_buffer_time = BufferTime
        buffer_time_int = int(dealer_buffer_time)
        buffer_time_weeks_to_days = buffer_time_int*7
        buffer_time_in_days = timedelta(days=buffer_time_weeks_to_days)

        if lead_time_parameter == 'increase':
            new_lead_time_int = lead_time_int + old_lead_time_int
            est_deliver_time = datetime_object + old_lead_time_in_days + new_lead_time_in_days + buffer_time_in_days
            est_deliver_time_date_time_object = datetime.strptime(str(est_deliver_time),'%Y-%m-%d')
            new_est_deliver_time_date_time_object_date = est_deliver_time_date_time_object.strftime("%m-%d-%Y")
            
            lTime_info['est_deliver_time'] = new_est_deliver_time_date_time_object_date
            print("-----------------------------------------lTime_info['est_deliver_time'] : ",lTime_info['est_deliver_time'])
            

        else:
            new_lead_time_int = old_lead_time_int - lead_time_int 
            est_deliver_time = datetime_object + old_lead_time_in_days - new_lead_time_in_days + buffer_time_in_days
            est_deliver_time_date_time_object = datetime.strptime(str(est_deliver_time),'%Y-%m-%d')
            new_est_deliver_time_date_time_object_date = est_deliver_time_date_time_object.strftime("%m-%d-%Y")
            lTime_info['est_deliver_time'] = new_est_deliver_time_date_time_object_date
            print("======================================lTime_info['est_deliver_time'] : ",lTime_info['est_deliver_time'])


        lTime_info['change_time_entity'] = "Manufacturing lead time".strip()
        lTime_info['lead_time_parameter'] = lead_time_parameter
        lTime_info['total_lead_time'] = new_lead_time_int
        lTime_info['lead_time_reason'] = lead_time_reason

        print('--------------------------final vals------------------------')
        print(lead_time_parameter)
        print(total_lead_time)
        print("Lead time info : -----------", lTime_info)

        DOL_DB.update_wf_leadtime_record(nid, lTime_info)

        lTime_logs['NexusId'] = nid
        lTime_logs['order_date'] = str(order_date)
        lTime_logs['change_time_entity'] = "Manufacturing lead time"
        lTime_logs["lead_time_int"] = str(lead_time_int)
        lTime_logs["lead_time_parameter"] = lead_time_parameter
        lTime_logs['est_deliver_time'] = new_est_deliver_time_date_time_object_date
        lTime_logs['original_est_dlr_date'] = original_est_dlr_date
        lTime_logs['consumer_phone'] = consumer_phone
        lTime_logs['consumer_email'] = consumer_email
        lTime_logs['po_no'] = po_no
        lTime_logs['lead_time_reason'] = lead_time_reason

        save_lead_time_logs(lTime_logs)
    print(form.errors)
    return redirect(url_for('edit_work_flow_order_records',nid=NexusId))


def save_lead_time_logs(lTime_logs):
    communication_Info = {}
    consumer_info_list = []
    cstm_type_list = []
    type_list = []
    type_list_email = []
    communication_Info_Email = {}
    last_acti_list = []

    session['sub_1'] = ''
    session['salutaion_1'] = ''
    session['text_body_1'] = ''
    session['conclusion_1'] = ''

    session['sub_2'] = ''
    session['salutaion_2'] = ''
    session['text_body_2'] = ''
    session['conclusion_2'] = ''
    
    
    nid = lTime_logs["NexusId"]
    print(nid)
    consumer_phone = lTime_logs["consumer_phone"]
    consumer_email = lTime_logs["consumer_email"]
    
    if int(lTime_logs['lead_time_int']) > 1:
        week_placeholder_text = " weeks" 
    elif int(lTime_logs['lead_time_int']) == 1:
        week_placeholder_text = " week"
    else:
        week_placeholder_text = " week"

    consumer_cursor = DOL_DB.get_consumer_data_by_phone(consumer_phone)
    for c in consumer_cursor:
        consumer_info_list.append(c)
    print("---------------------------------------------consumer_info_list")
    print("Consumer Database------------ : ",consumer_info_list)

    cstm_msg_cursor = DOL_DB.get_custom_order_related_texts()
    for cst in cstm_msg_cursor:
        cstm_type_list.append(cst['custom_message_type'])
    print("----------------------Custom Type-----------------------------------------------")
    print(cstm_type_list)

    if cstm_type_list:
        for typ in cstm_type_list:

            if typ == "Order Lead Time Change":
                print("=====================================TRUE")
                
                typ_cursor = DOL_DB.get_custom_order_related_texts_by_type(typ)
                for t in typ_cursor:
                    type_list.append(t)
                print("-------------------------------------------------------",type_list)
                print(type_list)

        
                session['sub_1'] = type_list[0]['create_order_text_box_1']
                session['salutaion_1'] = type_list[0]['create_order_text_box_2']
                session['text_body_1'] = type_list[0]['create_order_text_box_3']
                session['conclusion_1'] = type_list[0]['create_order_text_box_4']
                
                text_message_1 = session['sub_1'] + lTime_logs['change_time_entity'] + " has been " + lTime_logs["lead_time_parameter"] + "d" + " by " + lTime_logs['lead_time_int'] + week_placeholder_text + session['salutaion_1'] + lTime_logs['est_deliver_time'] + session['text_body_1'] +  config['consumer_portal_url']['CUST_URL']  + session['conclusion_1'] + lTime_logs['NexusId'] + "." + " Reason: " + lTime_logs['lead_time_reason']



            if  typ == "Order Lead Time Change Email":
                print("===================EMAIL==================TRUE")
                typ_cursor_email = DOL_DB.get_custom_order_related_texts_by_type(typ)
                for t in typ_cursor_email:
                    type_list_email.append(t)
                print("-----------------------------------------type_list_email--------------")
                print(type_list_email)

                session['sub_2'] = type_list_email[0]['create_order_text_box_1']
                session['salutaion_2'] = type_list_email[0]['create_order_text_box_2']
                session['text_body_2'] = type_list_email[0]['create_order_text_box_3']
                session['conclusion_2'] = type_list_email[0]['create_order_text_box_4']
                
                text_message_2 = session['salutaion_2'] + lTime_logs['change_time_entity'] + " has been " + lTime_logs["lead_time_parameter"] + "d" + " by " + lTime_logs['lead_time_int'] + week_placeholder_text + session['text_body_2'] + lTime_logs['est_deliver_time'] + session['conclusion_2'] + config['consumer_portal_url']['CUST_URL'] + "Your Order ID is " + lTime_logs['NexusId'] + "." + " Reason: " + lTime_logs['lead_time_reason']

                print("text_message_2-----------------------------------------------------------------text_message_2")
                print(text_message_2)
                
        communication_log_id = generate_id(4,2)
        currentDT = datetime.today()
        current_log_datetime = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")

        communication_Info['communication_log_id'] = communication_log_id.strip()
        communication_Info['nexus_id'] = nid.strip()
        communication_Info['po_number'] = lTime_logs['po_no'].strip()
        communication_Info['logger_id'] = session['orgId_retailer']
        communication_Info['logger_name'] = session['fullname_retailer']
        communication_Info['logger_type'] = "Dealer".strip()
        communication_Info['subject'] = session['sub_1']
        communication_Info['sending_mode'] = "SMS".strip()
        communication_Info['message_plain_text'] = text_message_1
        communication_Info['current_log_datetime'] = current_log_datetime.strip()
        communication_Info['action_taken'] = "".strip()

        communication_Info_Email['communication_log_id'] = communication_log_id.strip()
        communication_Info_Email['nexus_id'] = nid.strip()
        communication_Info_Email['po_number'] = lTime_logs['po_no'].strip()
        communication_Info_Email['logger_id'] = session['orgId_retailer']
        communication_Info_Email['logger_name'] = session['fullname_retailer']
        communication_Info_Email['logger_type'] = "Dealer".strip()
        communication_Info_Email['subject'] = session['sub_2']
        communication_Info_Email['sending_mode'] = "Email".strip()
        communication_Info_Email['message_plain_text'] = text_message_2
        communication_Info_Email['current_log_datetime'] = current_log_datetime.strip()
        communication_Info_Email['action_taken'] = "".strip()

        print('=========================communication_Info==========================')
        
        if consumer_info_list:
            if consumer_info_list[0]['receive_sms_notification']==True and consumer_info_list[0]['receive_mail_notification']==False:
                sendSms.send_comm_log_msg(consumer_phone,communication_Info)
                DOL_DB.save_communication_logs(communication_Info)

            elif consumer_info_list[0]['receive_mail_notification']==True and consumer_info_list[0]['receive_sms_notification']==False:
                sendMail.send_comm_to_mail(consumer_email,communication_Info_Email)
                DOL_DB.save_communication_logs(communication_Info_Email)

            elif consumer_info_list[0]['receive_mail_notification']==True and consumer_info_list[0]['receive_sms_notification']==True:
                sendSms.send_comm_log_msg(consumer_phone,communication_Info)
                DOL_DB.save_communication_logs(communication_Info)
                sendMail.send_comm_to_mail(consumer_email,communication_Info_Email)
                DOL_DB.save_communication_logs(communication_Info_Email)

            else:
                print("No action")
        else:
             sendSms.send_comm_log_msg(consumer_phone,communication_Info)
             DOL_DB.save_communication_logs(communication_Info)
             sendMail.send_comm_to_mail(consumer_email,communication_Info_Email)
             DOL_DB.save_communication_logs(communication_Info_Email)
    
    currentDT = datetime.today()
    current_datetime_for_last_activity = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")

    last_acti_cur = DOL_DB.get_one_wforder_detail(nid)
    for la in last_acti_cur:
        last_acti_list.append(la)

    last_activity = last_acti_list[0]['last_activity']

    print("==================================================")
    print(last_activity)
    print("==================================================")

    last_activity = current_datetime_for_last_activity
    print(last_activity)

    DOL_DB.update_last_activity_of_an_order_change(nid,last_activity)
    return


@app.route("/update_WFbuffer/<NexusId>/<OrderDate>/<BufferTime>/<LeadTime>", methods=['POST'])
@login_required
def update_workflow_buffer_records(NexusId,OrderDate,BufferTime,LeadTime):
    form = WFOrderUpdateBufferTimeForm()
    if form.validate_on_submit():
        bTime_info = {}
        bTime_logs = {}
        nid = NexusId
        orderList = []
        order_cur = DOL_DB.get_one_wforder_detail(nid)

        for o in order_cur:
            orderList.append(o)

        consumer_phone = orderList[0]['consumer_mobile_number']
        consumer_email = orderList[0]['consumer_email']
        po_no = orderList[0]['po_number']
        original_est_dlr_date = orderList[0]['est_deliver_time']
        print("-----------------------original_est_dlr_date : ",original_est_dlr_date)

        old_buffer_time_int = int(BufferTime)
        old_buffer_time_weeks_to_days = old_buffer_time_int*7
        old_buffer_time_in_days = timedelta(days=old_buffer_time_weeks_to_days)

        order_date = OrderDate
        print(order_date)
        date_object = datetime.strptime(order_date,'%m-%d-%Y')
        datetime_object = date_object.date()

        buffer_time_parameter = request.form['cal_WFbuffer_type']
        dealer_buffer_time = request.form['delr_bfr_tm']
        buffer_time_reason = request.form['bfrtm_reason']
        print(dealer_buffer_time)

        buffer_time_int = int(dealer_buffer_time)
        print(buffer_time_int)
        new_buffer_time_weeks_to_days = buffer_time_int*7
        new_buffer_time_in_days = timedelta(days=new_buffer_time_weeks_to_days)

        old_lead_time_int = int(LeadTime)
        old_lead_time_weeks_to_days = old_lead_time_int*7
        old_lead_time_in_days = timedelta(days=old_lead_time_weeks_to_days)

        if buffer_time_parameter == 'increase':
            new_buffer_time_int = buffer_time_int + old_buffer_time_int
            est_deliver_time = datetime_object + old_buffer_time_in_days + new_buffer_time_in_days + old_lead_time_in_days
            est_deliver_time_date_time_object = datetime.strptime(str(est_deliver_time),'%Y-%m-%d')
            new_est_deliver_time_date_time_object_date = est_deliver_time_date_time_object.strftime("%m-%d-%Y")
            bTime_info['est_deliver_time'] = new_est_deliver_time_date_time_object_date
            print("-----------------------------------------bTime_info['est_deliver_time'] : ",bTime_info['est_deliver_time'])
        else:
            new_buffer_time_int = old_buffer_time_int - buffer_time_int 
            est_deliver_time = datetime_object + old_buffer_time_in_days - new_buffer_time_in_days + old_lead_time_in_days
            est_deliver_time_date_time_object = datetime.strptime(str(est_deliver_time),'%Y-%m-%d')
            new_est_deliver_time_date_time_object_date = est_deliver_time_date_time_object.strftime("%m-%d-%Y")
            bTime_info['est_deliver_time'] = new_est_deliver_time_date_time_object_date
            print("-----------------------------------------bTime_info['est_deliver_time'] : ",bTime_info['est_deliver_time'])


        bTime_info['change_time_entity'] = "Dealer lead time".strip()
        bTime_info['buffer_time_parameter'] = buffer_time_parameter
        bTime_info['dealer_buffer_time'] = new_buffer_time_int
        bTime_info['buffer_time_reason'] = buffer_time_reason

        print('--------------------------final vals------------------------')
        print(buffer_time_parameter)
        print(dealer_buffer_time)
        DOL_DB.update_wf_buffertime_record(nid, bTime_info)

        bTime_logs['NexusId'] = nid
        bTime_logs['order_date'] = str(order_date)
        bTime_logs['change_time_entity'] = "Dealer lead time"
        bTime_logs["buffer_time_int"] = str(buffer_time_int)
        bTime_logs["buffer_time_parameter"] = buffer_time_parameter
        bTime_logs['est_deliver_time'] = new_est_deliver_time_date_time_object_date
        bTime_logs['original_est_dlr_date'] = original_est_dlr_date
        bTime_logs['consumer_phone'] = consumer_phone
        bTime_logs['consumer_email'] = consumer_email
        bTime_logs['po_no'] = po_no
        bTime_logs['buffer_time_reason'] = buffer_time_reason
        save_buffer_time_logs(bTime_logs)
    return redirect(url_for('edit_work_flow_order_records',nid=NexusId))


def save_buffer_time_logs(bTime_logs):
    communication_Info = {}
    communication_Info_Email = {}
    consumer_info_list = []
    cstm_type_list = []
    type_list = []
    last_acti_list = []

    type_list_email = []
    
    session['sub_1'] = ''
    session['salutaion_1'] = ''
    session['text_body_1'] = ''
    session['conclusion_1'] = ''

    session['sub_2'] = ''
    session['salutaion_2'] = ''
    session['text_body_2'] = ''
    session['conclusion_2'] = ''
    
    
    nid = bTime_logs["NexusId"]
    print(nid)
    consumer_phone = bTime_logs["consumer_phone"]
    consumer_email = bTime_logs["consumer_email"]
    
    if int(bTime_logs['buffer_time_int']) > 1:
        week_placeholder_text = " weeks" 
    elif int(bTime_logs['buffer_time_int']) == 1:
        week_placeholder_text = " week"
    else:
        week_placeholder_text = " week"

    consumer_cursor = DOL_DB.get_consumer_data_by_phone(consumer_phone)
    for c in consumer_cursor:
        consumer_info_list.append(c)
    print("---------------------------------------------consumer_info_list")
    print("Consumer Database------------ : ",consumer_info_list)

    cstm_msg_cursor = DOL_DB.get_custom_order_related_texts()
    for cst in cstm_msg_cursor:
        cstm_type_list.append(cst['custom_message_type'])
    print("----------------------Custom Type-----------------------------------------------")
    print(cstm_type_list)

    if cstm_type_list:
        for typ in cstm_type_list:

            if typ == "Order Buffer Time Change":
                print("=====================================TRUE")
                
                typ_cursor = DOL_DB.get_custom_order_related_texts_by_type(typ)
                for t in typ_cursor:
                    type_list.append(t)
                print("-------------------------------------------------------",type_list)

                
            
                session['sub_1'] = type_list[0]['create_order_text_box_1']
                session['salutaion_1'] = type_list[0]['create_order_text_box_2']
                session['text_body_1'] = type_list[0]['create_order_text_box_3']
                session['conclusion_1'] = type_list[0]['create_order_text_box_4']

                
                text_message_1 = session['sub_1'] + bTime_logs['change_time_entity'] + " has been " + bTime_logs["buffer_time_parameter"] + "d" + " by " + bTime_logs['buffer_time_int'] + week_placeholder_text + session['salutaion_1'] + bTime_logs['est_deliver_time'] + session['text_body_1'] + config['consumer_portal_url']['CUST_URL'] + session['conclusion_1'] + bTime_logs['NexusId'] + "." + " Reason: " + bTime_logs['buffer_time_reason']

            if  typ == "Order Buffer Time Change Email":
                print("===================EMAIL==================TRUE")
                typ_cursor_email = DOL_DB.get_custom_order_related_texts_by_type(typ)
                for t in typ_cursor_email:
                    type_list_email.append(t)
                print("-----------------------------------------type_list_email--------------")
                print(type_list_email)

                session['sub_2'] = type_list_email[0]['create_order_text_box_1']
                session['salutaion_2'] = type_list_email[0]['create_order_text_box_2']
                session['text_body_2'] = type_list_email[0]['create_order_text_box_3']
                session['conclusion_2'] = type_list_email[0]['create_order_text_box_4']
                
                text_message_2 = session['salutaion_2'] + bTime_logs['change_time_entity'] + " has been " + bTime_logs["buffer_time_parameter"] + "d" + " by " + bTime_logs['buffer_time_int'] + week_placeholder_text + session['text_body_2'] + bTime_logs['est_deliver_time'] + session['conclusion_2'] + config['consumer_portal_url']['CUST_URL'] + "Your Order ID is " + bTime_logs['NexusId'] + "." + " Reason: " + bTime_logs['buffer_time_reason']
                print("text_message_2-----------------------------------------------------------------text_message_2")
                print(text_message_2)
        

        communication_log_id = generate_id(4,2)
        currentDT = datetime.today()
        current_log_datetime = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")

        communication_Info['communication_log_id'] = communication_log_id.strip()
        communication_Info['nexus_id'] = nid.strip()
        communication_Info['po_number'] = bTime_logs['po_no'].strip()
        communication_Info['logger_id'] = session['orgId_retailer']
        communication_Info['logger_name'] = session['fullname_retailer']
        communication_Info['logger_type'] = "Dealer".strip()
        communication_Info['subject'] = session['sub_2']
        communication_Info['sending_mode'] = "SMS".strip()
        communication_Info['message_plain_text'] = text_message_2
        communication_Info['current_log_datetime'] = current_log_datetime.strip()
        communication_Info['action_taken'] = "".strip()

        communication_Info_Email['communication_log_id'] = communication_log_id.strip()
        communication_Info_Email['nexus_id'] = nid.strip()
        communication_Info_Email['po_number'] = bTime_logs['po_no'].strip()
        communication_Info_Email['logger_id'] = session['orgId_retailer']
        communication_Info_Email['logger_name'] = session['fullname_retailer']
        communication_Info_Email['logger_type'] = "Dealer".strip()
        communication_Info_Email['subject'] = session['sub_2']
        communication_Info_Email['sending_mode'] = "Email".strip()
        communication_Info_Email['message_plain_text'] = text_message_2
        communication_Info_Email['current_log_datetime'] = current_log_datetime.strip()
        communication_Info_Email['action_taken'] = "".strip()

        print('=========================communication_Info==========================')

        if consumer_info_list:
            if consumer_info_list[0]['receive_sms_notification']==True and consumer_info_list[0]['receive_mail_notification']==False:
                sendSms.send_comm_log_msg(consumer_phone,communication_Info)
                DOL_DB.save_communication_logs(communication_Info)

            elif consumer_info_list[0]['receive_mail_notification']==True and consumer_info_list[0]['receive_sms_notification']==False:
                sendMail.send_comm_to_mail(consumer_email,communication_Info_Email)
                DOL_DB.save_communication_logs(communication_Info_Email)

            elif consumer_info_list[0]['receive_mail_notification']==True and consumer_info_list[0]['receive_sms_notification']==True:
                sendSms.send_comm_log_msg(consumer_phone,communication_Info)
                DOL_DB.save_communication_logs(communication_Info)
                sendMail.send_comm_to_mail(consumer_email,communication_Info_Email)
                DOL_DB.save_communication_logs(communication_Info_Email)
            else:
                print("No Action")

        else:
            sendSms.send_comm_log_msg(consumer_phone,communication_Info)
            DOL_DB.save_communication_logs(communication_Info)
            sendMail.send_comm_to_mail(consumer_email,communication_Info_Email)
            DOL_DB.save_communication_logs(communication_Info_Email)

    currentDT = datetime.today()
    current_datetime_for_last_activity = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")

    last_acti_cur = DOL_DB.get_one_wforder_detail(nid)
    for la in last_acti_cur:
        last_acti_list.append(la)

    last_activity = last_acti_list[0]['last_activity']

    print("==================================================")
    print(last_activity)
    print("==================================================")

    last_activity = current_datetime_for_last_activity
    print(last_activity)

    DOL_DB.update_last_activity_of_an_order_change(nid,last_activity)    
    return

@app.route("/update_wf_timeline/<NexusId>/<wrkflw_name>/<po_no>/<f_stage>/<c_id>", methods=['POST'])
@login_required
def update_workflow_timeline_records(NexusId,wrkflw_name,po_no,f_stage,c_id):
    print("===================inside: ",c_id)
    form = WFOrderUpdateProgressTimeLineForm()
    progress_stage_list = []
    cstm_type_list = []
    type_list = []
    communication_Info_Email = {}
    communication_Info = {}

    type_list_email = []

    last_acti_list = []
    
    session['sub_1'] = ''
    session['salutaion_1'] = ''
    session['text_body_1'] = ''
    session['conclusion_1'] = ''

    session['sub_2'] = ''
    session['salutaion_2'] = ''
    session['text_body_2'] = ''
    session['conclusion_2'] = ''
    
    
    prgrs_cursor = DOL_DB.get_one_wforder_detail(NexusId)
    for p in prgrs_cursor:
        progress_stage_list.append(p)
    workflw_request_automated_reviews = progress_stage_list[0]['request_automated_reviews']
    workflw_stages = progress_stage_list[0]['work_flow_stages']

    form.pgrs_stage_name.choices = [(s, s)for s in workflw_stages]


    if form.validate_on_submit():
        pgrs_info = {}
        order_list = []
        consumer_info_list = []
        print(wrkflw_name)

        sub_date_list = []

        order_cur = DOL_DB.get_one_wforder_detail(NexusId)
        for o in order_cur:
            order_list.append(o)

        consumer_phone = order_list[0]['consumer_mobile_number']
        consumer_email = order_list[0]['consumer_email']
        consumer_f_name = order_list[0]['consumer_first_name']
        consumer_l_name = order_list[0]['consumer_last_name']
        print(consumer_phone,consumer_email)

        progress_timeline = request.form['pgrs_stage_name']
        print(progress_timeline)
        

        progress_stage_number = workflw_stages.index(progress_timeline)


        pgrs_info['progress_timeline'] = progress_timeline
        pgrs_info['progress_stage_number'] = progress_stage_number

        DOL_DB.update_wf_timeline_progress(NexusId,pgrs_info)

        currentDT = datetime.today()
        order_submit_date = currentDT.strftime("%Y %b %d")

        if progress_timeline == f_stage:
            order_submit_cursor = DOL_DB.get_one_wforder_detail(NexusId)
            for sub in order_submit_cursor:
                sub_date_list.append(sub)

            order_submitted_date = sub_date_list[0]["order_completion_date"]

            order_submitted_date = order_submit_date
            DOL_DB.update_submitted_date_of_an_order(NexusId,order_submitted_date)

        

        consumer_cursor = DOL_DB.get_consumer_data_by_phone(consumer_phone)
        for c in consumer_cursor:
            consumer_info_list.append(c)


        cstm_msg_cursor = DOL_DB.get_custom_order_related_texts()
        for cst in cstm_msg_cursor:
            cstm_type_list.append(cst['custom_message_type'])

        if cstm_type_list:
            for typ in cstm_type_list:

                if typ == "Order Progress Time Line Change":
                    
                    typ_cursor = DOL_DB.get_custom_order_related_texts_by_type(typ)
                    for t in typ_cursor:
                        type_list.append(t)

                    
                
                    session['sub_1'] = type_list[0]['create_order_text_box_1']
                    session['salutaion_1'] = type_list[0]['create_order_text_box_2']
                    session['text_body_1'] = type_list[0]['create_order_text_box_3']

                    text_message_1 = session['sub_1'] + progress_timeline + session['salutaion_1'] + config['consumer_portal_url']['CUST_URL'] + session['text_body_1'] + NexusId


                if  typ == "Order Progress Time Line Change Email":
                    typ_cursor_email = DOL_DB.get_custom_order_related_texts_by_type(typ)
                    for t in typ_cursor_email:
                        type_list_email.append(t)

                    session['sub_2'] = type_list_email[0]['create_order_text_box_1']
                    session['salutaion_2'] = type_list_email[0]['create_order_text_box_2']
                    session['text_body_2'] = type_list_email[0]['create_order_text_box_3']
                    session['conclusion_2'] = type_list_email[0]['create_order_text_box_4']
                    text_message_2 = session['salutaion_2'] + progress_timeline + session['text_body_2'] + config['consumer_portal_url']['CUST_URL'] + session['conclusion_2'] + NexusId

            communication_log_id = generate_id(4,2)
            currentDT = datetime.today()
            current_log_datetime = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")

            communication_Info['communication_log_id'] = communication_log_id.strip()
            communication_Info['nexus_id'] = NexusId.strip()
            communication_Info['po_number'] = po_no.strip()
            communication_Info['logger_id'] = session['orgId_retailer']
            communication_Info['logger_name'] = session['fullname_retailer']
            communication_Info['logger_type'] = "Dealer".strip()
            communication_Info['subject'] = session['sub_2']
            communication_Info['sending_mode'] = 'SMS'.strip()
            communication_Info['message_plain_text'] = text_message_1
            communication_Info['current_log_datetime'] = current_log_datetime.strip()
            communication_Info['action_taken'] = "".strip()

            communication_Info_Email['communication_log_id'] = communication_log_id.strip()
            communication_Info_Email['nexus_id'] = NexusId.strip()
            communication_Info_Email['po_number'] = po_no.strip()
            communication_Info_Email['logger_id'] = session['orgId_retailer']
            communication_Info_Email['logger_name'] = session['fullname_retailer']
            communication_Info_Email['logger_type'] = "Dealer".strip()
            communication_Info_Email['subject'] = session['sub_2']
            communication_Info_Email['sending_mode'] = 'Email'.strip()
            communication_Info_Email['message_plain_text'] = text_message_2
            communication_Info_Email['current_log_datetime'] = current_log_datetime.strip()
            communication_Info_Email['action_taken'] = "".strip()


            if consumer_info_list:
                if consumer_info_list[0]['receive_sms_notification']==True and consumer_info_list[0]['receive_mail_notification']==False:
                    sendSms.send_comm_log_msg(consumer_phone,communication_Info)
                    DOL_DB.save_communication_logs(communication_Info)

                elif consumer_info_list[0]['receive_mail_notification']==True and consumer_info_list[0]['receive_sms_notification']==False:
                    sendMail.send_comm_to_mail(consumer_email,communication_Info_Email)
                    DOL_DB.save_communication_logs(communication_Info_Email)

                elif consumer_info_list[0]['receive_mail_notification']==True and consumer_info_list[0]['receive_sms_notification']==True:
                    sendSms.send_comm_log_msg(consumer_phone,communication_Info)
                    DOL_DB.save_communication_logs(communication_Info)
                    sendMail.send_comm_to_mail(consumer_email,communication_Info_Email)
                    DOL_DB.save_communication_logs(communication_Info_Email)

                else:
                    print("No action")
            else:
                sendSms.send_comm_log_msg(consumer_phone,communication_Info)
                DOL_DB.save_communication_logs(communication_Info)
                sendMail.send_comm_to_mail(consumer_email,communication_Info_Email)
                DOL_DB.save_communication_logs(communication_Info_Email)

        if progress_timeline == f_stage and workflw_request_automated_reviews == "Yes":
            print("------------------------------final stage review block")
            review_smart_process(NexusId,po_no,consumer_phone,consumer_email,consumer_f_name,consumer_l_name,c_id)
        

        currentDT = datetime.today()
        current_datetime_for_last_activity = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")

        last_acti_cur = DOL_DB.get_one_wforder_detail(NexusId)
        for la in last_acti_cur:
            last_acti_list.append(la)

        last_activity = last_acti_list[0]['last_activity']

        print("==================================================")
        print(last_activity)
        print("==================================================")

        last_activity = current_datetime_for_last_activity
        print(last_activity)

        DOL_DB.update_last_activity_of_an_order_change(NexusId,last_activity)    
    print(form.errors)
    return redirect(url_for('edit_work_flow_order_records',nid=NexusId))


def review_smart_process(n_id,po_no,c_ph_num,c_email,c_fname,c_lname,c_id):
    print("====================================consumer id: ", c_id)
    review_info = {}
    communication_Info = {}
    communication_Info_Email = {}
    consumer_info_list = []
    nexus_id = n_id
    dealer_id = session["orgId_retailer"]

    session['sub_1'] = ''
    session['salutaion_1'] = ''
    session['text_body_1'] = ''
    session['conclusion_1'] = ''
    session['sub_2'] = ''
    session['salutaion_2'] = ''
    session['text_body_2'] = ''
    session['conclusion_2'] = ''
    cstm_type_list = []
    type_list = []
    type_list_email = []

    domain_qa = "https://customer-ops.herokuapp.com"
    domain_local = "http://127.0.0.1:5000"
    

    review_activate_token  = generate_activation_token(5,5)
    print(review_activate_token)
    dynamic_url = domain_qa + "/smart_review/" + dealer_id + "/" + nexus_id + "/" + c_id + "/" + review_activate_token
    print(dynamic_url)

    review_info['nexus_id'] = nexus_id
    review_info['review_id'] = generate_id(4,2)
    review_info['consumer_id'] = c_id
    review_info['dealer_id'] = session['orgId_retailer']
    review_info['consumer_first_name'] = c_fname
    review_info['consumer_last_name'] = c_lname
    review_info['dealer_id'] = session['orgId_retailer']
    review_info['review_activate_token'] = review_activate_token
    review_info['dynamic_url'] = dynamic_url
    review_info['activation_state'] = "Inactive"
    review_info['review_opened_date_time'] = []
    review_info['review_submitted_date_time'] = ""
    review_info['service_review_stars'] = ""
    review_info['product_review_dynamic_url'] = ""
    review_info['product_review_activate_token'] = ""
    review_info['product_review_activation_state'] = "Inactive"
    review_info['product_review_activation_date_time'] = ""
    review_info['product_review_stars'] = ""
    review_info['product_review_feedback'] = ""
    review_info['product_review_opened_date_time'] = []
    review_info['product_review_submitted_date_time'] = ""
    review_info['consumer_feedback'] = ""
    review_info['professionalism'] = "No"
    review_info['good_communication'] = "No"
    review_info['on_time'] = "No"
    review_info['workmanship'] = "No"
    review_info['cleanliness'] = "No"
    review_info['design'] = "No"
    review_info['construction'] = "No"
    review_info['insulation'] = "No"
    review_info['color_and_finish'] = "No"
    review_info['too_noisy'] = "No"
    review_info['windows'] = "No"
    review_info['door_seals'] = "No"
    review_info['hardware'] = "No"
    review_info['consumer_feedback_date_time'] = ""
    review_info['review_clicked_yelp'] = ""
    review_info['review_clicked_google'] = ""

    DOL_DB.save_review_process_information(review_info)

    consumer_cursor = DOL_DB.get_consumer_data_by_phone(c_ph_num)
    for c in consumer_cursor:
        consumer_info_list.append(c)
    print("---------------------------------------------consumer_info_list")
    print("Consumer Database------------ : ",consumer_info_list)

    cstm_msg_cursor = DOL_DB.get_custom_order_related_texts()
    for cst in cstm_msg_cursor:
        cstm_type_list.append(cst['custom_message_type'])
    print("----------------------Custom Type-----------------------------------------------")
    print(cstm_type_list)

    if cstm_type_list:
        for typ in cstm_type_list:

            if typ == "Consumer Review Change":
                print("=====================================TRUE")
                    
                typ_cursor = DOL_DB.get_custom_order_related_texts_by_type(typ)
                for t in typ_cursor:
                    type_list.append(t)
                print("-------------------------------------------------------",type_list)
                
                session['sub_1'] = type_list[0]['create_order_text_box_1']
                session['salutaion_1'] = type_list[0]['create_order_text_box_2']

                text_message_1 = session['sub_1'] + dynamic_url + " " + session['salutaion_1'] + nexus_id
                print(text_message_1)


            if  typ == "Consumer Review Change Email":
                print("===================EMAIL==================TRUE")
                typ_cursor_email = DOL_DB.get_custom_order_related_texts_by_type(typ)
                for t in typ_cursor_email:
                    type_list_email.append(t)
                print("-----------------------------------------type_list_email--------------")
                print(type_list_email)

                session['sub_2'] = type_list_email[0]['create_order_text_box_1']
                session['salutaion_2'] = type_list_email[0]['create_order_text_box_2']
                session['text_body_2'] = type_list_email[0]['create_order_text_box_3']
                
                text_message_2 = session['salutaion_2'] + dynamic_url + " " + session['text_body_2'] + nexus_id
                print("============================================================================")
                print(text_message_2)
                print("==========================================================")

    

    #text_message = "Hello from Modern Garage Doors! Thank You for doing business with us. Feel free to provide us your feedback or review by clicking on this link. " + dynamic_url
    communication_log_id = generate_id(4,2)
    currentDT = datetime.today()
    current_log_datetime = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")

    communication_Info['communication_log_id'] = communication_log_id.strip()
    communication_Info['nexus_id'] = nexus_id.strip()
    communication_Info['po_number'] = po_no.strip()
    communication_Info['logger_id'] = session['orgId_retailer']
    communication_Info['logger_name'] = session['fullname_retailer']
    communication_Info['logger_type'] = "Dealer".strip()
    communication_Info['subject'] = session['sub_1']
    communication_Info['sending_mode'] = "SMS".strip()
    communication_Info['message_plain_text'] = text_message_1
    communication_Info['current_log_datetime'] = current_log_datetime.strip()
    communication_Info['action_taken'] = "".strip()

    communication_Info_Email['communication_log_id'] = communication_log_id.strip()
    communication_Info_Email['nexus_id'] = nexus_id.strip()
    communication_Info_Email['po_number'] = po_no.strip()
    communication_Info_Email['logger_id'] = session['orgId_retailer']
    communication_Info_Email['logger_name'] = session['fullname_retailer']
    communication_Info_Email['logger_type'] = "Dealer".strip()
    communication_Info_Email['subject'] = session['sub_2']
    communication_Info_Email['sending_mode'] = "Email".strip()
    communication_Info_Email['message_plain_text'] = text_message_2
    communication_Info_Email['current_log_datetime'] = current_log_datetime.strip()
    communication_Info_Email['action_taken'] = "".strip()

    print("--------------communication_Info-----------------------------------------------")
    print(communication_Info)
    
    if consumer_info_list:
        if consumer_info_list[0]['receive_sms_notification']==True and consumer_info_list[0]['receive_mail_notification']==False:
            print("k sms")
            sendSms.send_dynamic_url_to_consumer_via_SMS(c_ph_num,communication_Info)
            DOL_DB.save_communication_logs(communication_Info)

        elif consumer_info_list[0]['receive_mail_notification']==True and consumer_info_list[0]['receive_sms_notification']==False:
            sendMail.send_dynamic_url_to_consumer_via_email(c_email,communication_Info_Email)
            DOL_DB.save_communication_logs(communication_Info_Email)

        elif consumer_info_list[0]['receive_mail_notification']==True and consumer_info_list[0]['receive_sms_notification']==True:
            sendSms.send_dynamic_url_to_consumer_via_SMS(c_ph_num,communication_Info)
            DOL_DB.save_communication_logs(communication_Info)
            sendMail.send_dynamic_url_to_consumer_via_email(c_email,communication_Info_Email)
            DOL_DB.save_communication_logs(communication_Info_Email)

        else:
            print("No action")
    
    else:
        sendSms.send_dynamic_url_to_consumer_via_SMS(c_ph_num,communication_Info)
        DOL_DB.save_communication_logs(communication_Info)
        sendMail.send_dynamic_url_to_consumer_via_email(c_email,communication_Info_Email)
        DOL_DB.save_communication_logs(communication_Info_Email)
    return 


@app.route("/update_wf_preference/<NexusId>", methods=['POST'])
@login_required
def update_workflow_replyback_records(NexusId):
	form = WFOrderUpdateReplyPreferenceForm()
	if form.validate_on_submit():
		pfrnc_reply = request.form['pre_ference']
		print(pfrnc_reply)
		DOL_DB.update_wf_preference_replyback(NexusId,pfrnc_reply)
	return redirect(url_for('edit_work_flow_order_records',nid=NexusId))

@app.route("/deleteWFOrder/<nid>/<po_no>/<wf_name>/<od_prc>/<ph_num>", methods=['GET'])
@login_required
def delete_work_flow_order_by_ID(nid,po_no,wf_name,od_prc,ph_num):
    delete_logs = {}
    con_nx_list = []
    con_nix_Disc = {}
    
    d_id = session['orgId_retailer']
    nexus_id = nid
    
    delete_logs['delete_log_id'] = generate_id(4,2)
    delete_logs['nexus_id'] = nid
    delete_logs['po_number'] = po_no
    delete_logs['work_flow_name'] = wf_name
    delete_logs['order_price'] = od_prc
    delete_logs['deleted_by_id'] = session['orgId_retailer']
    delete_logs['deleted_by_name'] = session['fullname_retailer']
    print(delete_logs)

    con_nid_cursor = DOL_DB.get_po_phone_matrix_details_by_ph_num(ph_num)
    for ni in con_nid_cursor:
        con_nx_list.append(ni)
    print("con_nx_list : ",con_nx_list)
    for key in con_nx_list[0]:
        if key==d_id:
            nexus_id_list = con_nx_list[0][key]
            nexus_id_list.remove(nexus_id)
            con_nix_Disc[key]=nexus_id_list
            DOL_DB.update_po_numbers_after_delete_an_order(ph_num,con_nix_Disc)
    
    DOL_DB.save_delete_logs(delete_logs)
    DOL_DB.delete_an_wf_Order(nid)
    return redirect(url_for('WF_orderWrapper'))


#======================================SMS Logs Table====================================================================

@app.route("/sms_logs_table/<nid>", methods=['GET','POST'])
@login_required
def view_sms_logs(nid):
    sms_data = []

    sms_cur = DOL_DB.get_message_delivery_logs()
    for s in sms_cur:
        sms_data.append(s)
    return render_template('sms_logs_form.html',
                            smsList = sms_data,
                            user = session['username_retailer'],
                            org = session['org_retailer'])


@app.route("/delivery_status/<log_para>", methods=['GET'])
@login_required
def check_sms_delivery_status(log_para):
    log_para_list = log_para.split('_')
    msid = log_para_list[0]
    n_id = log_para_list[1]
    sendSms.send_sid_to_check_delivery_status(n_id,msid)
    return redirect(url_for('view_sms_logs', nid=n_id))



#======================================Order Custom View =============================================================
@app.route("/save_orderfields")
@login_required
def save_empty_fields():
    order_empinfo = DOL_info.setKeyFields()
    print(order_empinfo)
    DOL_DB.save_empty_keys_to_db(order_empinfo)
    return redirect(url_for('custom_viewWrapper'))


@app.route("/custom_view")
@login_required
def custom_viewWrapper():
    form_custom = OrderCustomViewerForm()
    form_wrkflw = WorkFlowCreate()
    form_cstm_order_msg = CustomOrdeEntryrMsg()
    form_cstm_order_edit_msg = CustomOrdeEditingMsg()
    form_cstm_order_lead_time_msg = CustomOrdeLeadTimeChangeMsg()
    form_cstm_order_buffer_time_msg = CustomOrdeBufferTimeChangeMsg()
    form_cstm_order_pgrs_time_line_msg = CustomOrdeProgressTimeLineChangeMsg()
    form_cstm_redbtn_lead_time_msg = CustomRedButtonLeadTimeChangeMsg()
    form_cstm_redbtn_buffer_time_msg = CustomRedButtonBufferTimeChangeMsg()
    form_cstm_custm_review_msg = CustomConsumerReviewMsg()
    form_cstm_custm_product_review_msg = CustomConsumerProductReviewMsg()
    form_cstm_blk_pgrs_tmln_msg = CustomRedbtnProgressTimeLineChangeMsg()
    form_cstm_welcome_note_msg = CustomWelcomeMessageMsg()

    form_cstm_order_mail = CustomOrdeEntryrMail()
    form_cstm_order_edit_mail = CustomOrdeEditingMail()
    form_cstm_order_lead_time_mail = CustomOrdeLeadTimeChangeMail()
    form_cstm_order_buffer_time_mail = CustomOrdeBufferTimeChangeMail()
    form_cstm_order_pgrs_time_line_mail = CustomOrdeProgressTimeLineChangeMail()
    form_cstm_redbtn_lead_time_mail = CustomRedButtonLeadTimeChangeMail()
    form_cstm_redbtn_buffer_time_mail = CustomRedButtonBufferTimeChangeMail()
    form_cstm_custm_review_mail = CustomConsumerReviewMail()
    form_cstm_custm_product_review_mail = CustomConsumerProductReviewMail()
    form_cstm_blk_pgrs_tm_line_mail = CustomRedbtnProgressTimeLineChangeMail()
    form_cstm_welcome_note_mail = CustomWelcomeMessageMail()

    form_review_page = ReviewPageCutomization()
    form_prod_review_page = ProductReviewPageCutomization()
    form_feedback_page = ReviewConsumerFeedbackPageCutomization()
    form_feedback_four_page = ReviewConsumerFeedbackPageCutomizationForFourandMore()
    form_covid_precaution = CovidPrecautionaryMessageForm()
    
    formclass = 'form-control'
    emp_dol_list = []
    emp_key_list = []
    work_flow_list = []
    key_dics = {}
    
    entry_msg_list = []
    edit_msg_list = []
    leadtime_msg_list = []
    bfrtime_msg_list = []
    pgrstmln_msg_list = []
    red_btn_ld_time_msg_list = []
    red_btn_bfr_time_msg_list = []
    consumer_review_msg_list = []
    consumer_product_review_msg_list = []
    red_btn_pgrs_time_line_msg_list = []
    welcome_note_msg_list = []

    entry_email_list = []
    edit_email_list = []
    leadtime_email_list = []
    bfrtime_email_list = []
    pgrstmln_email_list = []
    red_btn_ld_time_email_list = []
    red_btn_bfr_time_email_list = []
    consumer_review_email_list = []
    consumer_product_review_email_list = []
    red_btn_pgrs_time_line_email_list = []
    welcome_note_email_list = []

    review_greets_list = []
    prod_review_greets_list = []
    feedback_greets_list = []
    feedback_four_greets_list = []
    covid_precaution_list = []
    custom_workflow_list = []

    
    cst_mgs_type_list = []

    emp_DolCur = DOL_DB.get_empty_keys_from_db()
    for k in emp_DolCur:
        emp_dol_list.append(k)

    dealer_id = emp_dol_list[0]['dealer_id']

    order_keylist = []
    order_valuelist = []

    for keys_dict in emp_dol_list:
        for key, value in keys_dict.items():
            order_keylist.append(key)
            order_valuelist.append(value)

        order_id = order_keylist[0]
        po_number = order_keylist[1]
        order_date = order_keylist[2]
        work_flow_name = order_keylist[3]
        order_value = order_keylist[4]
        order_cost = order_keylist[5]
        model = order_keylist[6]
        size = order_keylist[7]
        user_type = order_keylist[8]
        job_name = order_keylist[9]
        consumer_first_name = order_keylist[10]
        consumer_last_name = order_keylist[11]
        consumer_mobile_number = order_keylist[12]
        consumer_email = order_keylist[13]
        zip_code = order_keylist[14]
        country = order_keylist[15]
        state = order_keylist[16]
        address = order_keylist[17]
        city = order_keylist[18]
        brand = order_keylist[20]
        total_lead_time = order_keylist[21]
        dealer_buffer_time = order_keylist[22]
        est_deliver_time = order_keylist[23]
        lead_time_parameter = order_keylist[24]
        buffer_time_parameter = order_keylist[25]
        progress_timeline = order_keylist[26]
        preference_reply_back = order_keylist[27]
        order_notes = order_keylist[28]
        last_activity  = order_keylist[29]
        order_completion_date  = order_keylist[30]

        form_custom.order_id.default = emp_dol_list[0]['order_id']
        form_custom.po_number.default = emp_dol_list[0]['po_number']
        form_custom.order_date.default = emp_dol_list[0]['order_date']
        form_custom.work_flow_name.default = emp_dol_list[0]['work_flow_name']
        form_custom.order_value.default = emp_dol_list[0]['order_value']
        form_custom.order_cost.default = emp_dol_list[0]['order_cost']
        form_custom.model.default = emp_dol_list[0]['model']
        form_custom.size.default = emp_dol_list[0]['size']
        form_custom.user_type.default = emp_dol_list[0]['user_type']
        form_custom.job_name.default = emp_dol_list[0]['job_name']
        form_custom.consumer_first_name.default = emp_dol_list[0]['consumer_first_name']
        form_custom.consumer_last_name.default = emp_dol_list[0]['consumer_last_name']
        form_custom.consumer_mobile_number.default = emp_dol_list[0]['consumer_mobile_number']
        form_custom.consumer_email.default = emp_dol_list[0]['consumer_email']
        form_custom.zip_code.default = emp_dol_list[0]['zip_code']
        form_custom.country.default = emp_dol_list[0]['country']
        form_custom.state.default = emp_dol_list[0]['state']
        form_custom.address.default = emp_dol_list[0]['address']
        form_custom.city.default = emp_dol_list[0]['city']
        form_custom.brand.default = emp_dol_list[0]['brand']
        form_custom.total_lead_time.default = emp_dol_list[0]['total_lead_time']
        form_custom.dealer_buffer_time.default = emp_dol_list[0]['dealer_buffer_time']
        form_custom.est_deliver_time.default = emp_dol_list[0]['est_deliver_time']
        form_custom.lead_time_parameter.default = emp_dol_list[0]['lead_time_parameter']
        form_custom.buffer_time_parameter.default = emp_dol_list[0]['buffer_time_parameter']
        form_custom.progress_timeline.default = emp_dol_list[0]['progress_timeline']
        form_custom.preference_reply_back.default = emp_dol_list[0]['preference_reply_back']
        form_custom.order_notes.default = emp_dol_list[0]['order_notes']
        form_custom.last_activity.default = emp_dol_list[0]['last_activity']
        form_custom.order_completion_date.default = emp_dol_list[0]['order_completion_date']
        form_custom.process()


    phone_num = session['phonenum_retailer']
    cstm_wrkflw_cur = DOL_DB.get_dealer_basic_details_from_dealer_account_by_phone_num(phone_num)
    for d in cstm_wrkflw_cur:
        custom_workflow_list.append(d)
    cstm_workflow = custom_workflow_list[0]['custom_workflow']



    wrk_flw_cur = DOL_DB.get_all_work_flow_data()
    for r in wrk_flw_cur:
        work_flow_list.append(r)

    entry_msg_cur = DOL_DB.get_custom_order_related_texts()
    for e in entry_msg_cur:
       cst_mgs_type_list.append(e['custom_message_type'])

    for typ in cst_mgs_type_list:
        
        if typ == 'Order Entry':
            typ_cur = DOL_DB.get_custom_order_related_texts_by_type(typ)
            for t in typ_cur:
                entry_msg_list.append(t)


        elif typ == 'Order Editing':
            typ_cur = DOL_DB.get_custom_order_related_texts_by_type(typ)
            for t in typ_cur:
                edit_msg_list.append(t)

        elif typ == 'Order Lead Time Change':
            typ_cur = DOL_DB.get_custom_order_related_texts_by_type(typ)
            for t in typ_cur:
                leadtime_msg_list.append(t)
        
        elif typ == 'Order Buffer Time Change':
            typ_cur = DOL_DB.get_custom_order_related_texts_by_type(typ)
            for t in typ_cur:
                bfrtime_msg_list.append(t)

        elif typ == 'Order Progress Time Line Change':
            typ_cur = DOL_DB.get_custom_order_related_texts_by_type(typ)
            for t in typ_cur:
                pgrstmln_msg_list.append(t)

        elif typ == 'Red Button Lead Time Change':
            typ_cur = DOL_DB.get_custom_order_related_texts_by_type(typ)
            for t in typ_cur:
                red_btn_ld_time_msg_list.append(t)

        elif typ == 'Red Button Buffer Time Change':
            typ_cur = DOL_DB.get_custom_order_related_texts_by_type(typ)
            for t in typ_cur:
                red_btn_bfr_time_msg_list.append(t)

        elif typ == 'Consumer Review Change':
            typ_cur = DOL_DB.get_custom_order_related_texts_by_type(typ)
            for t in typ_cur:
                consumer_review_msg_list.append(t)

        elif typ == 'Consumer Product Review Change':
            typ_cur = DOL_DB.get_custom_order_related_texts_by_type(typ)
            for t in typ_cur:
                consumer_product_review_msg_list.append(t)

        elif typ == 'Red Button Progress Time Line Change':
            typ_cur = DOL_DB.get_custom_order_related_texts_by_type(typ)
            for t in typ_cur:
                red_btn_pgrs_time_line_msg_list.append(t)

        elif typ == 'Welcome Note Change':
            typ_cur = DOL_DB.get_custom_order_related_texts_by_type(typ)
            for t in typ_cur:
                welcome_note_msg_list.append(t)
        
        elif typ == 'Order Entry Email':
            typ_cur = DOL_DB.get_custom_order_related_texts_by_type(typ)
            for t in typ_cur:
                entry_email_list.append(t)


        elif typ == 'Order Editing Email':
            typ_cur = DOL_DB.get_custom_order_related_texts_by_type(typ)
            for t in typ_cur:
                edit_email_list.append(t)

        elif typ == 'Order Lead Time Change Email':
            typ_cur = DOL_DB.get_custom_order_related_texts_by_type(typ)
            for t in typ_cur:
                leadtime_email_list.append(t)

        elif typ == 'Order Buffer Time Change Email':
            typ_cur = DOL_DB.get_custom_order_related_texts_by_type(typ)
            for t in typ_cur:
                bfrtime_email_list.append(t)

        elif typ == 'Order Progress Time Line Change Email':
            typ_cur = DOL_DB.get_custom_order_related_texts_by_type(typ)
            for t in typ_cur:
                pgrstmln_email_list.append(t)

        elif typ == 'Red Button Lead Time Change Email':
            typ_cur = DOL_DB.get_custom_order_related_texts_by_type(typ)
            for t in typ_cur:
                red_btn_ld_time_email_list.append(t)

        elif typ == 'Red Button Buffer Time Change Email':
            typ_cur = DOL_DB.get_custom_order_related_texts_by_type(typ)
            for t in typ_cur:
                red_btn_bfr_time_email_list.append(t)

        elif typ == 'Consumer Review Change Email':
            typ_cur = DOL_DB.get_custom_order_related_texts_by_type(typ)
            for t in typ_cur:
                consumer_review_email_list.append(t)

        elif typ == 'Consumer Product Review Change Email':
            typ_cur = DOL_DB.get_custom_order_related_texts_by_type(typ)
            for t in typ_cur:
                consumer_product_review_email_list.append(t)

        elif typ == 'Red Button Progress Time Line Change Email':
            typ_cur = DOL_DB.get_custom_order_related_texts_by_type(typ)
            for t in typ_cur:
                red_btn_pgrs_time_line_email_list.append(t)

        elif typ == 'Welcome Note Change Email':
            typ_cur = DOL_DB.get_custom_order_related_texts_by_type(typ)
            for t in typ_cur:
                welcome_note_email_list.append(t)

        elif typ == 'Review Page Customization':
            typ_cur = DOL_DB.get_custom_order_related_texts_by_type(typ)
            for t in typ_cur:
                review_greets_list.append(t)

        elif typ == 'Product Review Page Customization':
            typ_cur = DOL_DB.get_custom_order_related_texts_by_type(typ)
            for t in typ_cur:
                prod_review_greets_list.append(t)

        elif typ == 'Consumer Feedback Review Page Customization':
            typ_cur = DOL_DB.get_custom_order_related_texts_by_type(typ)
            for t in typ_cur:
                feedback_greets_list.append(t)

        elif typ == 'Consumer Feedback Review Page For Four And More Customization':
            typ_cur = DOL_DB.get_custom_order_related_texts_by_type(typ)
            for t in typ_cur:
                feedback_four_greets_list.append(t)

        elif typ == 'Covid Precautions Customization':
            typ_cur = DOL_DB.get_custom_order_related_texts_by_type(typ)
            for t in typ_cur:
                covid_precaution_list.append(t)
    
    return render_template('order_customView.html',
                            empList = emp_dol_list,
                            dealer_id= dealer_id,
                            order_keylist = order_keylist,
                            order_valuelist = order_valuelist,
                            order_id = order_id,
                            po_number = po_number,
                            order_date = order_date,
                            work_flow_name = work_flow_name,
                            order_value = order_value,
                            order_cost = order_cost,
                            model = model,
                            size = size,
                            user_type= user_type,
                            consumer_first_name = consumer_first_name,
                            consumer_last_name = consumer_last_name,
                            consumer_mobile_number = consumer_mobile_number,
                            consumer_email = consumer_email,
                            Country = country,
                            State = state,
                            address = address,
                            city = city,
                            zip_code = zip_code,
                            brand = brand,
                            total_lead_time = total_lead_time,
                            dealer_buffer_time = dealer_buffer_time,
                            est_deliver_time = est_deliver_time,
                            lead_time_parameter = lead_time_parameter,
                            buffer_time_parameter = buffer_time_parameter,
                            progress_timeline = progress_timeline,
                            preference_reply_back = preference_reply_back,
                            job_name = job_name,
                            order_notes = order_notes,
                            last_activity = last_activity,
                            order_completion_date = order_completion_date,
                            formclass=formclass,
                            form_custom = form_custom,
                            form_wrkflw = form_wrkflw,
                            workFlowlist = work_flow_list,
                            entry_msg_list = entry_msg_list,
                            edit_msg_list = edit_msg_list,
                            leadtime_msg_list = leadtime_msg_list,
                            bfrtime_msg_list = bfrtime_msg_list,
                            pgrstmln_msg_list = pgrstmln_msg_list,
                            red_btn_ld_time_msg_list = red_btn_ld_time_msg_list,
                            red_btn_bfr_time_msg_list = red_btn_bfr_time_msg_list,
                            consumer_review_msg_list = consumer_review_msg_list,
                            consumer_product_review_msg_list = consumer_product_review_msg_list,
                            red_btn_pgrs_time_line_msg_list = red_btn_pgrs_time_line_msg_list,
                            welcome_note_msg_list = welcome_note_msg_list,
                            entry_email_list = entry_email_list,
                            edit_email_list = edit_email_list,
                            leadtime_email_list = leadtime_email_list,
                            bfrtime_email_list = bfrtime_email_list,
                            pgrstmln_email_list = pgrstmln_email_list,
                            red_btn_ld_time_email_list = red_btn_ld_time_email_list,
                            red_btn_bfr_time_email_list = red_btn_bfr_time_email_list,
                            consumer_review_email_list = consumer_review_email_list,
                            consumer_product_review_email_list = consumer_product_review_email_list,
                            red_btn_pgrs_time_line_email_list = red_btn_pgrs_time_line_email_list,
                            welcome_note_email_list = welcome_note_email_list,
                            review_greets_list = review_greets_list,
                            feedback_greets_list = feedback_greets_list,
                            feedback_four_greets_list = feedback_four_greets_list,
                            prod_review_greets_list = prod_review_greets_list,
                            covid_precaution_list = covid_precaution_list,
                            form_cstm_order_msg = form_cstm_order_msg,
                            form_cstm_order_edit_msg = form_cstm_order_edit_msg,
                            form_cstm_order_lead_time_msg = form_cstm_order_lead_time_msg,
                            form_cstm_order_buffer_time_msg = form_cstm_order_buffer_time_msg,
                            form_cstm_order_pgrs_time_line_msg = form_cstm_order_pgrs_time_line_msg,
                            form_cstm_redbtn_lead_time_msg = form_cstm_redbtn_lead_time_msg,
                            form_cstm_redbtn_buffer_time_msg = form_cstm_redbtn_buffer_time_msg,
                            form_cstm_custm_review_msg = form_cstm_custm_review_msg,
                            form_cstm_custm_product_review_msg = form_cstm_custm_product_review_msg,
                            form_cstm_blk_pgrs_tmln_msg = form_cstm_blk_pgrs_tmln_msg,
                            form_cstm_order_mail = form_cstm_order_mail,
                            form_cstm_order_edit_mail = form_cstm_order_edit_mail,
                            form_cstm_order_lead_time_mail = form_cstm_order_lead_time_mail,
                            form_cstm_order_buffer_time_mail = form_cstm_order_buffer_time_mail,
                            form_cstm_order_pgrs_time_line_mail = form_cstm_order_pgrs_time_line_mail,
                            form_cstm_redbtn_lead_time_mail = form_cstm_redbtn_lead_time_mail,
                            form_cstm_redbtn_buffer_time_mail = form_cstm_redbtn_buffer_time_mail,
                            form_cstm_custm_review_mail = form_cstm_custm_review_mail,
                            form_cstm_custm_product_review_mail = form_cstm_custm_product_review_mail,
                            form_cstm_blk_pgrs_tm_line_mail = form_cstm_blk_pgrs_tm_line_mail,
                            form_cstm_welcome_note_msg = form_cstm_welcome_note_msg,
                            form_cstm_welcome_note_mail = form_cstm_welcome_note_mail,
                            form_review_page = form_review_page,
                            form_feedback_page = form_feedback_page,
                            form_feedback_four_page = form_feedback_four_page,
                            form_prod_review_page = form_prod_review_page,
                            form_covid_precaution = form_covid_precaution,
                            cstm_workflow = cstm_workflow,
                            user = session['username_retailer'],
                            org = session['org_retailer'],
                            org_id = session['orgId_retailer'])


@app.route("/update_customvals/<deal_id>",methods=['POST'])
@login_required
def update_order_custm_values(deal_id):
    form_custom = OrderCustomViewerForm()
    formclass = 'form-control'
    order_vals = {}
    emp_dol_list = []

    if form_custom.validate_on_submit():
        order_vals['order_id'] = request.form['order_id']
        order_vals['po_number'] = request.form['po_number']
        order_vals['order_date'] = request.form['order_date']
        order_vals['work_flow_name'] = request.form['work_flow_name']
        order_vals['order_value'] = request.form['order_value']
        order_vals['order_cost'] = request.form['order_cost']
        order_vals['model'] = request.form['model']
        order_vals['size'] = request.form['size']
        order_vals['user_type'] = request.form['user_type']
        order_vals['job_name'] = request.form['job_name']
        order_vals['consumer_first_name'] = request.form['consumer_first_name']
        order_vals['consumer_last_name'] = request.form['consumer_last_name']
        order_vals['consumer_mobile_number'] = request.form['consumer_mobile_number']
        order_vals['consumer_email'] = request.form['consumer_email']
        order_vals['country'] = request.form['country']
        order_vals['state'] = request.form['state']
        order_vals['address'] = request.form['address']
        order_vals['city'] = request.form['city']
        order_vals['brand'] = request.form['brand']
        order_vals['total_lead_time'] = request.form['total_lead_time']
        order_vals['dealer_buffer_time'] = request.form['dealer_buffer_time']
        order_vals['est_deliver_time'] = request.form['est_deliver_time']
        order_vals['lead_time_parameter'] = request.form['lead_time_parameter']
        order_vals['buffer_time_parameter'] = request.form['buffer_time_parameter']
        order_vals['progress_timeline'] = request.form['progress_timeline']
        order_vals['preference_reply_back'] = request.form['preference_reply_back']
        order_vals['order_notes'] = request.form['order_notes']
        order_vals['last_activity'] = request.form['last_activity']
        order_vals['order_completion_date'] = request.form['order_completion_date']

        DOL_DB.update_custom_choice_values_to_db(deal_id,order_vals)
    return redirect(url_for('WF_orderWrapper'))


#=======================================Custom Message for Order Entry SMS======================================================================

@app.route("/save_odr_msg",methods=['GET','POST'])
@login_required
def save_custom_order_entry_message():
    form_cstm_order_msg = CustomOrdeEntryrMsg()
    formclass = 'form-control'
    order_entry_msg = {}
    cst_mgs_type_list = []
    cstm_type_list = []
    session["order_entry_sms_cstm_type"] = ''
    print("--------------------------------inside save oder")
    phone = session['phonenum_retailer']
    print("----------------phone: ",phone)

    entry_msg_cur = DOL_DB.get_custom_order_related_texts()
    for e in entry_msg_cur:
        cst_mgs_type_list.append(e['custom_message_type'])
    print(cst_mgs_type_list)

    if cst_mgs_type_list:
        for typ in cst_mgs_type_list:
            
            if typ == 'Order Entry':
                session["order_entry_sms_cstm_type"] = typ
        
        typ_curs = DOL_DB.get_custom_order_related_sms_for_order_entry_by_cst_type()
        for t in typ_curs:
            cstm_type_list.append(t)
        print(cstm_type_list)

        if cstm_type_list:
            if form_cstm_order_msg.validate_on_submit():
                create_order_text_box_1 = request.form['crt_odr_tb_1']
                create_order_text_box_2 = request.form['crt_odr_tb_2']
                create_order_text_box_3 = request.form['crt_odr_tb_3']
                create_order_text_box_4 = request.form['crt_odr_tb_4']
                
                order_entry_msg['create_order_text_box_1'] = create_order_text_box_1
                order_entry_msg['create_order_text_box_2'] = create_order_text_box_2
                order_entry_msg['create_order_text_box_3'] = create_order_text_box_3
                order_entry_msg['create_order_text_box_4'] = create_order_text_box_4
                print("------------------------------------if :",order_entry_msg)

                text_message = order_entry_msg['create_order_text_box_1'] + "abcd12" + order_entry_msg['create_order_text_box_2'] + "02-03-2022" + order_entry_msg['create_order_text_box_3'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + ". " + order_entry_msg['create_order_text_box_4']
                DOL_DB.update_custom_order_entry_related_sms_by_type(order_entry_msg)
                sendSms.send_custom_test_message_to_dealer(phone,text_message)

        else:
            if form_cstm_order_msg.validate_on_submit():

                create_order_text_box_1 = request.form['crt_odr_tb_1']
                create_order_text_box_2 = request.form['crt_odr_tb_2']
                create_order_text_box_3 = request.form['crt_odr_tb_3']
                create_order_text_box_4 = request.form['crt_odr_tb_4']


                order_entry_msg['custom_message_type'] = "Order Entry".strip()
                order_entry_msg['create_order_text_box_1'] = create_order_text_box_1
                order_entry_msg['create_order_text_box_2'] = create_order_text_box_2
                order_entry_msg['create_order_text_box_3'] = create_order_text_box_3
                order_entry_msg['create_order_text_box_4'] = create_order_text_box_4
                text_message = order_entry_msg['create_order_text_box_1'] + "abcd12" + order_entry_msg['create_order_text_box_2'] + "02-03-2022" + order_entry_msg['create_order_text_box_3'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + ". " + order_entry_msg['create_order_text_box_4']
                DOL_DB.save_custom_order_related_texts(order_entry_msg)
                sendSms.send_custom_test_message_to_dealer(phone,text_message)
                  

    else:
        if form_cstm_order_msg.validate_on_submit():

            create_order_text_box_1 = request.form['crt_odr_tb_1']
            create_order_text_box_2 = request.form['crt_odr_tb_2']
            create_order_text_box_3 = request.form['crt_odr_tb_3']
            create_order_text_box_4 = request.form['crt_odr_tb_4']


            order_entry_msg['custom_message_type'] = "Order Entry"
            order_entry_msg['create_order_text_box_1'] = create_order_text_box_1
            order_entry_msg['create_order_text_box_2'] = create_order_text_box_2
            order_entry_msg['create_order_text_box_3'] = create_order_text_box_3
            order_entry_msg['create_order_text_box_4'] = create_order_text_box_4
            text_message = order_entry_msg['create_order_text_box_1'] + "abcd12" + order_entry_msg['create_order_text_box_2'] + "02-03-2022" + order_entry_msg['create_order_text_box_3'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + ". " + order_entry_msg['create_order_text_box_4']
            DOL_DB.save_custom_order_related_texts(order_entry_msg)
            sendSms.send_custom_test_message_to_dealer(phone,text_message)
                
    return redirect(url_for('custom_viewWrapper'))

@app.route("/save_odr_editmsg",methods=['POST'])
@login_required
def save_custom_order_edit_message():
    form_cstm_order_edit_msg = CustomOrdeEditingMsg()
    formclass = 'form-control'
    order_edit_msg = {}
    cst_mgs_type_list = []
    cstm_type_list = []
    session["order_edit_sms_cstm_type"] = ''
    phone = session['phonenum_retailer']

    entry_msg_cur = DOL_DB.get_custom_order_related_texts()
    for e in entry_msg_cur:
        cst_mgs_type_list.append(e['custom_message_type'])
    print(cst_mgs_type_list)

    if cst_mgs_type_list:
        for typ in cst_mgs_type_list:
            
            if typ == 'Order Editing':
                session["order_edit_sms_cstm_type"] = typ
        
        typ_curs = DOL_DB.get_custom_order_related_sms_for_order_edit_by_cst_type()
        for t in typ_curs:
            cstm_type_list.append(t)
        print(cstm_type_list)

        if cstm_type_list:
            if form_cstm_order_edit_msg.validate_on_submit():
                create_order_text_box_1 = request.form['crt_odr_ed_tb_1']
                create_order_text_box_2 = request.form['crt_odr_ed_tb_2']
                create_order_text_box_3 = request.form['crt_odr_ed_tb_3']
                
                order_edit_msg['create_order_text_box_1'] = create_order_text_box_1
                order_edit_msg['create_order_text_box_2'] = create_order_text_box_2
                order_edit_msg['create_order_text_box_3'] = create_order_text_box_3
                
                text_message = order_edit_msg['create_order_text_box_1'] + "abcd12" + order_edit_msg['create_order_text_box_2'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + order_edit_msg['create_order_text_box_3']
                DOL_DB.update_custom_order_edit_related_sms_by_type(order_edit_msg)
                sendSms.send_custom_test_message_to_dealer(phone,text_message)

        else:
            if form_cstm_order_edit_msg.validate_on_submit():

                create_order_text_box_1 = request.form['crt_odr_ed_tb_1']
                create_order_text_box_2 = request.form['crt_odr_ed_tb_2']
                create_order_text_box_3 = request.form['crt_odr_ed_tb_3']


                order_edit_msg['custom_message_type'] = "Order Editing"
                order_edit_msg['create_order_text_box_1'] = create_order_text_box_1
                order_edit_msg['create_order_text_box_2'] = create_order_text_box_2
                order_edit_msg['create_order_text_box_3'] = create_order_text_box_3
                
                text_message = order_edit_msg['create_order_text_box_1'] + "abcd12" + order_edit_msg['create_order_text_box_2'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + order_edit_msg['create_order_text_box_3']
                DOL_DB.save_custom_order_related_texts(order_edit_msg)
                sendSms.send_custom_test_message_to_dealer(phone,text_message)

    else:
        if form_cstm_order_edit_msg.validate_on_submit():

            create_order_text_box_1 = request.form['crt_odr_ed_tb_1']
            create_order_text_box_2 = request.form['crt_odr_ed_tb_2']
            create_order_text_box_3 = request.form['crt_odr_ed_tb_3']


            order_edit_msg['custom_message_type'] = "Order Editing"
            order_edit_msg['create_order_text_box_1'] = create_order_text_box_1
            order_edit_msg['create_order_text_box_2'] = create_order_text_box_2
            order_edit_msg['create_order_text_box_3'] = create_order_text_box_3

            text_message = order_edit_msg['create_order_text_box_1'] + "abcd12" + order_edit_msg['create_order_text_box_2'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + order_edit_msg['create_order_text_box_3']
            DOL_DB.save_custom_order_related_texts(order_edit_msg)
            sendSms.send_custom_test_message_to_dealer(phone,text_message)
    return redirect(url_for('custom_viewWrapper'))


@app.route("/save_odr_ldtimemsg",methods=['POST'])
@login_required
def save_custom_order_lead_time_message():
    form_cstm_order_lead_time_msg = CustomOrdeLeadTimeChangeMsg()
    formclass = 'form-control'
    order_ldtime_msg = {}
    cst_mgs_type_list = []
    cstm_type_list = []
    session["lead_time_sms_cstm_type"] = ''
    phone = session['phonenum_retailer']

    entry_msg_cur = DOL_DB.get_custom_order_related_texts()
    for e in entry_msg_cur:
        cst_mgs_type_list.append(e['custom_message_type'])
    print(cst_mgs_type_list)

    if cst_mgs_type_list:
        for typ in cst_mgs_type_list:
            
            if typ == 'Order Lead Time Change':
                session["lead_time_sms_cstm_type"] = typ
        typ_curs = DOL_DB.get_custom_order_related_sms_for_order_lead_time_by_cst_type()
        for t in typ_curs:
            cstm_type_list.append(t)
        print(cstm_type_list)

        if cstm_type_list:
            if form_cstm_order_lead_time_msg.validate_on_submit():
                create_order_text_box_1 = request.form['crt_odr_ld_tb_1']
                create_order_text_box_2 = request.form['crt_odr_ld_tb_2']
                create_order_text_box_3 = request.form['crt_odr_ld_tb_3']
                create_order_text_box_4 = request.form['crt_odr_ld_tb_4']
                
                order_ldtime_msg['create_order_text_box_1'] = create_order_text_box_1
                order_ldtime_msg['create_order_text_box_2'] = create_order_text_box_2
                order_ldtime_msg['create_order_text_box_3'] = create_order_text_box_3
                order_ldtime_msg['create_order_text_box_4'] = create_order_text_box_4
                
                text_message = order_ldtime_msg['create_order_text_box_1'] + "Manufacturing lead time has been increased/decreased by 7 week/weeks" + order_ldtime_msg['create_order_text_box_2'] + "Estimated Delivery Date - 11-23-2021"  + order_ldtime_msg['create_order_text_box_3'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + order_ldtime_msg['create_order_text_box_4'] + "abcd12"
                DOL_DB.update_custom_order_leadtime_related_sms_by_type(order_ldtime_msg)
                sendSms.send_custom_test_message_to_dealer(phone,text_message)

        else:
            if form_cstm_order_lead_time_msg.validate_on_submit():

                create_order_text_box_1 = request.form['crt_odr_ld_tb_1']
                create_order_text_box_2 = request.form['crt_odr_ld_tb_2']
                create_order_text_box_3 = request.form['crt_odr_ld_tb_3']
                create_order_text_box_4 = request.form['crt_odr_ld_tb_4']


                order_ldtime_msg['custom_message_type'] = "Order Lead Time Change"
                order_ldtime_msg['create_order_text_box_1'] = create_order_text_box_1
                order_ldtime_msg['create_order_text_box_2'] = create_order_text_box_2
                order_ldtime_msg['create_order_text_box_3'] = create_order_text_box_3
                order_ldtime_msg['create_order_text_box_4'] = create_order_text_box_4

                text_message = order_ldtime_msg['create_order_text_box_1'] + "Manufacturing lead time has been increased/decreased by 7 week/weeks" + order_ldtime_msg['create_order_text_box_2'] + "Estimated Delivery Date - 11-23-2021"  + order_ldtime_msg['create_order_text_box_3'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + order_ldtime_msg['create_order_text_box_4'] + "abcd12"
                DOL_DB.save_custom_order_related_texts(order_ldtime_msg)
                sendSms.send_custom_test_message_to_dealer(phone,text_message)

    else:
        if form_cstm_order_lead_time_msg.validate_on_submit():

            create_order_text_box_1 = request.form['crt_odr_ld_tb_1']
            create_order_text_box_2 = request.form['crt_odr_ld_tb_2']
            create_order_text_box_3 = request.form['crt_odr_ld_tb_3']
            create_order_text_box_4 = request.form['crt_odr_ld_tb_4']


            order_ldtime_msg['custom_message_type'] = "Order Lead Time Change"
            order_ldtime_msg['create_order_text_box_1'] = create_order_text_box_1
            order_ldtime_msg['create_order_text_box_2'] = create_order_text_box_2
            order_ldtime_msg['create_order_text_box_3'] = create_order_text_box_3
            order_ldtime_msg['create_order_text_box_4'] = create_order_text_box_4

            text_message = order_ldtime_msg['create_order_text_box_1'] + "Manufacturing lead time has been increased/decreased by 7 week/weeks" + order_ldtime_msg['create_order_text_box_2'] + "Estimated Delivery Date - 11-23-2021"  + order_ldtime_msg['create_order_text_box_3'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + order_ldtime_msg['create_order_text_box_4'] + "abcd12"
            DOL_DB.save_custom_order_related_texts(order_ldtime_msg)
            sendSms.send_custom_test_message_to_dealer(phone,text_message)
    return redirect(url_for('custom_viewWrapper'))


@app.route("/save_odr_bftimemsg",methods=['POST'])
@login_required
def save_custom_order_buffer_time_message():
    form_cstm_order_buffer_time_msg = CustomOrdeBufferTimeChangeMsg()
    formclass = 'form-control'
    order_bftime_msg = {}
    cst_mgs_type_list = []
    cstm_type_list = []
    session["buffer_time_sms_cstm_type"] = ''
    phone = session['phonenum_retailer']

    entry_msg_cur = DOL_DB.get_custom_order_related_texts()
    for e in entry_msg_cur:
        cst_mgs_type_list.append(e['custom_message_type'])
    print(cst_mgs_type_list)

    if cst_mgs_type_list:
        for typ in cst_mgs_type_list:
            
            if typ == 'Order Buffer Time Change':
                session["buffer_time_sms_cstm_type"] = typ
        typ_curs = DOL_DB.get_custom_order_related_sms_for_order_buffer_by_cst_type()
        for t in typ_curs:
            cstm_type_list.append(t)
        print(cstm_type_list)

        if cstm_type_list:
            if form_cstm_order_buffer_time_msg.validate_on_submit():
                create_order_text_box_1 = request.form['crt_odr_bf_tb_1']
                create_order_text_box_2 = request.form['crt_odr_bf_tb_2']
                create_order_text_box_3 = request.form['crt_odr_bf_tb_3']
                create_order_text_box_4 = request.form['crt_odr_bf_tb_4']
                
                order_bftime_msg['create_order_text_box_1'] = create_order_text_box_1
                order_bftime_msg['create_order_text_box_2'] = create_order_text_box_2
                order_bftime_msg['create_order_text_box_3'] = create_order_text_box_3
                order_bftime_msg['create_order_text_box_4'] = create_order_text_box_4
                
                text_message = order_bftime_msg['create_order_text_box_1'] + "Dealer lead time has been increased/decreased by 7 week/weeks" + order_bftime_msg['create_order_text_box_2'] + " Estimated Delivery Date - 11-23-2021" + order_bftime_msg['create_order_text_box_3'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + order_bftime_msg['create_order_text_box_4'] + "abcd12"
                DOL_DB.update_custom_order_buffertime_related_sms_by_type(order_bftime_msg)
                sendSms.send_custom_test_message_to_dealer(phone,text_message)

        else:
            if form_cstm_order_buffer_time_msg.validate_on_submit():

                create_order_text_box_1 = request.form['crt_odr_bf_tb_1']
                create_order_text_box_2 = request.form['crt_odr_bf_tb_2']
                create_order_text_box_3 = request.form['crt_odr_bf_tb_3']
                create_order_text_box_4 = request.form['crt_odr_bf_tb_4']


                order_bftime_msg['custom_message_type'] = "Order Buffer Time Change"
                order_bftime_msg['create_order_text_box_1'] = create_order_text_box_1
                order_bftime_msg['create_order_text_box_2'] = create_order_text_box_2
                order_bftime_msg['create_order_text_box_3'] = create_order_text_box_3
                order_bftime_msg['create_order_text_box_4'] = create_order_text_box_4

                text_message = order_bftime_msg['create_order_text_box_1'] + "Dealer lead time has been increased/decreased by 7 week/weeks" + order_bftime_msg['create_order_text_box_2'] + " Estimated Delivery Date - 11-23-2021" + order_bftime_msg['create_order_text_box_3'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + order_bftime_msg['create_order_text_box_4'] + "abcd12"
                DOL_DB.save_custom_order_related_texts(order_bftime_msg)
                sendSms.send_custom_test_message_to_dealer(phone,text_message)

    else:
        if form_cstm_order_buffer_time_msg.validate_on_submit():

            create_order_text_box_1 = request.form['crt_odr_bf_tb_1']
            create_order_text_box_2 = request.form['crt_odr_bf_tb_2']
            create_order_text_box_3 = request.form['crt_odr_bf_tb_3']
            create_order_text_box_4 = request.form['crt_odr_bf_tb_4']


            order_bftime_msg['custom_message_type'] = "Order Buffer Time Change"
            order_bftime_msg['create_order_text_box_1'] = create_order_text_box_1
            order_bftime_msg['create_order_text_box_2'] = create_order_text_box_2
            order_bftime_msg['create_order_text_box_3'] = create_order_text_box_3
            order_bftime_msg['create_order_text_box_4'] = create_order_text_box_4

            text_message = order_bftime_msg['create_order_text_box_1'] + "Dealer lead time has been increased/decreased by 7 week/weeks" + order_bftime_msg['create_order_text_box_2'] + " Estimated Delivery Date - 11-23-2021" + order_bftime_msg['create_order_text_box_3'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + order_bftime_msg['create_order_text_box_4'] + "abcd12"
            DOL_DB.save_custom_order_related_texts(order_bftime_msg)
            sendSms.send_custom_test_message_to_dealer(phone,text_message)
    return redirect(url_for('custom_viewWrapper'))

@app.route("/save_odr_pgrstimemsg",methods=['POST'])
@login_required
def save_custom_order_pgrs_timeline_message():
    form_cstm_order_pgrs_time_line_msg = CustomOrdeProgressTimeLineChangeMsg()
    formclass = 'form-control'
    order_pgrstime_msg = {}
    cst_mgs_type_list = []
    cstm_type_list = []
    session["prgs_time_line_sms_cstm_type"] = ''
    phone = session['phonenum_retailer']

    entry_msg_cur = DOL_DB.get_custom_order_related_texts()
    for e in entry_msg_cur:
        cst_mgs_type_list.append(e['custom_message_type'])
    print(cst_mgs_type_list)

    if cst_mgs_type_list:
        for typ in cst_mgs_type_list:
            
            if typ == 'Order Progress Time Line Change':
                print("---------------------------------True")
                session["prgs_time_line_sms_cstm_type"] = typ
            
            typ_curs = DOL_DB.get_custom_order_related_sms_for_progress_time_line_by_cst_type()
            for t in typ_curs:
                cstm_type_list.append(t)
        print(cstm_type_list)

        if cstm_type_list:
            if form_cstm_order_pgrs_time_line_msg.validate_on_submit():
                create_order_text_box_1 = request.form['crt_odr_pglt_tb_1']
                create_order_text_box_2 = request.form['crt_odr_pglt_tb_2']
                create_order_text_box_3 = request.form['crt_odr_pglt_tb_3']
                
                order_pgrstime_msg['create_order_text_box_1'] = create_order_text_box_1
                order_pgrstime_msg['create_order_text_box_2'] = create_order_text_box_2
                order_pgrstime_msg['create_order_text_box_3'] = create_order_text_box_3
                
                text_message = order_pgrstime_msg['create_order_text_box_1'] + "Shipped" + order_pgrstime_msg['create_order_text_box_2'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + order_pgrstime_msg['create_order_text_box_3'] + "abcd12"
                DOL_DB.update_custom_progress_time_line_related_sms_by_type(order_pgrstime_msg)
                sendSms.send_custom_test_message_to_dealer(phone,text_message)

        else:
            if form_cstm_order_pgrs_time_line_msg.validate_on_submit():

                create_order_text_box_1 = request.form['crt_odr_pglt_tb_1']
                create_order_text_box_2 = request.form['crt_odr_pglt_tb_2']
                create_order_text_box_3 = request.form['crt_odr_pglt_tb_3']


                order_pgrstime_msg['custom_message_type'] = "Order Progress Time Line Change"
                order_pgrstime_msg['create_order_text_box_1'] = create_order_text_box_1
                order_pgrstime_msg['create_order_text_box_2'] = create_order_text_box_2
                order_pgrstime_msg['create_order_text_box_3'] = create_order_text_box_3

                text_message = order_pgrstime_msg['create_order_text_box_1'] + "Shipped" + order_pgrstime_msg['create_order_text_box_2'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + order_pgrstime_msg['create_order_text_box_3'] + "abcd12"
                DOL_DB.save_custom_order_related_texts(order_pgrstime_msg)
                sendSms.send_custom_test_message_to_dealer(phone,text_message)

    else:
        if form_cstm_order_pgrs_time_line_msg.validate_on_submit():

            create_order_text_box_1 = request.form['crt_odr_pglt_tb_1']
            create_order_text_box_2 = request.form['crt_odr_pglt_tb_2']
            create_order_text_box_3 = request.form['crt_odr_pglt_tb_3']


            order_pgrstime_msg['custom_message_type'] = "Order Progress Time Line Change".strip()
            order_pgrstime_msg['create_order_text_box_1'] = create_order_text_box_1
            order_pgrstime_msg['create_order_text_box_2'] = create_order_text_box_2
            order_pgrstime_msg['create_order_text_box_3'] = create_order_text_box_3

            text_message = order_pgrstime_msg['create_order_text_box_1'] + "Shipped" + order_pgrstime_msg['create_order_text_box_2'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + order_pgrstime_msg['create_order_text_box_3'] + "abcd12"
            DOL_DB.save_custom_order_related_texts(order_pgrstime_msg)
            sendSms.send_custom_test_message_to_dealer(phone,text_message)
    return redirect(url_for('custom_viewWrapper'))

@app.route("/save_redbtn_ldtimemsg",methods=['POST'])
@login_required
def save_custom_redbutton_lead_time_message():
    form_cstm_redbtn_lead_time_msg = CustomRedButtonLeadTimeChangeMsg()
    formclass = 'form-control'
    order_rdbtnldtime_msg = {}
    cst_mgs_type_list = []
    cstm_type_list = []
    session["ld_time_sms_cstm_type"] = ''
    phone = session['phonenum_retailer']

    entry_msg_cur = DOL_DB.get_custom_order_related_texts()
    for e in entry_msg_cur:
        cst_mgs_type_list.append(e['custom_message_type'])
    print(cst_mgs_type_list)

    if cst_mgs_type_list:
        print("========================================TRUE")
        for typ in cst_mgs_type_list:
            
            if typ == 'Red Button Lead Time Change':
                session["ld_time_sms_cstm_type"] = typ
                print("---------------------------------True")
        typ_curs = DOL_DB.get_custom_order_related_sms_for_red_button_lead_by_cst_type()
        for t in typ_curs:
            cstm_type_list.append(t)
        print(cstm_type_list)

        if cstm_type_list:
            if form_cstm_redbtn_lead_time_msg.validate_on_submit():
                create_order_text_box_2 = request.form['crt_rbtnld_tb_2']
                create_order_text_box_3 = request.form['crt_rbtnld_tb_3']
                create_order_text_box_4 = request.form['crt_rbtnld_tb_4']
                
                order_rdbtnldtime_msg['create_order_text_box_2'] = create_order_text_box_2
                order_rdbtnldtime_msg['create_order_text_box_3'] = create_order_text_box_3
                order_rdbtnldtime_msg['create_order_text_box_4'] = create_order_text_box_4
                
                text_message = order_rdbtnldtime_msg['create_order_text_box_2'] + "Manufacturing lead time has been increased/decreased by 7 week/weeks. New estimated delivery date is 11-23-2021" + order_rdbtnldtime_msg['create_order_text_box_3'] + "abcd12" + order_rdbtnldtime_msg['create_order_text_box_4'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/"
                DOL_DB.update_custom_red_button_leadtime_related_sms_by_type(order_rdbtnldtime_msg)
                sendSms.send_custom_test_message_to_dealer(phone,text_message)


        else:
            if form_cstm_redbtn_lead_time_msg.validate_on_submit():
                create_order_text_box_2 = request.form['crt_rbtnld_tb_2']
                create_order_text_box_3 = request.form['crt_rbtnld_tb_3']
                create_order_text_box_4 = request.form['crt_rbtnld_tb_4']

                order_rdbtnldtime_msg['custom_message_type'] = "Red Button Lead Time Change"
                order_rdbtnldtime_msg['create_order_text_box_2'] = create_order_text_box_2
                order_rdbtnldtime_msg['create_order_text_box_3'] = create_order_text_box_3
                order_rdbtnldtime_msg['create_order_text_box_4'] = create_order_text_box_4
                
                text_message = order_rdbtnldtime_msg['create_order_text_box_2'] + "Manufacturing lead time has been increased/decreased by 7 week/weeks. New estimated delivery date is 11-23-2021" + order_rdbtnldtime_msg['create_order_text_box_3'] + "abcd12" + order_rdbtnldtime_msg['create_order_text_box_4'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/"
                DOL_DB.save_custom_order_related_texts(order_rdbtnldtime_msg)
                sendSms.send_custom_test_message_to_dealer(phone,text_message)


    else:
        if form_cstm_redbtn_lead_time_msg.validate_on_submit():
            create_order_text_box_2 = request.form['crt_rbtnld_tb_2']
            create_order_text_box_3 = request.form['crt_rbtnld_tb_3']
            create_order_text_box_4 = request.form['crt_rbtnld_tb_4']
            
            order_rdbtnldtime_msg['custom_message_type'] = "Red Button Lead Time Change"
            order_rdbtnldtime_msg['create_order_text_box_2'] = create_order_text_box_2
            order_rdbtnldtime_msg['create_order_text_box_3'] = create_order_text_box_3
            order_rdbtnldtime_msg['create_order_text_box_4'] = create_order_text_box_4

            text_message = order_rdbtnldtime_msg['create_order_text_box_2'] + "Manufacturing lead time has been increased/decreased by 7 week/weeks. New estimated delivery date is 11-23-2021" + order_rdbtnldtime_msg['create_order_text_box_3'] + "abcd12" + order_rdbtnldtime_msg['create_order_text_box_4'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/"
            DOL_DB.save_custom_order_related_texts(order_rdbtnldtime_msg)
            sendSms.send_custom_test_message_to_dealer(phone,text_message)
    

    print("=====================================================================")
    print(form_cstm_redbtn_lead_time_msg.errors)
    return redirect(url_for('custom_viewWrapper'))

@app.route("/save_redbtn_bfrtimemsg",methods=['POST'])
@login_required
def save_custom_redbutton_buffer_time_message():
    form_cstm_redbtn_buffer_time_msg = CustomRedButtonBufferTimeChangeMsg()
    formclass = 'form-control'
    redbtn_bftime_msg = {}
    cst_mgs_type_list = []
    cstm_type_list = []
    session["bfr_time_sms_cstm_type"] = ''
    phone = session['phonenum_retailer']

    entry_msg_cur = DOL_DB.get_custom_order_related_texts()
    for e in entry_msg_cur:
        cst_mgs_type_list.append(e['custom_message_type'])
    print(cst_mgs_type_list)

    if cst_mgs_type_list:
        for typ in cst_mgs_type_list:
            
            if typ == 'Red Button Buffer Time Change':
                session["bfr_time_sms_cstm_type"] = typ
        
        typ_curs = DOL_DB.get_custom_order_related_sms_for_red_button_buffer_by_cst_type()
        for t in typ_curs:
            cstm_type_list.append(t)
        print(cstm_type_list)

        if cstm_type_list:
            if form_cstm_redbtn_buffer_time_msg.validate_on_submit():
                create_order_text_box_2 = request.form['crt_rbtnlbfrd_tb_2']
                create_order_text_box_3 = request.form['crt_rbtnlbfrd_tb_3']
                create_order_text_box_4 = request.form['crt_rbtnlbfrd_tb_4']
                
                redbtn_bftime_msg['create_order_text_box_2'] = create_order_text_box_2
                redbtn_bftime_msg['create_order_text_box_3'] = create_order_text_box_3
                redbtn_bftime_msg['create_order_text_box_4'] = create_order_text_box_4
                
                text_message = redbtn_bftime_msg['create_order_text_box_2'] + "Dealer lead time has been increased/decreased by 7 week/weeks. New estimated delivery date is 11-23-2021" + redbtn_bftime_msg['create_order_text_box_3'] + "abcd12" + redbtn_bftime_msg['create_order_text_box_4'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/"
                DOL_DB.update_custom_red_button_buffertime_related_sms_by_type(redbtn_bftime_msg)
                sendSms.send_custom_test_message_to_dealer(phone,text_message)

        else:
            if form_cstm_redbtn_buffer_time_msg.validate_on_submit():
                create_order_text_box_2 = request.form['crt_rbtnlbfrd_tb_2']
                create_order_text_box_3 = request.form['crt_rbtnlbfrd_tb_3']
                create_order_text_box_4 = request.form['crt_rbtnlbfrd_tb_4']


                redbtn_bftime_msg['custom_message_type'] = "Red Button Buffer Time Change"
                redbtn_bftime_msg['create_order_text_box_2'] = create_order_text_box_2
                redbtn_bftime_msg['create_order_text_box_3'] = create_order_text_box_3
                redbtn_bftime_msg['create_order_text_box_4'] = create_order_text_box_4

                text_message = redbtn_bftime_msg['create_order_text_box_2'] + "Dealer lead time has been increased/decreased by 7 week/weeks. New estimated delivery date is 11-23-2021" + redbtn_bftime_msg['create_order_text_box_3'] + "abcd12" + redbtn_bftime_msg['create_order_text_box_4'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/"
                DOL_DB.save_custom_order_related_texts(redbtn_bftime_msg)
                sendSms.send_custom_test_message_to_dealer(phone,text_message)

    else:
        if form_cstm_redbtn_buffer_time_msg.validate_on_submit():
            create_order_text_box_2 = request.form['crt_rbtnlbfrd_tb_2']
            create_order_text_box_3 = request.form['crt_rbtnlbfrd_tb_3']
            create_order_text_box_4 = request.form['crt_rbtnlbfrd_tb_4']


            redbtn_bftime_msg['custom_message_type'] = "Red Button Buffer Time Change"
            redbtn_bftime_msg['create_order_text_box_2'] = create_order_text_box_2
            redbtn_bftime_msg['create_order_text_box_3'] = create_order_text_box_3
            redbtn_bftime_msg['create_order_text_box_4'] = create_order_text_box_4

            text_message = redbtn_bftime_msg['create_order_text_box_2'] + "Dealer lead time has been increased/decreased by 7 week/weeks. New estimated delivery date is 11-23-2021" + redbtn_bftime_msg['create_order_text_box_3'] + "abcd12" + redbtn_bftime_msg['create_order_text_box_4'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/"
            DOL_DB.save_custom_order_related_texts(redbtn_bftime_msg)
            sendSms.send_custom_test_message_to_dealer(phone,text_message)
    return redirect(url_for('custom_viewWrapper'))


@app.route("/save_custmreviewmsg",methods=['POST'])
@login_required
def save_custom_customer_review_message():
    print("=========================INSIDE REVIEW")
    form_cstm_custm_review_msg = CustomConsumerReviewMsg()
    formclass = 'form-control'
    custm_review_msg = {}
    cst_mgs_type_list = []
    cstm_type_list = []
    session["consumer_review_sms_cstm_type"] = ''
    phone = session['phonenum_retailer']

    entry_msg_cur = DOL_DB.get_custom_order_related_texts()
    for e in entry_msg_cur:
        cst_mgs_type_list.append(e['custom_message_type'])
    print(cst_mgs_type_list)

    if cst_mgs_type_list:
        for typ in cst_mgs_type_list:
            
            if typ == 'Consumer Review Change':
                session["consumer_review_sms_cstm_type"] = typ
        
        typ_curs = DOL_DB.get_custom_order_related_sms_for_consumer_review_by_cst_type()
        for t in typ_curs:
            cstm_type_list.append(t)
        print(cstm_type_list)

        if cstm_type_list:
            if form_cstm_custm_review_msg.validate_on_submit():
                create_order_text_box_1 = request.form['crt_cstnreview_tb_1']
                create_order_text_box_2 = request.form['crt_cstnreview_tb_2']
                
                custm_review_msg['create_order_text_box_1'] = create_order_text_box_1
                custm_review_msg['create_order_text_box_2'] = create_order_text_box_2
                
                text_message = custm_review_msg['create_order_text_box_1'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + custm_review_msg['create_order_text_box_2'] + "abcd12"
                DOL_DB.update_custom_consumer_review_related_sms_by_type(custm_review_msg)
                sendSms.send_custom_test_message_to_dealer(phone,text_message)

        else:
            if form_cstm_custm_review_msg.validate_on_submit():

                create_order_text_box_1 = request.form['crt_cstnreview_tb_1']
                create_order_text_box_2 = request.form['crt_cstnreview_tb_2']


                custm_review_msg['custom_message_type'] = "Consumer Review Change"
                custm_review_msg['create_order_text_box_1'] = create_order_text_box_1
                custm_review_msg['create_order_text_box_2'] = create_order_text_box_2

                text_message = custm_review_msg['create_order_text_box_1'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + custm_review_msg['create_order_text_box_2'] + "abcd12"
                DOL_DB.save_custom_order_related_texts(custm_review_msg)
                sendSms.send_custom_test_message_to_dealer(phone,text_message)

    else:
        if form_cstm_custm_review_msg.validate_on_submit():

            create_order_text_box_1 = request.form['crt_cstnreview_tb_1']
            create_order_text_box_2 = request.form['crt_cstnreview_tb_2']


            custm_review_msg['custom_message_type'] = "Consumer Review Change"
            custm_review_msg['create_order_text_box_1'] = create_order_text_box_1
            custm_review_msg['create_order_text_box_2'] = create_order_text_box_2

            text_message = custm_review_msg['create_order_text_box_1'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + custm_review_msg['create_order_text_box_2'] + "abcd12"
            DOL_DB.save_custom_order_related_texts(custm_review_msg)
            sendSms.send_custom_test_message_to_dealer(phone,text_message)
    return redirect(url_for('custom_viewWrapper'))

@app.route("/save_custmprod_reviewmsg",methods=['POST'])
@login_required
def save_custom_customer_product_review_message():
    print("=========================INSIDE REVIEW")
    form_cstm_custm_product_review_msg = CustomConsumerProductReviewMsg()
    formclass = 'form-control'
    custm_prod_review_msg = {}
    cst_mgs_type_list = []
    cstm_type_list = []
    session["consumer_product_review_sms_cstm_type"] = ''
    phone = session['phonenum_retailer']

    entry_msg_cur = DOL_DB.get_custom_order_related_texts()
    for e in entry_msg_cur:
        cst_mgs_type_list.append(e['custom_message_type'])
    print(cst_mgs_type_list)

    if cst_mgs_type_list:
        for typ in cst_mgs_type_list:
            
            if typ == 'Consumer Product Review Change':
                session["consumer_product_review_sms_cstm_type"] = typ
        
        typ_curs = DOL_DB.get_custom_order_related_sms_for_consumer_product_review_by_cst_type()
        for t in typ_curs:
            cstm_type_list.append(t)
        print(cstm_type_list)

        if cstm_type_list:
            if form_cstm_custm_product_review_msg.validate_on_submit():
                create_order_text_box_1 = request.form['crt_cstn_prodreview_tb_1']
                create_order_text_box_2 = request.form['crt_cstn_prodreview_tb_2']
                
                custm_prod_review_msg['create_order_text_box_1'] = create_order_text_box_1
                custm_prod_review_msg['create_order_text_box_2'] = create_order_text_box_2
                
                text_message = custm_prod_review_msg['create_order_text_box_1'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + custm_prod_review_msg['create_order_text_box_2'] + "abcd12"
                DOL_DB.update_custom_consumer_product_review_related_sms_by_type(custm_prod_review_msg)
                sendSms.send_custom_test_message_to_dealer(phone,text_message)

        else:
            if form_cstm_custm_product_review_msg.validate_on_submit():

                create_order_text_box_1 = request.form['crt_cstn_prodreview_tb_1']
                create_order_text_box_2 = request.form['crt_cstn_prodreview_tb_2']


                custm_prod_review_msg['custom_message_type'] = "Consumer Product Review Change"
                custm_prod_review_msg['create_order_text_box_1'] = create_order_text_box_1
                custm_prod_review_msg['create_order_text_box_2'] = create_order_text_box_2

                text_message = custm_prod_review_msg['create_order_text_box_1'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + custm_prod_review_msg['create_order_text_box_2'] + "abcd12"
                DOL_DB.save_custom_order_related_texts(custm_prod_review_msg)
                sendSms.send_custom_test_message_to_dealer(phone,text_message)

    else:
        if form_cstm_custm_product_review_msg.validate_on_submit():

            create_order_text_box_1 = request.form['crt_cstn_prodreview_tb_1']
            create_order_text_box_2 = request.form['crt_cstn_prodreview_tb_2']


            custm_prod_review_msg['custom_message_type'] = "CConsumer Product Review Change"
            custm_prod_review_msg['create_order_text_box_1'] = create_order_text_box_1
            custm_prod_review_msg['create_order_text_box_2'] = create_order_text_box_2

            text_message = custm_prod_review_msg['create_order_text_box_1'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + custm_prod_review_msg['create_order_text_box_2'] + "abcd12"
            DOL_DB.save_custom_order_related_texts(custm_prod_review_msg)
            sendSms.send_custom_test_message_to_dealer(phone,text_message)
    return redirect(url_for('custom_viewWrapper'))


@app.route("/save_blk_pgrstimemsg",methods=['POST'])
@login_required
def save_custom_bulk_pgrs_timeline_message():
    form_cstm_order_pgrs_time_line_msg = CustomRedbtnProgressTimeLineChangeMsg()
    formclass = 'form-control'
    blk_pgrstime_msg = {}
    cst_mgs_type_list = []
    cstm_type_list = []
    session["blk_prgs_time_line_sms_cstm_type"] = ''
    phone = session['phonenum_retailer']

    entry_msg_cur = DOL_DB.get_custom_order_related_texts()
    for e in entry_msg_cur:
        cst_mgs_type_list.append(e['custom_message_type'])
    print(cst_mgs_type_list)

    if cst_mgs_type_list:
        for typ in cst_mgs_type_list:
            
            if typ == 'Red Button Progress Time Line Change':
                print("---------------------------------True")
                session["blk_prgs_time_line_sms_cstm_type"] = typ
            
            typ_curs = DOL_DB.get_custom_blk_related_sms_for_progress_time_line_by_cst_type()
            for t in typ_curs:
                cstm_type_list.append(t)
        print(cstm_type_list)

        if cstm_type_list:
            if form_cstm_order_pgrs_time_line_msg.validate_on_submit():
                create_order_text_box_1 = request.form['crt_redbtn_pglt_tb_1']
                create_order_text_box_2 = request.form['crt_redbtn_pglt_tb_2']
                create_order_text_box_3 = request.form['crt_redbtn_pglt_tb_3']
                create_order_text_box_4 = request.form['crt_redbtn_pglt_tb_4']
                
                blk_pgrstime_msg['create_order_text_box_1'] = create_order_text_box_1
                blk_pgrstime_msg['create_order_text_box_2'] = create_order_text_box_2
                blk_pgrstime_msg['create_order_text_box_3'] = create_order_text_box_3
                blk_pgrstime_msg['create_order_text_box_4'] = create_order_text_box_4
                
                text_message = blk_pgrstime_msg['create_order_text_box_1'] + blk_pgrstime_msg['create_order_text_box_2'] + "Order is confirmed" + blk_pgrstime_msg['create_order_text_box_3'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + blk_pgrstime_msg['create_order_text_box_4'] + "abcd12"
                DOL_DB.update_custom_blk_progress_time_line_related_sms_by_type(blk_pgrstime_msg)
                sendSms.send_custom_test_message_to_dealer(phone,text_message)

        else:
            if form_cstm_order_pgrs_time_line_msg.validate_on_submit():

                create_order_text_box_1 = request.form['crt_redbtn_pglt_tb_1']
                create_order_text_box_2 = request.form['crt_redbtn_pglt_tb_2']
                create_order_text_box_3 = request.form['crt_redbtn_pglt_tb_3']
                create_order_text_box_4 = request.form['crt_redbtn_pglt_tb_4']


                blk_pgrstime_msg['custom_message_type'] = "Red Button Progress Time Line Change"
                blk_pgrstime_msg['create_order_text_box_1'] = create_order_text_box_1
                blk_pgrstime_msg['create_order_text_box_2'] = create_order_text_box_2
                blk_pgrstime_msg['create_order_text_box_3'] = create_order_text_box_3
                blk_pgrstime_msg['create_order_text_box_4'] = create_order_text_box_4

                text_message = blk_pgrstime_msg['create_order_text_box_1'] + blk_pgrstime_msg['create_order_text_box_2'] + "Order is confirmed" + blk_pgrstime_msg['create_order_text_box_3'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + blk_pgrstime_msg['create_order_text_box_4'] + "abcd12"
                DOL_DB.save_custom_order_related_texts(blk_pgrstime_msg)
                sendSms.send_custom_test_message_to_dealer(phone,text_message)

    else:
        if form_cstm_order_pgrs_time_line_msg.validate_on_submit():

            create_order_text_box_1 = request.form['crt_redbtn_pglt_tb_1']
            create_order_text_box_2 = request.form['crt_redbtn_pglt_tb_2']
            create_order_text_box_3 = request.form['crt_redbtn_pglt_tb_3']
            create_order_text_box_4 = request.form['crt_redbtn_pglt_tb_4']


            blk_pgrstime_msg['custom_message_type'] = "Red Button Progress Time Line Change".strip()
            blk_pgrstime_msg['create_order_text_box_1'] = create_order_text_box_1
            blk_pgrstime_msg['create_order_text_box_2'] = create_order_text_box_2
            blk_pgrstime_msg['create_order_text_box_3'] = create_order_text_box_3
            blk_pgrstime_msg['create_order_text_box_4'] = create_order_text_box_4

            text_message = blk_pgrstime_msg['create_order_text_box_1'] + blk_pgrstime_msg['create_order_text_box_2'] + "Order is confirmed" + blk_pgrstime_msg['create_order_text_box_3'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + blk_pgrstime_msg['create_order_text_box_4'] + "abcd12"
            DOL_DB.save_custom_order_related_texts(blk_pgrstime_msg)
            sendSms.send_custom_test_message_to_dealer(phone,text_message)
    return redirect(url_for('custom_viewWrapper'))



@app.route("/save_welcome",methods=['POST'])
@login_required
def save_custom_welcome_note_message():
    form_cstm_welcome_note_msg = CustomWelcomeMessageMsg()
    formclass = 'form-control'
    welcome_msg = {}
    cst_mgs_type_list = []
    cstm_type_list = []
    session["welcome_note"] = ''
    phone = session['phonenum_retailer']

    entry_msg_cur = DOL_DB.get_custom_order_related_texts()
    for e in entry_msg_cur:
        cst_mgs_type_list.append(e['custom_message_type'])
    print(cst_mgs_type_list)

    if cst_mgs_type_list:
        for typ in cst_mgs_type_list:
            
            if typ == 'Welcome Note Change':
                print("---------------------------------True")
                session["welcome_note"] = typ
            
            typ_curs = DOL_DB.get_custom_welcome_note_sms_by_cst_type()
            for t in typ_curs:
                cstm_type_list.append(t)
        print(cstm_type_list)

        if cstm_type_list:
            if form_cstm_welcome_note_msg.validate_on_submit():
                create_order_text_box_1 = request.form['crt_wlcmmsg_tb_1']
                welcome_msg['create_order_text_box_1'] = create_order_text_box_1
                
                text_message = welcome_msg['create_order_text_box_1']
                DOL_DB.update_custom_wecome_note_sms_by_type(welcome_msg)
                sendSms.send_custom_test_message_to_dealer(phone,text_message)

        else:
            if form_cstm_welcome_note_msg.validate_on_submit():

                create_order_text_box_1 = request.form['crt_wlcmmsg_tb_1']
                
                welcome_msg['custom_message_type'] = "Welcome Note Change"
                welcome_msg['create_order_text_box_1'] = create_order_text_box_1
                
                text_message = welcome_msg['create_order_text_box_1']
                DOL_DB.save_custom_order_related_texts(welcome_msg)
                sendSms.send_custom_test_message_to_dealer(phone,text_message)

    else:
        if form_cstm_welcome_note_msg.validate_on_submit():

            create_order_text_box_1 = request.form['crt_wlcmmsg_tb_1']

            welcome_msg['custom_message_type'] = "Welcome Note Change".strip()
            welcome_msg['create_order_text_box_1'] = create_order_text_box_1

            text_message = welcome_msg['create_order_text_box_1']
            DOL_DB.save_custom_order_related_texts(welcome_msg)
            sendSms.send_custom_test_message_to_dealer(phone,text_message)
    return redirect(url_for('custom_viewWrapper'))


#=================================================Custom Email for Order==========================================================

@app.route("/save_odr_mail",methods=['POST'])
@login_required
def save_custom_order_entry_email():
    form_cstm_order_mail = CustomOrdeEntryrMail()
    formclass = 'form-control'
    order_entry_mail = {}
    cst_mgs_type_list = []
    cstm_type_list = []
    session["order_entry_cstm_type"] = ''
    email = session['email_retailer']

    entry_msg_cur = DOL_DB.get_custom_order_related_texts()
    for e in entry_msg_cur:
        cst_mgs_type_list.append(e['custom_message_type'])
    print(cst_mgs_type_list)

    if cst_mgs_type_list:
        for typ in cst_mgs_type_list:
            
            if typ == 'Order Entry Email':
                session["order_entry_cstm_type"] = typ
        
        typ_curs = DOL_DB.get_custom_order_related_texts_for_order_entry_by_cst_type()
        for t in typ_curs:
            cstm_type_list.append(t)
        print(cstm_type_list)

        if cstm_type_list:
            if form_cstm_order_mail.validate_on_submit():
                create_order_text_box_1 = request.form['crt_odr_mail_tb_1']
                create_order_text_box_2 = request.form['crt_odr_mail_tb_2']
                create_order_text_box_3 = request.form['crt_odr_mail_tb_3']
                create_order_text_box_4 = request.form['crt_odr_mail_tb_4']
                
                order_entry_mail['create_order_text_box_1'] = create_order_text_box_1
                order_entry_mail['create_order_text_box_2'] = create_order_text_box_2
                order_entry_mail['create_order_text_box_3'] = create_order_text_box_3
                order_entry_mail['create_order_text_box_4'] = create_order_text_box_4
                
                subject = order_entry_mail['create_order_text_box_1']
                text_message = order_entry_mail['create_order_text_box_2'] + "abcd12" + order_entry_mail['create_order_text_box_3'] + "02-03-2022" + order_entry_mail['create_order_text_box_4'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/"
                DOL_DB.update_custom_order_entry_related_texts_by_type(order_entry_mail)
                sendMail.send_custom_test_email_to_dealer(email,subject,text_message)

        else:
            if form_cstm_order_mail.validate_on_submit():

                create_order_text_box_1 = request.form['crt_odr_mail_tb_1']
                create_order_text_box_2 = request.form['crt_odr_mail_tb_2']
                create_order_text_box_3 = request.form['crt_odr_mail_tb_3']
                create_order_text_box_4 = request.form['crt_odr_mail_tb_4']
                
                order_entry_mail['custom_message_type'] = "Order Entry Email"
                order_entry_mail['create_order_text_box_1'] = create_order_text_box_1
                order_entry_mail['create_order_text_box_2'] = create_order_text_box_2
                order_entry_mail['create_order_text_box_3'] = create_order_text_box_3
                order_entry_mail['create_order_text_box_4'] = create_order_text_box_4
                
                subject = order_entry_mail['create_order_text_box_1']
                text_message = order_entry_mail['create_order_text_box_2'] + "abcd12" + order_entry_mail['create_order_text_box_3'] + "02-03-2022" + order_entry_mail['create_order_text_box_4'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/"
                DOL_DB.save_custom_order_related_texts(order_entry_mail)
                sendMail.send_custom_test_email_to_dealer(email,subject,text_message)


    else:
        if form_cstm_order_mail.validate_on_submit():

            create_order_text_box_1 = request.form['crt_odr_mail_tb_1']
            create_order_text_box_2 = request.form['crt_odr_mail_tb_2']
            create_order_text_box_3 = request.form['crt_odr_mail_tb_3']
            create_order_text_box_4 = request.form['crt_odr_mail_tb_4']
            
            order_entry_mail['custom_message_type'] = "Order Entry Email"
            order_entry_mail['create_order_text_box_1'] = create_order_text_box_1
            order_entry_mail['create_order_text_box_2'] = create_order_text_box_2
            order_entry_mail['create_order_text_box_3'] = create_order_text_box_3
            order_entry_mail['create_order_text_box_4'] = create_order_text_box_4
            subject = order_entry_mail['create_order_text_box_1']
            text_message = order_entry_mail['create_order_text_box_2'] + "abcd12" + order_entry_mail['create_order_text_box_3'] + "02-03-2022" + order_entry_mail['create_order_text_box_4'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/"
            DOL_DB.save_custom_order_related_texts(order_entry_mail)
            sendMail.send_custom_test_email_to_dealer(email,subject,text_message)

    return redirect(url_for('custom_viewWrapper'))


@app.route("/save_odr_editmail",methods=['POST'])
@login_required
def save_custom_order_edit_email():
    form_cstm_order_edit_mail = CustomOrdeEditingMail()
    formclass = 'form-control'
    order_edit_mail = {}
    cst_mgs_type_list = []
    cstm_type_list = []
    session["order_edit_cstm_type"] = ''
    email = session['email_retailer']

    entry_msg_cur = DOL_DB.get_custom_order_related_texts()
    for e in entry_msg_cur:
        cst_mgs_type_list.append(e['custom_message_type'])
    print(cst_mgs_type_list)

    if cst_mgs_type_list:
        for typ in cst_mgs_type_list:
            
            if typ == 'Order Editing Email':
                session["order_edit_cstm_type"] = typ
        
        typ_curs = DOL_DB.get_custom_order_related_texts_for_order_edit_by_cst_type()
        for t in typ_curs:
            cstm_type_list.append(t)
        print(cstm_type_list)

        if cstm_type_list:
            if form_cstm_order_edit_mail.validate_on_submit():
                create_order_text_box_1 = request.form['crt_odr_mail_ed_tb_1']
                create_order_text_box_2 = request.form['crt_odr_mail_ed_tb_2']
                create_order_text_box_3 = request.form['crt_odr_mail_ed_tb_3']
                create_order_text_box_4 = request.form['crt_odr_mail_ed_tb_4']
                
                order_edit_mail['create_order_text_box_1'] = create_order_text_box_1
                order_edit_mail['create_order_text_box_2'] = create_order_text_box_2
                order_edit_mail['create_order_text_box_3'] = create_order_text_box_3
                order_edit_mail['create_order_text_box_4'] = create_order_text_box_4
                
                subject = order_edit_mail['create_order_text_box_1']
                text_message = order_edit_mail['create_order_text_box_2'] + "abcd12" + order_edit_mail['create_order_text_box_3'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + order_edit_mail['create_order_text_box_4']
                DOL_DB.update_custom_order_edit_related_texts_by_type(order_edit_mail)
                sendMail.send_custom_test_email_to_dealer(email,subject,text_message)

        else:
            if form_cstm_order_edit_mail.validate_on_submit():

                create_order_text_box_1 = request.form['crt_odr_mail_ed_tb_1']
                create_order_text_box_2 = request.form['crt_odr_mail_ed_tb_2']
                create_order_text_box_3 = request.form['crt_odr_mail_ed_tb_3']
                create_order_text_box_4 = request.form['crt_odr_mail_ed_tb_4']


                order_edit_mail['custom_message_type'] = "Order Editing Email"
                order_edit_mail['create_order_text_box_1'] = create_order_text_box_1
                order_edit_mail['create_order_text_box_2'] = create_order_text_box_2
                order_edit_mail['create_order_text_box_3'] = create_order_text_box_3
                order_edit_mail['create_order_text_box_4'] = create_order_text_box_4

                subject = order_edit_mail['create_order_text_box_1']
                text_message = order_edit_mail['create_order_text_box_2'] + "abcd12" + order_edit_mail['create_order_text_box_3'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + order_edit_mail['create_order_text_box_4']
                DOL_DB.save_custom_order_related_texts(order_edit_mail)
                sendMail.send_custom_test_email_to_dealer(email,subject,text_message)

    else:
        if form_cstm_order_edit_mail.validate_on_submit():

            create_order_text_box_1 = request.form['crt_odr_mail_ed_tb_1']
            create_order_text_box_2 = request.form['crt_odr_mail_ed_tb_2']
            create_order_text_box_3 = request.form['crt_odr_mail_ed_tb_3']
            create_order_text_box_4 = request.form['crt_odr_mail_ed_tb_4']


            order_edit_mail['custom_message_type'] = "Order Editing Email"
            order_edit_mail['create_order_text_box_1'] = create_order_text_box_1
            order_edit_mail['create_order_text_box_2'] = create_order_text_box_2
            order_edit_mail['create_order_text_box_3'] = create_order_text_box_3
            order_edit_mail['create_order_text_box_4'] = create_order_text_box_4

            subject = order_edit_mail['create_order_text_box_1']
            text_message = order_edit_mail['create_order_text_box_2'] + "abcd12" + order_edit_mail['create_order_text_box_3'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + order_edit_mail['create_order_text_box_4']
            DOL_DB.save_custom_order_related_texts(order_edit_mail)
            sendMail.send_custom_test_email_to_dealer(email,subject,text_message)
    return redirect(url_for('custom_viewWrapper'))


@app.route("/save_odr_ldtimemail",methods=['POST'])
@login_required
def save_custom_order_lead_time_email():
    form_cstm_order_lead_time_mail = CustomOrdeLeadTimeChangeMail()
    formclass = 'form-control'
    order_ldtime_mail = {}
    cst_mgs_type_list = []
    cstm_type_list = []
    session["order_lead_cstm_type"] = ''
    email = session['email_retailer']

    entry_msg_cur = DOL_DB.get_custom_order_related_texts()
    for e in entry_msg_cur:
        cst_mgs_type_list.append(e['custom_message_type'])
    print(cst_mgs_type_list)

    if cst_mgs_type_list:
        for typ in cst_mgs_type_list:
            
            if typ == 'Order Lead Time Change Email':
                session["order_lead_cstm_type"] = typ
        typ_curs = DOL_DB.get_custom_order_related_texts_for_order_lead_time_by_cst_type()
        for t in typ_curs:
            cstm_type_list.append(t)
        print(cstm_type_list)

        if cstm_type_list:

            if form_cstm_order_lead_time_mail.validate_on_submit():
                create_order_text_box_1 = request.form['crt_odr_mail_ld_tb_1']
                create_order_text_box_2 = request.form['crt_odr_mail_ld_tb_2']
                create_order_text_box_3 = request.form['crt_odr_mail_ld_tb_3']
                create_order_text_box_4 = request.form['crt_odr_mail_ld_tb_4']
                
                order_ldtime_mail['create_order_text_box_1'] = create_order_text_box_1
                order_ldtime_mail['create_order_text_box_2'] = create_order_text_box_2
                order_ldtime_mail['create_order_text_box_3'] = create_order_text_box_3
                order_ldtime_mail['create_order_text_box_4'] = create_order_text_box_4
                
                subject = order_ldtime_mail['create_order_text_box_1']
                text_message = order_ldtime_mail['create_order_text_box_2'] + "Manufacturing lead time has been increased/decreased by 7 week/weeks" + order_ldtime_mail['create_order_text_box_3'] + "Estimated Delivery Date - 11-23-2021" + order_ldtime_mail['create_order_text_box_4'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + "abcd12"
                DOL_DB.update_custom_order_leadtime_related_texts_by_type(order_ldtime_mail)
                sendMail.send_custom_test_email_to_dealer(email,subject,text_message)

        else:
            if form_cstm_order_lead_time_mail.validate_on_submit():

                create_order_text_box_1 = request.form['crt_odr_mail_ld_tb_1']
                create_order_text_box_2 = request.form['crt_odr_mail_ld_tb_2']
                create_order_text_box_3 = request.form['crt_odr_mail_ld_tb_3']
                create_order_text_box_4 = request.form['crt_odr_mail_ld_tb_4']


                order_ldtime_mail['custom_message_type'] = "Order Lead Time Change Email".strip()
                order_ldtime_mail['create_order_text_box_1'] = create_order_text_box_1
                order_ldtime_mail['create_order_text_box_2'] = create_order_text_box_2
                order_ldtime_mail['create_order_text_box_3'] = create_order_text_box_3
                order_ldtime_mail['create_order_text_box_4'] = create_order_text_box_4

                subject = order_ldtime_mail['create_order_text_box_1']
                text_message = order_ldtime_mail['create_order_text_box_2'] + "Manufacturing lead time has been increased/decreased by 7 week/weeks" + order_ldtime_mail['create_order_text_box_3'] + "Estimated Delivery Date - 11-23-2021" + order_ldtime_mail['create_order_text_box_4'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + "abcd12"
                DOL_DB.save_custom_order_related_texts(order_ldtime_mail)
                sendMail.send_custom_test_email_to_dealer(email,subject,text_message)

    else:
        if form_cstm_order_lead_time_mail.validate_on_submit():

            create_order_text_box_1 = request.form['crt_odr_mail_ld_tb_1']
            create_order_text_box_2 = request.form['crt_odr_mail_ld_tb_2']
            create_order_text_box_3 = request.form['crt_odr_mail_ld_tb_3']
            create_order_text_box_4 = request.form['crt_odr_mail_ld_tb_4']


            order_ldtime_mail['custom_message_type'] = "Order Lead Time Change Email"
            order_ldtime_mail['create_order_text_box_1'] = create_order_text_box_1
            order_ldtime_mail['create_order_text_box_2'] = create_order_text_box_2
            order_ldtime_mail['create_order_text_box_3'] = create_order_text_box_3
            order_ldtime_mail['create_order_text_box_4'] = create_order_text_box_4

            subject = order_ldtime_mail['create_order_text_box_1']
            text_message = order_ldtime_mail['create_order_text_box_2'] + "Manufacturing lead time has been increased/decreased by 7 week/weeks" + order_ldtime_mail['create_order_text_box_3'] + "Estimated Delivery Date - 11-23-2021" + order_ldtime_mail['create_order_text_box_4'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + "abcd12"
            DOL_DB.save_custom_order_related_texts(order_ldtime_mail)
            sendMail.send_custom_test_email_to_dealer(email,subject,text_message)
    return redirect(url_for('custom_viewWrapper'))


@app.route("/save_odr_bftimemail",methods=['POST'])
@login_required
def save_custom_order_buffer_time_email():
    form_cstm_order_buffer_time_mail = CustomOrdeBufferTimeChangeMail()
    formclass = 'form-control'
    order_bftime_mail = {}
    cst_mgs_type_list = []
    cstm_type_list = []
    session["order_buffer_cstm_type"] = ''
    email = session['email_retailer']

    entry_msg_cur = DOL_DB.get_custom_order_related_texts()
    for e in entry_msg_cur:
        cst_mgs_type_list.append(e['custom_message_type'])
    print(cst_mgs_type_list)

    if cst_mgs_type_list:
        for typ in cst_mgs_type_list:
            
            if typ == 'Order Buffer Time Change Email':
                session["order_buffer_cstm_type"] = typ
        typ_curs = DOL_DB.get_custom_order_related_texts_for_order_buffer_by_cst_type()
        for t in typ_curs:
            cstm_type_list.append(t)
        print(cstm_type_list)

        if cstm_type_list:
            if form_cstm_order_buffer_time_mail.validate_on_submit():
                create_order_text_box_1 = request.form['crt_odr_mail_bf_tb_1']
                create_order_text_box_2 = request.form['crt_odr_mail_bf_tb_2']
                create_order_text_box_3 = request.form['crt_odr_mail_bf_tb_3']
                create_order_text_box_4 = request.form['crt_odr_mail_bf_tb_4']
                
                order_bftime_mail['create_order_text_box_1'] = create_order_text_box_1
                order_bftime_mail['create_order_text_box_2'] = create_order_text_box_2
                order_bftime_mail['create_order_text_box_3'] = create_order_text_box_3
                order_bftime_mail['create_order_text_box_4'] = create_order_text_box_4
                
                subject = order_bftime_mail['create_order_text_box_1']
                text_message = order_bftime_mail['create_order_text_box_2'] + "Dealer buffer time has been increased/decreased by 7 week/weeks" + order_bftime_mail['create_order_text_box_3'] + "Estimated Delivery Date - 11-23-2021" + order_bftime_mail['create_order_text_box_4'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + "abcd12"
                DOL_DB.update_custom_order_buffertime_related_texts_by_type(order_bftime_mail)
                sendMail.send_custom_test_email_to_dealer(email,subject,text_message)

        else:
            if form_cstm_order_buffer_time_mail.validate_on_submit():

                create_order_text_box_1 = request.form['crt_odr_mail_bf_tb_1']
                create_order_text_box_2 = request.form['crt_odr_mail_bf_tb_2']
                create_order_text_box_3 = request.form['crt_odr_mail_bf_tb_3']
                create_order_text_box_4 = request.form['crt_odr_mail_bf_tb_4']


                order_bftime_mail['custom_message_type'] = "Order Buffer Time Change Email"
                order_bftime_mail['create_order_text_box_1'] = create_order_text_box_1
                order_bftime_mail['create_order_text_box_2'] = create_order_text_box_2
                order_bftime_mail['create_order_text_box_3'] = create_order_text_box_3
                order_bftime_mail['create_order_text_box_4'] = create_order_text_box_4

                subject = order_bftime_mail['create_order_text_box_1']
                text_message = order_bftime_mail['create_order_text_box_2'] + "Dealer buffer time has been increased/decreased by 7 week/weeks" + order_bftime_mail['create_order_text_box_3'] + "Estimated Delivery Date - 11-23-2021" + order_bftime_mail['create_order_text_box_4'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + "abcd12"
                DOL_DB.save_custom_order_related_texts(order_bftime_mail)
                sendMail.send_custom_test_email_to_dealer(email,subject,text_message)

    else:
        if form_cstm_order_buffer_time_mail.validate_on_submit():

            create_order_text_box_1 = request.form['crt_odr_mail_bf_tb_1']
            create_order_text_box_2 = request.form['crt_odr_mail_bf_tb_2']
            create_order_text_box_3 = request.form['crt_odr_mail_bf_tb_3']
            create_order_text_box_4 = request.form['crt_odr_mail_bf_tb_4']


            order_bftime_mail['custom_message_type'] = "Order Buffer Time Change Email"
            order_bftime_mail['create_order_text_box_1'] = create_order_text_box_1
            order_bftime_mail['create_order_text_box_2'] = create_order_text_box_2
            order_bftime_mail['create_order_text_box_3'] = create_order_text_box_3
            order_bftime_mail['create_order_text_box_4'] = create_order_text_box_4

            subject = order_bftime_mail['create_order_text_box_1']
            text_message = order_bftime_mail['create_order_text_box_2'] + "Dealer buffer time has been increased/decreased by 7 week/weeks" + order_bftime_mail['create_order_text_box_3'] + "Estimated Delivery Date - 11-23-2021" + order_bftime_mail['create_order_text_box_4'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + "abcd12"
            DOL_DB.save_custom_order_related_texts(order_bftime_mail)
            sendMail.send_custom_test_email_to_dealer(email,subject,text_message)
    return redirect(url_for('custom_viewWrapper'))

@app.route("/save_odr_pgrstimemail",methods=['POST'])
@login_required
def save_custom_order_pgrs_timeline_email():
    form_cstm_order_pgrs_time_line_mail = CustomOrdeProgressTimeLineChangeMail()
    formclass = 'form-control'
    order_pgrstime_mail = {}
    cst_mgs_type_list = []
    cstm_type_list = []
    session["pgrstmln_cstm_type"] = ''
    email = session['email_retailer']

    entry_msg_cur = DOL_DB.get_custom_order_related_texts()
    for e in entry_msg_cur:
        cst_mgs_type_list.append(e['custom_message_type'])
    print(cst_mgs_type_list)

    if cst_mgs_type_list:
        for typ in cst_mgs_type_list:
            
            if typ == 'Order Progress Time Line Change Email':
                session["pgrstmln_cstm_type"] = typ
                
        typ_curs = DOL_DB.get_custom_order_related_texts_for_progress_time_line_by_cst_type()
        for t in typ_curs:
            cstm_type_list.append(t)
        print(cstm_type_list)

        if cstm_type_list:
            if form_cstm_order_pgrs_time_line_mail.validate_on_submit():
                create_order_text_box_1 = request.form['crt_odr_mail_pglt_tb_1']
                create_order_text_box_2 = request.form['crt_odr_mail_pglt_tb_2']
                create_order_text_box_3 = request.form['crt_odr_mail_pglt_tb_3']
                create_order_text_box_4 = request.form['crt_odr_mail_pglt_tb_4']
                
                order_pgrstime_mail['create_order_text_box_1'] = create_order_text_box_1
                order_pgrstime_mail['create_order_text_box_2'] = create_order_text_box_2
                order_pgrstime_mail['create_order_text_box_3'] = create_order_text_box_3
                order_pgrstime_mail['create_order_text_box_4'] = create_order_text_box_4
                
                subject = order_pgrstime_mail['create_order_text_box_1']
                text_message = order_pgrstime_mail['create_order_text_box_2'] + "Shipped" + order_pgrstime_mail['create_order_text_box_3'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + order_pgrstime_mail['create_order_text_box_4'] + "abcd12"
                DOL_DB.update_custom_progress_time_line_related_texts_by_type(order_pgrstime_mail)
                sendMail.send_custom_test_email_to_dealer(email,subject,text_message)

        else:
            if form_cstm_order_pgrs_time_line_mail.validate_on_submit():

                create_order_text_box_1 = request.form['crt_odr_mail_pglt_tb_1']
                create_order_text_box_2 = request.form['crt_odr_mail_pglt_tb_2']
                create_order_text_box_3 = request.form['crt_odr_mail_pglt_tb_3']
                create_order_text_box_4 = request.form['crt_odr_mail_pglt_tb_4']


                order_pgrstime_mail['custom_message_type'] = "Order Progress Time Line Change Email"
                order_pgrstime_mail['create_order_text_box_1'] = create_order_text_box_1
                order_pgrstime_mail['create_order_text_box_2'] = create_order_text_box_2
                order_pgrstime_mail['create_order_text_box_3'] = create_order_text_box_3
                order_pgrstime_mail['create_order_text_box_4'] = create_order_text_box_4

                subject = order_pgrstime_mail['create_order_text_box_1']
                text_message = order_pgrstime_mail['create_order_text_box_2'] + "Shipped" + order_pgrstime_mail['create_order_text_box_3'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + order_pgrstime_mail['create_order_text_box_4'] + "abcd12"
                DOL_DB.save_custom_order_related_texts(order_pgrstime_mail)
                sendMail.send_custom_test_email_to_dealer(email,subject,text_message)

    else:
        if form_cstm_order_pgrs_time_line_mail.validate_on_submit():

            create_order_text_box_1 = request.form['crt_odr_mail_pglt_tb_1']
            create_order_text_box_2 = request.form['crt_odr_mail_pglt_tb_2']
            create_order_text_box_3 = request.form['crt_odr_mail_pglt_tb_3']
            create_order_text_box_4 = request.form['crt_odr_mail_pglt_tb_4']


            order_pgrstime_mail['custom_message_type'] = "Order Progress Time Line Change Email"
            order_pgrstime_mail['create_order_text_box_1'] = create_order_text_box_1
            order_pgrstime_mail['create_order_text_box_2'] = create_order_text_box_2
            order_pgrstime_mail['create_order_text_box_3'] = create_order_text_box_3
            order_pgrstime_mail['create_order_text_box_4'] = create_order_text_box_4

            subject = order_pgrstime_mail['create_order_text_box_1']
            text_message = order_pgrstime_mail['create_order_text_box_2'] + "Shipped" + order_pgrstime_mail['create_order_text_box_3'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + order_pgrstime_mail['create_order_text_box_4'] + "abcd12"
            DOL_DB.save_custom_order_related_texts(order_pgrstime_mail)
            sendMail.send_custom_test_email_to_dealer(email,subject,text_message)
    return redirect(url_for('custom_viewWrapper'))

@app.route("/save_redbtn_ldtimemail",methods=['POST'])
@login_required
def save_custom_redbutton_lead_time_email():
    print("---------------------------------lead time mail")
    form_cstm_redbtn_lead_time_mail = CustomRedButtonLeadTimeChangeMail()
    formclass = 'form-control'
    order_rdbtn_ldtime_mail = {}
    cst_mgs_type_list = []
    cstm_type_list = []
    session["ld_cstm_type"] = ''
    email = session['email_retailer']

    entry_msg_cur = DOL_DB.get_custom_order_related_texts()
    for e in entry_msg_cur:
        cst_mgs_type_list.append(e['custom_message_type'])
    print(cst_mgs_type_list)

    if cst_mgs_type_list:
        for typ in cst_mgs_type_list:
            
            if typ == 'Red Button Lead Time Change Email':
                session["ld_cstm_type"] = typ
                
        typ_curs = DOL_DB.get_custom_order_related_texts_for_red_button_lead_by_cst_type()
        for t in typ_curs:
            cstm_type_list.append(t)
        print(cstm_type_list)

        if cstm_type_list:
            print("-----------------------------------------if exists")
            if form_cstm_redbtn_lead_time_mail.validate_on_submit():
                create_order_text_box_1 = request.form['crt_rbtnld_mail_tb_1']
                create_order_text_box_2 = request.form['crt_rbtnld_mail_tb_2']
                create_order_text_box_3 = request.form['crt_rbtnld_mail_tb_3']
                create_order_text_box_4 = request.form['crt_rbtnld_mail_tb_4']
                
                order_rdbtn_ldtime_mail['create_order_text_box_1'] = create_order_text_box_1
                order_rdbtn_ldtime_mail['create_order_text_box_2'] = create_order_text_box_2
                order_rdbtn_ldtime_mail['create_order_text_box_3'] = create_order_text_box_3
                order_rdbtn_ldtime_mail['create_order_text_box_4'] = create_order_text_box_4
                
                subject = order_rdbtn_ldtime_mail['create_order_text_box_1']
                text_message = order_rdbtn_ldtime_mail['create_order_text_box_2'] + "Manufacturing lead time has been increased/decreased by 7 week/weeks. New estimated delivery date is 11-23-2021" + order_rdbtn_ldtime_mail['create_order_text_box_3'] + "abcd12" + order_rdbtn_ldtime_mail['create_order_text_box_4'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/"
                DOL_DB.update_custom_red_button_leadtime_related_texts_by_type(order_rdbtn_ldtime_mail)
                sendMail.send_custom_test_email_to_dealer(email,subject,text_message)

        else:
            print("----------------------else type doesnt exist--------------inside first else")
            if form_cstm_redbtn_lead_time_mail.validate_on_submit():

                create_order_text_box_1 = request.form['crt_rbtnld_mail_tb_1']
                create_order_text_box_2 = request.form['crt_rbtnld_mail_tb_2']
                create_order_text_box_3 = request.form['crt_rbtnld_mail_tb_3']
                create_order_text_box_4 = request.form['crt_rbtnld_mail_tb_4']


                order_rdbtn_ldtime_mail['custom_message_type'] = "Red Button Lead Time Change Email"
                order_rdbtn_ldtime_mail['create_order_text_box_1'] = create_order_text_box_1
                order_rdbtn_ldtime_mail['create_order_text_box_2'] = create_order_text_box_2
                order_rdbtn_ldtime_mail['create_order_text_box_3'] = create_order_text_box_3
                order_rdbtn_ldtime_mail['create_order_text_box_4'] = create_order_text_box_4

                subject = order_rdbtn_ldtime_mail['create_order_text_box_1']
                text_message = order_rdbtn_ldtime_mail['create_order_text_box_2'] + "Manufacturing lead time has been increased/decreased by 7 week/weeks. New estimated delivery date is 11-23-2021" + order_rdbtn_ldtime_mail['create_order_text_box_3'] + "abcd12" + order_rdbtn_ldtime_mail['create_order_text_box_4'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/"
                DOL_DB.save_custom_order_related_texts(order_rdbtn_ldtime_mail)
                sendMail.send_custom_test_email_to_dealer(email,subject,text_message)

    else:
        print("---------------------------------------inside second else")
        if form_cstm_redbtn_lead_time_mail.validate_on_submit():

            create_order_text_box_1 = request.form['crt_rbtnld_mail_tb_1']
            create_order_text_box_2 = request.form['crt_rbtnld_mail_tb_2']
            create_order_text_box_3 = request.form['crt_rbtnld_mail_tb_3']
            create_order_text_box_4 = request.form['crt_rbtnld_mail_tb_4']


            order_rdbtn_ldtime_mail['custom_message_type'] = "Red Button Lead Time Change Email"
            order_rdbtn_ldtime_mail['create_order_text_box_1'] = create_order_text_box_1
            order_rdbtn_ldtime_mail['create_order_text_box_2'] = create_order_text_box_2
            order_rdbtn_ldtime_mail['create_order_text_box_3'] = create_order_text_box_3
            order_rdbtn_ldtime_mail['create_order_text_box_4'] = create_order_text_box_4

            subject = order_rdbtn_ldtime_mail['create_order_text_box_1']
            text_message = order_rdbtn_ldtime_mail['create_order_text_box_2'] + "Manufacturing lead time has been increased/decreased by 7 week/weeks. New estimated delivery date is 11-23-2021" + order_rdbtn_ldtime_mail['create_order_text_box_3'] + "abcd12" + order_rdbtn_ldtime_mail['create_order_text_box_4'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/"
            DOL_DB.save_custom_order_related_texts(order_rdbtn_ldtime_mail)
            sendMail.send_custom_test_email_to_dealer(email,subject,text_message)
    return redirect(url_for('custom_viewWrapper'))

@app.route("/save_redbtn_bfrtimemail",methods=['POST'])
@login_required
def save_custom_redbutton_buffer_time_email():
    form_cstm_redbtn_buffer_time_mail = CustomRedButtonBufferTimeChangeMail()
    formclass = 'form-control'
    order_rdbtn_bfrtime_mail = {}
    cst_mgs_type_list = []
    cstm_type_list = []
    session["bfr_cstm_type"] = ''
    email = session['email_retailer']

    entry_msg_cur = DOL_DB.get_custom_order_related_texts()
    for e in entry_msg_cur:
        cst_mgs_type_list.append(e['custom_message_type'])
    print("=============================================cst_mgs_type_list")
    print(cst_mgs_type_list)

    if cst_mgs_type_list:
        for typ in cst_mgs_type_list:
            
            if typ == 'Red Button Buffer Time Change Email':
                session["bfr_cstm_type"] = typ
                print("****************************************************")
                print(session["bfr_cstm_type"])
                print("******************************************************")
                


        print("========OUTSIDE IF=======================IF TRUE====================")
        typ_curs = DOL_DB.get_custom_order_related_texts_for_red_button_buffer_by_cst_type()
        for t in typ_curs:
            cstm_type_list.append(t)
        print("---------------------------------------------------------------")
        print(cstm_type_list)
        print("------------------------------------------------")

        if cstm_type_list:
            print("-------------------------------SECOND IF TRUE---------------------")
            print(cstm_type_list)
            print("========================================================================")
            if form_cstm_redbtn_buffer_time_mail.validate_on_submit():
                create_order_text_box_1 = request.form['crt_rbtnlbfrd_mail_tb_1']
                create_order_text_box_2 = request.form['crt_rbtnlbfrd_mail_tb_2']
                create_order_text_box_3 = request.form['crt_rbtnlbfrd_mail_tb_3']
                create_order_text_box_4 = request.form['crt_rbtnlbfrd_mail_tb_4']
                
                order_rdbtn_bfrtime_mail['create_order_text_box_1'] = create_order_text_box_1
                order_rdbtn_bfrtime_mail['create_order_text_box_2'] = create_order_text_box_2
                order_rdbtn_bfrtime_mail['create_order_text_box_3'] = create_order_text_box_3
                order_rdbtn_bfrtime_mail['create_order_text_box_4'] = create_order_text_box_4
                
                print(order_rdbtn_bfrtime_mail)
                
                subject = order_rdbtn_bfrtime_mail['create_order_text_box_1']
                text_message = order_rdbtn_bfrtime_mail['create_order_text_box_2'] + "Dealer lead time has been increased/decreased by 7 week/weeks. New estimated delivery date is 11-23-2021" + order_rdbtn_bfrtime_mail['create_order_text_box_3'] + "abcd12" + order_rdbtn_bfrtime_mail['create_order_text_box_4'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/"
                DOL_DB.update_custom_red_button_buffertime_related_texts_by_type(order_rdbtn_bfrtime_mail)
                sendMail.send_custom_test_email_to_dealer(email,subject,text_message)

        else:
            print("=====================================ELSE FIRST")
            if form_cstm_redbtn_buffer_time_mail.validate_on_submit():

                create_order_text_box_1 = request.form['crt_rbtnlbfrd_mail_tb_1']
                create_order_text_box_2 = request.form['crt_rbtnlbfrd_mail_tb_2']
                create_order_text_box_3 = request.form['crt_rbtnlbfrd_mail_tb_3']
                create_order_text_box_4 = request.form['crt_rbtnlbfrd_mail_tb_4']


                order_rdbtn_bfrtime_mail['custom_message_type'] = "Red Button Buffer Time Change Email"
                order_rdbtn_bfrtime_mail['create_order_text_box_1'] = create_order_text_box_1
                order_rdbtn_bfrtime_mail['create_order_text_box_2'] = create_order_text_box_2
                order_rdbtn_bfrtime_mail['create_order_text_box_3'] = create_order_text_box_3
                order_rdbtn_bfrtime_mail['create_order_text_box_4'] = create_order_text_box_4

                subject = order_rdbtn_bfrtime_mail['create_order_text_box_1']
                text_message = order_rdbtn_bfrtime_mail['create_order_text_box_2'] + "Dealer lead time has been increased/decreased by 7 week/weeks. New estimated delivery date is 11-23-2021" + order_rdbtn_bfrtime_mail['create_order_text_box_3'] + "abcd12" + order_rdbtn_bfrtime_mail['create_order_text_box_4'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/"
                DOL_DB.save_custom_order_related_texts(order_rdbtn_bfrtime_mail)
                sendMail.send_custom_test_email_to_dealer(email,subject,text_message)

    else:
        print("--------------------------------------INSIDE LAST ELSE")
        if form_cstm_redbtn_buffer_time_mail.validate_on_submit():

            create_order_text_box_1 = request.form['crt_rbtnlbfrd_mail_tb_1']
            create_order_text_box_2 = request.form['crt_rbtnlbfrd_mail_tb_2']
            create_order_text_box_3 = request.form['crt_rbtnlbfrd_mail_tb_3']
            create_order_text_box_4 = request.form['crt_rbtnlbfrd_mail_tb_4']


            order_rdbtn_bfrtime_mail['custom_message_type'] = "Red Button Buffer Time Change Email"
            order_rdbtn_bfrtime_mail['create_order_text_box_1'] = create_order_text_box_1
            order_rdbtn_bfrtime_mail['create_order_text_box_2'] = create_order_text_box_2
            order_rdbtn_bfrtime_mail['create_order_text_box_3'] = create_order_text_box_3
            order_rdbtn_bfrtime_mail['create_order_text_box_4'] = create_order_text_box_4

            subject = order_rdbtn_bfrtime_mail['create_order_text_box_1']
            text_message = order_rdbtn_bfrtime_mail['create_order_text_box_2'] + "Dealer lead time has been increased/decreased by 7 week/weeks. New estimated delivery date is 11-23-2021" + order_rdbtn_bfrtime_mail['create_order_text_box_3'] + "abcd12" + order_rdbtn_bfrtime_mail['create_order_text_box_4'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/"
            DOL_DB.save_custom_order_related_texts(order_rdbtn_bfrtime_mail)
            sendMail.send_custom_test_email_to_dealer(email,subject,text_message)
    return redirect(url_for('custom_viewWrapper'))


@app.route("/save_custmreviewmail",methods=['POST'])
@login_required
def save_custom_customer_review_email():
    print("=========================INSIDE REVIEW")
    form_cstm_custm_review_mail = CustomConsumerReviewMail()
    formclass = 'form-control'
    custm_review_mail = {}
    cst_mgs_type_list = []
    cstm_type_list = []
    session["consumer_review_email_cstm_type"] = ''
    email = session['email_retailer']

    entry_msg_cur = DOL_DB.get_custom_order_related_texts()
    for e in entry_msg_cur:
        cst_mgs_type_list.append(e['custom_message_type'])
    print(cst_mgs_type_list)

    if cst_mgs_type_list:
        for typ in cst_mgs_type_list:
            
            if typ == 'Consumer Review Change Email':
                session["consumer_review_email_cstm_type"] = typ
        
        typ_curs = DOL_DB.get_custom_order_related_texts_for_consumer_review_by_cst_type()
        for t in typ_curs:
            cstm_type_list.append(t)
        print(cstm_type_list)

        if cstm_type_list:
            if form_cstm_custm_review_mail.validate_on_submit():
                create_order_text_box_1 = request.form['crt_cstnreview_mail_tb_1']
                create_order_text_box_2 = request.form['crt_cstnreview_mail_tb_2']
                create_order_text_box_3 = request.form['crt_cstnreview_mail_tb_3']
                
                custm_review_mail['create_order_text_box_1'] = create_order_text_box_1
                custm_review_mail['create_order_text_box_2'] = create_order_text_box_2
                custm_review_mail['create_order_text_box_3'] = create_order_text_box_3
                
                subject = custm_review_mail['create_order_text_box_1']
                text_message = custm_review_mail['create_order_text_box_2'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + custm_review_mail['create_order_text_box_3'] + "abcd12"
                DOL_DB.update_custom_consumer_review_related_texts_by_type(custm_review_mail)
                sendMail.send_custom_test_email_to_dealer(email,subject,text_message)

        else:
            if form_cstm_custm_review_mail.validate_on_submit():

                create_order_text_box_1 = request.form['crt_cstnreview_mail_tb_1']
                create_order_text_box_2 = request.form['crt_cstnreview_mail_tb_2']
                create_order_text_box_3 = request.form['crt_cstnreview_mail_tb_3']


                custm_review_mail['custom_message_type'] = "Consumer Review Change Email"
                custm_review_mail['create_order_text_box_1'] = create_order_text_box_1
                custm_review_mail['create_order_text_box_2'] = create_order_text_box_2
                custm_review_mail['create_order_text_box_3'] = create_order_text_box_3

                subject = custm_review_mail['create_order_text_box_1']
                text_message = custm_review_mail['create_order_text_box_2'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + custm_review_mail['create_order_text_box_3'] + "abcd12"
                DOL_DB.save_custom_order_related_texts(custm_review_mail)
                sendMail.send_custom_test_email_to_dealer(email,subject,text_message)

    else:
        if form_cstm_custm_review_mail.validate_on_submit():

            create_order_text_box_1 = request.form['crt_cstnreview_mail_tb_1']
            create_order_text_box_2 = request.form['crt_cstnreview_mail_tb_2']
            create_order_text_box_3 = request.form['crt_cstnreview_mail_tb_3']


            custm_review_mail['custom_message_type'] = "Consumer Review Change Email"
            custm_review_mail['create_order_text_box_1'] = create_order_text_box_1
            custm_review_mail['create_order_text_box_2'] = create_order_text_box_2
            custm_review_mail['create_order_text_box_3'] = create_order_text_box_3

            subject = custm_review_mail['create_order_text_box_1']
            text_message = custm_review_mail['create_order_text_box_2'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + custm_review_mail['create_order_text_box_3'] + "abcd12"
            DOL_DB.save_custom_order_related_texts(custm_review_mail)
            sendMail.send_custom_test_email_to_dealer(email,subject,text_message)
    return redirect(url_for('custom_viewWrapper'))

@app.route("/save_prodcustmreviewmail",methods=['POST'])
@login_required
def save_custom_customer_product_review_email():
    print("=========================INSIDE REVIEW")
    form_cstm_custm_product_review_mail = CustomConsumerProductReviewMail()
    formclass = 'form-control'
    custm_product_review_mail = {}
    cst_mgs_type_list = []
    cstm_type_list = []
    session["consumer_product_review_email_cstm_type"] = ''
    email = session['email_retailer']

    entry_msg_cur = DOL_DB.get_custom_order_related_texts()
    for e in entry_msg_cur:
        cst_mgs_type_list.append(e['custom_message_type'])
    print(cst_mgs_type_list)

    if cst_mgs_type_list:
        for typ in cst_mgs_type_list:
            
            if typ == 'Consumer Product Review Change Email':
                session["consumer_product_review_email_cstm_type"] = typ
        
        typ_curs = DOL_DB.get_custom_order_related_texts_for_consumer_product_review_by_cst_type()
        for t in typ_curs:
            cstm_type_list.append(t)
        print(cstm_type_list)

        if cstm_type_list:
            if form_cstm_custm_product_review_mail.validate_on_submit():
                create_order_text_box_1 = request.form['crt_cstn_prodreview_mail_tb_1']
                create_order_text_box_2 = request.form['crt_cstn_prodreview_mail_tb_2']
                create_order_text_box_3 = request.form['crt_cstn_prodreview_mail_tb_3']
                
                custm_product_review_mail['create_order_text_box_1'] = create_order_text_box_1
                custm_product_review_mail['create_order_text_box_2'] = create_order_text_box_2
                custm_product_review_mail['create_order_text_box_3'] = create_order_text_box_3
                
                subject = custm_product_review_mail['create_order_text_box_1']
                text_message = custm_product_review_mail['create_order_text_box_2'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + custm_product_review_mail['create_order_text_box_3'] + "abcd12"
                DOL_DB.update_custom_consumer_product_review_related_texts_by_type(custm_product_review_mail)
                sendMail.send_custom_test_email_to_dealer(email,subject,text_message)

        else:
            if form_cstm_custm_product_review_mail.validate_on_submit():

                create_order_text_box_1 = request.form['crt_cstn_prodreview_mail_tb_1']
                create_order_text_box_2 = request.form['crt_cstn_prodreview_mail_tb_2']
                create_order_text_box_3 = request.form['crt_cstn_prodreview_mail_tb_3']


                custm_product_review_mail['custom_message_type'] = "Consumer Product Review Change Email"
                custm_product_review_mail['create_order_text_box_1'] = create_order_text_box_1
                custm_product_review_mail['create_order_text_box_2'] = create_order_text_box_2
                custm_product_review_mail['create_order_text_box_3'] = create_order_text_box_3

                subject = custm_product_review_mail['create_order_text_box_1']
                text_message = custm_product_review_mail['create_order_text_box_2'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + custm_product_review_mail['create_order_text_box_3'] + "abcd12"
                DOL_DB.save_custom_order_related_texts(custm_product_review_mail)
                sendMail.send_custom_test_email_to_dealer(email,subject,text_message)

    else:
        if form_cstm_custm_product_review_mail.validate_on_submit():

            create_order_text_box_1 = request.form['crt_cstn_prodreview_mail_tb_1']
            create_order_text_box_2 = request.form['crt_cstn_prodreview_mail_tb_2']
            create_order_text_box_3 = request.form['crt_cstn_prodreview_mail_tb_3']


            custm_product_review_mail['custom_message_type'] = "Consumer Product Review Change Email"
            custm_product_review_mail['create_order_text_box_1'] = create_order_text_box_1
            custm_product_review_mail['create_order_text_box_2'] = create_order_text_box_2
            custm_product_review_mail['create_order_text_box_3'] = create_order_text_box_3

            subject = custm_product_review_mail['create_order_text_box_1']
            text_message = custm_product_review_mail['create_order_text_box_2'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + custm_product_review_mail['create_order_text_box_3'] + "abcd12"
            DOL_DB.save_custom_order_related_texts(custm_product_review_mail)
            sendMail.send_custom_test_email_to_dealer(email,subject,text_message)
    return redirect(url_for('custom_viewWrapper'))


@app.route("/save_bulk_pgrstimemail",methods=['POST'])
@login_required
def save_custom_bulk_order_pgrs_timeline_email():
    print("===========================inside bulk progress timeline email")
    form_cstm_bulk_pgrs_time_line_mail = CustomRedbtnProgressTimeLineChangeMail()
    formclass = 'form-control'
    redbtn_pgrstime_mail = {}
    cst_mgs_type_list = []
    cstm_type_list = []
    session["redbtn_pgrstmln_cstm_type"] = ''
    email = session['email_retailer']

    entry_msg_cur = DOL_DB.get_custom_order_related_texts()
    for e in entry_msg_cur:
        cst_mgs_type_list.append(e['custom_message_type'])
    print(cst_mgs_type_list)

    if cst_mgs_type_list:
        for typ in cst_mgs_type_list:
            
            if typ == 'Red Button Progress Time Line Change Email':
                session["redbtn_pgrstmln_cstm_type"] = typ
                
        typ_curs = DOL_DB.get_custom_redbtn_related_texts_for_progress_time_line_by_cst_type()
        for t in typ_curs:
            cstm_type_list.append(t)
        print(cstm_type_list)

        if cstm_type_list:
            if form_cstm_bulk_pgrs_time_line_mail.validate_on_submit():
                create_order_text_box_1 = request.form['crt_rbtnpglt_mail_tb_1']
                create_order_text_box_2 = request.form['crt_rbtnpglt_mail_tb_2']
                create_order_text_box_3 = request.form['crt_rbtnpglt_mail_tb_3']
                create_order_text_box_4 = request.form['crt_rbtnpglt_mail_tb_4']
                
                redbtn_pgrstime_mail['create_order_text_box_1'] = create_order_text_box_1
                redbtn_pgrstime_mail['create_order_text_box_2'] = create_order_text_box_2
                redbtn_pgrstime_mail['create_order_text_box_3'] = create_order_text_box_3
                redbtn_pgrstime_mail['create_order_text_box_4'] = create_order_text_box_4
                
                subject = redbtn_pgrstime_mail['create_order_text_box_1']
                text_message = redbtn_pgrstime_mail['create_order_text_box_2'] + "Order is confirmed" + redbtn_pgrstime_mail['create_order_text_box_3'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + redbtn_pgrstime_mail['create_order_text_box_4'] + "abcd12"
                DOL_DB.update_custom_redbtn_progress_time_line_related_texts_by_type(redbtn_pgrstime_mail)
                sendMail.send_custom_test_email_to_dealer(email,subject,text_message)

        else:
            if form_cstm_bulk_pgrs_time_line_mail.validate_on_submit():

                create_order_text_box_1 = request.form['crt_rbtnpglt_mail_tb_1']
                create_order_text_box_2 = request.form['crt_rbtnpglt_mail_tb_2']
                create_order_text_box_3 = request.form['crt_rbtnpglt_mail_tb_3']
                create_order_text_box_4 = request.form['crt_rbtnpglt_mail_tb_4']


                redbtn_pgrstime_mail['custom_message_type'] = "Red Button Progress Time Line Change Email"
                redbtn_pgrstime_mail['create_order_text_box_1'] = create_order_text_box_1
                redbtn_pgrstime_mail['create_order_text_box_2'] = create_order_text_box_2
                redbtn_pgrstime_mail['create_order_text_box_3'] = create_order_text_box_3
                redbtn_pgrstime_mail['create_order_text_box_4'] = create_order_text_box_4

                subject = order_entry_mail['create_order_text_box_1']
                text_message = redbtn_pgrstime_mail['create_order_text_box_2'] + "Order is confirmed" + redbtn_pgrstime_mail['create_order_text_box_3'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + redbtn_pgrstime_mail['create_order_text_box_4'] + "abcd12"
                DOL_DB.save_custom_order_related_texts(redbtn_pgrstime_mail)
                sendMail.send_custom_test_email_to_dealer(email,subject,text_message)

    else:
        if form_cstm_bulk_pgrs_time_line_mail.validate_on_submit():

            create_order_text_box_1 = request.form['crt_rbtnpglt_mail_tb_1']
            create_order_text_box_2 = request.form['crt_rbtnpglt_mail_tb_2']
            create_order_text_box_3 = request.form['crt_rbtnpglt_mail_tb_3']
            create_order_text_box_4 = request.form['crt_rbtnpglt_mail_tb_4']


            redbtn_pgrstime_mail['custom_message_type'] = "Red Button Progress Time Line Change Email"
            redbtn_pgrstime_mail['create_order_text_box_1'] = create_order_text_box_1
            redbtn_pgrstime_mail['create_order_text_box_2'] = create_order_text_box_2
            redbtn_pgrstime_mail['create_order_text_box_3'] = create_order_text_box_3
            redbtn_pgrstime_mail['create_order_text_box_4'] = create_order_text_box_4

            subject = order_entry_mail['create_order_text_box_1']
            text_message = redbtn_pgrstime_mail['create_order_text_box_2'] + "Order is confirmed" + redbtn_pgrstime_mail['create_order_text_box_3'] + "https://nexus-superapp-cust-staging.herokuapp.com/login/" + redbtn_pgrstime_mail['create_order_text_box_4'] + "abcd12"
            DOL_DB.save_custom_order_related_texts(redbtn_pgrstime_mail)
            sendMail.send_custom_test_email_to_dealer(email,subject,text_message)
    return redirect(url_for('custom_viewWrapper'))


@app.route("/save_welcome_note_email",methods=['POST'])
@login_required
def save_custom_welcome_note_email():
    form_cstm_welcome_note_mail = CustomWelcomeMessageMail()
    formclass = 'form-control'
    welcome_mail = {}
    cst_mgs_type_list = []
    cstm_type_list = []
    session["welcome_note_mail"] = ''
    email = session['email_retailer']

    entry_msg_cur = DOL_DB.get_custom_order_related_texts()
    for e in entry_msg_cur:
        cst_mgs_type_list.append(e['custom_message_type'])
    print(cst_mgs_type_list)

    if cst_mgs_type_list:
        for typ in cst_mgs_type_list:
            
            if typ == 'Welcome Note Change Email':
                session["welcome_note_mail"] = typ
                
        typ_curs = DOL_DB.get_custom_welcome_note_texts_by_cst_type()
        for t in typ_curs:
            cstm_type_list.append(t)
        print(cstm_type_list)

        if cstm_type_list:
            if form_cstm_welcome_note_mail.validate_on_submit():
                create_order_text_box_1 = request.form['crt_wlcmmsg_mail_tb_1']
                create_order_text_box_2 = request.form['crt_wlcmmsg_mail_tb_2']
                
                welcome_mail['create_order_text_box_1'] = create_order_text_box_1
                welcome_mail['create_order_text_box_2'] = create_order_text_box_2
                
                subject = welcome_mail['create_order_text_box_1']
                text_message = welcome_mail['create_order_text_box_2']
                DOL_DB.update_custom_welcome_note_texts_by_type(welcome_mail)
                sendMail.send_custom_test_email_to_dealer(email,subject,text_message)

        else:
            if form_cstm_welcome_note_mail.validate_on_submit():

                create_order_text_box_1 = request.form['crt_wlcmmsg_mail_tb_1']
                create_order_text_box_2 = request.form['crt_wlcmmsg_mail_tb_2']


                welcome_mail['custom_message_type'] = "Welcome Note Change Email"
                welcome_mail['create_order_text_box_1'] = create_order_text_box_1
                welcome_mail['create_order_text_box_2'] = create_order_text_box_2

                subject = welcome_mail['create_order_text_box_1']
                text_message = welcome_mail['create_order_text_box_2']
                DOL_DB.save_custom_order_related_texts(welcome_mail)
                sendMail.send_custom_test_email_to_dealer(email,subject,text_message)

    else:
        if form_cstm_welcome_note_mail.validate_on_submit():

            create_order_text_box_1 = request.form['crt_wlcmmsg_mail_tb_1']
            create_order_text_box_2 = request.form['crt_wlcmmsg_mail_tb_2']


            welcome_mail['custom_message_type'] = "Welcome Note Change Email"
            welcome_mail['create_order_text_box_1'] = create_order_text_box_1
            welcome_mail['create_order_text_box_2'] = create_order_text_box_2

            subject = welcome_mail['create_order_text_box_1']
            text_message = welcome_mail['create_order_text_box_2']
            DOL_DB.save_custom_order_related_texts(welcome_mail)
            sendMail.send_custom_test_email_to_dealer(email,subject,text_message)
    return redirect(url_for('custom_viewWrapper'))

@app.route("/save_review_page_details",methods=['POST'])
@login_required
def save_custom_review_page_details():
    form_review_page = ReviewPageCutomization()
    formclass = 'form-control'
    review_page_info = {}
    cst_mgs_type_list = []
    cstm_type_list = []
    session["review_page"] = ''
    email = session['email_retailer']

    entry_msg_cur = DOL_DB.get_custom_order_related_texts()
    for e in entry_msg_cur:
        cst_mgs_type_list.append(e['custom_message_type'])
    print(cst_mgs_type_list)

    if cst_mgs_type_list:
        for typ in cst_mgs_type_list:
            
            if typ == 'Review Page Customization':
                session["review_page"] = typ
                
        typ_curs = DOL_DB.get_custom_review_page_details_by_cst_type()
        for t in typ_curs:
            cstm_type_list.append(t)
        print(cstm_type_list)

        if cstm_type_list:
            if form_review_page.validate_on_submit():
                create_order_text_box_1 = request.form['review_page_heading']
                create_order_text_box_2 = request.form['review_page_textarea']
                
                review_page_info['create_order_text_box_1'] = create_order_text_box_1
                review_page_info['create_order_text_box_2'] = create_order_text_box_2
                DOL_DB.update_custom_review_page_details_by_type(review_page_info)

        else:
            if form_review_page.validate_on_submit():

                create_order_text_box_1 = request.form['review_page_heading']
                create_order_text_box_2 = request.form['review_page_textarea']


                review_page_info['custom_message_type'] = "Review Page Customization"
                review_page_info['create_order_text_box_1'] = create_order_text_box_1
                review_page_info['create_order_text_box_2'] = create_order_text_box_2
                DOL_DB.save_custom_order_related_texts(review_page_info)

    else:
        if form_review_page.validate_on_submit():

            create_order_text_box_1 = request.form['review_page_heading']
            create_order_text_box_2 = request.form['review_page_textarea']


            review_page_info['custom_message_type'] = "Review Page Customization"
            review_page_info['create_order_text_box_1'] = create_order_text_box_1
            review_page_info['create_order_text_box_2'] = create_order_text_box_2
            DOL_DB.save_custom_order_related_texts(review_page_info)
    return redirect(url_for('custom_viewWrapper'))


@app.route("/save_prod_review_page_details",methods=['POST'])
@login_required
def save_custom_product_review_page_details():
    form_prod_review_page = ProductReviewPageCutomization()
    formclass = 'form-control'
    prod_rev_info = {}
    cst_mgs_type_list = []
    cstm_type_list = []
    session["prod_review_page"] = ''
    email = session['email_retailer']

    entry_msg_cur = DOL_DB.get_custom_order_related_texts()
    for e in entry_msg_cur:
        cst_mgs_type_list.append(e['custom_message_type'])
    print(cst_mgs_type_list)

    if cst_mgs_type_list:
        for typ in cst_mgs_type_list:
            
            if typ == 'Product Review Page Customization':
                session["prod_review_page"] = typ
                
        typ_curs = DOL_DB.get_custom_product_review_page_details_by_cst_type()
        for t in typ_curs:
            cstm_type_list.append(t)
        print(cstm_type_list)

        if cstm_type_list:
            if form_prod_review_page.validate_on_submit():
                create_order_text_box_1 = request.form['product_review_page_heading']
                create_order_text_box_2 = request.form['product_review_page_textarea']
                
                prod_rev_info['create_order_text_box_1'] = create_order_text_box_1
                prod_rev_info['create_order_text_box_2'] = create_order_text_box_2
                
                DOL_DB.update_custom_product_review_page_details_by_type(prod_rev_info)

        else:
            if form_prod_review_page.validate_on_submit():

                create_order_text_box_1 = request.form['product_review_page_heading']
                create_order_text_box_2 = request.form['product_review_page_textarea']


                prod_rev_info['custom_message_type'] = "Product Review Page Customization"
                prod_rev_info['create_order_text_box_1'] = create_order_text_box_1
                prod_rev_info['create_order_text_box_2'] = create_order_text_box_2
                DOL_DB.save_custom_order_related_texts(prod_rev_info)

    else:
        if form_prod_review_page.validate_on_submit():

            create_order_text_box_1 = request.form['product_review_page_heading']
            create_order_text_box_2 = request.form['product_review_page_textarea']


            prod_rev_info['custom_message_type'] = "Product Review Page Customization"
            prod_rev_info['create_order_text_box_1'] = create_order_text_box_1
            prod_rev_info['create_order_text_box_2'] = create_order_text_box_2
            DOL_DB.save_custom_order_related_texts(prod_rev_info)
    return redirect(url_for('custom_viewWrapper'))


@app.route("/save_feedback_review_page_details",methods=['POST'])
@login_required
def save_custom_consumer_feedback_review_page_details():
    form_feedback_page = ReviewConsumerFeedbackPageCutomization()
    formclass = 'form-control'
    feedback_page_info = {}
    cst_mgs_type_list = []
    cstm_type_list = []
    session["feedback_review_page"] = ''
    email = session['email_retailer']

    entry_msg_cur = DOL_DB.get_custom_order_related_texts()
    for e in entry_msg_cur:
        cst_mgs_type_list.append(e['custom_message_type'])
    print(cst_mgs_type_list)

    if cst_mgs_type_list:
        for typ in cst_mgs_type_list:
            
            if typ == 'Consumer Feedback Review Page Customization':
                session["feedback_review_page"] = typ
                
        typ_curs = DOL_DB.get_custom_feedback_review_page_details_by_cst_type()
        for t in typ_curs:
            cstm_type_list.append(t)
        print(cstm_type_list)

        if cstm_type_list:
            if form_feedback_page.validate_on_submit():
                create_order_text_box_1 = request.form['feedbak_page_heading']
                create_order_text_box_2 = request.form['feedback_page_textarea']
                
                feedback_page_info['create_order_text_box_1'] = create_order_text_box_1
                feedback_page_info['create_order_text_box_2'] = create_order_text_box_2
                DOL_DB.update_custom_feedback_review_page_details_by_type(feedback_page_info)

        else:
            if form_feedback_page.validate_on_submit():

                create_order_text_box_1 = request.form['feedbak_page_heading']
                create_order_text_box_2 = request.form['feedback_page_textarea']


                feedback_page_info['custom_message_type'] = "Consumer Feedback Review Page Customization"
                feedback_page_info['create_order_text_box_1'] = create_order_text_box_1
                feedback_page_info['create_order_text_box_2'] = create_order_text_box_2
                DOL_DB.save_custom_order_related_texts(feedback_page_info)

    else:
        if form_feedback_page.validate_on_submit():

            create_order_text_box_1 = request.form['feedbak_page_heading']
            create_order_text_box_2 = request.form['feedback_page_textarea']


            feedback_page_info['custom_message_type'] = "Consumer Feedback Review Page Customization"
            feedback_page_info['create_order_text_box_1'] = create_order_text_box_1
            feedback_page_info['create_order_text_box_2'] = create_order_text_box_2
            DOL_DB.save_custom_order_related_texts(feedback_page_info)
    return redirect(url_for('custom_viewWrapper'))

@app.route("/save_feedback_review_page_four_details",methods=['POST'])
@login_required
def save_custom_consumer_feedback_review_page_four_details():
    form_feedback_four_page = ReviewConsumerFeedbackPageCutomizationForFourandMore()
    formclass = 'form-control'
    feedback_info = {}
    cst_mgs_type_list = []
    cstm_type_list = []
    session["feedback_four_review_page"] = ''
    email = session['email_retailer']

    entry_msg_cur = DOL_DB.get_custom_order_related_texts()
    for e in entry_msg_cur:
        cst_mgs_type_list.append(e['custom_message_type'])
    print(cst_mgs_type_list)

    if cst_mgs_type_list:
        for typ in cst_mgs_type_list:
            
            if typ == 'Consumer Feedback Review Page For Four And More Customization':
                session["feedback_four_review_page"] = typ
                
        typ_curs = DOL_DB.get_custom_feedback_review_page_four_details_by_cst_type()
        for t in typ_curs:
            cstm_type_list.append(t)
        print(cstm_type_list)

        if cstm_type_list:
            if form_feedback_four_page.validate_on_submit():
                create_order_text_box_1 = request.form['fdbk_page_heading']
                create_order_text_box_2 = request.form['fdbk_page_textarea']
                
                feedback_info['create_order_text_box_1'] = create_order_text_box_1
                feedback_info['create_order_text_box_2'] = create_order_text_box_2
                DOL_DB.update_custom_feedback_review_page_four_details_by_type(feedback_info)


        else:
            if form_feedback_four_page.validate_on_submit():

                create_order_text_box_1 = request.form['fdbk_page_heading']
                create_order_text_box_2 = request.form['fdbk_page_textarea']


                feedback_info['custom_message_type'] = "Consumer Feedback Review Page For Four And More Customization"
                feedback_info['create_order_text_box_1'] = create_order_text_box_1
                feedback_info['create_order_text_box_2'] = create_order_text_box_2
                DOL_DB.save_custom_order_related_texts(feedback_info)

    else:
        if form_feedback_four_page.validate_on_submit():

            create_order_text_box_1 = request.form['fdbk_page_heading']
            create_order_text_box_2 = request.form['fdbk_page_textarea']


            feedback_info['custom_message_type'] = "Consumer Feedback Review Page For Four And More Customization"
            feedback_info['create_order_text_box_1'] = create_order_text_box_1
            feedback_info['create_order_text_box_2'] = create_order_text_box_2
            
            DOL_DB.save_custom_order_related_texts(feedback_info)
    return redirect(url_for('custom_viewWrapper'))



@app.route("/save_covid_precautionary_details",methods=['POST'])
@login_required
def save_custom_covid_precautonary_details():
    form_covid_precaution = CovidPrecautionaryMessageForm()
    formclass = 'form-control'
    covid_info = {}
    cst_mgs_type_list = []
    cstm_type_list = []
    session["covid_precautions"] = ''
    email = session['email_retailer']

    entry_msg_cur = DOL_DB.get_custom_order_related_texts()
    for e in entry_msg_cur:
        cst_mgs_type_list.append(e['custom_message_type'])
    print(cst_mgs_type_list)

    if cst_mgs_type_list:
        for typ in cst_mgs_type_list:
            
            if typ == 'Covid Precautions Customization':
                session["covid_precautions"] = typ
                
        typ_curs = DOL_DB.get_custom_coivid_precaution_details_by_cst_type()
        for t in typ_curs:
            cstm_type_list.append(t)
        print(cstm_type_list)

        if cstm_type_list:
            if form_covid_precaution.validate_on_submit():
                create_order_text_box_1 = request.form['covd_page_heading']
                create_order_text_box_2 = request.form['covd_page_textarea']
                
                covid_info['create_order_text_box_1'] = create_order_text_box_1
                covid_info['create_order_text_box_2'] = create_order_text_box_2
                DOL_DB.update_custom_covide_precaution_by_type(covid_info)


        else:
            if form_covid_precaution.validate_on_submit():

                create_order_text_box_1 = request.form['covd_page_heading']
                create_order_text_box_2 = request.form['covd_page_textarea']


                covid_info['custom_message_type'] = "Covid Precautions Customization"
                covid_info['create_order_text_box_1'] = create_order_text_box_1
                covid_info['create_order_text_box_2'] = create_order_text_box_2
                DOL_DB.save_custom_order_related_texts(covid_info)

    else:
        if form_covid_precaution.validate_on_submit():

            create_order_text_box_1 = request.form['covd_page_heading']
            create_order_text_box_2 = request.form['covd_page_textarea']


            covid_info['custom_message_type'] = "Covid Precautions Customization"
            covid_info['create_order_text_box_1'] = create_order_text_box_1
            covid_info['create_order_text_box_2'] = create_order_text_box_2
            DOL_DB.save_custom_order_related_texts(covid_info)
    return redirect(url_for('custom_viewWrapper'))


#==========================================Seamless(Excel Uploader)==========================================================================
# @app.route("/excel_uploader", methods=['GET'])
# @login_required
# def seamless_Excel_sheet_uploader():
#     form = excelFile()
#     return render_template("excel_uploader.html",form=form)






#============================================================================================================================================
#---------------------------------Vendor Information-------------------------------------------------------------------------
@app.route("/vendor_info", methods=['GET'])
@login_required
def vendorWrapper():
    form = VendorInfoForm()
    form_cname = SearchVendorFormByConName()
    form_name = SearchVendorFormByName()
    form_cnum = SearchVendorFormByConNumber()
    form_city = SearchVendorFormByCity()
    formclass = 'form-control'

    vendor_records = []

    vendor_cur = DOL_DB.get_vendor_data()
    for v in vendor_cur:
        vendor_records.append(v)
    return render_template('vendor_form.html',
                            vendorRecords = vendor_records,
                            form = form,
                            form_cname = form_cname,
                            form_name = form_name,
                            form_cnum = form_cnum,
                            form_city = form_city,
                            formclass = formclass,
                            user = session['username_retailer'],
                            org = session['org_retailer'],
                            org_id = session['orgId_retailer'])


@app.route('/search_vends_records/<search_code>', methods=['POST'])
@login_required
def search_Vendor_Records(search_code):
    print("Inside Vendor search")
    form = VendorInfoForm()
    form_cname = SearchVendorFormByConName()
    form_name = SearchVendorFormByName()
    form_cnum = SearchVendorFormByConNumber()
    form_city = SearchVendorFormByCity()
    formclass = 'form-control'
    vendor_records = []

    if int(search_code) == 1:
        if form_name.validate_on_submit():
            session['vendor_name'] = request.form['searchbyName'].strip()
            print(session['vendor_name'])
            vends_cur = DOL_DB.search_by_v_name(session['vendor_name'], int(session['defaultPage']), int(session['rPerPage']))
            for o in vends_cur[0]:
                vendor_records.append(o)
            print("------------------------------------vendor_records of Search----------")
            print(vendor_records)
            session['searched_vendor_page_no'] = '1'
            session['searched_vendor_page_term'] = session['vendor_name']

    elif int(search_code) == 2:
        if form_cname.validate_on_submit():
            session['vendor_conname'] = request.form['searchbyCname'].strip()
            print(session['vendor_conname'])
            vends_cur = DOL_DB.search_by_con_name(session['vendor_conname'], int(session['defaultPage']), int(session['rPerPage']))
            for o in vends_cur[0]:
                vendor_records.append(o)
            print("------------------------------------vendor_records of Search----------")
            print(vendor_records)
            session['searched_vendor_page_no'] = ''
            session['searched_vendor_page_term'] = session['vendor_conname']

    elif int(search_code) == 3:
        if form_cnum.validate_on_submit():
            session['vendor_connum'] = str(request.form['searchbyCnum']).strip()        
            print(session['vendor_connum'])
            vends_cur = DOL_DB.search_by_con_number(session['vendor_connum'], int(session['defaultPage']), int(session['rPerPage']))
            for o in vends_cur[0]:
                vendor_records.append(o)
            print("------------------------------------vendor_records of Search----------")
            print(vendor_records)
            session['searched_vendor_page_no'] = ''
            session['searched_vendor_page_term'] = session['vendor_connum']

    elif int(search_code) == 4:
        if form_city.validate_on_submit():
            session['vendor_city'] = request.form['searchbyCity'].strip()
            print(session['vendor_city'])
            vends_cur = DOL_DB.search_by_v_city(session['vendor_city'], int(session['defaultPage']), int(session['rPerPage']))
            for o in vends_cur[0]:
                vendor_records.append(o)
            print("------------------------------------vendor_records of Search----------")
            print(vendor_records)
            session['searched_vendor_page_no'] = '4'
            session['searched_vendor_page_term'] = session['vendor_city']
    
    session['search_activated_vendor'] = True
    return render_template('vendor_form.html',
                            vendorRecords = vendor_records,
                            form = form,
                            form_cname = form_cname,
                            form_name = form_name,
                            form_cnum = form_cnum,
                            form_city = form_city,
                            formclass = formclass,
                            user = session['username_retailer'],
                            org = session['org_retailer'])


@app.route("/save_vendor_info", methods=['POST'])
@login_required
def save_vendor_information():
    session['search_activated_vendor'] = False
    form = VendorInfoForm()
    formclass = 'form-control'
    if form.validate_on_submit():
        vendor_Data = DOL_info.set_VendorData()
        print(vendor_Data)

        DOL_DB.save_vendor_informaton(vendor_Data)
    return redirect(url_for('vendorWrapper'))

@app.route("/edit_vendor_data/<v_id>", methods=['GET'])
@login_required
def edit_vendor_information(v_id):
    form = VendorEditInfoForm()
    formclass = 'form-control'
    v_recs = []

    v_cursor = DOL_DB.get_vendor_info_by_v_id(v_id)
    for vd in v_cursor:
        v_recs.append(vd)

    form.v_name.data = v_recs[0]['vendor_name']
    form.v_inds.data = v_recs[0]['vendor_industry']
    form.v_cnumber.data = v_recs[0]['vendor_contact_number']
    form.v_email.data = v_recs[0]['vendor_email_ids']
    form.v_city.data = v_recs[0]['vendor_city']
    form.v_addrs.data = v_recs[0]['vendor_address']
    form.v_con.data = v_recs[0]['vendor_country']
    form.v_cname.data = v_recs[0]['vendor_contact_name']
    form.v_zip.data = v_recs[0]['vendor_zip_code']
    form.v_desc.data = v_recs[0]['vendor_description']
    return render_template('vendor_edit_form.html',
                            v_recs = v_recs,
                            vendor_id = v_id,
                            form = form,
                            formclass = formclass )


@app.route("/update_vendor_info/<v_id>",methods=['POST'])
@login_required
def update_vendor_information(v_id):
    v_disc = {}
    form = VendorUpdateInfoForm()
    formclass = "form-control"
    if form.validate_on_submit():
        v_disc['vendor_name'] = request.form['v_name']
        v_disc['vendor_industry'] = request.form['v_inds']
        v_disc['vendor_address'] = request.form['v_addrs']
        v_disc['vendor_contact_name'] = request.form['v_cname']
        v_disc['vendor_contact_number'] = request.form['v_cnumber']
        v_disc['vendor_email_ids'] = request.form['v_email']
        v_disc['vendor_country'] = request.form['v_con']
        v_disc['vendor_city'] = request.form['v_city']
        v_disc['vendor_zip_code'] = request.form['v_zip']
        v_disc['vendor_description'] = request.form['v_desc']

        DOL_DB.update_vendor_data(v_id,v_disc)

    return redirect(url_for('edit_vendor_information',v_id = v_id))

@app.route("/delete_a_vendor/<v_id>", methods=['GET'])
@login_required
def delete_vendor_by_v_id(v_id):
    DOL_DB.delete_a_vendor(v_id)
    return redirect(url_for('vendorWrapper'))


#-----------------------------------------Search Linked PO----------------------------------------------------------
@app.route("/search_by_linked_po/<url_param>", methods=['POST','GET'])
@login_required
def search_all_orders_linked_to_po(url_param):
    form_po = SearchWFOrderFormByPO()
    form_city = SearchWFOrderFormByCity()
    form_otype = SearchWFOrderFormByWFType()
    form_state = SearchWFOrderFormByState()
    form_daterange = SearchWFOrderFormByDateRange()
    form_jobname = SearchWFOrderFormByJobName()
    form_fname = SearchWFOrderFormByFirstName()
    form_lname = SearchWFOrderFormByLastName()
    form_checkbox_pgrstmln = CheckboxForBulkPgrstimeline()
    form_blk_pgrstm = RedButtonWFOrderpgrogressTimelineForm()
    formclass = 'form-control'
    searched_data = []
    form_checkbox_pgrstmln.nexus_id_cbox.choices = []
    work_flow_stages_list = []
    form_blk_pgrstm.pgrs_stage_name.choices = []

    paras = url_param.split('_')
    po_no = paras[0]
    n_id = paras[1]

    search_cursor = DOL_DB.get_search_result_per_linked_po(po_no)
    for s in search_cursor:
        searched_data.append(s)
        work_flow_stages_list.append(s['work_flow_stages'])
        form_checkbox_pgrstmln.nexus_id_cbox.choices.append((s['nexus_id'],s['nexus_id']))
    wfl_stages = searched_data[0]['work_flow_stages']
    print("==================================================================================")
    print(form_checkbox_pgrstmln.nexus_id_cbox.choices)
    print("==================================================================================")

    form_info = zip(searched_data,form_checkbox_pgrstmln.nexus_id_cbox)

    print("-------------------------------------------------------------------------------")
    print(work_flow_stages_list)
    print("-------------------------------------------------------------------------------")

    form_blk_pgrstm.pgrs_stage_name.choices = [(s, s)for s in wfl_stages]
    print('``````````````````````````````````````````````````````````````````````````')
    print(form_blk_pgrstm.pgrs_stage_name.choices)
    print('``````````````````````````````````````````````````````````````````````````')


    return render_template('search_form.html',
                            orderInfoList = searched_data,
                            nexus_id = n_id,
                            user = session['username_retailer'],
                            org = session['org_retailer'],
                            org_id = session['orgId_retailer'],
                            form_po = form_po,
                            form_city = form_city,
                            form_otype = form_otype,
                            form_state = form_state,
                            form_daterange = form_daterange,
                            form_fname = form_fname,
                            form_lname = form_lname,
                            form_checkbox_pgrstmln = form_checkbox_pgrstmln,
                            form_blk_pgrstm = form_blk_pgrstm,
                            form_info=form_info,
                            po_no = po_no,
                            formclass = formclass )

#=============================================================================================

#----------------------------------------Consumer Information-------------------------------------------------------------
@app.route("/consumer_info", methods=['GET'])
@login_required
def consumerWrapper():
    form = ConsumerInfoForm()
    form_excel = consumerexcelFile()
    form_city = SearchConsumerFormByCity()
    form_state = SearchConsumerFormByState()
    form_mobile = SearchConsumerFormByMobile()
    form_fname = SearchConsumerFormByFName()
    formclass = 'form-control'
    consumer_list = []

    consumer_Cur = DOL_DB.get_consumer_data()
    for cons in consumer_Cur:
        consumer_list.append(cons)
    return render_template('consumer_form.html',
                            form = form,
                            form_excel = form_excel,
                            formclass = formclass,
                            form_city = form_city,
                            form_state = form_state,
                            form_mobile = form_mobile,
                            form_fname = form_fname,
                            consumerlist = consumer_list,
                            user = session['username_retailer'],
                            org = session['org_retailer'],
                            org_id = session['orgId_retailer'])

@app.route('/search_cons_records/<search_code>', methods=['POST'])
@login_required
def search_consumer_Records(search_code):
    print("Inside consumer search")
    form = ConsumerInfoForm()
    form_excel = consumerexcelFile()
    form_city = SearchConsumerFormByCity()
    form_state = SearchConsumerFormByState()
    form_mobile = SearchConsumerFormByMobile()
    form_fname = SearchConsumerFormByFName()
    formclass = 'form-control'
    consumer_list = []
    

    if int(search_code) == 1:
        if form_fname.validate_on_submit():
            session['consumer_fname'] = request.form['searchbyFName'].strip()
            print(session['consumer_fname'])
            cons_cur = DOL_DB.search_by_c_first_name(session['consumer_fname'], int(session['defaultPage']), int(session['rPerPage']))
            for o in cons_cur[0]:
                consumer_list.append(o)
            print("------------------------------------consumer_list of Search----------")
            print(consumer_list)
            session['searched_consumer_page_no'] = '1'
            session['searched_consumer_page_term'] = session['consumer_fname']

    elif int(search_code) == 2:
        if form_mobile.validate_on_submit():
            session['consumer_monum'] = str(request.form['searchbyMobile']).strip()
            print(session['consumer_monum'])
            cons_cur = DOL_DB.search_by_mob_number(session['consumer_monum'], int(session['defaultPage']), int(session['rPerPage']))
            for o in cons_cur[0]:
                consumer_list.append(o)
            print("------------------------------------consumer_list of Search----------")
            print(consumer_list)
            session['searched_consumer_page_no'] = '2'
            session['searched_consumer_page_term'] = session['consumer_monum']

    elif int(search_code) == 3:
        if form_city.validate_on_submit():
            session['consumer_city'] = request.form['searchbyCity'].strip()
            print(session['consumer_city'])
            cons_cur = DOL_DB.search_by_c_city(session['consumer_city'], int(session['defaultPage']), int(session['rPerPage']))
            for o in cons_cur[0]:
                consumer_list.append(o)
            print("------------------------------------consumer_list of Search----------")
            print(consumer_list)
            session['searched_consumer_page_no'] = '3'
            session['searched_consumer_page_term'] = session['consumer_city']


    elif int(search_code) == 4:
        if form_state.validate_on_submit():
            session['consumer_state'] = request.form['searchbyState'].strip()
            print(session['consumer_state'])
            cons_cur = DOL_DB.search_by_c_state(session['consumer_state'], int(session['defaultPage']), int(session['rPerPage']))
            for o in cons_cur[0]:
                consumer_list.append(o)
            print("------------------------------------consumer_list of Search----------")
            print(consumer_list)
            session['searched_consumer_page_no'] = '4'
            session['searched_consumer_page_term'] = session['consumer_state']

    

    print(form_state.errors)
    session['search_activated_consumer'] = True
    return render_template('consumer_form.html',
                            consumerlist = consumer_list,
                            form = form,
                            form_excel = form_excel,
                            form_city = form_city,
                            form_state = form_state,
                            form_mobile = form_mobile,
                            form_fname = form_fname,
                            formclass = formclass,
                            user = session['username_retailer'],
                            org = session['org_retailer'])


@app.route("/save_consumer_info", methods=['POST'])
@login_required
def save_consumer_information():
    session['search_activated_consumer'] = False
    form = ConsumerInfoForm()
    formclass = 'form-control'
    consumer_list = []
    if form.validate_on_submit():
        consumer_data = DOL_info.set_ConsumerData()
        print(consumer_data)

        ph_num = consumer_data['consumer_mobile_number']

        cons_cursor = DOL_DB. get_consumer_info_by_ph_num(ph_num)
        for c in cons_cursor:
            consumer_list.append(c)

        if consumer_list:
            print("User exist")
            pass
        else:
            DOL_DB.save_consumer_informaton(consumer_data)
    return redirect(url_for('consumerWrapper'))

@app.route("/edit_consumer_data/<c_id>", methods=['GET'])
@login_required
def edit_consumer_information(c_id):
    form = ConsumerInfoEditForm()
    formclass = 'form-control'
    con_recs = []

    con_cursor = DOL_DB.get_consumer_info_by_c_id(c_id)
    for cn in con_cursor:
        con_recs.append(cn)
    
    form.c_fname.data = con_recs[0]['consumer_first_name']
    form.c_lname.data = con_recs[0]['consumer_last_name']
    form.c_mobile.data = con_recs[0]['consumer_mobile_number']
    form.c_email.data = con_recs[0]['consumer_email']
    form.c_dob.data = con_recs[0]['consumer_date_of_birth']
    form.c_addrs.data = con_recs[0]['consumer_address']
    form.c_city.data = con_recs[0]['consumer_city']
    form.c_con.data = con_recs[0]['consumer_country']
    form.c_state.data = con_recs[0]['consumer_state']
    form.c_zip_code.data = con_recs[0]['consumer_zip_code']
    form.c_user_type.data = con_recs[0]['user_type']
    return render_template('consumer_edit_form.html',
                            consumers_recs = con_recs,
                            consumer_id = c_id,
                            form = form,
                            formclass = formclass )


@app.route("/update_consumer_info/<c_id>",methods=['POST'])
@login_required
def update_consumer_information(c_id):
    c_disc = {}
    form = ConsumerInfoUpdateForm()
    formclass = "form-control"
    if form.validate_on_submit():
        if request.form['c_dob']:
            c_disc['consumer_date_of_birth'] = request.form['c_dob']
        else:
            c_disc['consumer_date_of_birth'] = ""

        c_disc['consumer_first_name'] = request.form['c_fname']
        c_disc['consumer_last_name'] = request.form['c_lname']
        c_disc['consumer_mobile_number'] = request.form['c_mobile']
        c_disc['consumer_email'] = request.form['c_email']
        c_disc['consumer_address'] = request.form['c_addrs']
        c_disc['consumer_city'] = request.form['c_city']
        c_disc['consumer_country'] = request.form['c_con']
        c_disc['consumer_state'] = request.form['c_state']
        c_disc['consumer_zip_code'] = request.form['c_zip_code']
        c_disc['user_type'] = request.form['c_user_type']

        DOL_DB.update_consumer_data(c_id,c_disc)
    print(form.errors)

    return redirect(url_for('edit_consumer_information',c_id = c_id))

@app.route("/delConsumer/<c_id>/<ph_num>", methods=['GET'])
@login_required
def delete_a_consumer(c_id,ph_num):
    print(c_id)
    DOL_DB.delete_a_consumer(c_id,ph_num)
    DOL_DB.delete_a_consumer_credentials(ph_num)
    return redirect(url_for('consumerWrapper'))



@app.route("/excel_uploaderConsumer", methods=['POST'])
def excelReader_Consumer():
    consumer_data = {}
    form_excel = consumerexcelFile()
    f = form_excel.excelip.data
    print(f)
    filename = secure_filename(f.filename)
    print(filename)
    rows = []
    wb = xlrd.open_workbook(file_contents=f.read())
    sheet = wb.sheet_by_index(0)
    specific_cell = sheet.cell_value(0, 0)
    print(specific_cell)

    column_names_list = []
    column_name_index = 0

    currentDT = datetime.today()
    current_welcome_datetime = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")
    welcome_datetime = current_welcome_datetime
    cons_datetime = current_welcome_datetime



    # Extracting all columns name
    for i in range(sheet.ncols):
        column_names_list.append(sheet.cell_value(column_name_index, i))
    print(column_names_list)
    
    data_row = []


    starting_row = 1
    for i in range(starting_row, sheet.nrows):
        print(sheet.row_values(i))
        data_row.append(sheet.row_values(i))

    print("============================================")
    print(data_row)
    print("============================================")
    
    for i in range(len(data_row)):
        consumer_id = generate_id(4,2)

        consumer_data["consumer_id"]=consumer_id.strip()
        consumer_data["consumer_first_name"]=data_row[i][column_names_list.index('FIRST NAME')].strip()
        consumer_data["consumer_last_name"]=data_row[i][column_names_list.index('LAST NAME')].strip()
        consumer_data["consumer_mobile_number"]=str(int(data_row[i][column_names_list.index('MOBILE NUMBER')]))
        consumer_data["consumer_email"]=data_row[i][column_names_list.index('EMAIL')]
        consumer_data['consumer_date_of_birth'] = ""
        consumer_data["consumer_address"]=data_row[i][column_names_list.index('ADDRESS')].strip()
        consumer_data["consumer_city"]=data_row[i][column_names_list.index('CITY')].strip()
        consumer_data["consumer_country"]=data_row[i][column_names_list.index('COUNTRY')].strip()
        consumer_data["consumer_state"] = data_row[i][column_names_list.index('STATE')].strip()
        consumer_data["consumer_zip_code"]=str(data_row[i][column_names_list.index('ZIPCODE')]).strip()
        consumer_data['user_type'] = data_row[i][column_names_list.index('USER TYPE')].strip()
        consumer_data['welcome_email'] = False
        consumer_data['welcome_email_datetime'] = welcome_datetime
        consumer_data['consumer_origin'] = "Consumer Bulk"
        consumer_data['receive_mail_notification'] = True
        consumer_data['receive_sms_notification'] = True
        consumer_data['excel_upload'] = "Excel"
        consumer_data['consumer_datetime'] = cons_datetime
        DOL_DB.save_consumer_informaton(consumer_data)
        consumer_data = {}
    return redirect(url_for('consumerWrapper'))



#----------------------------------------Contractors Information-------------------------------------------------------------
@app.route("/contractor_info", methods=['GET'])
@login_required
def contractorWrapper():
    form = ContractorsInfoForm()
    form_city = SearchContractorsFormByCity()
    form_state = SearchContractorsFormByState()
    form_mobile = SearchContractorsFormByMobile()
    form_fname = SearchContractorsFormByFName()
    formclass = 'form-control'
    cons_list = []

    cons_cursor = DOL_DB.get_contractors_data()
    for con in cons_cursor:
        cons_list.append(con)
    return render_template('contractors.html',
                            form = form,
                            formclass = formclass,
                            form_city = form_city,
                            form_state = form_state,
                            form_mobile = form_mobile,
                            form_fname = form_fname,
                            consList = cons_list,
                            user = session['username_retailer'],
                            org = session['org_retailer'],
                            org_id = session['orgId_retailer'])


@app.route('/search_cont_records/<search_code>', methods=['POST'])
@login_required
def search_contractor_Records(search_code):
    print("Inside contractor search")
    form = ContractorsInfoForm()
    form_city = SearchContractorsFormByCity()
    form_state = SearchContractorsFormByState()
    form_mobile = SearchContractorsFormByMobile()
    form_fname = SearchContractorsFormByFName()
    formclass = 'form-control'
    cons_list = []
    

    if int(search_code) == 1:
        if form_fname.validate_on_submit():
            session['contractor_fname'] = request.form['searchbyFName']
            print(session['contractor_fname'])
            cont_cur = DOL_DB.search_by_cont_first_name(session['contractor_fname'], int(session['defaultPage']), int(session['rPerPage']))
            for o in cont_cur[0]:
                cons_list.append(o)
            print("------------------------------------cons_list of Search----------")
            print(cons_list)
            session['searched_contractor_page_no'] = '1'
            session['searched_contractor_page_term'] = session['contractor_fname']

    elif int(search_code) == 2:
        if form_mobile.validate_on_submit():
            session['contractor_monum'] = str(request.form['searchbyMobile']).strip()
            print(session['contractor_monum'])
            cont_cur = DOL_DB.search_by_cont_mob_number(session['contractor_monum'], int(session['defaultPage']), int(session['rPerPage']))
            for o in cont_cur[0]:
                cons_list.append(o)
            print("------------------------------------cons_list of Search----------")
            print(cons_list)
            session['searched_contractor_page_no'] = '2'
            session['searched_contractor_page_term'] = session['contractor_monum']

    elif int(search_code) == 3:
        if form_city.validate_on_submit():
            session['contractor_city'] = request.form['searchbyCity'].strip()
            print(session['contractor_city'])
            cont_cur = DOL_DB.search_by_cont_city(session['contractor_city'], int(session['defaultPage']), int(session['rPerPage']))
            for o in cont_cur[0]:
                cons_list.append(o)
            print("------------------------------------cons_list of Search----------")
            print(cons_list)
            session['searched_contractor_page_no'] = '3'
            session['searched_contractor_page_term'] = session['contractor_city']


    elif int(search_code) == 4:
        if form_state.validate_on_submit():
            session['contractor_state'] = request.form['searchbyState'].strip()
            print(session['contractor_state'])
            cont_cur = DOL_DB.search_by_cont_state(session['contractor_state'], int(session['defaultPage']), int(session['rPerPage']))
            for o in cont_cur[0]:
                cons_list.append(o)
            print("------------------------------------cons_list of Search----------")
            print(cons_list)
            session['searched_contractor_page_no'] = '4'
            session['searched_contractor_page_term'] = session['contractor_state']

    

    print(form_state.errors)
    session['search_activated_contractor'] = True
    return render_template('contractors.html',
                            consList = cons_list,
                            form = form,
                            form_city = form_city,
                            form_state = form_state,
                            form_mobile = form_mobile,
                            form_fname = form_fname,
                            formclass = formclass,
                            user = session['username_retailer'],
                            org = session['org_retailer'])


@app.route("/save_cont_info", methods=['POST'])
@login_required
def save_contractor_information():
    session['search_activated_contractor'] = False
    form = ContractorsInfoForm()
    formclass = 'form-control'
    if form.validate_on_submit():
        contractor_info = DOL_info.set_ContractorData()
        print(contractor_info)

        DOL_DB.save_contractors_information(contractor_info)
    return redirect(url_for('contractorWrapper'))

@app.route("/edit_cont_data/<cont_id>", methods=['GET'])
@login_required
def edit_contractorsinformation(cont_id):
    form = ContractorsInfoEditForm()
    formclass = 'form-control'
    cont_recs = []

    cont_cursor = DOL_DB.get_contractors_info_by_cont_id(cont_id)
    for ct in cont_cursor:
        cont_recs.append(ct)

    form.cont_fname.data = cont_recs[0]['contractor_first_name']
    form.cont_lname.data = cont_recs[0]['contractor_last_name']
    form.cont_mobile.data = cont_recs[0]['contractor_mobile_number']
    form.cont_email.data = cont_recs[0]['contractor_email']
    form.cont_addrs.data = cont_recs[0]['contractor_address']
    form.cont_city.data = cont_recs[0]['contractor_city']
    form.cont_con.data = cont_recs[0]['contractor_country']
    form.cont_state.data = cont_recs[0]['contractor_state']
    form.cont_zip.data = cont_recs[0]['contractor_zip_code']
    return render_template('contractor_edit_form.html',
                            contractors_recs = cont_recs,
                            contractor_id = cont_id,
                            form = form,
                            formclass = formclass )


@app.route("/update_contractor_info/<cont_id>",methods=['POST'])
@login_required
def update_contractor_information(cont_id):
    cont_disc = {}
    form = ContractorsInfoUpdateForm()
    formclass = "form-control"
    if form.validate_on_submit():
        cont_disc['contractor_first_name'] = request.form['cont_fname']
        cont_disc['contractor_last_name'] = request.form['cont_lname']
        cont_disc['contractor_mobile_number'] = request.form['cont_mobile']
        cont_disc['contractor_email'] = request.form['cont_email']
        cont_disc['contractor_address'] = request.form['cont_addrs']
        cont_disc['contractor_city'] = request.form['cont_city']
        cont_disc['contractor_country'] = request.form['cont_con']
        cont_disc['contractor_state'] = request.form['cont_state']
        cont_disc['contractor_zip_code'] = request.form['cont_zip']

        DOL_DB.update_contractors_data(cont_id,cont_disc)

    return redirect(url_for('edit_contractorsinformation',cont_id = cont_id))

@app.route("/deleteCont/<cont_id>", methods=['GET'])
@login_required
def delete_a_contractor_info(cont_id):
    DOL_DB.delete_a_contractor(cont_id)
    return redirect(url_for('contractorWrapper'))

#==============================================Red button custom message on Workflow order======================================================

@app.route("/redbtn_wfcstm_msg", methods=['POST'])
@login_required
def custm_messageWorkflowWrapper():
    form_redbtn = RedButtonWFOrderForm()
    formclass = 'form-control'
    org_id = session['orgId_retailer']
    all_order_phone_list = []
    all_order_email_list = []
    all_order_nexus_id_list = []
    all_order_po_list = []
    all_phone_Po_list = []
    communication_Info = {}
    communication_Info_Email = {}

    last_acti_list = []

    if form_redbtn.validate_on_submit():
        nexus_id_list = request.form['cstm_msg_ids'].split(',')
        print(nexus_id_list)

        for i in nexus_id_list:
            print("-----------------------i : ", i)
            cstm_cursor = DOL_DB.get_one_wforder_detail(i)

            for nx in cstm_cursor:
                all_order_phone_list.append(nx['consumer_mobile_number'])
                all_order_email_list.append(nx['consumer_email'])
                all_order_nexus_id_list.append(nx['nexus_id'])
                all_order_po_list.append(nx['po_number'])
                all_phone_Po_list.append([nx['consumer_mobile_number'],nx['po_number'],nx['consumer_email'],nx['nexus_id']])
            print(all_phone_Po_list)


        subject = request.form['sub_ject']
        email_subject = request.form['mail_subject']
        sending_mode = request.form['send_type']
        message_plain_text = request.form['msg']

        communication_log_id = generate_id(4,2)
        currentDT = datetime.today()
        current_log_datetime = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")


        communication_Info['communication_log_id'] = communication_log_id.strip()
        communication_Info['nexus_id'] = all_order_nexus_id_list
        communication_Info['po_number'] = all_order_po_list
        communication_Info['logger_id'] = session['orgId_retailer']
        communication_Info['logger_name'] = session['fullname_retailer']
        communication_Info['logger_type'] = "Dealer".strip()
        communication_Info['subject'] = subject
        communication_Info['sms_subject'] = email_subject
        communication_Info['sending_mode'] = "SMS".strip()
        communication_Info['message_plain_text'] = message_plain_text
        communication_Info['current_log_datetime'] = current_log_datetime.strip()
        communication_Info['action_taken'] = "".strip()

        communication_Info_Email['communication_log_id'] = communication_log_id.strip()
        communication_Info_Email['nexus_id'] = all_order_nexus_id_list
        communication_Info_Email['po_number'] = all_order_po_list
        communication_Info_Email['logger_id'] = session['orgId_retailer']
        communication_Info_Email['logger_name'] = session['fullname_retailer']
        communication_Info_Email['logger_type'] = "Dealer".strip()
        communication_Info_Email['subject'] = subject
        communication_Info_Email['email_subject'] = email_subject
        communication_Info_Email['sending_mode'] = "Email".strip()
        communication_Info_Email['message_plain_text'] = message_plain_text
        communication_Info_Email['current_log_datetime'] = current_log_datetime.strip()
        communication_Info_Email['action_taken'] = "".strip()
        
        print('===================================================')
        print(communication_Info)

        if sending_mode == 'SMS':
            sendSms.send_bulk_log_msg(all_order_phone_list,all_phone_Po_list,communication_Info)
            DOL_DB.save_communication_logs(communication_Info)
        else:
            sendSms.send_bulk_log_msg(all_order_phone_list,all_phone_Po_list,communication_Info)
            DOL_DB.save_communication_logs(communication_Info)
            sendMail.send_bulk_log_mail(all_order_email_list,all_phone_Po_list,communication_Info_Email)
            DOL_DB.save_communication_logs(communication_Info_Email)

        for nid in nexus_id_list:
            currentDT = datetime.today()
            current_datetime_for_last_activity = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")

            last_acti_cur = DOL_DB.get_one_wforder_detail(nid)
            for la in last_acti_cur:
                last_acti_list.append(la)

            last_activity = last_acti_list[0]['last_activity']

            print("==================================================")
            print(last_activity)
            print("==================================================")

            last_activity = current_datetime_for_last_activity
            print(last_activity)

            DOL_DB.update_last_activity_of_an_order_change(nid,last_activity)

            last_acti_list = []

    print(form_redbtn.errors)
    return redirect(url_for('WF_orderWrapper'))




#=============================================== Red button for lead Time Work flow orders ===================================================================

@app.route("/bulk_wfleadtime", methods=['POST'])
@login_required
def bulk_leadtime_updateWFWrapper():
    form_rbtnleadtime = RedButtonWFLeadTime()
    formclass = 'form-control'
    org_id = session['orgId_retailer']
    lTime_info = {}
    lTime_logs = {}
    order_List = []
    all_order_original_est_dlr_date = []
    all_order_phone_list = []
    all_order_email_list = []
    all_order_po_list = []
    all_order_original_lead_time = []
    all_order_original_buffer_time = []
    all_order_order_date_list = []
    est_deliver_time_list = []
    all_phone_Po_list = []
    old_lead_time_weeks_to_days_list = []
    old_lead_time_in_days_list = []
    buffer_time_weeks_to_days_list = []
    buffer_time_in_days_list = []
    datetime_object_list = []
    new_lead_time_int_list = []
    est_deliver_time_list_to_str = []
    est_deliver_time = ''
    est_deliver_time_list_to_new_format = []

    if form_rbtnleadtime.validate_on_submit():
        nexus_id_list = request.form['cst_leadtm_ids'].split(',')
        print(nexus_id_list)

        lead_time_parameter = request.form['cal_lead_type']
        total_lead_time = request.form['ttl_lt']
        lead_time_reason = request.form['cst_leadtm_reason']

        lead_time_int = int(total_lead_time)
        new_lead_time_weeks_to_days = lead_time_int*7
        new_lead_time_in_days = timedelta(days=new_lead_time_weeks_to_days)
        

        for i in nexus_id_list:
            cstm_cursor = DOL_DB.get_one_wforder_detail(i)
            print("-----i : ",i)

            for nx in cstm_cursor:
                all_order_phone_list.append(nx['consumer_mobile_number'])
                all_order_email_list.append(nx['consumer_email'])
                all_order_order_date_list.append(nx['order_date'])
                all_order_po_list.append(nx['po_number'])
                all_order_original_est_dlr_date.append(nx['est_deliver_time'])
                
                all_order_original_lead_time.append(int(nx['total_lead_time']))
                all_order_original_buffer_time.append(int(nx['dealer_buffer_time']))
                all_phone_Po_list.append((nx['consumer_mobile_number'],nx['po_number'],nx['consumer_email'],nx['nexus_id']))
                print("-----all_phone_Po_list : ",all_phone_Po_list)


        print("--------------------------all_order_order_date_list")
        print(all_order_order_date_list)
        
        print("--------------------------all_order_original_lead_time")
        print(all_order_original_lead_time)

        print("--------------------------all_order_original_buffer_time")
        print(all_order_original_buffer_time)


        print("--------------------------all_order_original_est_dlr_date")
        print(all_order_original_est_dlr_date)



        for ld in all_order_original_lead_time:
            old_lead_time_weeks_to_days_list.append(ld*7)
        print("=======================================old_lead_time_weeks_to_days_list")
        print(old_lead_time_weeks_to_days_list)


        for old in old_lead_time_weeks_to_days_list:
            old_lead_time_in_days_list.append(timedelta(days=old))
        print("------------------------------------------------old_lead_time_in_days_list")
        print(old_lead_time_in_days_list)


        for br in all_order_original_buffer_time:
            buffer_time_weeks_to_days_list.append(br*7)
        print('----------------------------------------------buffer_time_weeks_to_days_list')
        print(buffer_time_weeks_to_days_list)


        for brd in buffer_time_weeks_to_days_list:
            buffer_time_in_days_list.append(timedelta(days=brd))
        print('==============================================buffer_time_in_days_list')
        print(buffer_time_in_days_list)


        for od in all_order_order_date_list:
            date_object = datetime.strptime(od,'%m-%d-%Y')
            datetime_object_list.append(date_object.date())

        print('-------------------------------------------------datetime_object_list')
        print(datetime_object_list)



        if lead_time_parameter == 'increase':
            
            for oldi in all_order_original_lead_time:
                new_lead_time_int_list.append(lead_time_int + oldi)
            print(new_lead_time_int_list)


            for dto, oldi, brtd in zip(datetime_object_list, old_lead_time_in_days_list, buffer_time_in_days_list):
                est_deliver_time_list.append(dto + oldi + new_lead_time_in_days + brtd)
            print('--------------------------------------est_deliver_time_list')
            print(est_deliver_time_list)

            for est in est_deliver_time_list:
                est_deliver_time_list_to_new_format.append(datetime.strptime(str(est),'%Y-%m-%d'))

            for nestime in est_deliver_time_list_to_new_format:
                est_deliver_time_list_to_str.append(nestime.strftime("%m-%d-%Y"))
            print('--------------------------------------------est_deliver_time_list_to_str')
            print("------------------------est type of new date : ",est_deliver_time_list_to_str)

            #est_deliver_time_date_time_object = datetime.strptime(est_deliver_time_date,'%Y-%m-%d')
            #new_est_deliver_time_date_time_object_date = est_deliver_time_date_time_object.strftime("%m-%d-%Y")
            #print("--------------------------est-new date : ", new_est_deliver_time_date_time_object_date)
            #print("------------------------est type of new date : ",type(new_est_deliver_time_date_time_object_date))
        else:
            for oldi in all_order_original_lead_time:
                new_lead_time_int_list.append(oldi - lead_time_int)
            print(new_lead_time_int_list)

            for dto, oldi, brtd in zip(datetime_object_list, old_lead_time_in_days_list, buffer_time_in_days_list):
                est_deliver_time_list.append(dto + oldi - new_lead_time_in_days + brtd)
            print('--------------------------------------est_deliver_time_list')
            print(est_deliver_time_list)

            for est in est_deliver_time_list:
                est_deliver_time_list_to_new_format.append(datetime.strptime(str(est),'%Y-%m-%d'))

            for nestime in est_deliver_time_list_to_new_format:
                est_deliver_time_list_to_str.append(nestime.strftime("%m-%d-%Y"))
            print('--------------------------------------------est_deliver_time_list_to_str')
            print("------------------------est type of new date : ",est_deliver_time_list_to_str)


        for nid, nldi, est in zip(nexus_id_list, new_lead_time_int_list, est_deliver_time_list_to_str):
            lTime_info['change_time_entity'] = "Manufacturing lead time".strip()
            lTime_info['lead_time_parameter'] = lead_time_parameter
            lTime_info['total_lead_time'] = nldi
            lTime_info['est_deliver_time'] = str(est)
            lTime_info["lead_time_reason"] = lead_time_reason

            print("-----------------lTime_info",lTime_info)

            DOL_DB.update_wf_leadtime_record(nid, lTime_info)

        lTime_logs['change_time_entity'] = "Manufacturing lead time"
        lTime_logs["total_lead_time"] = str(lead_time_int)
        lTime_logs["lead_time_parameter"] = lead_time_parameter
        lTime_logs["lead_time_reason"] = lead_time_reason
        
        print('--------------------------------------lTime_logs------------------------------------')
        print(lTime_logs)

        save_and_send_bulk_lead_time_WFlogs(nexus_id_list, all_order_po_list, lTime_logs, all_order_order_date_list,all_phone_Po_list, all_order_original_est_dlr_date, est_deliver_time_list_to_str)
    print(form_rbtnleadtime.errors)
    return redirect(url_for('WF_orderWrapper'))


def save_and_send_bulk_lead_time_WFlogs(nexus_id_list, all_order_po_list, lTime_logs, all_order_order_date_list,all_phone_Po_list, all_order_original_est_dlr_date, est_deliver_time_list_to_str):
    communication_Info = {}
    communication_Info_Email = {}
    comm_log = {}
    text_message_list_sms = []
    text_message_list_email = []
    consumer_info_list = []

    type_list_email = []
    type_list = []
    cstm_type_list = []

    last_acti_list = []

    session['sub_1'] = ''
    session['salutaion_1'] = ''
    session['text_body_1'] = ''
    session['conclusion_1'] = ''

    session['sub_2'] = ''
    session['salutaion_2'] = ''
    session['text_body_2'] = ''
    session['conclusion_2'] = ''

    print("-------------------all phone for lead time--------------------------------")
    print(all_phone_Po_list)

    cstm_msg_cursor = DOL_DB.get_custom_order_related_texts()
    for cst in cstm_msg_cursor:
        cstm_type_list.append(cst['custom_message_type'])
    print("----------------------Custom Type-----------------------------------------------")
    print(cstm_type_list)

    if cstm_type_list:
        for typ in cstm_type_list:

            if typ == "Red Button Lead Time Change":
                print("=====================================TRUE")
                
                typ_cursor = DOL_DB.get_custom_order_related_texts_by_type(typ)
                for t in typ_cursor:
                    type_list.append(t)
                print("-------------------------------------------------------",type_list)
                print(type_list)
                print("=========================================================================")

                # session['sub_1'] = type_list[0]['create_order_text_box_1']
                # print("Subject 1 ---------------------------------: ",session['sub_1'] )
                session['salutaion_1'] = type_list[0]['create_order_text_box_2']
                print("Salutation 1 ---------------------------------: ",session['salutaion_1'] )
                session['text_body_1'] = type_list[0]['create_order_text_box_3']
                print("Text body 1 ---------------------------------: ",session['text_body_1'] )
                session['conclusion_1'] = type_list[0]['create_order_text_box_4']
                print("Conclusion 1 ---------------------------------: ",session['conclusion_1'] )
                print("=========================================================================")


            if  typ == "Red Button Lead Time Change Email":
                print("===================EMAIL==================TRUE")
                typ_cursor_email = DOL_DB.get_custom_order_related_texts_by_type(typ)
                for t in typ_cursor_email:
                    type_list_email.append(t)
                print("-----------------------------------------type_list_email--------------")
                print(type_list_email)

                session['sub_2'] = type_list_email[0]['create_order_text_box_1']
                session['salutaion_2'] = type_list_email[0]['create_order_text_box_2']
                session['text_body_2'] = type_list_email[0]['create_order_text_box_3']
                session['conclusion_2'] = type_list_email[0]['create_order_text_box_4']


    if int(lTime_logs['total_lead_time']) > 1:
        week_placeholder_text = " weeks" 
    elif int(lTime_logs['total_lead_time']) == 1:
        week_placeholder_text = " week"
    else:
        week_placeholder_text = " week"

    print(type(est_deliver_time_list_to_str))

    #comm_log['subject'] = "Related to Delivery".strip()
    comm_log['subject_sms'] = session['sub_1']
    comm_log['salutaion_sms'] = session['salutaion_1']
    comm_log['text_body_sms'] = session['text_body_1']
    comm_log['conclusion_sms'] = session['conclusion_1']

    comm_log['subject_email'] = session['sub_2']
    comm_log['salutaion_email'] = session['salutaion_2']
    comm_log['text_body_email'] = session['text_body_2']
    comm_log['conclusion_email'] = session['conclusion_2']

    comm_log['reason'] = lTime_logs["lead_time_reason"]

    for i in est_deliver_time_list_to_str:
        print("***************************************")
        print(i)
        print('***********************************************')


    for odtl, oest, nest in zip(all_order_order_date_list, all_order_original_est_dlr_date, est_deliver_time_list_to_str):
        text_message_list_sms.append(lTime_logs['change_time_entity'] +' has been ' + lTime_logs["lead_time_parameter"] + 'd' + " by " + lTime_logs['total_lead_time'] + week_placeholder_text + "." + " New estimated delivery date is " +  str(nest) + " ")
        text_message_list_email.append(lTime_logs['change_time_entity'] +' has been ' + lTime_logs["lead_time_parameter"] + 'd' + " by " + lTime_logs['total_lead_time'] + week_placeholder_text + "." + " New estimated delivery date is " +  str(nest) + " ")
    
    print('------------------------------------------------text_message_list_sms')
    print(text_message_list_sms)
    print('------------------------------------------------text_message_list_sms')


    for ph in all_phone_Po_list:
        print(ph[0])
        consumer_cursor = DOL_DB.get_consumer_data_by_phone(ph[0])
        for c in consumer_cursor:
            consumer_info_list.append(c)
        print("---------------------------------------------consumer_info_list")
        print("Consumer Database------------ : ",consumer_info_list)

    if consumer_info_list:
        if consumer_info_list[0]['receive_sms_notification']==True and consumer_info_list[0]['receive_mail_notification']==False:
            print("SMS True")
            sendSms.send_bulk_log_msg_for_lead_and_buffer_time(all_phone_Po_list,comm_log,text_message_list_sms)
            #DOL_DB.save_communication_logs(communication_Info)
            #communication_Info = {}

        elif consumer_info_list[0]['receive_mail_notification']==True and consumer_info_list[0]['receive_sms_notification']==False:
            print("Email True")
            sendMail.send_bulk_log_mail_for_lead_and_buffer_time(all_phone_Po_list,comm_log,text_message_list_email)
            #DOL_DB.save_communication_logs(communication_Info_Email)
            #communication_Info_Email = {}

        elif consumer_info_list[0]['receive_mail_notification']==True and consumer_info_list[0]['receive_sms_notification']==True:
            print("Both true")
            sendSms.send_bulk_log_msg_for_lead_and_buffer_time(all_phone_Po_list,comm_log,text_message_list_sms)
            #DOL_DB.save_communication_logs(communication_Info)
            #communication_Info = {}
            sendMail.send_bulk_log_mail_for_lead_and_buffer_time(all_phone_Po_list,comm_log,text_message_list_email)
            #DOL_DB.save_communication_logs(communication_Info_Email)
            #communication_Info_Email = {}

        else:
            print("No action")
    else:
        print("Consumer data does not exit")
        sendSms.send_bulk_log_msg_for_lead_and_buffer_time(all_phone_Po_list,comm_log,text_message_list_sms)
        #DOL_DB.save_communication_logs(communication_Info)
        #communication_Info = {}
        sendMail.send_bulk_log_mail_for_lead_and_buffer_time(all_phone_Po_list,comm_log,text_message_list_email)
        #DOL_DB.save_communication_logs(communication_Info_Email)
        #communication_Info_Email = {}


    for nid, po, txt, txte in zip(nexus_id_list, all_order_po_list,text_message_list_sms,text_message_list_email):
        communication_log_id = generate_id(4,2)
        currentDT = datetime.today()
        current_log_datetime = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")

        communication_Info['communication_log_id'] = communication_log_id.strip()
        communication_Info['nexus_id'] = nid
        communication_Info['po_number'] = po
        communication_Info['logger_id'] = session['orgId_retailer']
        communication_Info['logger_name'] = session['fullname_retailer']
        communication_Info['logger_type'] = "Dealer".strip()
        communication_Info['subject'] = session['sub_1']
        communication_Info['sending_mode'] = "SMS".strip()
        communication_Info['message_plain_text'] = txt
        communication_Info['Reason'] = lTime_logs["lead_time_reason"]
        communication_Info['current_log_datetime'] = current_log_datetime.strip()
        communication_Info['action_taken'] = "".strip()

        communication_Info_Email['communication_log_id'] = communication_log_id.strip()
        communication_Info_Email['nexus_id'] = nid
        communication_Info_Email['po_number'] = po
        communication_Info_Email['logger_id'] = session['orgId_retailer']
        communication_Info_Email['logger_name'] = session['fullname_retailer']
        communication_Info_Email['logger_type'] = "Dealer".strip()
        communication_Info_Email['subject'] = session['sub_2']
        communication_Info_Email['sending_mode'] = "Email".strip()
        communication_Info_Email['message_plain_text'] = txte
        communication_Info_Email['Reason'] = lTime_logs["lead_time_reason"]
        communication_Info_Email['current_log_datetime'] = current_log_datetime.strip()
        communication_Info_Email['action_taken'] = "".strip()

        print('=========================communication_Info==========================')
        print(communication_Info)
        DOL_DB.save_communication_logs(communication_Info)
        communication_Info = {}

        print('=========================communication_Info_Email==========================')
        print(communication_Info_Email)

        DOL_DB.save_communication_logs(communication_Info_Email)
        communication_Info_Email = {}


    for nid in nexus_id_list:
        currentDT = datetime.today()
        current_datetime_for_last_activity = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")

        last_acti_cur = DOL_DB.get_one_wforder_detail(nid)
        for la in last_acti_cur:
            last_acti_list.append(la)

        last_activity = last_acti_list[0]['last_activity']

        print("==================================================")
        print(last_activity)
        print("==================================================")

        last_activity = current_datetime_for_last_activity
        print(last_activity)

        DOL_DB.update_last_activity_of_an_order_change(nid,last_activity)

        last_acti_list = []
    
    return

#=============================================== Red button for buffer Time workflow orders ===================================================================


@app.route("/bulk_wfbuffertime", methods=['POST'])
@login_required
def bulk_buffertime_updateWFWrapper():
    form_rbtnbuffertime = RedButtonWFBufferTime()
    formclass = 'form-control'
    org_id = session['orgId_retailer']
    bTime_info = {}
    bTime_logs = {}
    order_List = []
    all_order_original_est_dlr_date = []
    all_order_phone_list = []
    all_order_email_list = []
    all_order_po_list = []
    all_order_original_lead_time = []
    all_order_original_buffer_time = []
    all_order_order_date_list = []
    est_deliver_time_list = []
    all_phone_Po_list = []
    old_lead_time_weeks_to_days_list = []
    old_lead_time_in_days_list = []
    buffer_time_weeks_to_days_list = []
    buffer_time_in_days_list = []
    datetime_object_list = []
    new_buffer_time_int_list = []
    est_deliver_time_list_to_str = []
    est_deliver_time = ''
    est_deliver_time_list_to_new_format = []

    if form_rbtnbuffertime.validate_on_submit():
        nexus_id_list = request.form['cstm_bfrtm_ids'].split(',')
        print(nexus_id_list)

        buffer_time_parameter = request.form['cal_buffer_type']
        dealer_buffer_time = request.form['dlr_bfr_tm']
        buffer_time_reason = request.form['cst_bfrtm_reason']

        buffer_time_int = int(dealer_buffer_time)
        new_buffer_time_weeks_to_days = buffer_time_int*7
        new_buffer_time_in_days = timedelta(days=new_buffer_time_weeks_to_days)


        for i in nexus_id_list:
            cstm_cursor = DOL_DB.get_one_wforder_detail(i)
            print("--------------i : ", i)

            for nx in cstm_cursor:
                all_order_phone_list.append(nx['consumer_mobile_number'])
                all_order_email_list.append(nx['consumer_email'])
                all_order_order_date_list.append(nx['order_date'])
                all_order_po_list.append(nx['po_number'])
                all_order_original_est_dlr_date.append(nx['est_deliver_time'])
                
                all_order_original_lead_time.append(int(nx['total_lead_time']))
                all_order_original_buffer_time.append(int(nx['dealer_buffer_time']))
                all_phone_Po_list.append((nx['consumer_mobile_number'],nx['po_number'],nx['consumer_email'],nx['nexus_id']))
                print("----------------------------all_phone_Po_list : ",all_phone_Po_list)

        for ld in all_order_original_lead_time:
            old_lead_time_weeks_to_days_list.append(ld*7)
        print("=======================================old_lead_time_weeks_to_days_list")
        print(old_lead_time_weeks_to_days_list)

        for old in old_lead_time_weeks_to_days_list:
            old_lead_time_in_days_list.append(timedelta(days=old))
        print("------------------------------------------------old_lead_time_in_days_list")
        print(old_lead_time_in_days_list)

        for br in all_order_original_buffer_time:
            buffer_time_weeks_to_days_list.append(br*7)
        print('----------------------------------------------buffer_time_weeks_to_days_list')
        print(buffer_time_weeks_to_days_list)


        for brd in buffer_time_weeks_to_days_list:
            buffer_time_in_days_list.append(timedelta(days=brd))
        print('==============================================buffer_time_in_days_list')
        print(buffer_time_in_days_list)


        for od in all_order_order_date_list:
            date_object = datetime.strptime(od,'%m-%d-%Y')
            datetime_object_list.append(date_object.date())

        print('-------------------------------------------------datetime_object_list')
        print(datetime_object_list)

        if buffer_time_parameter == 'increase':
            for obrdi in all_order_original_buffer_time:
                new_buffer_time_int_list.append(buffer_time_int + obrdi)
            print(new_buffer_time_int_list)

            for dto, obrd, oldi in zip(datetime_object_list, buffer_time_in_days_list, old_lead_time_in_days_list):
                est_deliver_time_list.append(dto + obrd + new_buffer_time_in_days + oldi)
            print('--------------------------------------est_deliver_time_list')
            print(est_deliver_time_list)

            for est in est_deliver_time_list:
                est_deliver_time_list_to_new_format.append(datetime.strptime(str(est),'%Y-%m-%d'))

            for nestime in est_deliver_time_list_to_new_format:
                est_deliver_time_list_to_str.append(nestime.strftime("%m-%d-%Y"))
            print('--------------------------------------------est_deliver_time_list_to_str')
            print("------------------------est type of new date : ",est_deliver_time_list_to_str)

        else:
            for obrdi in all_order_original_buffer_time:
                new_buffer_time_int_list.append(obrdi - buffer_time_int)
            print(new_buffer_time_int_list)

            for dto, obrd, oldi in zip(datetime_object_list, buffer_time_in_days_list, old_lead_time_in_days_list):
                est_deliver_time_list.append(dto + obrd - new_buffer_time_in_days + oldi)
            print('--------------------------------------est_deliver_time_list')
            print(est_deliver_time_list)

            for est in est_deliver_time_list:
                est_deliver_time_list_to_new_format.append(datetime.strptime(str(est),'%Y-%m-%d'))

            for nestime in est_deliver_time_list_to_new_format:
                est_deliver_time_list_to_str.append(nestime.strftime("%m-%d-%Y"))
            print('--------------------------------------------est_deliver_time_list_to_str')
            print("------------------------est type of new date : ",est_deliver_time_list_to_str)

        for nid, nbrl, est in zip(nexus_id_list, new_buffer_time_int_list, est_deliver_time_list_to_str):
            bTime_info['change_time_entity'] = "Dealer lead time".strip()
            bTime_info['buffer_time_parameter'] = buffer_time_parameter
            bTime_info['dealer_buffer_time'] = nbrl
            bTime_info['est_deliver_time'] = str(est)
            bTime_info["buffer_time_reason"] = buffer_time_reason

            DOL_DB.update_wf_buffertime_record(nid, bTime_info)


        bTime_logs['change_time_entity'] = "Dealer lead time"
        bTime_logs["dealer_buffer_time"] = str(buffer_time_int)
        bTime_logs["buffer_time_parameter"] = buffer_time_parameter
        bTime_logs["buffer_time_reason"] = buffer_time_reason

        print('--------------------------------------bTime_logs------------------------------------')
        print(bTime_logs)


        save_and_send_bulk_wf_buffer_time_logs(nexus_id_list, all_order_po_list, bTime_logs, all_order_order_date_list,all_phone_Po_list, all_order_original_est_dlr_date, est_deliver_time_list_to_str)



    print(form_rbtnbuffertime.errors)
    return redirect(url_for('WF_orderWrapper'))


def save_and_send_bulk_wf_buffer_time_logs(nexus_id_list, all_order_po_list, bTime_logs, all_order_order_date_list,all_phone_Po_list, all_order_original_est_dlr_date, est_deliver_time_list_to_str):
    communication_Info = {}
    communication_Info_Email = {}
    comm_log = {}
    text_message_list_sms = []
    text_message_list_email = []
    consumer_info_list = []

    type_list_email = []
    type_list = []
    cstm_type_list = []

    last_acti_list = []

    session['sub_1'] = ''
    session['salutaion_1'] = ''
    session['text_body_1'] = ''
    session['conclusion_1'] = ''

    session['sub_2'] = ''
    session['salutaion_2'] = ''
    session['text_body_2'] = ''
    session['conclusion_2'] = ''

    print("-------------------all phone for lead time--------------------------------")
    print(all_phone_Po_list)

    cstm_msg_cursor = DOL_DB.get_custom_order_related_texts()
    for cst in cstm_msg_cursor:
        cstm_type_list.append(cst['custom_message_type'])
    print("----------------------Custom Type-----------------------------------------------")
    print(cstm_type_list)

    if cstm_type_list:
        for typ in cstm_type_list:

            if typ == "Red Button Buffer Time Change":
                print("=====================================TRUE")
                
                typ_cursor = DOL_DB.get_custom_order_related_texts_by_type(typ)
                for t in typ_cursor:
                    type_list.append(t)
                print("-------------------------------------------------------",type_list)
                print(type_list)
                print("=========================================================================")

                # session['sub_1'] = type_list[0]['create_order_text_box_1']
                # print("Subject 1 ---------------------------------: ",session['sub_1'] )
                session['salutaion_1'] = type_list[0]['create_order_text_box_2']
                print("Salutation 1 ---------------------------------: ",session['salutaion_1'] )
                session['text_body_1'] = type_list[0]['create_order_text_box_3']
                print("Text body 1 ---------------------------------: ",session['text_body_1'] )
                session['conclusion_1'] = type_list[0]['create_order_text_box_4']
                print("Conclusion 1 ---------------------------------: ",session['conclusion_1'] )
                print("=========================================================================")


            if  typ == "Red Button Buffer Time Change Email":
                print("===================EMAIL==================TRUE")
                typ_cursor_email = DOL_DB.get_custom_order_related_texts_by_type(typ)
                for t in typ_cursor_email:
                    type_list_email.append(t)
                print("-----------------------------------------type_list_email--------------")
                print(type_list_email)

                session['sub_2'] = type_list_email[0]['create_order_text_box_1']
                session['salutaion_2'] = type_list_email[0]['create_order_text_box_2']
                session['text_body_2'] = type_list_email[0]['create_order_text_box_3']
                session['conclusion_2'] = type_list_email[0]['create_order_text_box_4']



    if int(bTime_logs['dealer_buffer_time']) > 1:
        week_placeholder_text = " weeks" 
    elif int(bTime_logs['dealer_buffer_time']) == 1:
        week_placeholder_text = " week"
    else:
        week_placeholder_text = " week"

    print(type(est_deliver_time_list_to_str))
    
    comm_log['subject_sms'] = session['sub_1']
    comm_log['salutaion_sms'] = session['salutaion_1']
    comm_log['text_body_sms'] = session['text_body_1']
    comm_log['conclusion_sms'] = session['conclusion_1']

    comm_log['subject_email'] = session['sub_2']
    comm_log['salutaion_email'] = session['salutaion_2']
    comm_log['text_body_email'] = session['text_body_2']
    comm_log['conclusion_email'] = session['conclusion_2']
    comm_log['reason'] = bTime_logs["buffer_time_reason"]

    for i in est_deliver_time_list_to_str:
        print("***************************************")
        print(i)
        print('***********************************************')


    for odtl, oest, nest in zip(all_order_order_date_list, all_order_original_est_dlr_date, est_deliver_time_list_to_str):
        text_message_list_sms.append(bTime_logs['change_time_entity'] +' has been ' + bTime_logs["buffer_time_parameter"] + 'd' + " by " + bTime_logs['dealer_buffer_time'] + week_placeholder_text + "." + " New estimated delivery date is " +  str(nest) + " ")
        text_message_list_email.append(bTime_logs['change_time_entity'] +' has been ' + bTime_logs["buffer_time_parameter"] + 'd' + " by " + bTime_logs['dealer_buffer_time'] + week_placeholder_text + "." + " New estimated delivery date is " +  str(nest) + " ")
    
    print('------------------------------------------------text_message_list_sms')
    print(text_message_list_sms)
    print('------------------------------------------------')

    for ph in all_phone_Po_list:
        print(ph[0])
        consumer_cursor = DOL_DB.get_consumer_data_by_phone(ph[0])
        for c in consumer_cursor:
            consumer_info_list.append(c)
        print("---------------------------------------------consumer_info_list")
        print("Consumer Database------------ : ",consumer_info_list)

    if consumer_info_list:
        if consumer_info_list[0]['receive_sms_notification']==True and consumer_info_list[0]['receive_mail_notification']==False:
            print("SMS True")
            sendSms.send_bulk_log_msg_for_lead_and_buffer_time(all_phone_Po_list,comm_log,text_message_list_sms)

        elif consumer_info_list[0]['receive_mail_notification']==True and consumer_info_list[0]['receive_sms_notification']==False:
            print("Email True")
            sendMail.send_bulk_log_mail_for_lead_and_buffer_time(all_phone_Po_list,comm_log,text_message_list_email)

        elif consumer_info_list[0]['receive_mail_notification']==True and consumer_info_list[0]['receive_sms_notification']==True:
            print("Both true")
            sendSms.send_bulk_log_msg_for_lead_and_buffer_time(all_phone_Po_list,comm_log,text_message_list_sms)
            sendMail.send_bulk_log_mail_for_lead_and_buffer_time(all_phone_Po_list,comm_log,text_message_list_email)

        else:
            print("No action")
    else:
        print("Consumer data does not exit")
        sendSms.send_bulk_log_msg_for_lead_and_buffer_time(all_phone_Po_list,comm_log,text_message_list_sms)
        sendMail.send_bulk_log_mail_for_lead_and_buffer_time(all_phone_Po_list,comm_log,text_message_list_email)


    for nid, po, txt, txte in zip(nexus_id_list, all_order_po_list,text_message_list_sms,text_message_list_email):
        communication_log_id = generate_id(4,2)
        currentDT = datetime.today()
        current_log_datetime = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")

        communication_Info['communication_log_id'] = communication_log_id.strip()
        communication_Info['nexus_id'] = nid
        communication_Info['po_number'] = po
        communication_Info['logger_id'] = session['orgId_retailer']
        communication_Info['logger_name'] = session['fullname_retailer']
        communication_Info['logger_type'] = "Dealer".strip()
        communication_Info['subject'] = session['sub_1']
        communication_Info['sending_mode'] = "SMS".strip()
        communication_Info['message_plain_text'] = txt
        communication_Info['Reason'] = bTime_logs["buffer_time_reason"]
        communication_Info['current_log_datetime'] = current_log_datetime.strip()
        communication_Info['action_taken'] = "".strip()

        communication_Info_Email['communication_log_id'] = communication_log_id.strip()
        communication_Info_Email['nexus_id'] = nid
        communication_Info_Email['po_number'] = po
        communication_Info_Email['logger_id'] = session['orgId_retailer']
        communication_Info_Email['logger_name'] = session['fullname_retailer']
        communication_Info_Email['logger_type'] = "Dealer".strip()
        communication_Info_Email['subject'] = session['sub_2']
        communication_Info_Email['sending_mode'] = "Email".strip()
        communication_Info_Email['message_plain_text'] = txte
        communication_Info_Email['Reason'] = bTime_logs["buffer_time_reason"]
        communication_Info_Email['current_log_datetime'] = current_log_datetime.strip()
        communication_Info_Email['action_taken'] = "".strip()

        print('=========================communication_Info==========================')
        print(communication_Info)
        DOL_DB.save_communication_logs(communication_Info)
        communication_Info = {}

        print('=========================communication_Info_Email==========================')
        print(communication_Info_Email)

        DOL_DB.save_communication_logs(communication_Info_Email)
        communication_Info_Email = {}

    for nid in nexus_id_list:
        currentDT = datetime.today()
        current_datetime_for_last_activity = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")

        last_acti_cur = DOL_DB.get_one_wforder_detail(nid)
        for la in last_acti_cur:
            last_acti_list.append(la)

        last_activity = last_acti_list[0]['last_activity']

        print("==================================================")
        print(last_activity)
        print("==================================================")

        last_activity = current_datetime_for_last_activity
        print(last_activity)

        DOL_DB.update_last_activity_of_an_order_change(nid,last_activity)

        last_acti_list = []
    
    return


@app.route("/bulk_progress_time_line_update/<po_no>/<n_id>", methods=['POST'])
@login_required
def update_bulk_progress_timeline_records(po_no,n_id):
    form_po = SearchWFOrderFormByPO()
    form_city = SearchWFOrderFormByCity()
    form_otype = SearchWFOrderFormByWFType()
    form_state = SearchWFOrderFormByState()
    form_daterange = SearchWFOrderFormByDateRange()
    form_jobname = SearchWFOrderFormByJobName()
    form_fname = SearchWFOrderFormByFirstName()
    form_lname = SearchWFOrderFormByLastName()
    form_checkbox_pgrstmln = CheckboxForBulkPgrstimeline()
    form_blk_pgrstm = RedButtonWFOrderpgrogressTimelineForm()
    formclass = 'form-control'
    searched_data = []
    form_checkbox_pgrstmln.nexus_id_cbox.choices = []
    work_flow_stages_list = []
    form_blk_pgrstm.pgrs_stage_name.choices = []
    nexus_id_list = []

    all_order_phone_list = []
    all_order_email_list = []
    all_order_fname_list = []
    all_order_lname_list = []
    all_order_original_progress_timeline = []
    all_phone_Po_list = []
    all_order_final_stage_list = []
    all_order_consumer_id_list =[]
    pgrs_info = {}
    cstm_type_list = []
    type_list = []
    type_list_email = []
    text_message_list_sms = []
    text_message_list_email = []
    consumer_info_list = []
    communication_Info = {}
    communication_Info_Email = {}

    last_acti_list=[]

    session['sub_1'] = ''
    session['salutaion_1'] = ''
    session['text_body_1'] = ''
    session['conclusion_1'] = ''

    session['sub_2'] = ''
    session['salutaion_2'] = ''
    session['text_body_2'] = ''
    session['conclusion_2'] = ''

    comm_log = {}

    sub_date_list = []

    search_cursor = DOL_DB.get_search_result_per_linked_po(po_no)
    for s in search_cursor:
        searched_data.append(s)
        work_flow_stages_list.append(s['work_flow_stages'])
        form_checkbox_pgrstmln.nexus_id_cbox.choices.append((s['nexus_id'],s['nexus_id']))
    

    wfl_stages = searched_data[0]['work_flow_stages']
    wfl_request_automated_reviews = searched_data[0]['request_automated_reviews']
    final_wfl_stages = searched_data[0]['final_work_flow_stages']
    print("==================================================================================")
    print(form_checkbox_pgrstmln.nexus_id_cbox.choices)
    print("==================================================================================")

    form_info = zip(searched_data,form_checkbox_pgrstmln.nexus_id_cbox)

    print("-------------------------------------------------------------------------------")
    print(work_flow_stages_list)
    print("-------------------------------------------------------------------------------")
    print(final_wfl_stages)

    form_blk_pgrstm.pgrs_stage_name.choices = [(s, s)for s in wfl_stages]
    print('``````````````````````````````````````````````````````````````````````````')
    print(form_blk_pgrstm.pgrs_stage_name.choices)
    print('``````````````````````````````````````````````````````````````````````````')

    if form_blk_pgrstm.validate_on_submit():
        nexus_id_list = request.form['cstm_nex_ids'].split(',')
        print("test")
        print(request.form['cstm_nex_ids'])
        print(nexus_id_list)
        print("=================================================")

        progress_tmln_stage = request.form['pgrs_stage_name']
        print("=================================================")
        print(progress_tmln_stage)
        print("=================================================")

        for i in nexus_id_list:
            cstm_cursor = DOL_DB.get_search_result_per_linked_po_n_id(i)
            print("--------------i : ", i)

            for nx in cstm_cursor:
                all_order_phone_list.append(nx['consumer_mobile_number'])
                all_order_email_list.append(nx['consumer_email'])
                all_order_fname_list.append(nx['consumer_first_name'])
                all_order_lname_list.append(nx['consumer_last_name'])
                all_order_consumer_id_list.append(nx['relationship_number'])
                all_phone_Po_list.append((nx['consumer_mobile_number'],nx['po_number'],nx['consumer_email'],nx['nexus_id']))
                print("----------------------------all_phone_Po_list : ",all_phone_Po_list)

        
        progress_stage_number = wfl_stages.index(progress_tmln_stage)
        print("*****************************************")
        print(progress_stage_number)

        pgrs_info['progress_timeline'] = progress_tmln_stage
        pgrs_info['progress_stage_number'] = progress_stage_number

        for nex_id in nexus_id_list:
            print("##########################################################")
            print(pgrs_info)
            DOL_DB.update_wf_timeline_progress(nex_id,pgrs_info)
            print("#######################################################################")


        cstm_msg_cursor = DOL_DB.get_custom_order_related_texts()
        for cst in cstm_msg_cursor:
            cstm_type_list.append(cst['custom_message_type'])


        if cstm_type_list:
            for typ in cstm_type_list:

                if typ == "Red Button Progress Time Line Change":
                    
                    typ_cursor = DOL_DB.get_custom_order_related_texts_by_type(typ)
                    for t in typ_cursor:
                        type_list.append(t)

                    
                
                    session['sub_1'] = type_list[0]['create_order_text_box_1']
                    session['salutaion_1'] = type_list[0]['create_order_text_box_2']
                    session['text_body_1'] = type_list[0]['create_order_text_box_3']
                    session['conclusion_1'] = type_list[0]['create_order_text_box_4']

                    #text_message_1 = session['sub_1'] + progress_timeline + session['salutaion_1'] + config['consumer_portal_url']['CUST_URL'] + session['text_body_1'] + NexusId


                if  typ == "Red Button Progress Time Line Change Email":
                    print("===================EMAIL==================TRUE")
                    typ_cursor_email = DOL_DB.get_custom_order_related_texts_by_type(typ)
                    for t in typ_cursor_email:
                        type_list_email.append(t)
                    print("-----------------------------------------type_list_email--------------")
                    print(type_list_email)

                    session['sub_2'] = type_list_email[0]['create_order_text_box_1']
                    session['salutaion_2'] = type_list_email[0]['create_order_text_box_2']
                    session['text_body_2'] = type_list_email[0]['create_order_text_box_3']
                    session['conclusion_2'] = type_list_email[0]['create_order_text_box_4']


        comm_log['subject_sms'] = session['sub_1']
        comm_log['salutaion_sms'] = session['salutaion_1']
        comm_log['text_body_sms'] = session['text_body_1']
        comm_log['conclusion_sms'] = session['conclusion_1']

        comm_log['subject_email'] = session['sub_2']
        comm_log['salutaion_email'] = session['salutaion_2']
        comm_log['text_body_email'] = session['text_body_2']
        comm_log['conclusion_email'] = session['conclusion_2']


        for nex_id in nexus_id_list:
            text_message_list_sms.append(comm_log['subject_sms'] + progress_tmln_stage + comm_log['salutaion_sms'] + config['consumer_portal_url']['CUST_URL'] + comm_log['text_body_sms'] + comm_log['conclusion_sms'] + nex_id)
            text_message_list_email.append(comm_log['salutaion_email'] + progress_tmln_stage + comm_log['text_body_email'] + config['consumer_portal_url']['CUST_URL'] + comm_log['conclusion_email'] + nex_id)


        for ph in all_phone_Po_list:
            print(ph[0])
            consumer_cursor = DOL_DB.get_consumer_data_by_phone(ph[0])
            for c in consumer_cursor:
                consumer_info_list.append(c)

        if consumer_info_list:
            if consumer_info_list[0]['receive_sms_notification']==True and consumer_info_list[0]['receive_mail_notification']==False:
                print("SMS True")
                sendSms.send_bulk_log_msg_for_progress_time_line_update(all_phone_Po_list,text_message_list_sms)

            elif consumer_info_list[0]['receive_mail_notification']==True and consumer_info_list[0]['receive_sms_notification']==False:
                print("Email True")
                sendMail.send_bulk_log_mail_for_progress_time_line_update(all_phone_Po_list,comm_log,text_message_list_email)

            elif consumer_info_list[0]['receive_mail_notification']==True and consumer_info_list[0]['receive_sms_notification']==True:
                print("Both true")
                sendSms.send_bulk_log_msg_for_progress_time_line_update(all_phone_Po_list,text_message_list_sms)
                sendMail.send_bulk_log_mail_for_progress_time_line_update(all_phone_Po_list,comm_log,text_message_list_email)

            else:
                print("No action")

        else:
            print("Consumer data does not exit")
            sendSms.send_bulk_log_msg_for_progress_time_line_update(all_phone_Po_list,text_message_list_sms)
            sendMail.send_bulk_log_mail_for_progress_time_line_update(all_phone_Po_list,comm_log,text_message_list_email)


        for nid, txt, txte in zip(nexus_id_list,text_message_list_sms,text_message_list_email):
            communication_log_id = generate_id(4,2)
            currentDT = datetime.today()
            current_log_datetime = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")

            communication_Info['communication_log_id'] = communication_log_id.strip()
            communication_Info['nexus_id'] = nid
            communication_Info['po_number'] = po_no
            communication_Info['logger_id'] = session['orgId_retailer']
            communication_Info['logger_name'] = session['fullname_retailer']
            communication_Info['logger_type'] = "Dealer".strip()
            communication_Info['subject'] = session['sub_1']
            communication_Info['sending_mode'] = "SMS".strip()
            communication_Info['message_plain_text'] = txt
            communication_Info['current_log_datetime'] = current_log_datetime.strip()
            communication_Info['action_taken'] = "".strip()

            communication_Info_Email['communication_log_id'] = communication_log_id.strip()
            communication_Info_Email['nexus_id'] = nid
            communication_Info_Email['po_number'] = po_no
            communication_Info_Email['logger_id'] = session['orgId_retailer']
            communication_Info_Email['logger_name'] = session['fullname_retailer']
            communication_Info_Email['logger_type'] = "Dealer".strip()
            communication_Info_Email['subject'] = session['sub_2']
            communication_Info_Email['sending_mode'] = "Email".strip()
            communication_Info_Email['message_plain_text'] = txte
            communication_Info_Email['current_log_datetime'] = current_log_datetime.strip()
            communication_Info_Email['action_taken'] = "".strip()


            DOL_DB.save_communication_logs(communication_Info)
            communication_Info = {}

            DOL_DB.save_communication_logs(communication_Info_Email)
            communication_Info_Email = {}

        for nid,c_ph_num,c_email,c_fname,c_lname,cn_id in zip(nexus_id_list,all_order_phone_list,all_order_email_list,all_order_fname_list,all_order_lname_list,all_order_consumer_id_list):
            if progress_tmln_stage == final_wfl_stages and wfl_request_automated_reviews == 'Yes':
                print("------------------------------final stage review block")
                review_smart_process(nid,po_no,c_ph_num,c_email,c_fname,c_lname,cn_id)

        currentDT = datetime.today()
        order_submit_date = currentDT.strftime("%Y %b %d")
        for nid in nexus_id_list:
            if progress_tmln_stage == final_wfl_stages:
                order_submit_cursor = DOL_DB.get_one_wforder_detail(nid)
                for sub in order_submit_cursor:
                    sub_date_list.append(sub)

                order_submitted_date = sub_date_list[0]["order_completion_date"]

                order_submitted_date = order_submit_date
                DOL_DB.update_submitted_date_of_an_order(nid,order_submitted_date)

                sub_date_list = []


        for nid in nexus_id_list:
            currentDT = datetime.today()
            current_datetime_for_last_activity = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")

            last_acti_cur = DOL_DB.get_one_wforder_detail(nid)
            for la in last_acti_cur:
                last_acti_list.append(la)
            print(last_acti_list)

            if last_acti_list:

                last_activity = last_acti_list[0]['last_activity']

                print("==================================================")
                print(last_activity)
                print("==================================================")

                last_activity = current_datetime_for_last_activity
                print(last_activity)

                DOL_DB.update_last_activity_of_an_order_change(nid,last_activity)

                last_acti_list = []
           
            else:
                print("---------------------------------else")
                last_activity = current_datetime_for_last_activity
                print(last_activity)
                DOL_DB.update_last_activity_of_an_order_change(nid,last_activity)
                last_acti_list = []



    url_param = po_no + "_" + n_id

    print(form_blk_pgrstm.errors)
    return redirect(url_for("search_all_orders_linked_to_po",url_param = url_param))



#===========================================================================================================
@app.route("/reviews", methods=['GET'])
@login_required
def review_linksWrapper():
    form_online_review_links = ReviewLinksSettingForm()
    formclass = 'form-control'
    links_data = []
    review_list = []
    nex_id_list = []
    consumer_info = []
    consumer_f_name_list = []
    consumer_l_name_list = []
    rev_list = []

    link_cur = DOL_DB.get_review_links_details()
    for c in link_cur:
        links_data.append(c)

    review_cursor = DOL_DB.get_review_data_for_the_dealer()
    for r in review_cursor:
        review_list.append(r)

    return render_template("review_online.html",
                            form_online_review_links = form_online_review_links,
                            formclass = formclass,
                            links_data = links_data,
                            review_list= review_list,
                            consumer_info = consumer_info,
                            user = session['username_retailer'],
                            org = session['org_retailer'])

@app.route("/review_link_setting", methods=['POST'])
@login_required
def save_review_links_settings():
    form_online_review_links = ReviewLinksSettingForm()
    formclass = 'form-control'

    links_data = {}

    if form_online_review_links.validate_on_submit():
        review_link_name = request.form['rw_link_name']
        review_link_url = request.form['rw_link_url']
        review_link_label = request.form['rw_link_label']

        review_link_id = generate_id(4,2)
        links_data['review_link_id'] = review_link_id.strip()
        links_data['review_link_name'] = review_link_name.strip()
        links_data['review_link_url'] = review_link_url.strip()
        links_data['review_link_label'] = review_link_label.strip()

        DOL_DB.save_review_link_information(links_data)

    return redirect(url_for('review_linksWrapper'))

@app.route("/edit_review_link/<link_id>", methods=['GET'])
@login_required
def edit_review_link_details(link_id):
    form_online_review_links = ReviewLinksSettingForm()
    formclass = 'form-control'

    link_records = []

    link_cursor = DOL_DB.get_review_links_details_by_review_id(link_id)
    for c in link_cursor:
        link_records.append(c)


    form_online_review_links.rw_link_name.data = link_records[0]['review_link_name']
    form_online_review_links.rw_link_url.data = link_records[0]['review_link_url']
    form_online_review_links.rw_link_label.data = link_records[0]['review_link_label']

    return render_template("review_onlineEdit.html",
                            form_online_review_links = form_online_review_links,
                            formclass = formclass,
                            link_id = link_id,
                            user = session['username_retailer'],
                            org = session['org_retailer'])


@app.route("/update_review_link_info/<r_id>",methods=['POST'])
@login_required
def update_review_links_information(r_id):
    review_link_disc = {}
    form_online_review_links = ReviewLinksSettingForm()
    formclass = "form-control"
    if form_online_review_links.validate_on_submit():
        review_link_disc['review_link_name'] = request.form['rw_link_name']
        review_link_disc['review_link_url'] = request.form['rw_link_url']
        review_link_disc['review_link_label'] = request.form['rw_link_label']

        DOL_DB.update_review_link_data(r_id,review_link_disc)

    return redirect(url_for('edit_review_link_details',link_id = r_id))

@app.route("/delete_review_link/<r_id>",methods=['GET'])
@login_required
def delete_review_links_information(r_id):
    DOL_DB.delete_a_review_link_using_link_id(r_id)
    return redirect(url_for('review_linksWrapper'))

@app.route("/view_all_reviews/<review_paras>",methods=['GET','POST'])
@login_required
def view_all_review_Wrapper(review_paras):
    print("========================",review_paras)
    all_review_data = []
    all_consumer_data = []

    meta_list = []

    review_parameters = review_paras.split('_')
    
    r_id = review_parameters[0]
    n_id = review_parameters[1]
    c_id = review_parameters[2]

    all_review_cur = DOL_DB.get_review_data_by_review_id(r_id)
    for rev in all_review_cur:
        all_review_data.append(rev)

    print(all_review_data)
    service_review = all_review_data[0]['service_review_stars']
    
    cons_feddback = all_review_data[0]['consumer_feedback']

    all_consumer_cur = DOL_DB.get_one_wforder_detail(n_id)
    for con in all_consumer_cur:
        all_consumer_data.append(con)
    print("=========================",all_consumer_data)
    return render_template('view_reviews.html',
                            all_review_data = all_review_data,
                            all_consumer_data = all_consumer_data,
                            review_id = r_id,
                            nexus_id = n_id,
                            consumer_id = c_id,
                            cons_feddback = cons_feddback,
                            service_review = service_review,
                            user = session['username_retailer'],
                            org = session['org_retailer'])


@app.route("/activate_product_review/<review_paras>",methods=['POST'])
@login_required
def activate_product_review_Wrapper(review_paras):
    all_consumer_data = []

    review_parameters = review_paras.split('_')
    
    r_id = review_parameters[0]
    n_id = review_parameters[1]
    c_id = review_parameters[2]
    d_id = session['orgId_retailer']
    print("=============================: ", n_id)

    all_consumer_cur = DOL_DB.get_one_wforder_detail(n_id)
    for con in all_consumer_cur:
        all_consumer_data.append(con)

    print(all_consumer_data)
    po_no = all_consumer_data[0]["po_number"]
    c_ph_num = all_consumer_data[0]["consumer_mobile_number"]
    c_email = all_consumer_data[0]["consumer_email"]
    
    product_review_smart_process(r_id,d_id,n_id,po_no,c_ph_num,c_email,c_id)
    
    return redirect(url_for('view_all_review_Wrapper',review_paras = review_paras))




def product_review_smart_process(r_id,d_id,n_id,po_no,c_ph_num,c_email,c_id):
    print("=============================product smart review")
    print(n_id)
    print(po_no)
    print(c_ph_num)
    print(c_email)
    print(c_id)
    print("=================================================================")
    review_info = {}
    communication_Info = {}
    communication_Info_Email = {}
    consumer_info_list = []
    nexus_id = n_id

    session['sub_1'] = ''
    session['salutaion_1'] = ''
    session['text_body_1'] = ''
    session['conclusion_1'] = ''
    session['sub_2'] = ''
    session['salutaion_2'] = ''
    session['text_body_2'] = ''
    session['conclusion_2'] = ''
    cstm_type_list = []
    type_list = []
    type_list_email = []
    all_review_data = []

    domain_qa = "https://customer-ops.herokuapp.com"
    domain_local = "http://127.0.0.1:5000"

    prod_review_activate_token  = generate_activation_token(5,5)
    print(prod_review_activate_token)

    all_review_cur = DOL_DB.get_review_data_by_review_id(r_id)
    for rev in all_review_cur:
        all_review_data.append(rev)

    if all_review_data:
        dyn_url = all_review_data[0]['product_review_dynamic_url']
        prod_activation_state = all_review_data[0]['product_review_activation_state']
        prod_activation_date_time = all_review_data[0]['product_review_activation_date_time']
        prod_activation_token = all_review_data[0]['product_review_activate_token']

    if prod_activation_state == "Inactive":
        prod_activation_state = "Active"

    currentDT = datetime.today()
    current_review_datetime = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")
    prod_activation_date_time = current_review_datetime
    
    dynamic_url = domain_qa + "/product_review/" + d_id + "/" + r_id + "/" + prod_review_activate_token
    print(dynamic_url)

    DOL_DB.update_product_review_update_date_time_with_activation_token(r_id,prod_review_activate_token,prod_activation_date_time,prod_activation_state,dynamic_url)

    consumer_cursor = DOL_DB.get_consumer_data_by_phone(c_ph_num)
    for c in consumer_cursor:
        consumer_info_list.append(c)
    print("---------------------------------------------consumer_info_list")
    print("Consumer Database------------ : ",consumer_info_list)

    cstm_msg_cursor = DOL_DB.get_custom_order_related_texts()
    for cst in cstm_msg_cursor:
        cstm_type_list.append(cst['custom_message_type'])
    print("----------------------Custom Type-----------------------------------------------")
    print(cstm_type_list)

    if cstm_type_list:
        for typ in cstm_type_list:

            if typ == "Consumer Product Review Change":
                print("=====================================TRUE")
                    
                typ_cursor = DOL_DB.get_custom_order_related_texts_by_type(typ)
                for t in typ_cursor:
                    type_list.append(t)
                print("-------------------------------------------------------",type_list)
                
                session['sub_1'] = type_list[0]['create_order_text_box_1']
                session['salutaion_1'] = type_list[0]['create_order_text_box_2']
                #session['text_body_1'] = type_list[0]['create_order_text_box_3']
                #session['conclusion_1'] = type_list[0]['create_order_text_box_4']

                text_message_1 = session['sub_1'] + dynamic_url + " " + session['salutaion_1'] + nexus_id
                print(text_message_1)


            if  typ == "Consumer Product Review Change Email":
                print("===================EMAIL==================TRUE")
                typ_cursor_email = DOL_DB.get_custom_order_related_texts_by_type(typ)
                for t in typ_cursor_email:
                    type_list_email.append(t)
                print("-----------------------------------------type_list_email--------------")
                print(type_list_email)

                session['sub_2'] = type_list_email[0]['create_order_text_box_1']
                session['salutaion_2'] = type_list_email[0]['create_order_text_box_2']
                session['text_body_2'] = type_list_email[0]['create_order_text_box_3']
                #session['conclusion_2'] = type_list_email[0]['create_order_text_box_4']
                
                text_message_2 = session['salutaion_2'] + dynamic_url + " " + session['text_body_2'] + nexus_id
                print("============================================================================")
                print(text_message_2)
                print("==========================================================")

    

    #text_message = "Hello from Modern Garage Doors! Thank You for doing business with us. Feel free to provide us your feedback or review by clicking on this link. " + dynamic_url
    communication_log_id = generate_id(4,2)
    currentDT = datetime.today()
    current_log_datetime = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")

    communication_Info['communication_log_id'] = communication_log_id.strip()
    communication_Info['nexus_id'] = nexus_id.strip()
    communication_Info['po_number'] = po_no.strip()
    communication_Info['logger_id'] = session['orgId_retailer']
    communication_Info['logger_name'] = session['fullname_retailer']
    communication_Info['logger_type'] = "Dealer".strip()
    communication_Info['subject'] = session['sub_1']
    communication_Info['sending_mode'] = "SMS".strip()
    communication_Info['message_plain_text'] = text_message_1
    communication_Info['current_log_datetime'] = current_log_datetime.strip()
    communication_Info['action_taken'] = "".strip()

    communication_Info_Email['communication_log_id'] = communication_log_id.strip()
    communication_Info_Email['nexus_id'] = nexus_id.strip()
    communication_Info_Email['po_number'] = po_no.strip()
    communication_Info_Email['logger_id'] = session['orgId_retailer']
    communication_Info_Email['logger_name'] = session['fullname_retailer']
    communication_Info_Email['logger_type'] = "Dealer".strip()
    communication_Info_Email['subject'] = session['sub_2']
    communication_Info_Email['sending_mode'] = "Email".strip()
    communication_Info_Email['message_plain_text'] = text_message_2
    communication_Info_Email['current_log_datetime'] = current_log_datetime.strip()
    communication_Info_Email['action_taken'] = "".strip()

    print("--------------communication_Info-----------------------------------------------")
    print(communication_Info)
    
    if consumer_info_list:
        if consumer_info_list[0]['receive_sms_notification']==True and consumer_info_list[0]['receive_mail_notification']==False:
            print("k sms")
            sendSms.send_dynamic_url_to_consumer_via_SMS(c_ph_num,communication_Info)
            DOL_DB.save_communication_logs(communication_Info)

        elif consumer_info_list[0]['receive_mail_notification']==True and consumer_info_list[0]['receive_sms_notification']==False:
            sendMail.send_dynamic_url_to_consumer_via_email(c_email,communication_Info_Email)
            DOL_DB.save_communication_logs(communication_Info_Email)

        elif consumer_info_list[0]['receive_mail_notification']==True and consumer_info_list[0]['receive_sms_notification']==True:
            sendSms.send_dynamic_url_to_consumer_via_SMS(c_ph_num,communication_Info)
            DOL_DB.save_communication_logs(communication_Info)
            sendMail.send_dynamic_url_to_consumer_via_email(c_email,communication_Info_Email)
            DOL_DB.save_communication_logs(communication_Info_Email)

        else:
            print("No action")
    
    else:
        sendSms.send_dynamic_url_to_consumer_via_SMS(c_ph_num,communication_Info)
        DOL_DB.save_communication_logs(communication_Info)
        sendMail.send_dynamic_url_to_consumer_via_email(c_email,communication_Info_Email)
        DOL_DB.save_communication_logs(communication_Info_Email)
    return


#======================================================Profile DATA====================================================
@app.route("/profile_info", methods=['GET'])
@login_required
def profileWrapper():
    print("========================================inside profile page")
    dealers_info = []
    emp_info = []
    
    dealer_cursor = DOL_DB.get_dealer_basic_details_from_dealer_account()
    for dea in dealer_cursor:
        dealers_info.append(dea)
    print(dealers_info)

    emp_cursor = DOL_DB.get_dealer_basic_details_from_employee_account()
    for emp in emp_cursor:
        emp_info.append(emp)
    print(emp_info)
    return render_template('profile_page.html',
                            dealers_info = dealers_info,
                            emp_info = emp_info,
                            user = session['username_retailer'],
                            org = session['org_retailer'])

#===============================================ANNOUNCEMETS===========================================================

@app.route("/annc_data", methods=['GET'])
@login_required
def announcemetWrapper():
    print("========================================inside announcemets page")
    accouncemts_info = []
    
    annc_cursor = DOL_DB.get_all_announcements_for_dealers()
    for accn in annc_cursor:
        accouncemts_info.append(accn)
    print(accouncemts_info)
    return render_template('announcemts_page.html',
                            accouncemts_info = accouncemts_info,
                            user = session['username_retailer'],
                            org = session['org_retailer'])


#===============================================ANNOUNCEMETS===========================================================

@app.route("/logs_data", methods=['GET'])
@login_required
def LogsWrapper():
    print("========================================inside logs page")
    return render_template('all_logsForm.html',
                            user = session['username_retailer'],
                            org = session['org_retailer'])

@app.route("/view_logs_data", methods=['POST'])
@login_required
def view_LogsData():
    print("========================================inside logs data")
    logs_data = []
    year = request.form['selectye_ar']
    month = request.form['selectmon_th']
    print("--year: ",year)
    print("--month: ",month)

    log_cur = DOL_DB.get_dealer_logs_per_month(year,month)
    print('ALL: ',log_cur)

    log_email_cur = DOL_DB.get_dealer_email_logs_per_month(year,month)
    print('emails: ',log_email_cur)

    log_sms_cur = DOL_DB.get_dealer_sms_logs_per_month(year,month)
    print('SMS: ',log_sms_cur)
    # for d in log_cur:
    #     logs_data.append(d)
    # print('---------------------------------------')
    # print(logs_data)
    return redirect(url_for('LogsWrapper'))


@app.route("/terms_and_co_data", methods=['GET'])
@login_required
def TermsCoWrapper():
    print("========================================inside terms and co")

    terms_list = []
    terms_cur = DOL_DB.get_terms_and_condition_details()
    for x in terms_cur:
        terms_list.append(x)
    print(terms_list)
    return render_template('consumer_terms_n_co.html',
                            terms_list = terms_list,
                            user = session['username_retailer'],
                            org = session['org_retailer'])


#==========================================Seamless(Excel Uploader)==========================================================================
@app.route("/excel_uploader", methods=['GET'])
@login_required
def seamless_Excel_sheet_uploader():
    form = excelFile()
    return render_template("excel_uploader.html",form=form)

@app.route("/excel_uploader", methods=['POST'])
@login_required
def excelReader():
    WFOrderInfo = {}
    work_flow_list = []
    work_flow_request_for_automated_reviews_list = []
    work_flow_stages_list = []
    consumer_info_list = []
    consumer_cred_list = []
    consumer_nid_list = []
    nex_id_list = []
    cstm_type_list = []
    type_list = []
    type_list_email = []
    consumer_info_list_after_save = []
    
    welcome_type_list = []
    welcome_type_list_email = []

    conInfo = {}
    consumer_info = {}
    communication_Info = {}
    communication_Info_Email = {}
    consumer_po_dict = {}
    last_acti_list = []


    session['sub_1'] = ''
    session['salutaion_1'] = ''
    session['text_body_1'] = ''
    session['conclusion_1'] = ''

    session['sub_2'] = ''
    session['salutaion_2'] = ''
    session['text_body_2'] = ''
    session['conclusion_2'] = ''

    session['welcome_msg_sms'] = ''
    session['welcome_sub_email'] = ''
    session['welcome_msg_email'] = ''
    
    print("=================================Inside excel")
    form = excelFile()
    f = form.excelip.data
    filename = secure_filename(f.filename)
    rows = []
    wb = xlrd.open_workbook(file_contents=f.read())
    sheet = wb.sheet_by_index(0)
    specific_cell = sheet.cell_value(0, 0)

    column_names_list = []
    column_name_index = 0
    # Extracting all columns name
    for i in range(sheet.ncols):
        column_names_list.append(sheet.cell_value(column_name_index, i))
    
    data_row = []


    starting_row = 1
    for i in range(starting_row, sheet.nrows):
        print(sheet.row_values(i))
        data_row.append(sheet.row_values(i))
    
    for i in range(len(data_row)):
        nexus_id = generate_id(4,2)
        consumer_id = generate_id(4,2)

        WFOrderInfo["nexus_id"] = nexus_id.strip()
        WFOrderInfo["po_number"] = str(data_row[i][column_names_list.index('P.O. #')])
        
        order_date = data_row[i][column_names_list.index('ORDER DATE')].strip()

        datetime_object = datetime.strptime(order_date,'%m-%d-%Y')
        
        new_date = datetime_object.strftime("%m-%d-%Y")

        WFOrderInfo["order_date"] = new_date.strip()
        
        WFOrderInfo["work_flow_id"] = data_row[i][column_names_list.index('WORKFLOW ID')].strip()
        WFOrderInfo["order_price"] = str(data_row[i][column_names_list.index('PRICE')])
        WFOrderInfo["order_cost"] = str(data_row[i][column_names_list.index('COST')])
        WFOrderInfo["model"] = data_row[i][column_names_list.index('MODEL')]
        WFOrderInfo["size"] = data_row[i][column_names_list.index('SIZE')]
        WFOrderInfo["user_type"] = data_row[i][column_names_list.index('USER TYPE')]
        WFOrderInfo["relationship_number"] = consumer_id
        WFOrderInfo["job_name"] = data_row[i][column_names_list.index('JOB NAME')]
        WFOrderInfo["consumer_first_name"] = data_row[i][column_names_list.index('FIRST NAME')].strip()
        WFOrderInfo["consumer_last_name"] = data_row[i][column_names_list.index('LAST NAME')].strip()
        WFOrderInfo["consumer_mobile_number"] = str(int(data_row[i][column_names_list.index('PHONE NUMBER')]))
        WFOrderInfo["consumer_email"] = data_row[i][column_names_list.index('EMAIL')].strip()
        WFOrderInfo["consumer_date_of_birth"] = "".strip()
        WFOrderInfo["country"] = data_row[i][column_names_list.index('COUNTRY')].strip().strip()
        WFOrderInfo["state"] = data_row[i][column_names_list.index('STATE')].strip()
        WFOrderInfo["address"] = data_row[i][column_names_list.index('ADDRESS')].strip()
        WFOrderInfo["city"] = data_row[i][column_names_list.index('CITY')].strip()
        WFOrderInfo["dealer_id"] = session['orgId_retailer']
        WFOrderInfo["dealer_name"] = session['fullname_retailer']
        WFOrderInfo["dealer_phone"] = session['phonenum_retailer']
        WFOrderInfo["dealer_email"] = session['email_retailer']
        
        WFOrderInfo["brand"] = data_row[i][column_names_list.index('VENDOR')].strip()
        
        WFOrderInfo["total_lead_time"] = str(int(data_row[i][column_names_list.index('LEAD TIME')]))
        WFOrderInfo["dealer_buffer_time"] = str(int(data_row[i][column_names_list.index('BUFFER TIME')]))
        WFOrderInfo["consumer_zip_code"] = str(int(data_row[i][column_names_list.index('ZIPCODE')]))

        order_status = data_row[i][column_names_list.index('ORDER STATUS')].strip()

        now = datetime.today()

        new_now = now.strftime("%m-%d-%Y")

        delta = now - datetime_object

        delta_object_today = delta.days

        

        total_lead_time = WFOrderInfo["total_lead_time"]
        lead_time_int = int(total_lead_time)
        lead_time_weeks_to_days = lead_time_int*7
        lead_time_in_days = timedelta(days=lead_time_weeks_to_days)

        dealer_buffer_time = WFOrderInfo["dealer_buffer_time"]
        buffer_time_int = int(dealer_buffer_time)
        buffer_time_weeks_to_days = buffer_time_int*7
        buffer_time_in_days = timedelta(days=buffer_time_weeks_to_days)

        est_deliver_time = datetime_object + lead_time_in_days + buffer_time_in_days

        est_deliver_time_date = str(est_deliver_time.date())

        est_deliver_time_date_time_object = datetime.strptime(est_deliver_time_date,'%Y-%m-%d')
        new_est_deliver_time_date_time_object_date = est_deliver_time_date_time_object.strftime("%m-%d-%Y")
        print("--------------------------est-new date : ", new_est_deliver_time_date_time_object_date)
        print("------------------------est type of new date : ",type(new_est_deliver_time_date_time_object_date))

        est_deliver_time_today_raw = (((lead_time_weeks_to_days + buffer_time_weeks_to_days) - delta_object_today)/(lead_time_weeks_to_days + buffer_time_weeks_to_days))*100
        est_deliver_time_today = round((((lead_time_weeks_to_days + buffer_time_weeks_to_days) - delta_object_today)/(lead_time_weeks_to_days + buffer_time_weeks_to_days))*100)

        WFOrderInfo["est_deliver_time"] = new_est_deliver_time_date_time_object_date
        WFOrderInfo["lead_time_parameter"] = ""
        WFOrderInfo["buffer_time_parameter"] = ""
        WFOrderInfo["progress_timeline"] = ""
        WFOrderInfo['progress_stage_number'] = ""
        WFOrderInfo['last_activity'] = ""
        WFOrderInfo['order_completion_date'] = ""
        WFOrderInfo["preference_reply_back"] = "Email N SMS"

        wkflw_id = WFOrderInfo["work_flow_id"]

        wrk_flw_cur = DOL_DB.get_workflow_data_by_one_wrkflw_id(wkflw_id)
        for r in wrk_flw_cur:
            work_flow_list.append(r['work_flow_name'])
            work_flow_request_for_automated_reviews_list.append(r['request_automated_reviews'])
            work_flow_stages_list.append(r['work_flow_stages'])

        for l in work_flow_list:
            WFOrderInfo["work_flow_name"] = l

        for lis in work_flow_stages_list:
            WFOrderInfo["work_flow_stages"] = lis
            WFOrderInfo["final_work_flow_stages"] = lis[-1]

        for q in work_flow_request_for_automated_reviews_list:
            WFOrderInfo["request_automated_reviews"] = q
        
        
        WFOrderInfo["order_notes"] = data_row[i][column_names_list.index('NOTES')].strip()
        WFOrderInfo["data_source"] = "Excel Upload"

        mobile_num = WFOrderInfo["consumer_mobile_number"]
        e_mail = WFOrderInfo["consumer_email"]
        nx_id = WFOrderInfo['nexus_id']

        cstm_msg_cursor = DOL_DB.get_custom_order_related_texts()
        for cst in cstm_msg_cursor:
            cstm_type_list.append(cst['custom_message_type'])
        print("----------------------Custom Type-----------------------------------------------")
        print(cstm_type_list)

        consumer_cursor = DOL_DB.get_consumer_data_by_phone(mobile_num)
        for c in consumer_cursor:
            consumer_info_list.append(c)
        print("---------------------------------------------consumer_info_list")
        print("Consumer Database------------ : ",consumer_info_list)

        if consumer_info_list:
            consumer_cred_cur = DOL_DB.get_consumer_cred_by_ph_num(mobile_num)
            
            for cr in consumer_cred_cur:
                consumer_cred_list.append(cr)
            print(consumer_cred_list)

            if consumer_cred_list:
                print("User Exist--------------------")

            else:
                print("Only Consumer creds does not exits")
                consumer_user_id = generate_id(6,4)
                print("==================================nexus_consumer_id : ", consumer_user_id)

                password_Un = generate_id(4,2)
                print('--------------------------password_Un : ', password_Un)
                password_Encrypt = sha_encryption(password_Un)
                currentDT = datetime.today()
                date_time = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")

                new_password_Un = sensitive_wordsOrc.setWFpass_words(password_Un)
                print("======================new_password_Un: ",new_password_Un)

                conInfo["org_name"]="Consumer".strip()
                conInfo["first_name"]=WFOrderInfo["consumer_first_name"].strip()
                conInfo["last_name"]=WFOrderInfo["consumer_last_name"].strip()
                conInfo["user_contact"]=WFOrderInfo["consumer_mobile_number"].strip()
                conInfo["email"]=WFOrderInfo["consumer_email"].strip()
                conInfo["user_type"]="Consumer".strip()
                conInfo["user_id"] = consumer_user_id.strip()
                conInfo["password"]=password_Encrypt.strip()
                conInfo["created_date"] = date_time.strip()

                print(conInfo)
                DOL_DB.save_consumer_credentials(conInfo)

                password = new_password_Un
                phone = conInfo['user_contact']
                user_id = conInfo['user_id']
                first_name = conInfo["first_name"]
                org_name = conInfo["org_name"]
                email = conInfo["email"]

                new_password_Un = sensitive_wordsOrc.setWFpass_words(password_Un)
                print("======================new_password_Un: ",new_password_Un)

                if cstm_type_list:
                    for typ in cstm_type_list:

                        if typ == "Welcome Note Change":
                            print("=====================================TRUE")
                            
                            typ_cursor = DOL_DB.get_custom_order_related_texts_by_type(typ)
                            for t in typ_cursor:
                                welcome_type_list.append(t)
                            print("-------------------------------------------------------",welcome_type_list)
                            print(welcome_type_list)

                    
                            session['welcome_msg_sms'] = welcome_type_list[0]['create_order_text_box_1']

                            text_message_1 = session['welcome_msg_sms'] + config['consumer_portal_url']['CUST_URL']

                            print("------------------------------------------------------------text_message_1")
                            print(text_message_1)

                        if  typ == "Welcome Note Change Email":
                            print("===================EMAIL==================TRUE")
                            typ_cursor_email = DOL_DB.get_custom_order_related_texts_by_type(typ)
                            for t in typ_cursor_email:
                                welcome_type_list_email.append(t)
                            print("-----------------------------------------welcome_type_list_email--------------")
                            print(welcome_type_list_email)

                            session['welcome_sub_email'] = welcome_type_list_email[0]['create_order_text_box_1']
                            session['welcome_msg_email'] = welcome_type_list_email[0]['create_order_text_box_2']


                            text_message_2 = session['welcome_sub_email'] + session['welcome_msg_email'] + config['consumer_portal_url']['CUST_URL']
                            print("text_message_2-----------------------------------------------------------------text_message_2")
                            print(text_message_2)

                    communication_log_id = generate_id(4,2)
                    currentDT = datetime.today()
                    current_log_datetime = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")

                    communication_Info['communication_log_id'] = communication_log_id.strip()
                    communication_Info['nexus_id'] = WFOrderInfo['nexus_id'].strip()
                    communication_Info['po_number'] = WFOrderInfo['po_number'].strip()
                    communication_Info['logger_id'] = session['orgId_retailer']
                    communication_Info['logger_name'] = session['fullname_retailer']
                    communication_Info['logger_type'] = "Dealer".strip()
                    communication_Info['subject'] = "Welcome Note SMS"
                    communication_Info['sending_mode'] = "SMS".strip()
                    communication_Info['message_plain_text'] = text_message_1
                    communication_Info['current_log_datetime'] = current_log_datetime.strip()
                    communication_Info['action_taken'] = "".strip()

                    communication_Info_Email['communication_log_id'] = communication_log_id.strip()
                    communication_Info_Email['nexus_id'] = WFOrderInfo['nexus_id'].strip()
                    communication_Info_Email['po_number'] = WFOrderInfo['po_number'].strip()
                    communication_Info_Email['logger_id'] = session['orgId_retailer']
                    communication_Info_Email['logger_name'] = session['fullname_retailer']
                    communication_Info_Email['logger_type'] = "Dealer".strip()
                    communication_Info_Email['subject'] = session['welcome_sub_email']
                    communication_Info_Email['sending_mode'] = "Email".strip()
                    communication_Info_Email['message_plain_text'] = text_message_2
                    communication_Info_Email['current_log_datetime'] = current_log_datetime.strip()
                    communication_Info_Email['action_taken'] = "".strip()

                    if consumer_info_list[0]['welcome_email']==True and order_status == "Open":

                        if consumer_info_list[0]['receive_sms_notification']==True and consumer_info_list[0]['receive_mail_notification']==False:
                            print("Sms true")
                            sendSms.send_consumer_welcome_note_by_msg(phone,communication_Info)
                        elif consumer_info_list[0]['receive_mail_notification']==True and consumer_info_list[0]['receive_sms_notification']==False:
                            print("Emal true")
                            sendMail.send_consumer_welcome_note_by_mail(email,communication_Info_Email)
                        
                        elif consumer_info_list[0]['receive_mail_notification']==True and consumer_info_list[0]['receive_sms_notification']==True:
                            print("Both true")
                            sendSms.send_consumer_welcome_note_by_msg(phone,communication_Info)
                            sendMail.send_consumer_welcome_note_by_mail(email,communication_Info_Email)
                        else:
                            print("No action")
                   

                        if consumer_info_list[0]['receive_sms_notification']==True and consumer_info_list[0]['receive_mail_notification']==False:
                            print("Sms true")
                            sendSms.send_consumer_creds_by_msg(password,phone,user_id,first_name,org_name)
                        elif consumer_info_list[0]['receive_mail_notification']==True and consumer_info_list[0]['receive_sms_notification']==False:
                            print("Emal true")
                            sendMail.send_consumer_creds_by_mail(password,phone,email,user_id,first_name,org_name)
                        
                        elif consumer_info_list[0]['receive_mail_notification']==True and consumer_info_list[0]['receive_sms_notification']==True:
                            print("Both true")
                            sendSms.send_consumer_creds_by_msg(password,phone,user_id,first_name,org_name)
                            sendMail.send_consumer_creds_by_mail(password,phone,email,user_id,first_name,org_name)
                        else:
                            print("No action")
                    else:
                        print("No welcome message, no email, no credentials")
                        pass
        
        else:
            consumer_cred_cur = DOL_DB.get_consumer_cred_by_ph_num(mobile_num)
            for cr in consumer_cred_cur:
                consumer_cred_list.append(cr)
            print(consumer_cred_list)

            currentDT = datetime.today()
            current_welcome_datetime = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")
            welcome_datetime = current_welcome_datetime
            cons_datetime = current_welcome_datetime

            if consumer_cred_list:
                print("Consuemr exits!!! No creds")
                consumer_info['consumer_id'] = WFOrderInfo['relationship_number']
                consumer_info['consumer_first_name'] = WFOrderInfo['consumer_first_name']
                consumer_info['consumer_last_name'] = WFOrderInfo['consumer_last_name'].strip()
                consumer_info['consumer_mobile_number'] = WFOrderInfo['consumer_mobile_number'].strip()
                consumer_info['consumer_email'] = WFOrderInfo['consumer_email'].strip()
                consumer_info['consumer_date_of_birth'] = "".strip()
                consumer_info['consumer_address'] = WFOrderInfo['address'].strip()
                consumer_info['consumer_city'] = WFOrderInfo['city'].strip()
                consumer_info['consumer_country'] = WFOrderInfo['country'].strip()
                state = WFOrderInfo['state'].split('- ')
                print("-----------------------------state : ",state)
                consumer_info['consumer_state'] = state[0].strip()
                consumer_info['consumer_zip_code'] = WFOrderInfo["consumer_zip_code"].strip()
                consumer_info['user_type'] = WFOrderInfo['user_type'].strip()
                consumer_info['welcome_email'] = True
                consumer_info['welcome_email_datetime'] = welcome_datetime
                consumer_info['consumer_origin'] = "Bulk Order Entry"
                consumer_info['receive_mail_notification'] = True
                consumer_info['receive_sms_notification'] = True
                consumer_info['excel_upload'] = "Excel"
                consumer_info['receive_mail_notification'] = True
                consumer_info['receive_sms_notification'] = True
                consumer_info['consumer_datetime'] = cons_datetime
                
                DOL_DB.save_consumer_informaton(consumer_info)

            else:
                consumer_info['consumer_id'] = WFOrderInfo['relationship_number']
                consumer_info['consumer_first_name'] = WFOrderInfo['consumer_first_name']
                consumer_info['consumer_last_name'] = WFOrderInfo['consumer_last_name'].strip()
                consumer_info['consumer_mobile_number'] = WFOrderInfo['consumer_mobile_number'].strip()
                consumer_info['consumer_email'] = WFOrderInfo['consumer_email'].strip()
                consumer_info['consumer_date_of_birth'] = "".strip()
                consumer_info['consumer_address'] = WFOrderInfo['address'].strip()
                consumer_info['consumer_city'] = WFOrderInfo['city'].strip()
                consumer_info['consumer_country'] = WFOrderInfo['country'].strip()
                state = WFOrderInfo['state'].split('- ')
                print("-----------------------------state : ",state)
                consumer_info['consumer_state'] = state[0].strip()
                consumer_info['consumer_zip_code'] = WFOrderInfo["consumer_zip_code"].strip()
                consumer_info['user_type'] = WFOrderInfo['user_type'].strip()
                consumer_info['welcome_email'] = True
                consumer_info['welcome_email_datetime'] = welcome_datetime
                consumer_info['consumer_origin'] = "Bulk Order Entry"
                consumer_info['receive_mail_notification'] = True
                consumer_info['receive_sms_notification'] = True
                consumer_info['excel_upload'] = "Excel"
                consumer_info['receive_mail_notification'] = True
                consumer_info['receive_sms_notification'] = True
                consumer_info['consumer_datetime'] = cons_datetime
                
                DOL_DB.save_consumer_informaton(consumer_info)

                consumer_user_id = generate_id(6,4)
                print("==================================nexus_consumer_id : ", consumer_user_id)

                password_Un = generate_id(4,2)
                print('--------------------------password_Un : ', password_Un)
                password_Encrypt = sha_encryption(password_Un)
                currentDT = datetime.today()
                date_time = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")

                new_password_Un = sensitive_wordsOrc.setWFpass_words(password_Un)
                print("======================new_password_Un: ",new_password_Un)

                conInfo["org_name"]="Consumer".strip()
                conInfo["first_name"]=WFOrderInfo["consumer_first_name"].strip().strip()
                conInfo["last_name"]=WFOrderInfo["consumer_last_name"].strip().strip()
                conInfo["user_contact"]=WFOrderInfo["consumer_mobile_number"].strip().strip()
                conInfo["email"]=WFOrderInfo["consumer_email"].strip().strip()
                conInfo["user_type"]="Consumer".strip()
                conInfo["user_id"] = consumer_user_id.strip()
                conInfo["password"]=password_Encrypt.strip()
                conInfo["created_date"] = date_time.strip()

                print(conInfo)
                DOL_DB.save_consumer_credentials(conInfo)

                password = new_password_Un
                phone = conInfo['user_contact']
                user_id = conInfo['user_id']
                first_name = conInfo["first_name"]
                org_name = conInfo["org_name"]
                email = conInfo["email"]

                if cstm_type_list:
                    for typ in cstm_type_list:

                        if typ == "Welcome Note Change":
                            print("===================Welcome note sms==================TRUE")
                            
                            typ_cursor = DOL_DB.get_custom_order_related_texts_by_type(typ)
                            for t in typ_cursor:
                                welcome_type_list.append(t)
                            print("-------------------------------------------------------",welcome_type_list)
                            print(welcome_type_list)

                    
                            session['welcome_msg_sms'] = welcome_type_list[0]['create_order_text_box_1']

                            text_message_1 = session['welcome_msg_sms'] + config['consumer_portal_url']['CUST_URL']

                            print("------------------------------------------------------------text_message_1")
                            print(text_message_1)

                        if  typ == "Welcome Note Change Email":
                            print("===================EMAIL==================TRUE")
                            typ_cursor_email = DOL_DB.get_custom_order_related_texts_by_type(typ)
                            for t in typ_cursor_email:
                                welcome_type_list_email.append(t)
                            print("-----------------------------------------welcome_type_list_email--------------")
                            print(welcome_type_list_email)

                            session['welcome_sub_email'] = welcome_type_list_email[0]['create_order_text_box_1']
                            session['welcome_msg_email'] = welcome_type_list_email[0]['create_order_text_box_2']


                            text_message_2 = session['welcome_sub_email'] + session['welcome_msg_email'] + config['consumer_portal_url']['CUST_URL']

                            print("text_message_2-----------------------------------------------------------------text_message_2")
                            print(text_message_2)

                    communication_log_id = generate_id(4,2)
                    currentDT = datetime.today()
                    current_log_datetime = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")

                    communication_Info['communication_log_id'] = communication_log_id.strip()
                    communication_Info['nexus_id'] = WFOrderInfo['nexus_id'].strip()
                    communication_Info['po_number'] = WFOrderInfo['po_number'].strip()
                    communication_Info['logger_id'] = session['orgId_retailer']
                    communication_Info['logger_name'] = session['fullname_retailer']
                    communication_Info['logger_type'] = "Dealer".strip()
                    communication_Info['subject'] = "Welcome Note SMS"
                    communication_Info['sending_mode'] = "SMS".strip()
                    communication_Info['message_plain_text'] = text_message_1
                    communication_Info['current_log_datetime'] = current_log_datetime.strip()
                    communication_Info['action_taken'] = "".strip()

                    communication_Info_Email['communication_log_id'] = communication_log_id.strip()
                    communication_Info_Email['nexus_id'] = WFOrderInfo['nexus_id'].strip()
                    communication_Info_Email['po_number'] = WFOrderInfo['po_number'].strip()
                    communication_Info_Email['logger_id'] = session['orgId_retailer']
                    communication_Info_Email['logger_name'] = session['fullname_retailer']
                    communication_Info_Email['logger_type'] = "Dealer".strip()
                    communication_Info_Email['subject'] = session['welcome_sub_email']
                    communication_Info_Email['sending_mode'] = "Email".strip()
                    communication_Info_Email['message_plain_text'] = text_message_2
                    communication_Info_Email['current_log_datetime'] = current_log_datetime.strip()
                    communication_Info_Email['action_taken'] = "".strip()

                    #sendSms.send_consumer_welcome_note_by_msg(phone,communication_Info)
                    sendMail.send_consumer_welcome_note_by_mail(email,communication_Info_Email)
                
                sendSms.send_consumer_creds_by_msg(password,phone,user_id,first_name,org_name)
                sendMail.send_consumer_creds_by_mail(password,phone,email,user_id,first_name,org_name)

        con_po_cursor = DOL_DB.get_po_phone_matrix_details(mobile_num)
        for c in con_po_cursor:
            consumer_nid_list.append(c)
        print(consumer_nid_list)

        if consumer_nid_list:
            print('exist')
            print("-----------------------------nex_id_list")
            if session['orgId_retailer'] in consumer_nid_list[0]:
                nex_id_list = consumer_nid_list[0][session['orgId_retailer']]

                if nx_id in nex_id_list:
                    pass
                else:
                    print(nex_id_list)
                    dealer_dics = {}
                    nex_id_list.append(nx_id)
                    dealer_dics[session['orgId_retailer']] = nex_id_list
                    print("===================else===============nex_id_list")
                    print(nex_id_list)
                    DOL_DB.update_dealer_po_list(mobile_num,dealer_dics)

            else:
                dealer_dics = {}
                nex_id_list.append(nx_id)
                dealer_dics[session['orgId_retailer']] = nex_id_list
                print('=============================dealer_dics')
                print(dealer_dics)
                DOL_DB.update_dealer_po_list(mobile_num,dealer_dics)
        else:
            print("=========================else new------------------")
            consumer_po_dict['consumer_mobile_number'] = mobile_num
            consumer_po_dict['country'] = WFOrderInfo['country']
            consumer_po_dict[session['orgId_retailer']] = [nx_id]
            DOL_DB.save_consumer_po_data(consumer_po_dict)
            #consumer_po_dict = {}

           
        DOL_DB.save_wforder_details(WFOrderInfo)

        cstm_msg_cursor = DOL_DB.get_custom_order_related_texts()
        for cst in cstm_msg_cursor:
            cstm_type_list.append(cst['custom_message_type'])
        print("----------------------Custom Type-----------------------------------------------")
        print(cstm_type_list)

        if cstm_type_list:
            for typ in cstm_type_list:

                if typ == "Order Entry":
                    print("=====================================TRUE")
                    
                    typ_cursor = DOL_DB.get_custom_order_related_texts_by_type(typ)
                    for t in typ_cursor:
                        type_list.append(t)
                    print("-------------------------------------------------------",type_list)
                    print(type_list)

            
                    session['sub_1'] = type_list[0]['create_order_text_box_1']
                    session['salutaion_1'] = type_list[0]['create_order_text_box_2']
                    session['text_body_1'] = type_list[0]['create_order_text_box_3']
                    session['conclusion_1'] = type_list[0]['create_order_text_box_4']

                    text_message_1 = session['sub_1'] + WFOrderInfo['nexus_id'] + session['salutaion_1'] + WFOrderInfo['est_deliver_time'] + session['text_body_1'] + config['consumer_portal_url']['CUST_URL'] + session['conclusion_1']

                    print("------------------------------------------------------------text_message_1")
                    print(text_message_1)

                if  typ == "Order Entry Email":
                    print("===================EMAIL==================TRUE")
                    typ_cursor_email = DOL_DB.get_custom_order_related_texts_by_type(typ)
                    for t in typ_cursor_email:
                        type_list_email.append(t)
                    print("-----------------------------------------type_list_email--------------")
                    print(type_list_email)

                    session['sub_2'] = type_list_email[0]['create_order_text_box_1']
                    session['salutaion_2'] = type_list_email[0]['create_order_text_box_2']
                    session['text_body_2'] = type_list_email[0]['create_order_text_box_3']
                    session['conclusion_2'] = type_list_email[0]['create_order_text_box_4']


                    text_message_2 = session['salutaion_2'] + WFOrderInfo['nexus_id'] + session['text_body_2'] + WFOrderInfo['est_deliver_time'] + session['conclusion_2'] + config['consumer_portal_url']['CUST_URL']
                    print("text_message_2-----------------------------------------------------------------text_message_2")
                    print(text_message_2)

            communication_log_id = generate_id(4,2)
            currentDT = datetime.today()
            current_log_datetime = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")

            communication_Info['communication_log_id'] = communication_log_id.strip()
            communication_Info['nexus_id'] = WFOrderInfo['nexus_id'].strip()
            communication_Info['po_number'] = WFOrderInfo['po_number'].strip()
            communication_Info['logger_id'] = session['orgId_retailer']
            communication_Info['logger_name'] = session['fullname_retailer']
            communication_Info['logger_type'] = "Dealer".strip()
            communication_Info['subject'] = session['sub_1']
            communication_Info['sending_mode'] = "SMS".strip()
            communication_Info['message_plain_text'] = text_message_1
            communication_Info['current_log_datetime'] = current_log_datetime.strip()
            communication_Info['action_taken'] = "".strip()


            communication_Info_Email['communication_log_id'] = communication_log_id.strip()
            communication_Info_Email['nexus_id'] = WFOrderInfo['nexus_id'].strip()
            communication_Info_Email['po_number'] = WFOrderInfo['po_number'].strip()
            communication_Info_Email['logger_id'] = session['orgId_retailer']
            communication_Info_Email['logger_name'] = session['fullname_retailer']
            communication_Info_Email['logger_type'] = "Dealer".strip()
            communication_Info_Email['subject'] = session['sub_2']
            communication_Info_Email['sending_mode'] = "Email".strip()
            communication_Info_Email['message_plain_text'] = text_message_2
            communication_Info_Email['current_log_datetime'] = current_log_datetime.strip()
            communication_Info_Email['action_taken'] = "".strip()

            consumer_cursor = DOL_DB.get_consumer_data_by_phone(mobile_num)
            for c in consumer_cursor:
                consumer_info_list_after_save.append(c)
            print("---------------------------------------------consumer_info_list_after_save")
            print("Consumer Database------------ : ",consumer_info_list_after_save)

            if consumer_info_list_after_save:
                if consumer_info_list_after_save[0]['receive_sms_notification']==True and consumer_info_list_after_save[0]['receive_mail_notification']==False:
                    print("SMS True")
                    sendSms.send_order_entry_log_msg(mobile_num,communication_Info)
                    DOL_DB.save_communication_logs(communication_Info)

                elif consumer_info_list_after_save[0]['receive_mail_notification']==True and consumer_info_list_after_save[0]['receive_sms_notification']==False:
                    print("Email True")
                    sendMail.send_order_entry_to_mail(e_mail,communication_Info_Email)
                    DOL_DB.save_communication_logs(communication_Info_Email)

                elif consumer_info_list_after_save[0]['receive_mail_notification']==True and consumer_info_list_after_save[0]['receive_sms_notification']==True:
                    print("Both True")
                    sendSms.send_order_entry_log_msg(mobile_num,communication_Info)
                    DOL_DB.save_communication_logs(communication_Info)
                    sendMail.send_order_entry_to_mail(e_mail,communication_Info_Email)
                    DOL_DB.save_communication_logs(communication_Info_Email)
                else:
                    print("No action")

            else:
                print("consumer does not exit both send")
                sendSms.send_order_entry_log_msg(mobile_num,communication_Info)
                DOL_DB.save_communication_logs(communication_Info)
                sendMail.send_order_entry_to_mail(e_mail,communication_Info_Email)
                DOL_DB.save_communication_logs(communication_Info_Email)


        currentDT = datetime.today()
        current_datetime_for_last_activity = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")

        last_acti_cur = DOL_DB.get_one_wforder_detail(WFOrderInfo['nexus_id'])
        for la in last_acti_cur:
            last_acti_list.append(la)

        last_activity = last_acti_list[0]['last_activity']

        print("==================================================")
        print(last_activity)
        print("==================================================")

        last_activity = current_datetime_for_last_activity
        print(last_activity)

        DOL_DB.update_last_activity_of_an_order_change(WFOrderInfo['nexus_id'],last_activity)

        WFOrderInfo = {}
        communication_Info = {}
        communication_Info_Email = {}
        last_acti_list = []

    return redirect(url_for('WF_orderWrapper'))

#======================================================Activities DATA====================================================
@app.route("/activity_log", methods=['GET'])
@login_required
def activityLogWrapper():
    print("========================================inside activity log wrapper")
    log_recs = []
    nex_id_list = []
    consumer_info = []
    progress_timeline_list = []
    workflw_stages_list = []
    
    progress_stage_number = 0
    cons_info_cur = ''
    workflw_stages = ''
    progress_timeline = ''

    now = datetime.today()
    print("=============now: ",now)
    new_date = []
    d = now.strftime("%Y, %b, %d")
    print(d)
    new_date = d.split(',')
    print(new_date)
    year = new_date[0].strip()
    month = new_date[1].strip()
    to_date = new_date[2].strip()
    

    log_cur = DOL_DB.get_all_logs_of_consumer_type(year,month,to_date)
    for l in log_cur:
        log_recs.append(l)
        nex_id_list.append(l['nexus_id'])

    print(log_recs)
    print("=================================================================")
    print(nex_id_list)

    for nid in nex_id_list:
        cons_info_cur = DOL_DB.get_consumer_details_from_wforder_detail(nid)

    for cn in cons_info_cur:
        consumer_info.append(cn)
        progress_timeline_list.append(cn['progress_timeline'])
        workflw_stages_list.append(cn['work_flow_stages'])
    print(consumer_info)

    # if progress_timeline_list:
    #     for pg,wfl in (progress_timeline_list,workflw_stages_list):
    #         progress_stage_number = wfl.index(pg)

    if consumer_info:
        progress_timeline = consumer_info[0]['progress_timeline']
        print(progress_timeline)

        workflw_stages = consumer_info[0]['work_flow_stages']

    if progress_timeline:
        progress_stage_number = workflw_stages.index(progress_timeline)

    return render_template('activity_logForm.html',
                            log_recs = log_recs,
                            consumer_info = consumer_info,
                            wfl_stages = workflw_stages,
                            progress_stage_number = progress_stage_number,
                            all_logs_cons_info = zip(log_recs,consumer_info),
                            user = session['username_retailer'],
                            org = session['org_retailer'])

@app.route("/save_action_taken_field/<nid>", methods=['POST'])
@login_required
def save_action_taken_for_a_log(nid):
    act_disc = {}
    communication_log_id = generate_id(4,2)
    currentDT = datetime.today()
    current_act_datetime = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")
    
    action_taken = request.form.get('act_taken')
    print("================: ",action_taken)

    if action_taken == "Yes":
        print("inside if")
        action_taken = current_act_datetime
        act_disc['action_taken'] = action_taken
        DOL_DB.update_action_taken_value_for_a_consumer(act_disc,nid)
    return redirect(url_for('activityLogWrapper'))


#========================================================================================================================
@app.route("/activity_4log", methods=['GET'])
@login_required
def activityFourLogWrapper():
    print("========================================inside activity 4 log wrapper")
    log_recs = []
    nex_id_list = []
    consumer_info = []
    progress_timeline_list = []
    workflw_stages_list = []

    progress_stage_number = 0
    cons_info_cur = ''
    workflw_stages = ''
    progress_timeline = ''

    today_date = datetime.today()
    print("=============now: ",today_date)

    new_date_today = []
    d_today = today_date.strftime("%Y, %b, %d")
    print(d_today)
    new_date_today = d_today.split(',')
    print(new_date_today)
    year = new_date_today[0].strip()
    month = new_date_today[1].strip()
    to_date = new_date_today[2].strip()

    yesterday = today_date - timedelta(days = 1)
    print("=============yesterday: ",yesterday)

    new_date_yesterday = []
    d_yesterday = yesterday.strftime("%Y, %b, %d")
    print(d_yesterday)
    new_date_yesterday = d_yesterday.split(',')
    print(new_date_yesterday)
    yest_date = new_date_yesterday[2].strip()

    day_before_yesterday = today_date - timedelta(days = 2)
    print("=============day_before_yesterday: ",day_before_yesterday)

    new_date_day_before_yesterday = []
    d_day_before_yesterday = day_before_yesterday.strftime("%Y, %b, %d")
    print(d_day_before_yesterday)
    new_date_day_before_yesterday = d_day_before_yesterday.split(',')
    print(new_date_day_before_yesterday)
    day_before_yest_date = new_date_day_before_yesterday[2].strip()

    day_bfr_bfr_yesterday = today_date - timedelta(days = 2)
    print("=============day_bfr_bfr_yesterday: ",day_bfr_bfr_yesterday)

    new_date_day_bfr_before_yesterday = []
    d_day_bfr_before_yesterday = day_bfr_bfr_yesterday.strftime("%Y, %b, %d")
    print(d_day_bfr_before_yesterday)
    new_date_day_bfr_before_yesterday = d_day_bfr_before_yesterday.split(',')
    print(new_date_day_bfr_before_yesterday)
    day_bfr_before_yest_date = new_date_day_bfr_before_yesterday[2].strip()



    log_cur = DOL_DB.get_all_logs_of_consumer_type_for_4_days(year,month,to_date,yest_date,day_before_yest_date,day_bfr_before_yest_date)
    for l in log_cur:
        log_recs.append(l)
        nex_id_list.append(l['nexus_id'])

    print(log_recs)
    print("=================================================================")
    print(nex_id_list)

    for nid in nex_id_list:
        cons_info_cur = DOL_DB.get_consumer_details_from_wforder_detail(nid)

    for cn in cons_info_cur:
        consumer_info.append(cn)
        progress_timeline_list.append(cn['progress_timeline'])
        workflw_stages_list.append(cn['work_flow_stages'])
    print(consumer_info)

    # if progress_timeline_list:
    #     for pg,wfl in zip(progress_timeline_list,workflw_stages_list):
    #         progress_stage_number = wfl.index(pg)

    if consumer_info:
        progress_timeline = consumer_info[0]['progress_timeline']
        print(progress_timeline)

        workflw_stages = consumer_info[0]['work_flow_stages']

    if progress_timeline:
        progress_stage_number = workflw_stages.index(progress_timeline)
    return render_template('activity_4logForm.html',
                            log_recs = log_recs,
                            consumer_info = consumer_info,
                            wfl_stages = workflw_stages,
                            progress_stage_number = progress_stage_number,
                            all_logs_cons_info = zip(log_recs,consumer_info),
                            user = session['username_retailer'],
                            org = session['org_retailer'])

@app.route("/save_4action_taken_field/<nid>", methods=['POST'])
@login_required
def save_four_action_taken_for_a_log(nid):
    act_disc = {}
    communication_log_id = generate_id(4,2)
    currentDT = datetime.today()
    current_act_datetime = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")
    
    action_taken = request.form.get('act_4taken')
    print("================: ",action_taken)

    if action_taken == "Yes":
        print("inside if")
        action_taken = current_act_datetime
        act_disc['action_taken'] = action_taken
        DOL_DB.update_action_taken_value_for_a_consumer(act_disc,nid)
    return redirect(url_for('activityLogWrapper'))


#================================================================================================================
@app.route("/activity_7log", methods=['GET'])
@login_required
def activitySevenLogWrapper():
    print("========================================inside activity 7 log wrapper")
    log_recs = []
    nex_id_list = []
    consumer_info = []
    progress_timeline_list = []
    workflw_stages_list = []

    progress_stage_number = 0
    cons_info_cur = ''
    workflw_stages = ''
    progress_timeline = ''

    today_date = datetime.today()
    print("=============now: ",today_date)

    new_date_today = []
    d_today = today_date.strftime("%Y, %b, %d")
    print(d_today)
    new_date_today = d_today.split(',')
    print(new_date_today)
    year = new_date_today[0].strip()
    month = new_date_today[1].strip()
    to_date = new_date_today[2].strip()

    yesterday = today_date - timedelta(days = 1)
    print("=============yesterday: ",yesterday)

    new_date_yesterday = []
    d_yesterday = yesterday.strftime("%Y, %b, %d")
    print(d_yesterday)
    new_date_yesterday = d_yesterday.split(',')
    print(new_date_yesterday)
    yest_date = new_date_yesterday[2].strip()

    day_before_yesterday = today_date - timedelta(days = 2)
    print("=============day_before_yesterday: ",day_before_yesterday)

    new_date_day_before_yesterday = []
    d_day_before_yesterday = day_before_yesterday.strftime("%Y, %b, %d")
    print(d_day_before_yesterday)
    new_date_day_before_yesterday = d_day_before_yesterday.split(',')
    print(new_date_day_before_yesterday)
    day_before_yest_date = new_date_day_before_yesterday[2].strip()

    day_bfr_bfr_yesterday = today_date - timedelta(days = 2)
    print("=============day_bfr_bfr_yesterday: ",day_bfr_bfr_yesterday)

    new_date_day_bfr_before_yesterday = []
    d_day_bfr_before_yesterday = day_bfr_bfr_yesterday.strftime("%Y, %b, %d")
    print(d_day_bfr_before_yesterday)
    new_date_day_bfr_before_yesterday = d_day_bfr_before_yesterday.split(',')
    print(new_date_day_bfr_before_yesterday)
    day_bfr_before_yest_date = new_date_day_bfr_before_yesterday[2].strip()


    day_5_bfr_yesterday = today_date - timedelta(days = 3)
    print("=============day_5_bfr_yesterday: ",day_5_bfr_yesterday)

    new_date_day_5_before_yesterday = []
    d_day_5_before_yesterday = day_5_bfr_yesterday.strftime("%Y, %b, %d")
    print(d_day_5_before_yesterday)
    new_date_day_5_before_yesterday = d_day_5_before_yesterday.split(',')
    print(new_date_day_5_before_yesterday)
    day_5_before_yest_date = new_date_day_5_before_yesterday[2].strip()


    day_6_bfr_yesterday = today_date - timedelta(days = 4)
    print("=============day_6_bfr_yesterday: ",day_6_bfr_yesterday)

    new_date_day_6_before_yesterday = []
    d_day_6_before_yesterday = day_6_bfr_yesterday.strftime("%Y, %b, %d")
    print(d_day_6_before_yesterday)
    new_date_day_6_before_yesterday = d_day_6_before_yesterday.split(',')
    print(new_date_day_6_before_yesterday)
    day_6_before_yest_date = new_date_day_6_before_yesterday[2].strip()


    day_7_bfr_yesterday = today_date - timedelta(days = 5)
    print("=============day_7_bfr_yesterday: ",day_7_bfr_yesterday)

    new_date_day_7_before_yesterday = []
    d_day_7_before_yesterday = day_7_bfr_yesterday.strftime("%Y, %b, %d")
    print(d_day_7_before_yesterday)
    new_date_day_7_before_yesterday = d_day_7_before_yesterday.split(',')
    print(new_date_day_7_before_yesterday)
    day_7_before_yest_date = new_date_day_7_before_yesterday[2].strip()



    log_cur = DOL_DB.get_all_logs_of_consumer_type_for_7_days(year,month,to_date,yest_date,day_before_yest_date,day_bfr_before_yest_date,day_5_before_yest_date,day_6_before_yest_date,day_7_before_yest_date)
    for l in log_cur:
        log_recs.append(l)
        nex_id_list.append(l['nexus_id'])

    print(log_recs)
    print("=================================================================")
    print(nex_id_list)

    for nid in nex_id_list:
        cons_info_cur = DOL_DB.get_consumer_details_from_wforder_detail(nid)

    for cn in cons_info_cur:
        consumer_info.append(cn)
        progress_timeline_list.append(cn['progress_timeline'])
        workflw_stages_list.append(cn['work_flow_stages'])
    print(consumer_info)

    # if progress_timeline_list:
    #     for pg,wfl in (progress_timeline_list,workflw_stages_list):
    #         progress_stage_number = wfl.index(pg)

    if consumer_info:
        progress_timeline = consumer_info[0]['progress_timeline']
        print(progress_timeline)

        workflw_stages = consumer_info[0]['work_flow_stages']

    if progress_timeline:
        progress_stage_number = workflw_stages.index(progress_timeline)
    return render_template('activity_4logForm.html',
                            log_recs = log_recs,
                            consumer_info = consumer_info,
                            wfl_stages = workflw_stages,
                            progress_stage_number = progress_stage_number,
                            all_logs_cons_info = zip(log_recs,consumer_info),
                            user = session['username_retailer'],
                            org = session['org_retailer'])


@app.route("/save_7action_taken_field/<nid>", methods=['POST'])
@login_required
def save_seven_action_taken_for_a_log(nid):
    act_disc = {}
    communication_log_id = generate_id(4,2)
    currentDT = datetime.today()
    current_act_datetime = currentDT.strftime("%Y %b %d %a %I:%M:%S%p")
    
    action_taken = request.form.get('act_4taken')
    print("================: ",action_taken)

    if action_taken == "Yes":
        print("inside if")
        action_taken = current_act_datetime
        act_disc['action_taken'] = action_taken
        DOL_DB.update_action_taken_value_for_a_consumer(act_disc,nid)
    return redirect(url_for('activityLogWrapper'))
#---------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
  app.run(debug=True)
