#!/usr/bin/env python3

import msal
from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential
import config, struct
import mysql.connector


class dbcnx:
    def __init__(self):
        self.conn = None

    def get_credentials(self):
        tenant_id = config.get_config('Azure', 'tenant_id')
        app_id = config.get_config('Azure', 'app_id')
        secret = config.get_config('Azure', 'secret')
        kv_uri = config.get_config('Azure', 'kv_uri')
        credential = ClientSecretCredential(tenant_id, app_id, secret)
        client = SecretClient(vault_url=kv_uri, credential=credential)
        pw = client.get_secret('bfkdb')
        return pw

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
                ssl_verify_cert=True)
            return self.conn
        except Error as e:
            print(e)
        raise

    def get_db(self):
        if not self.conn:
            return self.connect()
        return self.conn



if __name__ == "__main__":
    db = dbcnx()
    print(db.get_credentials().value)
    
