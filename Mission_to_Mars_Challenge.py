#!/usr/bin/env python
# coding: utf-8

# In[32]:


#import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[33]:


#set your executable path in the next cell, then set up the URL
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


#HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[7]:


# slide_elemvariable holds a ton of information, so look inside of that information to find this specific data
slide_elem.find('div', class_='content_title')


# In[8]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[9]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[10]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[12]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[13]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[14]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[15]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[17]:


#Instead of scraping each row, or the data in each <td />, 
#we're going to scrape the entire table with Pandas' .read_html() function.
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[18]:


#converting df to html
df.to_html()


# In[3]:


#shut off browser
browser.quit()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# 
# ### Hemispheres

# In[41]:


# 1. Use browser to visit the URL 
url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/index.html'

browser.visit(url)


# In[51]:


hemisphere_image_urls = []

# Find number of image links
img_link = browser.find_by_css('a.product-item img')

# Parse HTML with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# 3. Write code to retrieve the image urls and titles for each hemisphere.

for i in range(len(img_link)):
    
    hemispheres = {}
    
    browser.find_by_css('a.product-item img')[i].click()
    
    img = browser.links.find_by_text('Sample').first
    
    hemispheres['img_url'] = img['href']
    
    hemispheres['title'] = browser.find_by_css("h2.title").text
    
    hemisphere_image_urls.append(hemispheres)
    
    browser.back()


# In[52]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[54]:


#shut off browser
browser.quit()


# In[ ]:





# In[ ]:





# In[ ]:




