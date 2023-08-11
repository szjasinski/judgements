import requests
from bs4 import BeautifulSoup

# TO DO: scrapy solution

# Make a request
url = "https://orzeczenia.nsa.gov.pl/cbo/find?p=1"
response = requests.get(url)
# Parse the HTML
soup = BeautifulSoup(response.content, "html.parser")
# Find the title element
title = soup.find("title")
# Print the text of the title element
print(title.text)

