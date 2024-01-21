from constants import ABORT_ALL_POSITIONS, FIND_COINTEGRATED
from func_connections import connect_dydx
from func_private import abort_all_positions
from func_public import construct_market_prices

if __name__ == "__main__":
    
    # Connect to client
    # try/except -> In case anything goes wrong, we want to exit the code immediately and get notifed
    try:
        print("Connecting to Client...")
        client = connect_dydx()
    except Exception as e:
        print("Error connecting to client: ", e) # For log file
        exit(1) # Kill the Python script 
        
    # Abort all open positions
    if ABORT_ALL_POSITIONS:
        try:
            print("Closing all positions...")
            clsoe_orders = abort_all_positions(client)
        except Exception as e:
            print("Error closing all positions: ", e)
            exit(1)
            
    # Find Cointegrated Pairs
    if FIND_COINTEGRATED:
        
        # Construct Market Prices
        try:
            print("Fetching market prices, please allow 3 mins...")
            df_market_prcies = construct_market_prices(client)
        except Exception as e:
            print("Error constructing market prices: ", e)
            exit(1)