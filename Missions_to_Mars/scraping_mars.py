from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import time

# Set Executable Path & Initialize Chrome Browser

def init_browser():

    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path)


def mars_news():

    
    # URL of page to be scraped"
    url = 'http://mars.nasa.gov/news/'

    browser = init_browser()
    browser.visit(url)

    time.sleep(10)
 
  

    # Create BeautifulSoup object; parse with 'html.parser
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    li_element = soup.select_one("ul.item_list li.slide")
    li_element.find("div", class_="content_title")

    news_title = li_element.find("div", class_="content_title").get_text()

    news_p = li_element.find("div", class_="article_teaser_body").get_text()

    browser.quit()
    
    return news_title, news_p

def mars_image():

    

    jpl_url = 'http://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser = init_browser()

    browser.visit(jpl_url)

    time.sleep(5)
    # Asking Splinter to Go to Site and Click Button with name full_image

    browser.find_by_id("full_image").click()

    time.sleep(5)
    

    browser.find_link_by_partial_text("more info").click()
 
    time.sleep(5)

    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # Retrieve current fetured mars image
    mars_image = soup.find('figure', class_='lede')
    img_url= mars_image.find('a')['href']
 
    new_url = '/'.join(jpl_url.split('/')[:3])
    featured_image_url = f'{new_url}{img_url}'

    browser.quit()
    return featured_image_url


def mars_weather():
    
    url = 'http://twitter.com/marswxreport?lang=en'

    browser = init_browser()
    browser.visit(url)
    time.sleep(5)

    html1 = browser.html
    # Parse HTML with Beautiful Soup
    soup1 = BeautifulSoup(html1, 'html.parser')
    # Retrieve mars tweet section
    mars_tweet_section = soup1.find('section', role='region')
   
    # Use Beautiful Soup's find() method to navigate and retrieve mars weather tweet
 
    mars_span= mars_tweet_section.find_all('span')[4].text
    mars_weather=','.join(mars_span.splitlines())

    browser.quit()
    return mars_weather

def  mars_fact_table():

    url = 'https://space-facts.com/mars/'
    df = pd.read_html(url)[0]
     
    df.columns=["Description", "Value"]
    df.set_index("Description", inplace=True)
    facts_table = df.to_html(header = True, index = True)

    return facts_table

def hemisphereImage():

    

    url='http://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser = init_browser()
    browser.visit(url)
       
    hemisphere_image_urls = []
   
    # Get a List of All the Hemispheres
    links = browser.find_by_css("a.product-item h3")

    for item in range(len(links)):
        hemispheres = {}
   
        # Find link to click",
        browser.find_by_css("a.product-item h3")[item].click()
   
         # Get Hemisphere Title
        hemispheres["title"] = browser.find_by_css("h2.title").text
 
        # Find Sample Image Anchor Tag & Extract <href>",
        sample = browser.links.find_by_text("Sample").first
        hemispheres["img_url"] = sample["href"]
    
        # Append Hemisphere Object to List
        hemisphere_image_urls.append(hemispheres)
    
        # Navigate Backwards
        browser.back()
        
        
    browser.quit()
    return hemisphere_image_urls



def scrape():

    
    mars_facts = mars_fact_table()
    mars_data ={}
    news_title, news_p = mars_news()
    mars_data['news_title']= news_title
    mars_data['news_p']= news_p
    mars_data['featured_image_url'] = mars_image()
    mars_data['mars_weather'] = mars_weather()
    mars_data['mars_facts']=mars_facts
    mars_data["mars_hemispheres"] = hemisphereImage()

   

    return mars_data



  