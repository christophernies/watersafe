#Create your views here.
from models import *
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from datetime import timedelta, date
import json, urllib, httplib2
from keys import *
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

  query = """
    SELECT PACR.`county_id` county, PACR.`incident_count` incidents, PACR.`rank` rank, PACR.`bucket` bucket
    FROM PA_COUNTY_VIOLATION_RANK PACR
    WHERE county_id = {0} 
  """
  results = connection.execute(query.format(county_code))

  count = [result[2] for result in results]
  return count[0]

def get_pws_details_by_county(county_code):
  # Probably will want to pass the connection in.
  engine = create_engine('mysql://admin:admin@localhost/watersafe')
  connection = engine.connect()

  query = """
    SELECT PWS.`PWS.PWSID` , PWS.`PWS.PWSNAME` , PWS.`PWS.CONTACTCITY` contact_city , PWS.`PWS.PSOURCE_LONGNAME` water_source, PWS.`PWS.RETPOPSRVD` population_served
    , PWS.`PWS.STATUS` pws_status , PAH.`vname` violation_name, PAH.`cname` contaminant, PAH.`viomeasure` violation_measure
    FROM PA_H20_VIOLATION PAH, PWS
    WHERE PAH.`pwsid` = PWS.`PWS.PWSID`
    AND PAH.`Vtype` NOT IN ('MR','Other')
    AND YEAR(PAH.`comp_begin_date`) >= 2012
    AND PAH.`County` = {0} 
  """

  results = connection.execute(query.format(county_code))

  county_list = []
  for result in results:
    county = {}
    county['pwsid'] = result[0]
    county['pws_name'] = result[1]
    county['contact_city'] = result[2]
    county['source_long_name'] = result[3]
    county['population_served'] = result[4]
    county['pws_status'] = result[5]
    county['violation_name'] = result[6]
    county['contaminant'] = result[7]
    county['contaminant_measure'] = result[8]
    county_list.append(county)
  return county_list

def Contact:
    cicero_url = 'https://cicero.azavea.com/v3.1/official?search_address='+address+'&search_country=US&user=watersafe&key='+cicero_api_key


def search_form(request):
  return render_to_response('index.html', context_instance=RequestContext(request))

def Search(request):
  if 'address' in request.GET:
        address = request.GET['address']
  else: address = "20 N. 3rd St Philadelphia"
  county_code = get_county_code_by_address(address)

  return render_to_response('results.html',{'county_id':county_code, 'address':address}, context_instance=RequestContext(request))
