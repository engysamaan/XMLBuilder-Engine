import sys
import os
import time
import urllib
import traceback
import pandas as pd
from mysql.connector import Error
from sqlalchemy import create_engine
"""
This file is untracked in Git
"""

ProfileID = int(sys.argv[1])

server_python_exe  = r'"C:\Users\Public\Public Scripts\DST AMS_CLM Azure Repo\venv\Scripts\python.exe"'
local_python_exe = r'C:\Users\581086\Scripts\AMS_CLM\venv\Scripts\python.exe'

python_exe = local_python_exe
#######################################
LocalScriptDir = r"C:/Users/581086/Scripts/AMS_CLM/AMS_"
ServerScriptDir = r'"C:\Users\Public\Public Scripts\AMS_CLM\AMS_"'

ScriptDir = LocalScriptDir
##############################################
server_output = 'C:\\Users\\Public\\Public Scripts\\AMS_CLM\\AMS_Trigger\\output'
local_output = 'C:\\Users\\581086\\Scripts\\AMS_CLM\\AMS_Trigger\\output'

output = local_output

###################### DB CONNECTION ######################################

class SQLServerUtilities(object):
    """
    Clss that conn to AMS DB
    """
    
    def __init__(self, Environment):
        scriptDir = os.path.dirname(os.path.abspath(__file__))

        # application_path = os.path.dirname(os.path.abspath(__file__))
        
        if getattr(sys, 'frozen', False):
            # Get Path of where Executable is running
            # If the application is run as a bundle/exe, the PyInstaller bootloader
            # extends the sys module by a flag frozen=True
            scriptDir = os.path.dirname(sys.executable)
        else:
            # Get Path of where Script is running
            scriptDir = os.path.dirname(os.path.abspath(__file__))
        Params = eval(open(scriptDir + '\\dbEnv.txt', 'r').read())
        
        self.SQLServer = Params[Environment]['SQLServer']
        # print(self.SQLServer)
        self.SQLUser = Params[Environment]['SQLUser']
        self.SQLPassword = Params[Environment]['SQLPassword']
    
    def AMSDBconnect(self):
        """dsfsd
        """
        Connection_string = (
                "Driver={};"
                "Server={};"
                "UID={};"
                "PWD={};"
                "Database=AMSDB;"
        ).format('ODBC Driver 17 for SQL Server', self.SQLServer, self.SQLUser, self.SQLPassword)
        
        quoted = urllib.parse.quote_plus(Connection_string)  # type: ignore
        engine = create_engine(
                f"mssql+pyodbc:///?odbc_connect={quoted}", fast_executemany=True
                )
        # with engine.connect() as cnn:
        con = engine.connect()
        return con

try:
    Environment = sys.argv[2]
    con = SQLServerUtilities(Environment).AMSDBconnect()


except Exception as error:
    print('---')
    print('An exception occurred: {}'.format(error))
    # traceBack = str(traceback.format_exc()).replace('\n', ' ').replace('\r', '')
    print('---')
    print(traceback.format_exc())


## DocuSignAPI ##
class DemoEnvironment(object):
    clm_base_url = "https://apiuatna11.springcm.com"
    esign_base_url = "https://demo.docusign.net/restapi"
    ds_account_id = "a56f6983-f94a-4b53-b199-4184b7957b69"
    endpoint_instance = "uatna11"
    iss = "f9d6da26-08b7-4117-abe1-7c9a53fd60df"
    sub = "50c52360-1d66-47bc-a4c2-3259de121080"
    aud = "account-d.docusign.com"
    scope = tuple(['signature', 'impersonation', 'spring_read', 'spring_write'])
    private_key = "-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA+GAD+19n+MX/xAaMNwYn7jcRrtKXh+u1t5/AZSS6NVjfAHjAMERXhywQBoVuR8rEvOpcxMzSWIViZMXjK+rYNtoIJVbEBgnACU8ZmMM5WOHYx4F03JVGzjGLAtApFTSuw+BWPxc27nPufSSDS2/K6o3SQbrFg1OLdjwu1IktIxTO3ZMiSBPu+oyIDjhN832gGm0+hN78UACqY2ovB+SLG1a3SCT8De9P4eZ9VJMLk0xPobgGnVqtbtrE62L/+YmZ2OBliiQDcnhUhw3fYw+e00v2q4eV3zRvLMMBI0DU6kdEubttHA2TE2AmjE4ECYhHgSNj1vnlkfAzm+CUMAqfXwIDAQABAoIBAAfAcpj3oYNJjEthUbwtGTWKStpkJwFbLiDpmUcCCwm7mO7z1dO4nlHqryL094jBrFUIReLvUMIdT5sJ9HNPcULgMfbjkVsHsBJz575omwAwjeQUINvHKoTCIq69mAdzmhMk8kW/z+57RP5rRraMNtunl3m6F/LN7bSMxk1kOdNpaBn/l2cMwPVmAt2LsfTOcs5z1cUMZG/CWuIoMOnrSRxNYgfgjhvcBCMMwx0iX+utBAQFf4s+2OpgvAlYI1XJvNLWxWD8coXoei6Do3K6d80AI1BIe8TRZeaWRfvz6KzqiKAva55WLD5+5hQguQQfKN2Ff2ZRNmUZs2HlbtV4g7ECgYEA/FDJTtcDgpMy9zSmz13rSlQFEMOZkMnmR9QqV2XoQeeD+E//2Euvz2t4679ORAYCGZZ3MB1ykOxtpyKWSiBmDUuilpLYke/kZXuvSNMyhGcHSrHDAWgQrd5BvtffVO5Rp24y4HqjPa6bTunTAfArATRKqEzDDcLagNgVLUHlIdcCgYEA/AB/qBtCvHyBaI3aJiJf8ckUhQ4sbXt9mwrSa2gWSk4rhFzGS8hj5gIeMozloHiSUPLO2PW1E5HqJfW8IR5eHzdCCV7ZDz2qU3KsUQcgJa276KzSEMkZDTrbs89v1vEE91gxlqYMHcoazf5/RUdgNHen1JHfV8hDnwpIOCIEzbkCgYA523yN65gOdRqWvSgTHQI7RRD0SyYHoYSArBIZgHDFzATjB9UvEAv8kDRmOrQDvSz2GR6zlc0TlmN+k9vKm6tLGTDrPjkTHeNNshL7rBJFciql4iVJSUep1vFUhcPcgdmPfyGDgBu2pTdP3SZZp2z1FbyY4yFHIotgSCxy+E1GeQKBgQDuOIZ04vhOeCBZNyeOvxYV2fFU6pYjFQcjBrLtp+LScVz/7jfiMdgF+eCUBs+XyAMBFNdnD7cSffBr3AXxBOUS+0io1Qm6N6AI7LFqk6LXG4o0JRMbnQ7ai9Ze/2yJMyRvseaGtAdmLcTzEG89jYCreKWl9BO+xujtsmmc7sO9uQKBgFlI3K8B9cQUnWPAWUf7KofBeL6AGI/18CczMIt0fCVulSKbdNcyRRO74oD/l6N6+ZQryMAgNQZmaQvv2luTHRIvNVtVyyoOn3U6oYWiUBltiuW2vIRNDlDpKlNueWAHVlkydlcjhxYKFPAQ8it8xXHx+VfdtxM/LFcp/B6i1gPA\n-----END RSA PRIVATE KEY-----"


class ProductionEnvironment(object):
    clm_base_url = "https://apina11.springcm.com"
    esign_base_url = "https://na4.docusign.net/restapi"
    ds_account_id = "c812fd83-a0df-45bf-b592-50f634836136"
    endpoint_instance = "apina11"
    iss = "f9d6da26-08b7-4117-abe1-7c9a53fd60df"
    sub = "f1f29c8b-6a26-4000-ad8b-a0d99a0357be"
    aud = "account.docusign.com"
    scope = tuple(['signature', 'impersonation', 'spring_read', 'spring_write'])
    private_key = "-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA+GAD+19n+MX/xAaMNwYn7jcRrtKXh+u1t5/AZSS6NVjfAHjAMERXhywQBoVuR8rEvOpcxMzSWIViZMXjK+rYNtoIJVbEBgnACU8ZmMM5WOHYx4F03JVGzjGLAtApFTSuw+BWPxc27nPufSSDS2/K6o3SQbrFg1OLdjwu1IktIxTO3ZMiSBPu+oyIDjhN832gGm0+hN78UACqY2ovB+SLG1a3SCT8De9P4eZ9VJMLk0xPobgGnVqtbtrE62L/+YmZ2OBliiQDcnhUhw3fYw+e00v2q4eV3zRvLMMBI0DU6kdEubttHA2TE2AmjE4ECYhHgSNj1vnlkfAzm+CUMAqfXwIDAQABAoIBAAfAcpj3oYNJjEthUbwtGTWKStpkJwFbLiDpmUcCCwm7mO7z1dO4nlHqryL094jBrFUIReLvUMIdT5sJ9HNPcULgMfbjkVsHsBJz575omwAwjeQUINvHKoTCIq69mAdzmhMk8kW/z+57RP5rRraMNtunl3m6F/LN7bSMxk1kOdNpaBn/l2cMwPVmAt2LsfTOcs5z1cUMZG/CWuIoMOnrSRxNYgfgjhvcBCMMwx0iX+utBAQFf4s+2OpgvAlYI1XJvNLWxWD8coXoei6Do3K6d80AI1BIe8TRZeaWRfvz6KzqiKAva55WLD5+5hQguQQfKN2Ff2ZRNmUZs2HlbtV4g7ECgYEA/FDJTtcDgpMy9zSmz13rSlQFEMOZkMnmR9QqV2XoQeeD+E//2Euvz2t4679ORAYCGZZ3MB1ykOxtpyKWSiBmDUuilpLYke/kZXuvSNMyhGcHSrHDAWgQrd5BvtffVO5Rp24y4HqjPa6bTunTAfArATRKqEzDDcLagNgVLUHlIdcCgYEA/AB/qBtCvHyBaI3aJiJf8ckUhQ4sbXt9mwrSa2gWSk4rhFzGS8hj5gIeMozloHiSUPLO2PW1E5HqJfW8IR5eHzdCCV7ZDz2qU3KsUQcgJa276KzSEMkZDTrbs89v1vEE91gxlqYMHcoazf5/RUdgNHen1JHfV8hDnwpIOCIEzbkCgYA523yN65gOdRqWvSgTHQI7RRD0SyYHoYSArBIZgHDFzATjB9UvEAv8kDRmOrQDvSz2GR6zlc0TlmN+k9vKm6tLGTDrPjkTHeNNshL7rBJFciql4iVJSUep1vFUhcPcgdmPfyGDgBu2pTdP3SZZp2z1FbyY4yFHIotgSCxy+E1GeQKBgQDuOIZ04vhOeCBZNyeOvxYV2fFU6pYjFQcjBrLtp+LScVz/7jfiMdgF+eCUBs+XyAMBFNdnD7cSffBr3AXxBOUS+0io1Qm6N6AI7LFqk6LXG4o0JRMbnQ7ai9Ze/2yJMyRvseaGtAdmLcTzEG89jYCreKWl9BO+xujtsmmc7sO9uQKBgFlI3K8B9cQUnWPAWUf7KofBeL6AGI/18CczMIt0fCVulSKbdNcyRRO74oD/l6N6+ZQryMAgNQZmaQvv2luTHRIvNVtVyyoOn3U6oYWiUBltiuW2vIRNDlDpKlNueWAHVlkydlcjhxYKFPAQ8it8xXHx+VfdtxM/LFcp/B6i1gPA\n-----END RSA PRIVATE KEY-----"


if __name__ == "__main__":
    print('AMS Configration')
