This file will force Github to create an "inputs" directory which is needed by the TOSCA 
translator service.

This directory is used to store temporary files, such as service templates, CSAR files, 
etc., by the service during translation for each incoming request (i.e., HTTP Post API 
call) to the service.  Upon completion of translation (success or failure) all 
temporary files are deleted.
