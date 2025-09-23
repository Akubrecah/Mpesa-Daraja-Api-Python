# Safaricom API Configuration

# Sandbox credentials (for testing)
SANDBOX_CONSUMER_KEY = 'DDQ5qANRaPssm27S2NGOwUwQRn2bs2UxguP4ydRydAxMGqeA'
SANDBOX_CONSUMER_SECRET = 'DNzltdXGX9hHgokxcAdWJwR4GgBQYs9FaXHuRTAEgNkSJ2VzLgWP9PhApbY0wSBT'

# Production credentials (when ready for production)
# PRODUCTION_CONSUMER_KEY = 'your_production_consumer_key_here'
# PRODUCTION_CONSUMER_SECRET = 'your_production_consumer_secret_here'

# API URLs
SANDBOX_BASE_URL = 'https://sandbox.safaricom.co.ke'
PRODUCTION_BASE_URL = 'https://api.safaricom.co.ke'

# Business shortcode and passkey
BUSINESS_SHORT_CODE = '174379'  # Sandbox test code
LIPA_NA_MPESA_PASSKEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"

# Other configuration
CALLBACK_URL = 'https://n8n.digibraille.com/' 
SUCCESS_REDIRECT_URL = "https://n8n.digibraille.com/success"
CANCEL_REDIRECT_URL = "https://n8n.digibraille.com/cancel"
TIMEOUT_REDIRECT_URL = "https://n8n.digibraille.com/timeout"