from bs4 import BeautifulSoup as soup
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# visit the Mars NASA news site
url = 'https://redplanetscience.com'
browser.visit(url)

# optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# set up the HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

# use the parent element to find the first 'a' tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()

# use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

# Featured images
# visit url
spaceimages_url = 'https://spaceimages-mars.com'
browser.visit(spaceimages_url)

# find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# parsing the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# use the base url to create an absolute url
img_url = f'{spaceimages_url}/{img_url_rel}'
img_url

# Mars Facts
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns = ['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)

# convert DataFrame back into HTML-ready code
df.to_html()

# quit the browser session
browser.quit()