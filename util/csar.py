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

import os
import zipfile
import TOSCA_definitions as tosca

CSAR_EXTENSIONS = set(['csar', 'CSAR', "zip", "ZIP"])


def is_csar(filename):
    return filename.rsplit('.', 1)[1] in CSAR_EXTENSIONS


def save_hot_template(temp_dir, contents):
    try:
        # trace("save_hot_template(): temp_dir: " + str(temp_dir))
        metafile = os.path.join(temp_dir,
                                tosca.TOSCA_METAFILE_DIRECTORY,
                                tosca.TOSCA_METAFILE_FILENAME)
        print "metafile:" + metafile
        fh = open(metafile, 'rb')

        myvars = {}

        for line in fh:
            name, var = line.partition(":")[::2]
            myvars[name.strip()] = var.strip()

        # trace("myvars:" + str(myvars))
        if tosca.TOSCA_METAFILE_KEY_ENTRYDEF in myvars:
            entry_def = myvars[tosca.TOSCA_METAFILE_KEY_ENTRYDEF]
            split_name = entry_def.split('.')
            print split_name
            length = len(split_name)
            print length
            split_name.insert(length - 1, 'hot')
            print split_name
            result = '.'.join(split_name)
            print result
            full_result = os.path.join(temp_dir, result)
            fh2 = open(full_result, 'w')
            fh2.write(contents)
            fh2.close()

    except Exception, e:
        print(e)
        raise


def unzip_csar(request, filename, temp_dir):
    try:
        # trace("opening file: [" + filename + "] ...")
        fh = open(filename, 'rb')
        z = zipfile.ZipFile(fh)
        for name in z.namelist():
            # print "extracting: [" + str(name) + "]"
            # Extract ZIP under temp. directory
            z.extract(name, temp_dir)
        fh.close()
    except Exception, e:
        print(str(e))
        raise
