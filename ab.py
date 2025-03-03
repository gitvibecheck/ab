import requests
import time
import json
import pandas as pd

# API Endpoints for different DEXs
ICPSWAP_API = "https://ic0.app/api/v2/canister/osyzs-xiaaa-aaaag-qc76q-cai/query"
KONGSWAP_API = "https://ic0.app/api/v2/canister/2ipq2-uqaaa-aaaar-qailq-cai/query"
OTHER_DEX_API = "https://ic0.app/api/v2/canister/4mmnk-kiaaa-aaaag-qbllq-cai/query"

# Function to fetch prices from ICPSwap
def fetch_icpswap_prices():
    try:
        response = requests.post(ICPSWAP_API, json={"request_type": "query"})
        if response.status_code == 200:
            return response.json()
        else:
            print("Error fetching ICPSwap prices:", response.status_code)
            return None
    except Exception as e:
        print("ICPSwap API Error:", e)
        return None

# Function to fetch prices from KongSwap
def fetch_kongswap_prices():
    try:
        response = requests.post(KONGSWAP_API, json={"request_type": "query"})
        if response.status_code == 200:
            return response.json()
        else:
            print("Error fetching KongSwap prices:", response.status_code)
            return None
    except Exception as e:
        print("KongSwap API Error:", e)
        return None

# Function to fetch prices from another DEX
def fetch_other_dex_prices():
    try:
        response = requests.post(OTHER_DEX_API, json={"request_type": "query"})
        if response.status_code == 200:
            return response.json()
        else:
            print("Error fetching Other DEX prices:", response.status_code)
            return None
    except Exception as e:
        print("Other DEX API Error:", e)
        return None

# Function to find arbitrage opportunities
def find_arbitrage():
    icp_prices = fetch_icpswap_prices()
    kong_prices = fetch_kongswap_prices()
    other_prices = fetch_other_dex_prices()
    
    if not icp_prices or not kong_prices or not other_prices:
        print("Skipping arbitrage check due to missing data.")
        return
    
    df_icp = pd.DataFrame(icp_prices)
    df_kong = pd.DataFrame(kong_prices)
    df_other = pd.DataFrame(other_prices)
    
    # Merging data for comparison
    df = df_icp.merge(df_kong, on='token', suffixes=('_icpswap', '_kongswap'))
    df = df.merge(df_other, on='token', suffixes=('', '_otherdex'))
    
    # Checking for arbitrage opportunities
    df['profit_buy_icpswap'] = (df['price_kongswap'] - df['price_icpswap']) / df['price_icpswap']
    df['profit_buy_kongswap'] = (df['price_icpswap'] - df['price_kongswap']) / df['price_kongswap']
    df['profit_buy_otherdex'] = (df['price_otherdex'] - df['price_icpswap']) / df['price_icpswap']
    
    # Filtering profitable trades (threshold: 0.5%)
    profitable_trades = df[(df['profit_buy_icpswap'] > 0.005) | (df['profit_buy_kongswap'] > 0.005) | (df['profit_buy_otherdex'] > 0.005)]
    
    if not profitable_trades.empty:
        print("Potential arbitrage opportunities found:")
        print(profitable_trades[['token', 'profit_buy_icpswap', 'profit_buy_kongswap', 'profit_buy_otherdex']])
    else:
        print("No arbitrage opportunities at the moment.")

# Run the bot every 30 seconds
if __name__ == "__main__":
    while True:
        find_arbitrage()
        time.sleep(30)
