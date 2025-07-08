import json
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os
app = Flask(__name__)
CORS(app)

def get_real_time_gold_price():
    """
    Fetches the GLD ETF (a stock that tracks gold prices) from Finnhub.io.
    Converts the stock price to the price per ounce, then to price per gram of gold.
    The API key is read from environment variables for security.
    """
    # 1. The API key is now read from environment variables instead of hardcoding it.
    # This is done using 'os.environ.get()'.
    API_KEY = os.environ.get("FINNHUB_API_KEY") 
    
    # 2. If the API key is not defined in the environment variables,
    # print an error message and return a safe default value.
    if not API_KEY:
        print("ERROR: FINNHUB_API_KEY environment variable not found. Using default value.")
        return 70.0  # Safe default price

    # 3. The request URL is constructed using the found API key.
    url = f"https://finnhub.io/api/v1/quote?symbol=GLD&token={API_KEY}"
    DEFAULT_GOLD_PRICE = 70.0
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if 'c' in data and data['c'] != 0:
            price_per_share = data['c']
            price_per_ounce = price_per_share * 10 
            price_per_gram = price_per_ounce / 31.1035
            print(f"Real-time gold price (Finnhub/GLD Proxy) fetched successfully: {round(price_per_gram, 2)} USD/gram")
            return price_per_gram
        else:
            print("Valid price data not received from API (GLD). Using default value.")
            return DEFAULT_GOLD_PRICE
    except requests.exceptions.RequestException as e:
        print(f"Could not reach Finnhub API (GLD): {e}. Using default value.")
        return DEFAULT_GOLD_PRICE


@app.route('/products', methods=['GET'])
def get_products():
    try:
        with open('products.json', 'r', encoding='utf-8') as f:
            products = json.load(f)

        gold_price = get_real_time_gold_price()

        processed_products = []
        for index, product in enumerate(products):
            product['id'] = index + 1
            price = ((product['popularityScore'] * 100) + 1) * product['weight'] * gold_price
            product['price'] = round(price, 2)
            rating = round(product['popularityScore'] * 5, 1)
            product['rating'] = rating
            processed_products.append(product)
        
        
        args = request.args
        
        # Price Range Filter
        min_price = args.get('min_price', type=float)
        if min_price is not None:
            processed_products = [p for p in processed_products if p['price'] >= min_price]

        max_price = args.get('max_price', type=float)
        if max_price is not None:
            processed_products = [p for p in processed_products if p['price'] <= max_price]
            
        # Popularity Score Filter
        min_popularity = args.get('min_popularity', type=float)
        if min_popularity is not None:
            
            filter_value = min_popularity / 100.0
            
            processed_products = [p for p in processed_products if p['popularityScore'] >= filter_value]

        max_popularity = args.get('max_popularity', type=float)
        if max_popularity is not None:
            filter_value = max_popularity / 100.0
            processed_products = [p for p in processed_products if p['popularityScore'] <= filter_value]

        

        return jsonify(processed_products)
        
    except FileNotFoundError:
        return jsonify({"error": "products.json file not found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)