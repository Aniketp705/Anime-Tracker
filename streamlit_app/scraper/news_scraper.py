
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os
import sys

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import anime_news


def fetch_and_store_news():
    anime_news.create_table()

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service('scraper/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get('https://www.cbr.com/category/anime-news/')
    time.sleep(1)

    try:
        main_container = driver.find_element(By.CLASS_NAME, 'sentinel-listing-page-list')
        articles = main_container.find_elements(By.CSS_SELECTOR, '.w-display-card-content.regular.article-block')

        for i, article in enumerate(articles, start=1):
            if i > 10:
                break
            try:
                link_element = article.find_element(By.CSS_SELECTOR, 'a[href]')
                title = link_element.text.strip()
                link = link_element.get_attribute('href')
                anime_news.add_news(title, "", link)
            except Exception as e:
                print("Error reading article:", e)

    finally:
        driver.quit()


fetch_and_store_news()