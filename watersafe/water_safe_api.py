#!/usr/bin/env python
# http://www.epa.gov/enviro/facts/services.html - info on the API
# http://iaspub.epa.gov/enviro/ef_metadata_html.ef_metadata_table?p_table_name=VIOLATION&p_topic=SDWIS - info on the violations table 

import urllib
import httplib2
import json

from bs4 import BeautifulSoup
http = httplib2.Http()

# XXX He's dead, Jim. 
# This site limits us to 30 requests a day, oh well.
# Scrape http://zip-info.com to get county info
def get_county_by_zip(zip):
  url = "http://www.zip-info.com/cgi-local/zipsrch.exe?cnty=cnty&zip={0}&Go=Go".format(zip)
  response = do_GET(url)
  soup = BeautifulSoup(response)
  print soup.prettify()

  # There's a handful of tables in the page, the one we care about is the third one.
  results_table_index = 3
  results_table = soup.find_all('table')[results_table_index]

  # 4th column has the county code
  county_column_index = 4
  county_code_tag = results_table.find_all('td')[county_column_index]
  county_code = county_code_tag.contents
  return county_code

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

## Debug stuffs

# Test getting county by zip
print get_county_by_zip(19131)

# Test getting violations by county
# philly_county_code = 42101
# water_systems = get_pws_by_county(philly_county_code)

# for water_system in water_systems:
#   pwsid = water_system['PWSID']
#   violations = get_violations_by_pws(pwsid) 
#   print violations
