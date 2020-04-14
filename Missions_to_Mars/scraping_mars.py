from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import time

def init_browser():

    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():


    mars_data ={}

    mars_data['news']= mars_news()
    mars_data['featured_image_url'] = mars_image()
    mars_data['mars_weather'] = mars_weather()
    mars_data['mars_fact']=mars_fact_table()
    mars_data["mars_hemispheres"] = hemisphereImage()

    return mars_data

def mars_news():

    browser = init_browser()

    # URL of page to be scraped\n"
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(2)
 
    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser
    soup = BeautifulSoup(response.text, 'html.parser')

    news ={}

    # Extract latest news title text
    results = soup.find('div', class_='content_title')
    news_title = results.a.text.strip()

    # Extract latest paragraph text
    paragraph = soup.find('div', class_='image_and_description_container')
    news_p = paragraph.a.text.strip()
    
    news['news_title'] = news_title
    news['paragraph_text'] = news_p

    browser.quit()
    time.sleep(5)
    return news

def mars_image():

    browser = init_browser()

    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(jpl_url)

    time.sleep(2)
    # Asking Splinter to Go to Site and Click Button with name full_image

    browser.find_by_id("full_image").click()

    browser.links.find_by_partial_text("more info").click()
 
    
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # Retrieve current fetured mars image
    mars_image = soup.find('figure', class_='lede')
    img_url= mars_image.find('a')['href']
 
    new_url = '/'.join(url.split('/')[:3])
    featured_image_url = f'{new_url}{img_url}'


    browser.quit()
    time.sleep(5)

    return featured_image_url


def mars_weather():

    browser = init_browser()
  
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(2)
    html1 = browser.html
    # Parse HTML with Beautiful Soup
    soup1 = BeautifulSoup(html1, 'html.parser')
    # Retrieve mars tweet section
    mars_tweet_section = soup1.find('section', role='region')
   
    # Use Beautiful Soup's find() method to navigate and retrieve mars weather tweet
 
    mars_span= mars_tweet_section.find_all('span')[4].text
    mars_weather=','.join(mars_span.splitlines())


    browser.quit()
    time.sleep(5)
   
    return mars_weather

def  mars_fact_table():

    browser = init_browser()

    url = 'https://space-facts.com/mars/'

    browser.visit(url)
    time.sleep(2)
    # HTML object
    html2= browser.html\
    # Parse HTML with Beautiful Soup
    soup2 = BeautifulSoup(html2, 'html.parser')
    # Retrieve mars fact table
    mars_fact_table = soup2.find('table', class_='tablepress tablepress-id-p-mars')
    
    keys=[]
    values=[]
    mars_table_col_1 = mars_fact_table.find_all(class_='column-1')
    mars_table_col_2 = mars_fact_table.find_all(class_='column-2')

    for num in range(9):
        keys.append(mars_table_col_1[num].text)
        values.append(mars_table_col_2[num].text)
  
  
    table_df = pd.DataFrame(values,keys),
    facts_table = table_df.to_html(header=False, index=False)

    browser.quit()
    time.sleep(5)

    return facts_table

def hemisphereImage():

    browser = init_browser()

  
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(2)
   
    hemisphere_image_urls = []
   
    # Get a List of All the Hemispheres
    links = browser.find_by_css("a.product-item h3")

    for item in range(len(links)):
        hemispheres = {}
   
        # Find link to click\n",
        browser.find_by_css("a.product-item h3")[item].click()
   
         # Get Hemisphere Title
        hemispheres["title"] = browser.find_by_css("h2.title").text
 
        # Find Sample Image Anchor Tag & Extract <href>\n",
        sample = browser.links.find_by_text("Sample").first
        hemispheres["img_url"] = sample["href"]
    
        # Append Hemisphere Object to List
        hemisphere_image_urls.append(hemispheres)
    
        # Navigate Backwards
        browser.back()


        browser.quit()
        time.sleep(5)


    return hemisphere_image_urls







  