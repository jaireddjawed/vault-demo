from locale import currency
import requests
import json
import stripe

vault_namespace = 'admin'
vault_token = 'token'

stripe_secret_key='token'
stripe_publishable_key='token'


'''
    Credit Card: 4242 4242 4242 4242
    Experiation
    CVC


    Stripe Token: hjkdshfkjds
'''
def createNamespace():
    '''Create Key/Value Pair storage in Vault'''
    kv_response = requests.post(
        'https://vault-cluster-2-public-vault-9b332b94.b2c7490e.z1.hashicorp.cloud:8200/v1/sys/mounts/hello3',
        headers={
            'X-Vault-Namespace': vault_namespace,
            'X-Vault-Token': vault_token
        },
        data={
            'type': 'kv-v2'
        }
    )

    print(kv_response.status_code)

# todo: create flask application that will create a web server that will charge a person's credit card
# todo (cont) using the Stripe API
'''
curl --header "X-Vault-Token: $VAULT_TOKEN" \
      --header "X-Vault-Namespace: admin" \
      --data @payload.json \
      $VAULT_ADDR/v1/secret/data/test/webapp | jq -r ".data"
'''

'''Store token response'''
def storeToken():
    store_token_response = requests.post(
        'https://vault-cluster-2-public-vault-9b332b94.b2c7490e.z1.hashicorp.cloud:8200/v1/hello/data/token',
        headers={
            'X-Vault-Namespace': vault_namespace,
            'X-Vault-Token': vault_token
        },
        json={
            "data": {
                "stripe-publishable-key": stripe_publishable_key,
                "stripe-secret-key": stripe_secret_key
            }
        }
    )

    print(store_token_response.text)

def readToken():
    read_token_response = requests.get(
        'https://vault-cluster-2-public-vault-9b332b94.b2c7490e.z1.hashicorp.cloud:8200/v1/hello/data/stripeSecret',
        headers={
            'X-Vault-Namespace': vault_namespace,
            'X-Vault-Token': vault_token
        }
    )

    print(json.dumps(json.loads(read_token_response.text), indent=4))
    return stripe_secret_key

storeToken()
stripe.api_key = readToken()



def createCharge():
    charge = stripe.Charge.create(
        amount=2000,
        currency="usd",
        source="tok_amex",
        description="Test Charge"
    )

    print(charge)


createCharge()
