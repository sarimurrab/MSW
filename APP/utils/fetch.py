# import requests
# from bs4 import BeautifulSoup
# ip = "sarimurrab"
# google_search = requests.get('https://www.google.com/search?q='+ip)

# soup = BeautifulSoup(google_search.text, 'html.parser')
# result = soup.select('.r a')
# print(result)

# for link in result:
#     print(link)

# from urllib.parse import urlencode, urlparse, parse_qs

# from lxml.html import fromstring
# from requests import get

# raw = get("https://www.google.com/search?q=sarimurrab").text
# page = fromstring(raw)

# for result in page.cssselect(".r a"):
#     url = result.get("href")
#     if url.startswith("/url?"):
#         url = parse_qs(urlparse(url).query)['q']
#     print(url[0])


from googlesearch import search

q = "chaudhary sarimurrab github "

for i in search(q):
    print(i)