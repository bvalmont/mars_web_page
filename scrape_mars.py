from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import cssutils



def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome",**executable_path, headless=False)

mars_data = {}

def scrape_mars_headlines():

    browser = init_browser()
    url='https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")

    headlines = soup.find('div', class_='image_and_description_container')
    news_title = headlines.find('div', class_='content_title').text
    news_p = headlines.find('div', class_='article_teaser_body').text

    mars_data['news_title'] = news_title
    mars_data['news_paragraph'] = news_p

    return mars_data

    browser.quit()

def scrape_image_url():

    browser = init_browser()

    url4 = 'https://www.jpl.nasa.gov/spaceimages/'
    browser.visit(url4)

    html_image = browser.html
    soup = bs(html_image, 'html.parser')

    div_style = soup.find('article')['style']
    div_style
    style = cssutils.parseStyle(div_style)
    url5 = style['background-image']
    url5 = url5.replace('url(', '').replace(')', '').replace('/spaceimages/','')

    featured_image_url =(url4 + url5)

    mars_data['featured_image_url'] = featured_image_url

    return mars_data

    browser.quit()

def scrape_weather():

    browser = init_browser()
    
    url2=('https://twitter.com/marswxreport?lang=en')
    browser.visit(url2)

    html_weather = browser.html
    soup = bs(html_weather, 'html.parser')

    mars_tweet = soup.find('div', class_='js-tweet-text-container')
    mars_weather = mars_tweet.find('p').text

    mars_data['mars_weather'] = mars_weather

    return mars_data

    browser.quit()

def scrape_facts():

    browser = init_browser()
    url3 = 'https://space-facts.com/mars/'
    browser.visit(url3)

    html_facts = browser.html
    soup = bs(html_facts, 'html.parser')

    tables = pd.read_html(url3)
    mars_table =tables[1]

    mars_table.columns = ['description', 'value']
    mars_table.set_index('description', inplace=True)

    mars_html_table = mars_table.to_html()
    mars_html_table2 = mars_html_table.replace('\n', '')

    mars_data['mars_facts'] = mars_html_table2

    return mars_data

    browser.quit()

def scrape_hemispheres():

    browser = init_browser()
    mars_hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemispheres_url)

    html_marshemispheres = browser.html
    soup = bs(html_marshemispheres, 'html.parser')
    information = soup.find_all('div', class_='item')
    marshemisphere_image_urls = []
    base_url = 'https://astrogeology.usgs.gov'
    for info in information: 
        title = info.find('h3').text
        partial_img_url = info.find('a', class_='itemLink product-item')['href']
    
        browser.visit(base_url + partial_img_url)
        partial_img_html = browser.html
    
        soup = bs( partial_img_html, 'html.parser')
        img_url = base_url + soup.find('img', class_='wide-image')['src']
    
        marshemisphere_image_urls.append({"title" : title, "img_url" : img_url})

    mars_data['hemispheres'] = marshemisphere_image_urls

    return mars_data

    browser.quit()


    






















