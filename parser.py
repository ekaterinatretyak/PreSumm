from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from requests import ConnectionError
import csv
import urllib
import re
import requests
import time
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-setuid-sandbox")

driver = webdriver.Chrome(ChromeDriverManager().install())

def get_html(url):
    page = requests.get(url)
    page.encoding = 'utf-8'
    print(page.status_code)
    print(scrolling(url))

def scrolling(url):
    driver.get(url)
    count = 1500
    while count:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            button = WebDriverWait(driver, 100).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'button-outline')))
            button.click()
            count -= 1
            time.sleep(3)

        except Exception as e:
            print(f'Error {e}', count)
            time.sleep(5)
    parsing(driver.page_source)

def parsing(page_text):
    soup = BeautifulSoup(page_text, 'html.parser')
    news = soup.findAll('a', 'text-marker' == 'Новость') and soup.findAll(class_='stream-item__title')

    for i in range(len(news)):
        links = []
        dates = []
        titles = []
        articles = []
        article_text = ''

        link = news[i]['href']
        links.append(link)
        try:
            article_page = requests.get(link, timeout=15) #.text
            soup2 = BeautifulSoup(article_page.content, 'html.parser')
        except requests.exceptions.ConnectionError:
            print("Let me sleep for 5 seconds")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
        except requests.exceptions.ReadTimeout:
            print("\n Переподключение к серверам \n")
            time.sleep(5)
        try:
            date = soup2.find('a', "headline__date--link").text or soup2.find('span', class_='headline__date').text
            title = soup2.find('h1', class_='text-title__title').text
            article_text = soup2.find('div', class_='r-text-content js-article-text').text
        except AttributeError:
            pass

        date = bytes(date, 'utf-8').decode('utf-8','ignore')
        dates.append(date.strip())
        title = bytes(title, 'utf-8').decode('utf-8', 'ignore')
        titles.append(title.strip())
        articles.append(article_text)

        res = list(zip(links, dates, articles, titles))
        write_csv(res)
        print("News for {}:".format(date), res)

def write_csv(corpus):
    with open('.../bumaga.csv', 'a', newline='', errors='ignore', encoding='utf-8') as file:
        csv_writer = csv.writer(file, delimiter=',')
        csv_writer.writerows(corpus)

if __name__ == "__main__":
    url = "https://paperpaper.ru/category/news/"
    get_html(url)