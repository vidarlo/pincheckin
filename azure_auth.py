#!/usr/bin/env python3

import msal
from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential
import config, struct
def get_credentials():
    tenant_id = config.get_config('Azure', 'tenant_id')
    app_id = config.get_config('Azure', 'app_id')
    secret = config.get_config('Azure', 'secret')
    kv_uri = config.get_config('Azure', 'kv_uri')
    credential = ClientSecretCredential(tenant_id, app_id, secret)
    client = SecretClient(vault_url=kv_uri, credential=credential)
    pw = client.get_secret('bfkdb')
    return pw

if __name__ == "__main__":
    print(get_credentials().value)
