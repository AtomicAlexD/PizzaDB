from azure.identity import ClientSecretCredential #, DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


credential = ClientSecretCredential(
    tenant_id='{my_tennant_id}',
    client_id='{service_principle_id}',
    client_secret='{service_principle_secret}'
)
Key_vault_url = f'https://{vault_name}.vault.azure.net/'
client = SecretClient(vault_url= Key_vault_url, credential=credential)
secret_key = client.get_secret('secret_name')
    
print(f'app secret key: {secret_key.value}')