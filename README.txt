# OASIS TOSCA Translator in Python

This is a Python Flask-based micro service that wraps the Pypi libraries “tosco-parser” and “heat-translator” and uses them to translate of application service templates written against the OASIS Topology Orchestration Spec. for Cloud Applications (TOSCA) Simple Profile in YAML v1.0 standard specification and convert them to the OpenStack Heat Orchestration template (HOT) format.  Essentially offering a RESTful micro service (single API) via an HTTP Post command. It also supports HTTP Get by providing a GUI experience for the same translation using Flask templates.


## Files

The Python starter application has files as below:

*   server.py

	This file contains a server for the translation service using Python Flask.

*   static/

	This directory contains the static files used for the “HTTP Get” translator GUI.

*   Procfile

	This file is required by the Python buildpack. It specifies the command to start the app.

*   requirements.txt

	This file is required by the Python buildpack. Its presence indicates that the application is a created for this buildpack. It can be used to list extra python packages not included by the buildpack by default.

