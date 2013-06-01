#!/usr/bin/env python
# http://www.epa.gov/enviro/facts/services.html - info on the API
# http://iaspub.epa.gov/enviro/ef_metadata_html.ef_metadata_table?p_table_name=VIOLATION&p_topic=SDWIS - info on the violations table 

import urllib
import httplib2

http = httplib2.Http()

def request_url(url):
  body = {}
  headers = {'Content-type': 'application/x-www-form-urlencoded'}
  response, content = http.request(url, 'GET', headers=headers, body=urllib.urlencode(body))
  return content

def get_pws_for_county(county_code):
  url =  "http://iaspub.epa.gov/enviro/efservice/PWS_COUNTY/fipscounty/{0}/json".format(42101)
  return request_url(url)

philly_county_code = 42101
response = get_pws_for_county(philly_county_code)
print response
