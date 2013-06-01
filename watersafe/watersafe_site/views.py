#Create your views here.
from models import *
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from datetime import timedelta, date
import json, urllib, httplib2

http = httplib2.Http()

def do_GET(url):
  body = {}
  headers = {'Content-type': 'application/x-www-form-urlencoded'}
  response, content = http.request(url, 'GET', headers=headers, body=urllib.urlencode(body))
  return content

def get_pws_by_county(county_code):
  url = "http://iaspub.epa.gov/enviro/efservice/PWS_COUNTY/fipscounty/{0}/json".format(county_code)
  response = do_GET(url)
  return json.loads(response)

def get_violations_by_pws(pwsid):
  url = "http://iaspub.epa.gov/enviro/efservice/VIOLATION/PWSID/{0}/json".format(pwsid)
  response = do_GET(url)
  return json.loads(response)

def Search(request):
	philly_county_code = 42101
	water_systems = get_pws_by_county(philly_county_code)
	a = ''

	for water_system in water_systems:
		pwsid = water_system['PWSID']
		violations = get_violations_by_pws(pwsid) 
		a = str(a) + ' ' + str(violations)
	return render_to_response('index.html',{'msg':a})
