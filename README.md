# Daraja M-Pesa Integration

This project demonstrates how to integrate with the Safaricom M-Pesa Daraja API to perform Lipa na M-Pesa Online payments.

## Features

- Sandbox and production environment support
- Proper error handling and timeouts

## Prerequisites

- Python 3.6+
- `requests` library
- Safaricom Daraja API credentials

## Installation

1. **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd daraja-mpesa-integration
    ```

2. **Install the required dependencies:**
    ```bash
    pip install requests
    ```

3. **Setup configuration:**
    ```bash
    # Copy the configuration template
    cp config.example.py config.py
    ```

4. **Edit `config.py` with your actual Safaricom API credentials:**
    ```python
    # Sandbox credentials (get from Safaricom Developer Portal)
    SANDBOX_CONSUMER_KEY = 'your_actual_sandbox_consumer_key'
    SANDBOX_CONSUMER_SECRET = 'your_actual_sandbox_consumer_secret'

    # Production credentials (for live environment)
    PRODUCTION_CONSUMER_KEY = 'your_production_consumer_key'
    PRODUCTION_CONSUMER_SECRET = 'your_production_consumer_secret'

    # Business shortcode and passkey
    BUSINESS_SHORT_CODE = '174379'  # Sandbox test code
    LIPA_NA_MPESA_PASSKEY = 'your_actual_passkey'

    # Callback URL for payment notifications
    CALLBACK_URL = 'https://yourdomain.com/callback'
    ```

## Project Structure

```
daraja-mpesa-integration/
├── .gitignore              # Git ignore rules for security
├── mpesa_integration.py    # Main integration code
├── config.example.py       # Configuration template (safe to commit)
├── config.py               # Actual configuration (DO NOT COMMIT)
└── README.md               # This file
```

## Usage

### Basic Payment Integration

```python
from mpesa_integration import get_access_token, lipa_na_mpesa_online

# Get access token
token = get_access_token(environment='sandbox')  # Use 'production' for live environment

if token:
    # Initiate payment
    response = lipa_na_mpesa_online(
        access_token=token,
        amount=100,                    # Amount in KES
        phone_number="254712345678",   # Customer phone number
        account_reference="Order123",  # Your internal reference
        environment='sandbox'          # Use 'production' for live
    )
    print("Payment Response:", response)
else:
    print("Failed to authenticate")
```

## Running the Script

Execute the main script directly:
```bash
python mpesa_integration.py
```

This will:
- Authenticate with the Daraja API
- Initiate a test payment of KES 100
- Display the API response

## API Endpoints

**Sandbox Environment**
- Base URL: `https://sandbox.safaricom.co.ke`
- Test Credentials: Available from Safaricom Developer Portal

**Production Environment**
- Base URL: `https://api.safaricom.co.ke`
- Live Credentials: Obtain from Safaricom after approval

## Error Handling

The code includes comprehensive error handling for:
- Network timeouts
- Authentication failures
- Invalid responses
- Missing configuration

## Configuration Options

| Variable                   | Description                        | Example                        |
|----------------------------|------------------------------------|--------------------------------|
| SANDBOX_CONSUMER_KEY       | Sandbox app consumer key           | 'your_sandbox_key'             |
| SANDBOX_CONSUMER_SECRET    | Sandbox app consumer secret        | 'your_sandbox_secret'          |
| PRODUCTION_*               | Production environment credentials | -                              |
| BUSINESS_SHORT_CODE        | Your business PayBill/till number  | '174379' (sandbox)             |
| LIPA_NA_MPESA_PASSKEY      | Lipa na M-Pesa passkey             | 'your_passkey'                 |
| CALLBACK_URL               | Payment confirmation webhook       | 'https://yourdomain.com/callback' |

## Troubleshooting


## Support

For API-related issues, refer to the [Safaricom Daraja API Documentation](https://developer.safaricom.co.ke/daraja/apis/post/safaricom-sandbox).

## License

This project is for educational purposes. Ensure you comply with Safaricom's terms of service when using in production.