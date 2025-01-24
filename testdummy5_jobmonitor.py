import requests
from bs4 import BeautifulSoup

# Specify the URL of the web page you want to parse
url = 'https://careers.hpe.com/us/en/search-results?ak=urk3r534f0wz'

# Send an HTTP request to the URL and get the page content
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    print(soup)
    # Now you can navigate and extract information from the parsed HTML
    # For example, let's extract all the links on the page
    links = soup.find_all('a')

    # Print the links
    for link in links:
        print(link.get('href'))

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
