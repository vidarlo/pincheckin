#!/usr/bin/env python3

import adal, pyodbc
import config, struct
def get_connstring():
    tenant_id = config.get_config('Azure', 'tenant_id')
    app_id = config.get_config('Azure', 'app_id')
    secret = config.get_config('Azure', 'secret')
    db_server = config.get_config('Azure', 'db_server')
    db_name = config.get_config('Azure', 'db_name')
    
    auth_url = ('https://login.microsoftonline.com/' + tenant_id)
    print(auth_url)
    
    context = adal.AuthenticationContext(
        auth_url, api_version=None
    )
    
    token = context.acquire_token_with_client_credentials(
        "https://database.windows.net/",
        app_id,
        secret)
    print(token)
    
    SQL_COPT_SS_ACCESS_TOKEN = 1256 
    connString = "Driver={ODBC Driver 17 for SQL Server};SERVER=" + db_server + ",1433;DATABASE=" + db_name + ";Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30"
    #get bytes from token obtained
    tokenb = bytes(token["accessToken"], "UTF-8")
    exptoken = b'';
    for i in tokenb:
        exptoken += bytes({i});
        exptoken += bytes(1);
    tokenstruct = struct.pack("=i", len(exptoken)) + exptoken;
    return(connString, tokenstruct, SQL_COPT_SS_ACCESS_TOKEN)


