import requests
import os
import numpy
from bs4 import BeautifulSoup

def get_estadao():

    url = "https://www.estadao.com.br/"
    url_request = requests.get(url)
    landing_page = url_request.content

    soup = BeautifulSoup(landing_page, 'html.parser')

    landing_page_news = soup.find_all('div', class_='intro') 
    soft_news = soup.find_all('section', class_='lista-soft')
    for n in numpy.arange(0, len(landing_page_news)):

        news_element = landing_page_news[n].find('a')
        news_url = news_element['href']
        if news_url is None:
            continue
        print(str(n) + " " + news_url)
        if "einvestidor" in news_url or "infograficos" in news_url or "paladar" in news_url or "estadao" not in news_url:
            print("NON-REGULAR ARTICLE, SKIPPED")
            continue

        news_request = requests.get(news_url)
        news_page = news_request.content
        news_soup = BeautifulSoup(news_page, 'html.parser')
        news_body = news_soup.find('div', class_='n--noticia__content content')
        if news_body is None:
            continue
        full_news = news_body.text

        try:
            children = news_body.findChildren('div', class_='n--noticia__citacao')
            for child in children:
                full_news = full_news.replace(child.text, '')
        except Exception as e:
            print("\n ERROR FINDING CHILDREN: " + str(e))

        text_file = open("artigos/"+str(news_url).replace('/','_').replace(':','_')+".txt","w", encoding="utf-8")
        text_file.write(str(full_news))
        text_file.flush()
        text_file.close()

def get_folha():
    url = "https://www.folha.uol.com.br/"
    url_request = requests.get(url)
    landing_page = url_request.content

    soup = BeautifulSoup(landing_page, 'html.parser')

    main_news = soup.find_all('href', class_='c-main-headline__url') 
    panel_news = soup.find_all('div', class_='c-list-links__content')
    secondary_news = soup.find_all('div', class_='c-headline__content')
    landing_page_news = main_news + panel_news + secondary_news

    for n in numpy.arange(0, len(landing_page_news)):

        news_element = landing_page_news[n].find('a')
        news_url = news_element['href']
        if news_url is None:
            continue
        print(str(n) + " " + news_url)

        news_request = requests.get(news_url)
        news_page = news_request.content
        news_soup = BeautifulSoup(news_page, 'html.parser', from_encoding="utf-8")
        news_body = news_soup.find('div', class_='c-news__body')
        if news_body is None:
            continue
        full_news = news_body.text

        try:
            children = news_body.findChildren('div', class_='js-gallery-widget rs_skip')
            for child in children:
                full_news = full_news.replace(child.text, '')
        except Exception as e:
            print("\n ERROR FINDING CHILDREN: " + str(e))

        text_file = open("artigos/"+str(news_url).replace('/','_').replace(':','_')+".txt","w", encoding="utf-8")
        text_file.write(str(full_news))
        text_file.flush()
        text_file.close()

current_dir = os.getcwd()
if not os.path.exists(current_dir + '/artigos'):
    os.makedirs(current_dir + '/artigos')
print("_____________________________________________________________________\n")
print("                  AGREGADOR DE NOTÍCIAS\n")
print("_____________________________________________________________________\n")
print("ESTADÃO :")
get_estadao()
print("FOLHA :")
get_folha()