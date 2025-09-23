import requests
from requests.auth import HTTPBasicAuth
import base64
from datetime import datetime
from flask import Flask, redirect, request, jsonify  # Added Flask for web handling

try:
    from config import (
        SANDBOX_CONSUMER_KEY,
        SANDBOX_CONSUMER_SECRET,
        BUSINESS_SHORT_CODE,
        LIPA_NA_MPESA_PASSKEY,
        SANDBOX_BASE_URL,
        CALLBACK_URL,
        SUCCESS_REDIRECT_URL,
        CANCEL_REDIRECT_URL,
        TIMEOUT_REDIRECT_URL
    )
except ImportError:
    print("Error: config.py file not found.")
    print("Please copy config.example.py to config.py and fill in your credentials.")
    exit(1)

app = Flask(__name__)

# Function to get the access token from Safaricom API
def get_access_token(environment='sandbox'):
    if environment == 'sandbox':
        consumer_key = SANDBOX_CONSUMER_KEY
        consumer_secret = SANDBOX_CONSUMER_SECRET
        base_url = SANDBOX_BASE_URL
    else:
        # For production - you'd need to set these in config.py
        from config import PRODUCTION_CONSUMER_KEY, PRODUCTION_CONSUMER_SECRET, PRODUCTION_BASE_URL
        consumer_key = PRODUCTION_CONSUMER_KEY
        consumer_secret = PRODUCTION_CONSUMER_SECRET
        base_url = PRODUCTION_BASE_URL
    
    api_url = f"{base_url}/oauth/v1/generate?grant_type=client_credentials"
    
    try:
        # Make a request to the API to get the access token
        response = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret), timeout=30)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        json_response = response.json()
        access_token = json_response['access_token']
        return access_token
    except requests.exceptions.RequestException as e:
        print(f"Error getting access token: {e}")
        return None
    except KeyError:
        print("Error: Access token not found in response")
        print(f"Response: {json_response}")
        return None

# Function to make a payment request using the access token
def lipa_na_mpesa_online(access_token, amount, phone_number, account_reference, environment='sandbox'):
    if environment == 'sandbox':
        base_url = SANDBOX_BASE_URL
    else:
        from config import PRODUCTION_BASE_URL
        base_url = PRODUCTION_BASE_URL
        
    api_url = f"{base_url}/mpesa/stkpush/v1/processrequest"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    
    # Generate the password by encoding the combination of Shortcode, Passkey, and Timestamp
    password = base64.b64encode(
        BUSINESS_SHORT_CODE.encode() + LIPA_NA_MPESA_PASSKEY.encode() + timestamp.encode()
    ).decode('utf-8')
    
    # Payload for the payment request
    payload = {
        "BusinessShortCode": BUSINESS_SHORT_CODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": str(amount),
        "PartyA": phone_number,
        "PartyB": BUSINESS_SHORT_CODE,
        "PhoneNumber": phone_number,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": account_reference,
        "TransactionDesc": "Payment"
    }
    
    try:
        # Make a request to the API to initiate the payment
        response = requests.post(api_url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making payment request: {e}")
        return {"error": str(e)}

# Route to initiate payment
@app.route('/initiate-payment', methods=['POST'])
def initiate_payment():
    if request.is_json:
        data = request.get_json()
        amount = data.get('amount')
        phone_number = data.get('phone_number')
        account_reference = data.get('account_reference')
    else:
        amount = request.form.get('amount')
        phone_number = request.form.get('phone_number')
        account_reference = request.form.get('account_reference')
    
    token = get_access_token()
    if token:
        response = lipa_na_mpesa_online(
            token, 
            amount=amount, 
            phone_number=phone_number, 
            account_reference=account_reference
        )
        
        if 'error' not in response:
            return jsonify({
                'status': 'success',
                'message': 'Payment initiated successfully',
                'response': response
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to initiate payment',
                'response': response
            }), 400
    else:
        return jsonify({
            'status': 'error',
            'message': 'Failed to retrieve access token'
        }), 400

# Callback URL endpoint - This is where Safaricom sends payment results
@app.route('/payment-callback', methods=['POST'])
def payment_callback():
    callback_data = request.json
    
    # Process the callback from Safaricom
    result_code = callback_data.get('Body', {}).get('stkCallback', {}).get('ResultCode')
    
    if result_code == 0:
        # Payment successful
        return redirect(SUCCESS_REDIRECT_URL)
    elif result_code == 1031:
        # Payment cancelled by user
        return redirect(CANCEL_REDIRECT_URL)
    elif result_code == 1032:
        # Payment timeout
        return redirect(TIMEOUT_REDIRECT_URL)
    else:
        # Other error - redirect to cancel URL or a generic error page
        return redirect(CANCEL_REDIRECT_URL)

# Simple redirect endpoints for immediate user feedback
@app.route('/payment-success')
def payment_success():
    return redirect(SUCCESS_REDIRECT_URL)

@app.route('/payment-cancel')
def payment_cancel():
    return redirect(CANCEL_REDIRECT_URL)

@app.route('/payment-timeout')
def payment_timeout():
    return redirect(TIMEOUT_REDIRECT_URL)

# Simple payment form for testing
@app.route('/')
def payment_form():
    return '''
    <html>
    <body>
        <h2>Make Payment</h2>
        <form action="/initiate-payment" method="post">
            <label>Amount:</label><br>
            <input type="number" name="amount" value="100" required><br><br>
            
            <label>Phone Number:</label><br>
            <input type="text" name="phone_number" value="254719299900" required><br><br>
            
            <label>Account Reference:</label><br>
            <input type="text" name="account_reference" value="TestPayment" required><br><br>
            
            <input type="submit" value="Pay Now">
        </form>
        
        <div style="margin-top: 20px;">
            <p>Test Links:</p>
            <a href="/payment-success">Simulate Success</a> | 
            <a href="/payment-cancel">Simulate Cancel</a> | 
            <a href="/payment-timeout">Simulate Timeout</a>
        </div>
    </body>
    </html>
    '''

if __name__ == "__main__":
    # Update your config.py with these new variables:
    # SUCCESS_REDIRECT_URL = "https://yourdomain.com/success"
    # CANCEL_REDIRECT_URL = "https://yourdomain.com/cancel" 
    # TIMEOUT_REDIRECT_URL = "https://yourdomain.com/timeout"
    
    app.run(debug=True, port=5000)