#Create your views here.
from models import *
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from datetime import timedelta, date
import json, urllib, httplib2

import urllib
import httplib2
import json

from sqlalchemy import create_engine
from bs4 import BeautifulSoup

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

def get_zip_from_address(address):
  encoded_address = urllib.quote(address)  
  url = "http://maps.google.com/maps/api/geocode/json?address={0}&sensor=false".format(encoded_address)
  response = do_GET(url)
  geocode_info = json.loads(response)

  if geocode_info['status'] != 'OK':
    print "Status is not OK"
  elif len(geocode_info['results']) == 0:
    print "No results were returned."
  else:
    address_components = geocode_info['results'][0]['address_components']
    for component in address_components:
      if 'postal_code' in component['types']:
        return component['short_name']

def get_county_code_by_address(address):
  zip = get_zip_from_address(address)

  # Probably will want to pass the connection in.
  engine = create_engine('mysql://admin:admin@localhost/watersafe')
  connection = engine.connect()

  result = connection.execute('select fips_county_id from zip_county_mapping where zip={0}'.format(zip).upper())
  counties = [row[0] for row in result]
  result.close()
  return counties[0]

def get_count(county_code):
  # Probably will want to pass the connection in.
  engine = create_engine('mysql://admin:admin@localhost/watersafe')
  connection = engine.connect()

  results = connection.execute('')

  for result in result:
    print result

def get_pws_details_by_county(county_code):
  # Probably will want to pass the connection in.
  engine = create_engine('mysql://admin:admin@localhost/watersafe')
  connection = engine.connect()

  results = connection.execute('')

  for result in result:
    print result

# XXX He's dead, Jim. 
# This site limits us to 30 requests a day, oh well.
# Scrape http://zip-info.com to get county info
def get_county_by_zip(zip):
  url = "http://www.zip-info.com/cgi-local/zipsrch.exe?cnty=cnty&zip={0}&Go=Go".format(zip)
  response = do_GET(url)
  soup = BeautifulSoup(response)

  # There's a handful of tables in the page, the one we care about is the third one.
  results_table_index = 3
  results_table = soup.find_all('table')[results_table_index]

  # 4th column has the county code
  county_column_index = 4
  county_code_tag = results_table.find_all('td')[county_column_index]
  county_code = county_code_tag.contents
  return county_code

def Search(request):
  test_address = "20 N. 3rd St Philadelphia"
  a = get_county_code_by_address(test_address)
  return render_to_response('index.html',{'msg':a})
