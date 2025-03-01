# Daraja M-Pesa Integration

This project demonstrates how to integrate with the Safaricom M-Pesa Daraja API to perform Lipa na M-Pesa Online payments.

## Prerequisites

- Python 3.x
- `requests` library

You can install the `requests` library using pip:

```sh
pip install requests


Getting Started
Access Token
The access_token.py script contains a function to generate an access token from the Safaricom API.

Lipa na M-Pesa Online Payment
The lipa_na_mpesa_online function initiates a payment request using the access token.

Running the Script
To run the script and initiate a payment request, execute the following:

if __name__ == "__main__":
    token = get_access_token()
    print("Access Token:", token)
    
    response = lipa_na_mpesa_online(token)
    print("Response:", response)