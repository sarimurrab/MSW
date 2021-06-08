# pip install google-search

from googlesearch.googlesearch import GoogleSearch
response = GoogleSearch().search("chaudhary sarimurrab github")
for result in response.results:
    print("Title: " + result.title)
    print("Content: " + result.getText())