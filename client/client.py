#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import requests
# import json

TOSCA_TRANSLATOR_ENDPOINT_DEV = 'http://localhost:5000/translate'
TOSCA_TRANSLATOR_ENDPOINT_PROD = 'http://localhost:5000/translate'
TEST_ENDPOINT = 'http://localhost:8000/'
TOSCA_TEST_FILE = 'tosca_helloworld.yaml'
TOSCA_MIME_TYPE_TEMPLATE = 'application/vnd.oasis.tosca.template'

# create the tuple the requests object will use to inject file
# into the POST (as a multi-part mime)
# Prepare FORM data for a POST
fileheader = {'Expires': '0'}
formdata = {'parameters': 'cpus=1'}

# Post file, Content-Type and Headers as a tuple
files = {'file': (TOSCA_TEST_FILE,
                  open(TOSCA_TEST_FILE, 'rb'),
                  TOSCA_MIME_TYPE_TEMPLATE,
                  fileheader)}

resp = requests.post(TOSCA_TRANSLATOR_ENDPOINT_DEV,
                     files=files, data=formdata)

# DEBUG trace of response
print "vvvvvvvvvvvvvvvvvvvv"
print "response.status_code: " + str(resp.status_code)
print "response.encoding: " + resp.encoding
print "response.headers:"
print resp.headers
print "response.text:"
print "--------------------"
print resp.text
print "^^^^^^^^^^^^^^^^^^^^"
