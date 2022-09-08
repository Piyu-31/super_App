 
from flask import Flask, render_template, request, flash, redirect, url_for, session
import shelve
# <<<<<<< HEAD
from wtforms import Form, StringField, BooleanField,TextAreaField,RadioField, SelectField, validators, PasswordField, DateField, SubmitField, \
 IntegerField, FileField
from wtforms.validators import DataRequired
from datetime import date
import uuid
from wtforms import widgets, SelectMultipleField

app = Flask(__name__)

#this is my form!
 class DoctorAppointment(Form):
   active = BooleanField(True, False)
   
   
@app.route("/doctorbooking")
def doctorbooking():
    doctor_form = DoctorAppointment(request.form)
    if request.method == 'POST' and form.validate():
        check_list = doctor_form.active.data
        doctorappointment = Timeslots(day,check_list)

        db_read = shelve.open("doctorappointment.db")

        try:
            doctorappointmentlist = db_read["doctorappointment"]

        except:
            doctorappointmentlist = {}

        doctorappointmentlist[day] = check_list.data


        db_read.close()


        flash("Appointment added sucessfully!")
        
          return render_template("DoctorBooking.html", title="Doctor Booking",dform = doctor_form)
Return to post