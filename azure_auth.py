#!/usr/bin/env python3

import msal
from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential
import config, struct
import mysql.connector
from datetime import datetime

class dbcnx:
    def __init__(self):
        self.conn = None
        self.pw = None

    def get_credentials(self):
        if not self.pw:
            tenant_id = config.get_config('Azure', 'tenant_id')
            app_id = config.get_config('Azure', 'app_id')
            secret = config.get_config('Azure', 'secret')
            kv_uri = config.get_config('Azure', 'kv_uri')
            credential = ClientSecretCredential(tenant_id, app_id, secret)
            client = SecretClient(vault_url=kv_uri, credential=credential)
            self.pw = client.get_secret('bfkdb')
        elif not self.pw.properties.expires_on == None:
            if self.pw.properties.expires_on > datetime.now():
                self.pw = None
                get_credentials(self)
        return self.pw

    def connect(self):
        """ Create a connection to database that we can use.
        :return: Connection object or raise exception
        """
        try:
            self.conn = mysql.connector.connect(
                user=config.get_config('Azure', 'db_user'),
                password=str(self.get_credentials().value),
                host=config.get_config('Azure', 'db_server'),
                port=3306,
                database=config.get_config('Azure', 'db_name'),
                ssl_ca={},
                ssl_cert={},
                ssl_key={},
                ssl_verify_cert=False)
            return self.conn
        except Error as e:
            print(e)
            raise  

    def get_db(self):
        return self.connect()



if __name__ == "__main__":
    db = dbcnx()
    print(db.get_credentials().value)
    
