from flask import Flask, render_template
import json
import requests

app = Flask(__name__)

def readVaultToken():
  vault_namespace = 'hello'
  vault_token = 'token'

  read_token_response = requests.get(
        'https://vault-cluster-2-public-vault-9b332b94.b2c7490e.z1.hashicorp.cloud:8200/v1/hello/data/token/stripe-secret-key',
        headers={
            'X-Vault-Namespace': vault_namespace,
            'X-Vault-Token': vault_token
        }
    )

  stripeInfo = read_token_response
  print(stripeInfo)

  return json.dumps(stripeInfo.text)

@app.route('/')
def renderCCForm():
  stripeInfo = readVaultToken()
  return render_template('index.html', stripePublishableKey=stripeInfo)

@app.route('/submitPayment')
def submitPayment():
  pass

if __name__ == "__main__":
  app.run(debug=True)
