import json
import requests
import time
import matplotlib.pyplot as plt

# Store prices and timestamps
prices = []
timestamps = []

# Set up the plot
plt.ion()  # Interactive mode ON
fig, ax = plt.subplots()

def make_gapi_request():
    api_key = "goldapi-5p9h9smdp8vqhz-io"
    symbol = "XAU"
    curr = "MYR"
    date = ""

    url = f"https://www.goldapi.io/api/{symbol}/{curr}{date}"
    
    headers = {
        "x-access-token": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = json.loads(response.text)
        price = data['price_gram_24k']
        print(f"Price (24K): {price}")
        
        # Save data
        prices.append(price)
        timestamps.append(time.strftime('%H:%M:%S'))

    except requests.exceptions.RequestException as e:
        print("Error:", str(e))

# Run and update plot every minute
while True:
    make_gapi_request()

    # Plotting
    ax.clear()
    ax.plot(timestamps, prices, marker='o', linestyle='-', color='black')
    ax.set_title("Gold Price (24K) in MYR")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price (MYR/g)")
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    plt.pause(1)  # Pause to update the plot

    time.sleep(60)  # Wait for 1 minute
