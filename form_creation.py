from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, BooleanField, TextAreaField, SelectMultipleField,HiddenField,DecimalField
from wtforms.fields.html5 import DateField, EmailField
from wtforms.validators import InputRequired,Length
from flask_wtf.file import FileField, FileRequired
from wtforms import widgets
#from wtforms.widgets import ListWidget,html_params
from werkzeug.utils import secure_filename


import configparser

config = configparser.ConfigParser()
config.read('config.ini')




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
    j_name = StringField('Job Name',validators=[InputRequired()], render_kw={"placeholder": "Job name"})
    co_fname = StringField('First Name',validators=[InputRequired()], render_kw={"placeholder": "First Name/Company"})
    co_lname = StringField('Last Name', render_kw={"placeholder": "Last Name"})
    co_mo_num = IntegerField('Mobile #', validators=[InputRequired()], render_kw={"placeholder": "Mobile number"})
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
    zip_code = StringField('Zipcode',validators=[InputRequired()], render_kw={"placeholder": "Zipcode"})






#=====================================================Excel Uploader=======================================================
class excelFile(FlaskForm):
    excelip = FileField(validators=[FileRequired()])