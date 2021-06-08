# pip install google

# from google import search

# num_page = 3
# search_results = search("This is my query", num_page)
# for result in search_results:
#     print(result.description)
# from google import search
# import requests

# for url in search("Sarim", stop=10):
#             r = requests.get(url)
#             title = everything_between(r.text, '<title>', '</title>')

from googleapi import google
num_page = 3
search_results = google.search("Chaudhary Sarimurrab", num_page)
print(search_results)



# from googleapi import google
# # num_page = 3
# search_results = google.search("Chaudhary Sarimurrab")
# for result in search_results:
#     # print(result.name)
#     # print("_____________________________")
#     print(result.link)
#     # print("_____________________________")
#     # print(result.google_link)
#     print("_____________________________")
#     # print(result.description)
#     print("_____________________________")
#     # print(result.thumb)
#     # print("_____________________________")
#     # print(result.cached)
#     # print("_____________________________")
#     # print(result.page)
#     # print("_____________________________")
#     # print(result.index)
#     print("***************************************")
#     print("***************************************")
