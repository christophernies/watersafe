#!/usr/bin/env python
# http://www.epa.gov/enviro/facts/services.html - info on the API
# http://iaspub.epa.gov/enviro/ef_metadata_html.ef_metadata_table?p_table_name=VIOLATION&p_topic=SDWIS - info on the violations table 

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

def get_count(county_code):
  # Probably will want to pass the connection in.
  engine = create_engine('mysql://admin:admin@localhost/watersafe')
  connection = engine.connect()

  query = """
    SELECT CSM.`FIPS_COUNTY_ID` countyid,  CSM.`COUNTY_NAME` countyname, count(*) violations
    FROM PA_H20_VIOLATION PAH, COUNTY_STATE_MAPPING CSM
    WHERE PAH.`Vtype` NOT IN ('MR','Other')
    AND PAH.`County` = CSM.`FIPS_COUNTY_ID`
    AND YEAR(PAH.`comp_begin_date`) >= 2012
    AND CSM.`FIPS_COUNTY_ID` = {0} 
  """
  results = connection.execute(query.format(county_code))

  count = [result[2] for result in results]
  return count[0]

def get_pws_details_by_county(county_code):
  # Probably will want to pass the connection in.
  engine = create_engine('mysql://root:root@localhost/watersafe')
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
    print result[4]
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

## Debug stuffs

# Test getting county by zip
# print get_county_by_zip(19131)

# Test getting zip by address
# test_address = "20 North 3rd Street, Philadelphia PA"
# print get_zip_from_address(test_address)

# Test getting violations by county
# philly_county_code = 42101
# water_systems = get_pws_by_county(philly_county_code)

# for water_system in water_systems:
#   pwsid = water_system['PWSID']
#   violations = get_violations_by_pws(pwsid) 
#   print violations

# Test database queries for county codes works
# test_address = "20 N. 3rd St Philadelphia"
# print get_county_code_by_address(test_address)

# Test getting the count of violations by county
# print get_count(42101)

# Test getting county details
print get_pws_details_by_county(42101)
