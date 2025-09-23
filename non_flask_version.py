import requests
from requests.auth import HTTPBasicAuth
import base64
from datetime import datetime
import webbrowser

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

def simulate_redirect(scenario):
    """Simulate redirecting to different URLs based on payment outcome"""
    redirect_urls = {
        'success': SUCCESS_REDIRECT_URL,
        'cancel': CANCEL_REDIRECT_URL,
        'timeout': TIMEOUT_REDIRECT_URL
    }
    
    url = redirect_urls.get(scenario, CANCEL_REDIRECT_URL)
    print(f"\n=== REDIRECTING TO: {url} ===\n")
    print(f"Payment scenario: {scenario.upper()}")
    print(f"You would now be redirected to: {url}")
    
    # Optional: Automatically open the URL in a web browser
    try:
        webbrowser.open(url)
        print("Browser opened automatically!")
    except:
        print("(Copy and paste the URL above into your browser)")

def interactive_payment_flow():
    """Interactive payment flow with simulated outcomes"""
    print("=== M-Pesa STK Push Payment Simulator ===")
    print("\n1. Initiate Real Payment")
    print("2. Simulate Successful Payment")
    print("3. Simulate Cancelled Payment") 
    print("4. Simulate Timeout Payment")
    
    choice = input("\nChoose an option (1-4): ").strip()
    
    if choice == "1":
        # Real payment flow
        token = get_access_token()
        if token:
            print("Access Token retrieved successfully")
            
            amount = input("Enter amount: ") or "100"
            phone = input("Enter phone number (254...): ") or "254719299900"
            reference = input("Enter account reference: ") or "TestPayment"
            
            response = lipa_na_mpesa_online(
                token, 
                amount=amount, 
                phone_number=phone, 
                account_reference=reference
            )
            print("Payment Response:", response)
            
            if 'error' not in response:
                print("\nSTK Push sent to your phone!")
                print("After completing the payment on your phone, you'll be redirected automatically.")
            else:
                simulate_redirect('cancel')
        else:
            print("Failed to retrieve access token")
            simulate_redirect('cancel')
    
    elif choice == "2":
        simulate_redirect('success')
    
    elif choice == "3":
        simulate_redirect('cancel')
    
    elif choice == "4":
        simulate_redirect('timeout')
    
    else:
        print("Invalid choice")

if __name__ == "__main__":
      
    interactive_payment_flow()