import requests
import argparse

# Initialize the argument parser
parser = argparse.ArgumentParser(description="Send a GET request with a specified initial cookie.")
parser.add_argument(
    "--cookie", 
    type=str, 
    required=True, 
    help="Initial session cookie value to include in the request header"
)

# Parse the arguments
args = parser.parse_args()

# Define the URL and headers, inserting the cookie from command-line argument
url = "http://34.143.251.219/"
headers = {
    "Host": "34.143.251.219",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.199 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Referer": "http://34.143.251.219/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "close",
    "Cookie": f"session={args.cookie}"
}

# Make the GET request with the headers including the user-provided cookie
response = requests.get(url, headers=headers)

# Print all 'Set-Cookie' values in the response headers
print("Response Cookies:")
for cookie in response.cookies:
    print(f"Cookie Name: {cookie.name}, Cookie Value: {cookie.value}")

# Alternatively, if you want the entire 'Set-Cookie' header
if "Set-Cookie" in response.headers:
    print("\nSet-Cookie Header:", response.headers["Set-Cookie"])
else:
    print("No Set-Cookie header found in the response.")
