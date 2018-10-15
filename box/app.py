import os
import requests
import numpy as np
import pandas as pd
import time
import re
import shutil
from PIL import Image
from splinter import Browser
from bs4 import BeautifulSoup as bs

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)      

def scrape():
    browser = init_browser()

# News Title
    url_mars_news = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    response = requests.get(url_mars_news)
    soup = bs(response.text, 'html.parser')
    # print(soup.prettify())
    # results = soup.find_all('li', class_="result-row")
    soup.find_all('div')
    news_title = soup.find_all('div', class_="content_title")[0].text.strip()
    news_p = soup.find_all('div', class_="rollover_description_inner")[0].text.strip()


# image
    url_mars_space_images = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_mars_space_images)
    html = browser.html
    soup = bs(html, 'html.parser')
    image = soup.find("article", class_="carousel_item")["style"]
    urls = re.findall("url\((.*?)\)", image)
    urls = ''.join(urls)
    url_img = urls[1:-1]

    featured_image_url = "https://jpl.nasa.gov" + url_img
    im = Image.open(requests.get(featured_image_url, stream=True).raw)


# Weather

    url_mars_twitter = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_mars_twitter)
    html = browser.html
    soup = bs(html, 'html.parser')
    mars_weather = soup.find(string=re.compile("Sol"))

# Mars Facts

    url_mars_facts = "http://space-facts.com/mars/"
    browser.visit(url_mars_facts)

    df = pd.read_html(url_mars_facts)
    mars_data = pd.DataFrame(df[0])
    mars_data.columns = ['Mars','Info']
    mars_table = mars_data.set_index("Mars").to_html(classes='marsdata').replace('\n', ' ')
    mars_table

# Mars Hemispheres Photos

    url_mars_hemi = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_mars_hemi)

    hemisphere_image_urls = []
    for i in range (4):
        time.sleep(3)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = bs(html, 'html.parser')
        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        hemi_data = {"title":img_title,"img_url":img_url}
        hemisphere_image_urls.append(hemi_data)
        browser.back()