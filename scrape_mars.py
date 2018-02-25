
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests as rq
from splinter import Browser
from flask import Flask, render_template
from flask import jsonify

import pymongo

def scrape():
    executable_path = {'executable_path':'chromedriver'}
    browser = Browser('chrome', **executable_path)
    browser.visit("https://mars.nasa.gov/news/")

    html_file = browser.html
    soup5 = bs(html_file, "html.parser")
    news_title = soup5.find("div", class_ = "content_title").text
    news_p = soup5.find("div", class_ = "article_teaser_body").text

    # response = rq.get("https://mars.nasa.gov/news/")
    # soup = bs(response.text, "html.parser")
    # news_title = soup.find("div", class_ = "content_title").text
    # news_p = soup.find("div", class_ = "article_teaser_body").text

    #Mars space images
    browser.visit("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")
    n_file = browser.html
    soup2 = bs(n_file, "html.parser")
    img_file = soup2.find("img", class_ = "thumb")
    featured_image_url = "https://www.jpl.nasa.gov"+img_file["src"]

    #mars weather
    url = "https://twitter.com/marswxreport?lang=en"
    response = rq.get(url)
    soup3 = bs(response.text, "html.parser")
    weather = soup3.find("div", class_ = "js-tweet-text-container").text
    weather = weather.replace("\n", "")

    #Mars facts
    tables = pd.read_html("https://space-facts.com/mars/")
    df = tables[0]
    df.columns = ['Attributes', "Values"]
    table  = df.to_html("table.html")

    #Mars Hemispheres
    valles_url = "https://astrogeology.usgs.gov/cache/images/8981a6d7057a7634dc312c0448f462c1_valles_marineris_unenhanced.tif_full.jpg"
    cerber_url = "https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg"
    schia_url = "https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg"
    syrt_url = "https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg"

    hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": valles_url},
    {"title": "Cerberus Hemisphere", "img_url": cerber_url},
    {"title": "Schiaparelli Hemisphere", "img_url": schia_url},
    {"title": "Syrtis Major Hemisphere", "img_url": syrt_url},
    ]

    mars_data = {
        "News title": news_title,
        "Description": news_p,
        "Featured Mars Image": featured_image_url,
        "weather": weather,
        "Table": table,
        "Hemisphere img": hemisphere_image_urls,
    }
    return mars_data
print(scrape())
