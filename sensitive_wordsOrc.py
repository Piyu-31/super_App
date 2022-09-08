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


def setWFpass_words(password_Un):
	di_ct = {"A": "Army","B":"Band","C":"Camp","D":"Dawn","E":"Even","F":"Fate","G":"Glad",
	"H":"Help","I":"Iron","J":"John","K":"King","L":"Luck","M":"Mike","N":"Nice","O":"Over",
	"P":"Pack","Q":"Quartz","R":"Rose","S":"Ship","T":"Tale","U":"User","V":"Vase","W":"Week","X":"Xeric","Y":"Year",
	"Z":"Zone","a": "army","b":"band","c":"camp","d":"dawn","e":"even","f":"fate","g":"glad",
	"h":"help","i":"iron","j":"john","k":"king","l":"luck","m":"mike","n":"nice","o":"over",
	"p":"pack","q":"quartz","r":"rose","s":"ship","t":"tale","u":"user","v":"vase","w":"week","x":"xeric","Yy":"Yyar",
	"z":"zone",
	}
	pa_ss = password_Un
	modified_pass = ""

	for p in pa_ss:
	    converted_pass = ""
	    print(p)
	    if p in di_ct:
	        converted_pass = p + "(" + di_ct[p] +")"
	    else:
	        converted_pass = p

	    modified_pass = modified_pass + converted_pass

	print(modified_pass)

	return modified_pass