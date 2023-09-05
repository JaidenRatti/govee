import requests
import time
import yfinance as yf
from govee import control_govee_lights


def get_symbol_and_monitor_price():
    symbol = input("Enter a stock ticker symbol (ALL CAPS) or a cryptocurrency name (lowercase): ").strip()

    # Determine the data source (yfinance or CoinGecko) based on input
    data_source = "yfinance" if symbol.isupper() else "CoinGecko"
    
    previous_price = None

    while True:
        try:
            if data_source == "yfinance":
                stock = yf.Ticker(symbol)
                stock_info = stock.info
                current_price = stock_info.get("currentPrice")
            elif data_source == "CoinGecko":
                crypto_api_url = "https://api.coingecko.com/api/v3/simple/price"
                params = {
                    "ids": symbol,
                    "vs_currencies": "usd"
                }
                response = requests.get(crypto_api_url, params=params)
                data = response.json()
                current_price = data[symbol]["usd"]
            else:
                print("Invalid data source.")
                return False

            if current_price is not None:
                if previous_price is not None:
                    if current_price > previous_price:
                        print(f"{symbol.upper()} price has risen. Changing lights to green.")
                        command = {"name": "color", "value": {"r": 0, "g": 255, "b": 0}}
                    elif current_price < previous_price:
                        print(f"{symbol.upper()} price has fallen. Changing lights to red.")
                        command = {"name": "color", "value": {"r": 255, "g": 0, "b": 0}}
                    else:
                        print(f"{symbol.upper()} price has not changed.")
                else:
                    print(f"Initial {symbol.upper()} price:", current_price)
                    command = {"name": "turn", "value": "off"}  # Turn off lights initially

                success = control_govee_lights(command)


                previous_price = current_price

            else:
                print(f"Unable to retrieve the price for {symbol.upper()}.")
        
        except Exception as e:
            print("Error:", str(e))

        time.sleep(60) 

if __name__ == "__main__":
    get_symbol_and_monitor_price()
