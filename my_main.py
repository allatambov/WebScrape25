import re
import requests
import pandas as pd

from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

def get_cards(html):
    soup = BeautifulSoup(html, "lxml")
    cards = soup.find_all("div", class_ = "card")
    return cards
    
def get_info(item):
    img = item.find("img")
    name = img.get("alt")
    image_link = img.get("src")
    price = item.find("div", class_ = "price_item_block").text
    link = item.find("a", class_ = "img-wrapper-index").get("href")
    return name, price, link, image_link
    
def scrape_to_table(key, sorting):

    br = wd.Chrome()
    br.maximize_window()

    br.get("https://www.biblio-globus.ru/")
    br.implicitly_wait(5)

    search = br.find_element(By.ID, "SearchBooks")
    search.send_keys(key)
    br.implicitly_wait(2)

    search.send_keys(Keys.ENTER)
    br.implicitly_wait(2)

    options = br.find_element(By.TAG_NAME, "select")
    options.send_keys(sorting)
    tick = br.find_element(By.CLASS_NAME, "custom-control-label")
    tick.click()
    br.implicitly_wait(2)

    html = br.page_source
    soup = BeautifulSoup(html)
    cards = soup.find_all("div", class_ = "card")
    
    last_page = br.find_element(By.PARTIAL_LINK_TEXT, "»»")
    last_href = last_page.get_attribute("href")
    last_n = int(re.search("page=(\d+)", last_href).group(1))

    full_res = cards.copy()

    for i in range(0, last_n - 1):
        next_page = br.find_element(By.PARTIAL_LINK_TEXT, "»")
        next_page.click()
        br.implicitly_wait(2)
        html = br.page_source
        cards_to_add = get_cards(html)
        full_res.extend(cards_to_add)
    
    full_clean = []

    for item in full_res:
        if len(item.get("class")) == 1:
            full_clean.append(item)
        
    L = [get_info(item) for item in full_clean]
    df = pd.DataFrame(L)
    df.columns = ["title", "price", "link", "image_link"]
    df["price"] = df["price"].str.strip(" ₽").astype(int)
    df.to_csv("BG_LAST.csv")
