import gradio as gr
import ccxt

# Initialize Bybit Testnet API
def initialize_bybit():
    try:
        api_key = "hAfzYWcGfED46pk9vp"  # Replace with your API Key
        api_secret = "U1yD4qMRyw4ATZ5F9uhaLIeJ7Fskv8tqjrVS"

        # Initialize Bybit Exchange
        exchange = ccxt.bybit({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
            'urls': {
                'api': {
                    'public': 'https://api-testnet.bybit.com',
                    'private': 'https://api-testnet.bybit.com'
                }
            }
        })
        return exchange

    except Exception as e:
        raise RuntimeError(f"Failed to initialize Bybit API: {str(e)}")

# Fetch Real-Time Market Data
def fetch_market_data(pair):
    try:
        bybit = initialize_bybit()
        ticker = bybit.fetch_ticker(pair)

        # Extract Market Data
        price = ticker.get('last', 'N/A')
        high = ticker.get('high', 'N/A')
        low = ticker.get('low', 'N/A')
        volume = ticker.get('quoteVolume', 'N/A')

        return (
            f"Pair: {pair}\n"
            f"Last Price: {price}\n"
            f"24h High: {high}\n"
            f"24h Low: {low}\n"
            f"24h Volume: {volume}"
        )

    except ccxt.BaseError as e:
        return f"API Error: {str(e)}"
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return f"Unexpected Error:\n{error_details}"

# Gradio Interface
iface = gr.Interface(
    fn=fetch_market_data,
    inputs="text",
    outputs="text",
    title="Bybit Real-Time Market Data"
)

iface.launch()
