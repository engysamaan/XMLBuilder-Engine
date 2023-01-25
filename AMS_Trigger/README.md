# AMS_Trigger
This Script is the trigger/runs all the other scripts for AMS Groups.

1. It extracts all the ProfileIDs where there status is new.
2. It runs the correct Group script based on the group abbreviation

## Config.py
Config file, has variables, DataBase connection
and DocuSignAPI

## dbEnv.txt
Contain the DB environment credentials ex: Prod and Test

## DocuSignAPI.py
Contains the codes that connect to DocuSign API that sends the XML file through a Post request. 
Code Sample:https://github.com/docusign/docusign-esign-python-client

## XMLbuilder_Utilities.py
Contains all the functions for converting dataframes to XML format.

## Main.py
Is the main script for AMS_Trigger
 - Structure:
   - Reads the Process table
   - SendMail() func that Send Email with all the successful XML files 
   - Sends the XML files to DocuSign
