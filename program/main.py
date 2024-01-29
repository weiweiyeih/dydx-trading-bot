from constants import ABORT_ALL_POSITIONS, FIND_COINTEGRATED, PLACE_TRADES, MANAGE_EXITS
from func_connections import connect_dydx
from func_private import abort_all_positions
from func_public import construct_market_prices
from func_cointegration import store_cointegration_results
from func_entry_pairs import open_positions
from func_exit_pairs import manage_trade_exits


if __name__ == "__main__":
    
    print("")
    print("===== CONNECTION =====")
    
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
        
        print("")
        print("===== ABORT ALL POSITIONS =====")
        
        try:
            
            print("Closing all positions...")
            clsoe_orders = abort_all_positions(client)
        except Exception as e:
            print("Error closing all positions: ", e)
            exit(1)
            
    # Find Cointegrated Pairs
    if FIND_COINTEGRATED:
        
        print("")
        print("===== FIND COINTEGRATION =====")
        
        # Construct Market Prices
        try:
            print("Fetching market prices, please allow 3 mins...")
            df_market_prcies = construct_market_prices(client)
        except Exception as e:
            print("Error constructing market prices: ", e)
            exit(1)
        
        # Stored cointegrated pairs
        try:
            print("Storing cointegrated pairs...")
            stores_reslut = store_cointegration_results(df_market_prcies)
            
            if stores_reslut != "saved":
                print("Error saving conintegrated pairs")
                exit(1) # Even no logic error, if no cointegrated pairs, we stop the script
        except Exception as e:
            print("Error saving conintegrated pairs: ", e)
            exit(1)
        
    # Run as always on
    while True:
    
        if MANAGE_EXITS:
            
            print("")
            print("===== MANAGE EXITS =====")
            
            try:
                print("Managing exits...")
                result = manage_trade_exits(client)
                print(result)
            except Exception as e:
                print("Error managing exiting positions: ", e)
                exit(1)
            
        # Place trades for opening positions
        if PLACE_TRADES:
            
            print("")
            print("===== PLACE TRADES =====")
            
            try:
                print("Finding trading opportunities...")
                open_positions(client)
            except Exception as e:
                print("Error finding trading pairs: ", e)
                exit(1)
