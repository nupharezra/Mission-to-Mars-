#import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt
import time


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    
    #tells Python that we'll be using our mars_news function to pull this data.
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }
    
    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #HTML parser
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('div.list_text')
        
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

# ## JPL Space Images Featured Image
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# ## Mars Facts
def mars_facts():
    try:
        #Instead of scraping each row, or the data in each <td />, 
        #we're going to scrape the entire table with Pandas' .read_html() function.
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)


    ## Convert dataframe into HTML format, add bootstrap
    return df.to_html()

def hemispheres(browser):
    # visit URL
    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url5)
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    for i in range(4):
        #hemispheres = {}
        browser.find_by_css('a.product-item h3')[i].click()
        #find_pic = browser.find_link_by_text('Sample').first
       # img_url = find_pic['href']
        #header = browser.find_by_css("h2.title").text
        #hemispheres["img_url"] = img_url
        #hemispheres["title"] = header
        hemisphere_data = scrape_hemisphere(browser.html)
        hemisphere_image_urls.append(hemisphere_data)
        browser.back()
    return hemisphere_image_urls

def scrape_hemisphere(html_text):
    #parse the text
    hemisphere_soup = soup(html_text, "html.parser")
    # add try and except for error handling
    try:
        hem_title = hemisphere_soup.find("h2", class_="title").get_text()
        hem_sample = hemisphere_soup.find("a", text="Sample").get("href")
    except AttributeError:
        hem_title = None
        hem_sample = None

    hemispheres = {"title": hem_title, "img_url": hem_sample}

    return hemispheres



if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())



