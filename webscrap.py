# pip install requests
# pip install fake_headers
# pip install beautifulsoup4
# pip install lxml




import bs4
import requests
import fake_headers
import json

URL = "https://spb.hh.ru/search/vacancy?text=python+django+flask&salary=&ored_clusters=true&search_field=description&excluded_text=&area=1&area=2&hhtmFrom=vacancy_search_list&hhtmFromLabel=vacancy_search_line"

def gen_headers():
    headers_gen = fake_headers.Headers(os="win", browser="chrome")
    return headers_gen.generate()

response = requests.get(URL,headers=gen_headers())#обьявляю что заходит человек
main_html=response.text
main_page=bs4.BeautifulSoup(main_html, "lxml")

artocle_list_tag=main_page.find("main", class_="vacancy-serp-content")
artocles_tags=artocle_list_tag.find_all("div", class_="vacancy-serp-item__layout")
Itog_diction={}

for artocle_tag in artocles_tags:
    #<h3 data-qa="bloko-header-3" class="bloko-header-section-3"
    h3_title = artocle_tag.find("h3", class_="bloko-header-section-3")
    span_title = h3_title.find("span",class_="serp-item__title-link serp-item__title")
    header= span_title.text.strip()
    #print(header)
    link_tag=h3_title.find("a",class_="bloko-link")
    link = link_tag.get("href")
    #print(link)
    block_compani = artocle_tag.find("div", class_="vacancy-serp-item__info")
    compani_tag = block_compani.find("div", class_="bloko-text")
    compani = compani_tag.text.strip()
    #print(compani)
    city_tag=block_compani.find("div", {'data-qa':"vacancy-serp__vacancy-address"})
    city=city_tag.text.strip()
    #print(city)
    compensation_tag=artocle_tag.find("span", class_="bloko-header-section-2")
    if compensation_tag==None:
        compensation="Не указана"
    else:
        compensation=compensation_tag.text.strip()
    #print(compensation)
    itog=[]
    itog.append(str(compani))
    itog.append(str(city))
    itog.append(str(compensation))
    itog.append(str(link))
    #print(itog)
    slov={header:itog}
    Itog_diction.update(slov)
#print(Itog_diction)
with open('sw_templates.json', 'w') as f:
    f.write(json.dumps(Itog_diction))
