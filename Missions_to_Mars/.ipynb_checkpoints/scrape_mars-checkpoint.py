from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import pandas as pd


def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_dict = {}
    
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    mars_dict["news title"] = soup.find('div', class_= 'content_title').get_text()
    mars_dict["news p"] = soup.find('div', class_='article_teaser_body').get_text()
    
    ###
    space_images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(space_images_url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    browser.links.find_by_partial_text('FULL IMAGE').click()
    browser.links.find_by_partial_text('more info').click()

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    featured_img = soup.find('figure', class_='lede').a['href']
    mars_dict["featured image url"] ='https://www.jpl.nasa.gov' + featured_img

    mars_facts_url = ('https://space-facts.com/mars/')
    mars_facts=pd.read_html(mars_facts_url)

    df = mars_facts[0]
    df.columns = ["",""]

    mars_dict["facts html string"] = df.to_html()
 
    ###
    browser = init_browser()
    mars_hemi_url ='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    browser.visit(mars_hemi_url)

    images = soup.find_all('div', class_='item')

    hemisphere_img_urls = []
    base_url = "https://astrogeology.usgs.gov"

    for image in images:
        image_url = image.find('a',class_='itemLink product-item')['href']
        title = image.h3.text

        browser.visit(base_url + image_url)
        html = browser.html
        soup = BeautifulSoup(html,'html.parser')

        img_url = base_url + soup.find('img', class_='wide-image')['src']
        hemisphere_img_urls.append({'title':title,'img_url':img_url})

    mars_dict["hemisphere img urls"] = hemisphere_img_urls
    
    return mars_dict
