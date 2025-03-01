import requests
from requests.auth import HTTPBasicAuth
import base64
from datetime import datetime

# Function to get the access token from Safaricom API
def get_access_token():
    consumer_key = 'DDQ5qANRaPssm27S2NGOwUwQRn2bs2UxguP4ydRydAxMGqeA'
    consumer_secret = 'DNzltdXGX9hHgokxcAdWJwR4GgBQYs9FaXHuRTAEgNkSJ2VzLgWP9PhApbY0wSBT'
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    
    # Make a request to the API to get the access token
    response = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    json_response = response.json()
    access_token = json_response['access_token']
    
    return access_token

# Function to make a payment request using the access token
def lipa_na_mpesa_online(access_token):
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    
    business_short_code = "174379"
    lipa_na_mpesa_online_passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    
    # Generate the password by encoding the combination of Shortcode, Passkey, and Timestamp
    password = base64.b64encode(business_short_code.encode() + lipa_na_mpesa_online_passkey.encode() + timestamp.encode()).decode('utf-8')
    
    # Payload for the payment request
    payload = {
        "BusinessShortCode": business_short_code,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": "100",
        "PartyA": "254719299900",
        "PartyB": business_short_code,
        "PhoneNumber": "254719299900",
        "CallBackURL": "https://mydomain.com/pat",
        "AccountReference": "Test",
        "TransactionDesc": "Test"
    }
    
    # Make a request to the API to initiate the payment
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

if __name__ == "__main__":
    # Get the access token
    token = get_access_token()
    print("Access Token:", token)
    
    # Make the payment request and print the response
    response = lipa_na_mpesa_online(token)
    print("Response:", response)