import requests
from bs4 import BeautifulSoup 
from pprint import pprint

base_url = "http://books.toscrape.com/catalogue/"
page_actuelle = "http://books.toscrape.com/index.html"
pages = []

def get_next_page(page_actuelle):
    
    li = page_actuelle.find("li", class_="next")
    if li == None:
        return None
    url = li.find("a").get("href")
    url = url.split("/")[-1]
    url = base_url + url 
    return url

while True:
    pages.append(page_actuelle)
    html_doc = requests.get(page_actuelle).text
    soup = BeautifulSoup(html_doc, "html.parser")
    page_suivante = get_next_page(soup)
    if page_suivante == None:
        break
    page_actuelle = page_suivante 
    
pprint(pages)

book_urls = []

def get_book_urls(page_actuelle):
    urls = []
    articles = page_actuelle.find_all("article", class_="product_pod")
    for article in articles:
        a = article.find("h3").find("a")
        url = a.get("href")
        url = url.split("catalogue/")[-1]
        url = base_url + url 
        urls.append(url)
    return urls

for page in pages:
    html_doc = requests.get(page).text
    soup = BeautifulSoup(html_doc, "html.parser")
    urls = get_book_urls(soup)
    book_urls.extend(urls)

pprint(book_urls)


books = []
def get_book_content(book_url):
    html_doc = requests.get(book_url).text
    soup = BeautifulSoup(html_doc, "html.parser")
    note_str = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    
    titre = soup.find("div", class_="product_main").find("h1").text.strip()
    categorie = soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()
    try:
        image = soup.find(id="product_gallery").find("img").get("src")
        image_url = base_url + image.split("../../")[-1]
    except:
        image = ""
    try:
        description_titre = soup.find(id="product_description")
        description = description_titre.find_next_sibling("p").text.strip()
    except:
        description = ""
    try:
        prix = soup.find("p", class_="price_color").text.strip()
    except:
        prix = ""
    
    try:
        note = soup.find("p", class_="star-rating").get("class")[-1]
        note = note_str[note]
    except:
        note = 0
    
    return {
        "Titre":titre,
        "Categorie":categorie, 
        "Description":description, 
        "Prix":prix, 
        "Note":note, 
        "Image":image_url
    }
for url in book_urls:
    try:
        book = get_book_content(url)
        books.append(book)
    except:
        print("Livre sans titre ou catégorie")
    

pprint(books)

import pandas as pd

df = pd.DataFrame(books)
df.to_excel("books.xlsx")




