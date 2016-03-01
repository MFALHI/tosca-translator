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

RAW_BASE = "https://raw.githubusercontent.com/openstack/heat-translator/master/" \
           "translator/tests/data/"
GIT_BASE = "https://github.com/openstack/heat-translator/blob/master/" \
           "translator/tests/data/"
STORAGE_PATH = "storage/"

NAME = "name"
PARMS = "parms"
FORMAT_RAW = "raw"
FORMAT_GIT = "git"
FORMATS = "formats"

TEMPLATE1 = "tosca_helloworld.yaml"
RAW1 = RAW_BASE + TEMPLATE1
GIT1 = GIT_BASE + TEMPLATE1
PARMS1 = None

TEMPLATE2 = "tosca_software_component.yaml"
RAW2 = RAW_BASE + TEMPLATE2
GIT2 = GIT_BASE + TEMPLATE2
PARMS2 = None

TEMPLATE3 = "tosca_single_server_with_defaults.yaml"
RAW3 = RAW_BASE + TEMPLATE3
GIT3 = GIT_BASE + TEMPLATE3
PARMS3 = None

TEMPLATE4 = "tosca_single_server.yaml"
RAW4 = RAW_BASE + TEMPLATE4
GIT4 = GIT_BASE + TEMPLATE4
PARMS4 = ["cpus: <integer>; [ 1, 2, 4, 8 ]"]

TEMPLATE5 = "tosca_web_application.yaml"
RAW5 = RAW_BASE + TEMPLATE5
GIT5 = GIT_BASE + TEMPLATE5
PARMS5 = None

TEMPLATE6 = "tosca_single_instance_wordpress.yaml"
RAW6 = RAW_BASE + TEMPLATE6
GIT6 = GIT_BASE + TEMPLATE6
PARMS6 = ["db_root_pwd: <string>"]

TEMPLATE7 = "tosca_single_instance_wordpress_with_url_import.yaml"
RAW7 = RAW_BASE + TEMPLATE7
GIT7 = GIT_BASE + TEMPLATE7
PARMS7 = ["db_root_pwd: <string>"]

TEMPLATE8 = "tosca_single_instance_wordpress_with_local_abspath_import.yaml"
RAW8 = RAW_BASE + TEMPLATE8
GIT8 = GIT_BASE + TEMPLATE8
PARMS8 = ["db_root_pwd: <string>"]

# Cannot use this as standalone test as it requires imports of other yaml files
# TEMPLATE9 = "tosca_nodejs_mongodb_two_instances.yaml"
# RAW9 = RAW_BASE + TEMPLATE9
# GIT9 = GIT_BASE + TEMPLATE9
# PARMS9 = None

TEMPLATE9 = "csar_elk.zip"
RAW9 = RAW_BASE + TEMPLATE9
GIT9 = GIT_BASE + TEMPLATE9
PARMS9 = ["my_cpus: <integer>; [ 1, 2, 4, 8 ]"]

TEMPLATE10 = "tosca_single_object_store.yaml"
RAW10 = RAW_BASE + STORAGE_PATH + TEMPLATE10
GIT10 = GIT_BASE + STORAGE_PATH + TEMPLATE10
PARMS10 = ["objectstore_name: <string>"]

TEMPLATE11 = "tosca_blockstorage_with_attachment.yaml"
RAW11 = RAW_BASE + STORAGE_PATH + TEMPLATE11
GIT11 = GIT_BASE + STORAGE_PATH + TEMPLATE11
PARMS11 = ["cpus: <integer>; <integer>; [ 1, 2, 4, 8 ]",
           "storage_snapshot_id: <string>",
           "storage_location: <string>"]

TEMPLATE12 = "tosca_blockstorage_with_attachment_notation1.yaml"
RAW12 = RAW_BASE + STORAGE_PATH + TEMPLATE12
GIT12 = GIT_BASE + STORAGE_PATH + TEMPLATE12
PARMS12 = ["cpus: <integer>; <integer>; [ 1, 2, 4, 8 ]",
           "storage_snapshot_id: <string>"]

TESTS = [{NAME: TEMPLATE1,
          FORMATS: {FORMAT_RAW: RAW1, FORMAT_GIT: GIT1}, PARMS: PARMS1},
         {NAME: TEMPLATE2,
          FORMATS: {FORMAT_RAW: RAW2, FORMAT_GIT: GIT2}, PARMS: PARMS2},
         {NAME: TEMPLATE3,
          FORMATS: {FORMAT_RAW: RAW3, FORMAT_GIT: GIT3}, PARMS: PARMS3},
         {NAME: TEMPLATE4,
          FORMATS: {FORMAT_RAW: RAW4, FORMAT_GIT: GIT4}, PARMS: PARMS4},
         {NAME: TEMPLATE5,
          FORMATS: {FORMAT_RAW: RAW5, FORMAT_GIT: GIT5}, PARMS: PARMS5},
         {NAME: TEMPLATE6,
          FORMATS: {FORMAT_RAW: RAW6, FORMAT_GIT: GIT6}, PARMS: PARMS6},
         {NAME: TEMPLATE7,
          FORMATS: {FORMAT_RAW: RAW7, FORMAT_GIT: GIT7}, PARMS: PARMS7},
         {NAME: TEMPLATE8,
          FORMATS: {FORMAT_RAW: RAW8, FORMAT_GIT: GIT8}, PARMS: PARMS8},
         {NAME: TEMPLATE9,
          FORMATS: {FORMAT_RAW: RAW9, FORMAT_GIT: GIT9}, PARMS: PARMS9},
         {NAME: TEMPLATE10,
          FORMATS: {FORMAT_RAW: RAW10, FORMAT_GIT: GIT10}, PARMS: PARMS10},
         {NAME: TEMPLATE11,
          FORMATS: {FORMAT_RAW: RAW11, FORMAT_GIT: GIT11}, PARMS: PARMS11},
         {NAME: TEMPLATE12,
          FORMATS: {FORMAT_RAW: RAW12, FORMAT_GIT: GIT12}, PARMS: PARMS12}
         ]
