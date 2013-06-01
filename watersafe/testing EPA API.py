#!/usr/bin/env python
# http://www.epa.gov/enviro/facts/services.html - info on the API
# http://iaspub.epa.gov/enviro/ef_metadata_html.ef_metadata_table?p_table_name=VIOLATION&p_topic=SDWIS - info on the violations table 

import urllib
import httplib2

http = httplib2.Http()

url = "http://iaspub.epa.gov/enviro/efservice/tri_facility/state_abbr/VA/rows/499:504/json"
body = {}
headers = {'Content-type': 'application/x-www-form-urlencoded'}
response, content = http.request(url, 'GET', headers=headers, body=urllib.urlencode(body))

print content
