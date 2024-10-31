import requests
import argparse
from bs4 import BeautifulSoup

# Initialize the argument parser
parser = argparse.ArgumentParser(description="Send a GET request with a specified initial cookie.")
parser.add_argument(
    "--cookie", 
    type=str, 
    required=True, 
    help="Initial session cookie value to include in the request header"
)
parser.add_argument(
    "--num_requests", 
    type=int, 
    required=True, 
    help="Number of additional requests to make (e.g., 150)"
)

# Parse the arguments
args = parser.parse_args()

# Define the URL
url = "http://34.143.251.219/"
initial_headers = {
    "Host": "34.143.251.219",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.199 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Referer": "http://34.143.251.219/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "close",
    "Cookie": 'session={}'.format(args.cookie)  # Changed to format method
}

# Function to perform the request
def perform_request(cookie_value):
    headers = initial_headers.copy()
    headers["Cookie"] = 'session={}'.format(cookie_value)  # Changed to format method
    
    response = requests.get(url, headers=headers)
    return response

# Make the initial GET request
initial_response = perform_request(args.cookie)

# Print all 'Set-Cookie' values in the response headers
print("Response Cookies:")
for cookie in initial_response.cookies:
    print("Cookie Name: {}, Cookie Value: {}".format(cookie.name, cookie.value))

# Print the Set-Cookie header if present
if "Set-Cookie" in initial_response.headers:
    new_cookie = initial_response.headers["Set-Cookie"].split(';')[0]  # Extracting just the cookie name and value
    print("\nSet-Cookie Header:", new_cookie)
else:
    print("No Set-Cookie header found in the response.")

# Parse the HTML response to find the CAPTCHA code and attempts information
soup = BeautifulSoup(initial_response.content, 'html.parser')

# Extract CAPTCHA code
captcha_img = soup.find('img', {'src': lambda x: x and x.startswith('/captcha/')})
if captcha_img and 'src' in captcha_img.attrs:
    captcha_code = captcha_img['src'].split('/')[-1].split('.')[0]
    print("\nCAPTCHA Code:", captcha_code)
else:
    print("No CAPTCHA image found in the response.")

# Extract attempts information
attempts_info = soup.find('p', string=lambda x: x and 'Attempts:' in x)
if attempts_info:
    attempts_text = attempts_info.get_text(strip=True)
    print("\nAttempts Information:", attempts_text)
else:
    print("No attempts information found in the response.")

# Now, perform the specified number of additional requests using the new cookie
for i in range(1, args.num_requests + 1):
    response = perform_request(new_cookie)
    print("\nResponse for request {}:".format(i))
    
    # Here, you can process the response as needed (e.g., extract more data)
    # For simplicity, we'll print out the cookie received in each response
    print("Response Cookies:")
    for cookie in response.cookies:
        print("Cookie Name: {}, Cookie Value: {}".format(cookie.name, cookie.value))

    # Optionally, print the status code of the response
    print("Response Status Code:", response.status_code)

    # Example: Extracting CAPTCHA code for each request
    soup = BeautifulSoup(response.content, 'html.parser')
    captcha_img = soup.find('img', {'src': lambda x: x and x.startswith('/captcha/')})
    if captcha_img and 'src' in captcha_img.attrs:
        captcha_code = captcha_img['src'].split('/')[-1].split('.')[0]
        print("CAPTCHA Code:", captcha_code)
    else:
        print("No CAPTCHA image found in this response.")

    # Optionally, extract attempts information again
    attempts_info = soup.find('p', string=lambda x: x and 'Attempts:' in x)
    if attempts_info:
        attempts_text = attempts_info.get_text(strip=True)
        print("Attempts Information:", attempts_text)
    else:
        print("No attempts information found in this response.")
