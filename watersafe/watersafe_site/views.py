#Create your views here.
from models import *
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from datetime import timedelta, date
import json, urllib, httplib2
from api_keys import *
from sqlalchemy import create_engine
from bs4 import BeautifulSoup

http = httplib2.Http()

def do_GET(url):
  body = {}
  headers = {'Content-type': 'application/x-www-form-urlencoded'}
  response, content = http.request(url, 'GET', headers=headers, body=urllib.urlencode(body))
  return content

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

def get_county_name_by_zip(zip):
  # Probably will want to pass the connection in.
  engine = create_engine('mysql://admin:admin@localhost/watersafe')
  connection = engine.connect()

  query = """
      SELECT CSM.`COUNTY_NAME`
    FROM COUNTY_STATE_MAPPING CSM, ZIP_COUNTY_MAPPING ZCM
    WHERE CSM.`FIPS_COUNTY_ID` = ZCM.`FIPS_COUNTY_ID`
    AND ZCM.`ZIP` = {0}
  """
  results = connection.execute(query.format(zip))
  county_names = [result[0] for result in results]
  county_name = county_names[0]

  return county_name
def get_ranking_info_by_county(county_code):
  # Probably will want to pass the connection in.
  engine = create_engine('mysql://admin:admin@localhost/watersafe')
  connection = engine.connect()

  query = """
    SELECT PACR.`county_id` county, PACR.`incident_count` incidents, PACR.`rank` rank, PACR.`bucket` bucket
    FROM PA_COUNTY_VIOLATION_RANK PACR
    WHERE county_id = {0} 
  """
  results = connection.execute(query.format(county_code))

  rankings = []
  for result in results:
    county_ranking_info = {}
    county_ranking_info['county_id'] = result[0]
    county_ranking_info['incident_count'] = result[1]
    county_ranking_info['rank'] = result[2]
    county_ranking_info['bucket'] = result[3]
    rankings.append(county_ranking_info)

  # This should only return one result.
  return rankings[0]

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

def Contact(address):
  address = address.replace(' ','+')
  url = 'https://cicero.azavea.com/v3.1/official?search_address='+address+'&search_country=US&user=watersafe&key='+cicero_api_key
  body = {}
  headers = {'Content-type': 'application/json'}
  response, content = http.request(url, 'GET', headers=headers, body=urllib.urlencode(body))
  return content

def search_form(request):
  return render_to_response('index.html', context_instance=RequestContext(request))

def Search(request):
  if 'address' in request.POST:
    address = request.POST['address']
  else: 
    address = "20 N. 3rd St Philadelphia"
  contact_results = Contact(address)

  county_code = get_county_code_by_address(address)
  ranking_info = get_ranking_info_by_county(county_code)
  pws_info = get_pws_details_by_county(county_code)
  county_name = get_county_name_by_zip(19131)

  if ranking_info['bucket'] == "G":
    rating_type = "green-rating"
    rating_button = "green-button"
  elif ranking_info['bucket'] == "Y":
    rating_type = "yellow-rating"
    rating_button = "yellow_button"
  else: 
    rating_type = "red-rating"
    rating_button = "red_button"

  return render_to_response('results.html', {
      'county_id': county_code, 
      'address': address,
      'incident_count': ranking_info['incident_count'],
      'bucket': ranking_info['bucket'],
      'rank': ranking_info['rank'],
      'rating_type': rating_type,
      'rating_button': rating_button,
      'pws_info': pws_info,
      'county_name': county_name.lower()
  }, context_instance=RequestContext(request))
