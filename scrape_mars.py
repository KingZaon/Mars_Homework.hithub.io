#!/usr/bin/env python
# coding: utf-8

# In[24]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
from splinter import Browser
from pprint import pprint
from time import sleep

def scrape():
# In[25]:


    executable_path = {'executable_path': 'C:/Users/mo610/Downloads/chromedriver75/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


# In[26]:


#Run the funcition below:

    news_title, news_p = mars_news(browser)

#Run the functions below and store in dictionary

    results = {
        "title": news_title,
        "paragraph": news_p,
        "image_url": jpl_image(browser),
        "facts": mars_facts,
        "hemispheres": mars_hemisphere(browser),
    }

#Quite the browser and return the scraped results

    browser.quit()
    return results

def mars_news(browser):
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    mars_news_soup = BeautifulSoup(html, 'html.parser')

    #Scrape the first article title and teaser paragraph text; return them
    news_title = mars_news_soup.find('div', class_='content_title').text
    news_p = mars_news_soup.find('div', class_='article_teaser_body').text
    return news_title, news_p

def jpl_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    #Go to 'FULL NAME' then to 'mroe info'
    browser.click_link_by_partial_text('FULL NAME')
    sleep(1)
    browser.click_link_by_partial_text('more info')

    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')

    #Scrape the URL and return
    feat_img_url = image_soup.find('figure', class_='lede').a['href']
    feat_img_full_url = f'https://jpl.nasa.gov{feat_img_url}'
    return feat_img_full_url

def mars_weather_tweet(browser):
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    tweet_soup = BeautifulSoup(html, 'html.parser')

    #Scrape the tweet info and return
    first_tweet = tweet_soup.find('p', class_='TweetTextSize').text
    return first_tweet

def mars_facts():
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    mars_info = tables[0]
    mars_info.columns = ['Property', 'Value']
    #Set index to property in preparation for import into mongodb
    return mars_info.to_html()

def mars_hemisphere(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    hemisphere_soup = BeautifulSoup(html, 'html.parser')

    hemi_strings = []
    links = hemisphere_soup.find_all('h3')

    for hemisphere in links:
        hemi_strings.append(hemisphere.text)

    # Initialize hemisphere_image_urls list
    hemisphere_image_urls = []

    # Loop through the hemisphere links to obtain the images
    for hemisphere in hemi_strings:
        # Initialize a dictionary for the hemisphere
        hemisphere_dict = {}

        # Click on the link with the corresponding text
        browser.click_link_by_partial(hemisphere)

        # Click the image url string and store into the dictionary
        hemisphere_dict["img_url"] = browser.find_by_text('Sample')['href']

        # The hemisphere title is already in hemi_strings, so store it into the dictionary
        hemisphere_dict["title"] = hemisphere
        # Add the dictionary to hemisphere_image_urls
        hemisphere_image_urls.append(hemisphere_dict)

        # Check for output
        pprint(hemisphere_image_urls)

        # Click the 'Back' Button
        browser.click_link_by_partial_text('Back')

    return hemisphere_image_urls

