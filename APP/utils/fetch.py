from requests import get
from bs4 import BeautifulSoup
import random
 


def search(term, num_results=10, lang="en"):
    usr_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/61.0.3163.100 Safari/537.36'}

    def fetch_results(search_term, number_results, language_code):
        escaped_search_term = search_term.replace(' ', '+')

        google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_results+1,
                                                                              language_code)
        response = get(google_url, headers=usr_agent)
        response.raise_for_status()

        return response.text

    def parse_results(raw_html):

        soup = BeautifulSoup(raw_html, 'html.parser')
        result_block = soup.find_all('div', attrs={'class': 'g'})
        for result in result_block:
            
            link = result.find('a', href=True)
            try:
                title = result.find('h3').text
            except:
                title = "TITLE NOT FOUND"
            description = result.find('div').text.split('›')[-1]
            try:
                link_title = result.find('span').text
            except: "LINK TITLE NOT FOUND"
            # print(title)
            # if link and title:
            #     
            yield {"link": link['href'],"title":title,"desc":description,"link_title":link_title}

            

    html = fetch_results(term, num_results, lang)
    
    return list(parse_results(html))

# q = "chaudhary sarimurrab github "


# list1 = [4,5,6,7,8,9]
# num_results = random.choice(list1)
# for i in search(q,num_results=num_results):
#     print(i)


# print(search(q,num_results=num_results))