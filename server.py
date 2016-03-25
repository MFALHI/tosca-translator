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

# from flask import Response, redirect, Markup, url_for
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
import uuid
import shutil
import util.csar as csar
import util.debug as debug

# TOSCA-specific imports
from toscaparser.tosca_template import ToscaTemplate
from translator.hot.tosca_translator import TOSCATranslator
from tests import TESTS

# TODO: Alter these values for production
PRODUCTION = True
DEBUG = False
OUTPUT_TO_FILE = False

# Log constants
REQUEST_SEPARATOR = "="

# TOSCA translator service
HTML_TITLE = "TOSCA to Heat - Translator service"
DEFAULT_MESSAGE = "Select a file to translate"

# Bluemix key-values
BLUEMIX_KEY_APP_PORT = 'VCAP_APP_PORT'
BLUEMIX_VALUE_APP_DEFAULT_PORT = '5000'

# Flask key-values
FLASK_KEY_UPLOAD_FOLDER = 'UPLOAD_FOLDER'
FLASK_KEY_MAX_CONTENT_LEN = 'MAX_CONTENT_LENGTH'
FLASK_KEY_REQUEST_FILE = 'file'

# TOSCA Translator service values for requests/responses
HTTP_REQUEST_KEY_CONTENT_TYPE = 'Content-Type'
TEMPLATE_TRANSLATE = 'translate.html'
RESPONSE_CONTENT_TYPE = 'text/plain'

# API and service paths
PATH_INPUT = './inputs'
API_HANDLER_TRANSLATE = 'translate'
API_PATH_TRANSLATE = '/translate'
API_PATH_V1_0_TRANSLATE = '/tosca/v1.0/translate'
API_PATH_CURRENT_TRANSLATE = API_PATH_V1_0_TRANSLATE

# Constants for TOSCA files
YAML_EXTENSIONS = set(['yaml', 'YAML'])
ALLOWED_EXTENSIONS = set().union(csar.CSAR_EXTENSIONS).union(YAML_EXTENSIONS)
MAX_FILE_SIZE_IN_MB = 16

# create WSGI application instance
app = Flask(__name__)
app.config[FLASK_KEY_UPLOAD_FOLDER] = PATH_INPUT

# Tell Flask to limit upload file size
# this will result in a "413 Request Entity Too Large" error
app.config[FLASK_KEY_MAX_CONTENT_LEN] = MAX_FILE_SIZE_IN_MB * 1024 * 1024

# Check environment vars
if(DEBUG):
    items = os.environ.items()
else:
    items = None


def trace(message):
    if(DEBUG):
        print(message)


def is_tosca_filetype(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def create_dir(path):
    trace("Creating temp directory in: " + path)
    # generate UUID for temp directory name  within the path supplied
    u = uuid.uuid4()
    dir = os.path.join(path, str(u))

    # if it does not exist create it
    try:
        os.stat(dir)
    except:
        curdir = os.getcwd()
        server_dir = os.path.dirname(os.path.realpath(__file__))
        os.mkdir(dir)
    return dir


def delete_dir(directory):
    try:
        if directory and os.path.exists(directory):
            trace("Deleting directory: " + directory)
            os.rmdir(directory)
    except Exception as e:
        print(e)


def save_tosca_file(file_name, temp_dir):

    if file_name and temp_dir:
        file = file_name

        # validate this is a known TOSCA file
        if file:
            # TODO: validate the content-type is valid for this translator
            content_type = file.headers['Content-Type']
            trace("file.headers['Content-Type']: " + content_type)

            if is_tosca_filetype(file.filename):
                return save_input_file(file_name, temp_dir)
            else:
                raise ValueError("Invalid TOSCA filetype. "
                                 "Valid extensions include: "
                                 "\n%s" % ", ".join(ALLOWED_EXTENSIONS))
        else:
            raise ValueError("%s: " + "Invalid file"
                             % save_tosca_file.__name__)
    else:
        raise ValueError("%s: " + "Invalid argument"
                         % save_tosca_file.__name__)


def save_input_file(file, temp_dir):
    try:
        if file and temp_dir:
            trace("Attempting to save file: " + file.filename)
            filename = secure_filename(file.filename)
            trace("secured filename: " + filename)

            # Save the file to specified folder
            full_filename = os.path.join(temp_dir, filename)
            trace("output_path/filename: " + full_filename)
            file.save(full_filename)
            return full_filename
        else:
            raise ValueError("%s: " + "Invalid argument"
                             % save_input_file.__name__)

    except Exception:
        raise


def save_translated_file(file_name_input, output_format, temp_dir, contents):
    try:
        if file_name_input and output_format and temp_dir and contents:
            file = file_name_input
            # print type(file.filename)
            # trace("file_name_input: " + file.filename)
            # trace("format: " + output_format)
            # trace("temp_dir: " + temp_dir)
            # trace("contents: " + contents)
            split_name = file.filename.split('.')

            # derive the output filename from the input name and ouput format
            length = len(split_name)
            split_name.insert(length - 1, output_format)
            result = '.'.join(split_name)
            file_name_output = os.path.join(temp_dir, result)

            trace("Attempting to save output to file: " + file_name_output)
            fh2 = open(file_name_output, 'w')
            fh2.write(contents)
            fh2.close()
        else:
            raise ValueError("%s: " + "Invalid argument"
                             % save_translated_file.__name__)

    except Exception:
        raise


def cleanup_temp_directories(full_filename):

    if full_filename:
        # Cleanup temporary, request-specific folders and files
        path, filename = os.path.split(full_filename)
        trace("Deleting path: " + path)
        trace("Which contains file: " + filename)

        for next_file in os.listdir(path):
            file_path = os.path.join(path, next_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print e
        # TODO: try shutil.rmtree(folder)
        delete_dir(path)


def parse_parameters(parameter_string):
    trace("Parsing parameter string... [" + parameter_string + "]")
    parsed_inputs = {}

    if parameter_string:

        # Convert unicode strings to utf-8 so we can parse it into a list
        if(isinstance(parameter_string, unicode)):
            trace("trace: converting from unicode to ascii...")
            parameter_string = parameter_string.encode('utf-8', 'ignore')

        # verify after unicode conversion we still have a string to parse
        if parameter_string:

            # Split parameter string into a list of key-value pairs
            keyvalue_pairs = parameter_string.replace('"', '').split(';')

            for pair in keyvalue_pairs:
                keyvalue = pair.split('=')

                # trace("keyvalue='" + str(keyvalue) + "'")

                # Assure that there is both a parameter name and value
                if keyvalue.__len__() is 2:
                    # Assure parameter name is not zero-length or whitespace
                    stripped_name = keyvalue[0].strip()
                    if not stripped_name:
                        trace("WARNING: Parameter missing name, skipping...")
                        continue

                    # Add the valid parameter to the dictionary
                    parsed_inputs[keyvalue[0]] = keyvalue[1]
                else:
                    trace("ERROR: Malformed parameter assignment [" +
                          str(keyvalue) + "] ; skipping parameter")

    # debug.dump(parsed_inputs)
    return parsed_inputs


@app.route('/')
def hello():
    return redirect(url_for(API_HANDLER_TRANSLATE))


@app.route(API_PATH_TRANSLATE, methods=['POST', 'GET'])
def tosca_v1_0_translate():
    return redirect(url_for(API_HANDLER_TRANSLATE))


@app.route(API_PATH_CURRENT_TRANSLATE, methods=['POST', 'GET'])
def translate():
    try:
        status_msg = None
        hot_output_string = None
        temp_dir = None
        full_filename = None
        params = ''

        # TODO: look at moving to a decorator
        trace(REQUEST_SEPARATOR)
        trace("request.method: " + request.method)
        trace("request.headers['Content-Type']:" +
              request.headers[HTTP_REQUEST_KEY_CONTENT_TYPE])

        # debug the request object
        # debug.dump(request.__dict__, 1, "Request")

        if request.method == 'POST':

            # Retrieve reference to the file to transcode
            fileinfo = request.files[FLASK_KEY_REQUEST_FILE]
            # debug.dump(fileinfo.__dict__, 1, "File Info")

            # create request-unique subdirectory to store YAML template / CSAR
            temp_dir = create_dir(app.config[FLASK_KEY_UPLOAD_FOLDER])
            full_filename = save_tosca_file(fileinfo, temp_dir)

            if full_filename and is_tosca_filetype(full_filename):
                # TODO: See if we can return a ZIP with HOT and artifacts
                # IF CSAR package unzip it for processing
                # if(is_csar(full_filename)):
                #     trace("Unzipping TOSCA CSAR archive file...")
                #     csar.unzip_csar(request, full_filename, temp_dir)
                # else:
                #     trace("Standalone TOSCA template file detected...")

                # TODO: "sniff" for TOSCA header in template file (for
                # standalone YAML) or the "entry-defintion" template
                # identified in tbe manifest of the CSAR

                # retrieve and validate form data
                form = request.form
                # debug.dump_form(request, 1):

                # Get --parameters from FORM data
                trace("retrieving parameters...")
                if 'parameters' in form:
                    params = form['parameters']
                    # trace("request.form['parameters']: [" + params + "]")
                params = parse_parameters(params)

                try:
                    # Parse the TOSCA template
                    trace("Parsing TOSCA template... [" + full_filename + "]")
                    tosca_template = ToscaTemplate(full_filename, params)

                    # Translate the TOSCA template/package to HOT
                    trace("Translating to Heat template...")
                    translator = TOSCATranslator(tosca_template, params)
                    hot_output_string = translator.translate()
                except Exception, e:
                    raise e

            else:
                # TODO: Show error message to indicate valid file types
                status_msg = "Invalid file ot filetype: file type not saved"

            # Optionally, save translated output
            if not PRODUCTION and OUTPUT_TO_FILE:
                trace("Saving translated output...")
                save_translated_file(fileinfo, "hot", "outputs",
                                     hot_output_string)

            # Add HOT output to the response and set its content type
            # to text/plain to avoid it being intpreted as HTML
            trace("Returning Heat template...")
            debug.dumpif(DEBUG, hot_output_string, 0, "HOT")
            response = app.make_response(hot_output_string)
            response.headers[HTTP_REQUEST_KEY_CONTENT_TYPE] = \
                RESPONSE_CONTENT_TYPE
            return response

        else:
            if request.method == 'GET':
                # Display the translate FORM page with the status message
                return render_template(TEMPLATE_TRANSLATE,
                                       title=HTML_TITLE,
                                       DEBUG=DEBUG,
                                       items=items,
                                       status=status_msg,
                                       output=hot_output_string,
                                       samples=TESTS)

    except Exception, e:
        # TODO: return HTTP error codes
        status_msg = str(e)
        trace("Displaying error to user... ")
        trace("status=[" + status_msg + "]")
        return render_template(TEMPLATE_TRANSLATE,
                               title=HTML_TITLE,
                               DEBUG=DEBUG,
                               items=items,
                               status=status_msg,
                               output=hot_output_string,
                               samples=TESTS)
    finally:
        if request.method == 'POST':
            trace("Cleaning up temporary files...")
            cleanup_temp_directories(full_filename)
            trace("Cleaning up temporary directory...")
            delete_dir(temp_dir)


if __name__ == "__main__":
    # Note: the debug parm. allows flask to automatically create HTML stack
    # traces on errors AND automtically restart the server as the python code
    if PRODUCTION:
        port = os.getenv(BLUEMIX_KEY_APP_PORT, BLUEMIX_VALUE_APP_DEFAULT_PORT)
        app.run(host='0.0.0.0', port=int(port))
    else:
        app.run(debug=DEBUG)
else:
    trace("TOSCA Translation service is being imported from another module")
