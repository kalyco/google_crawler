from selenium import webdriver
import os
import time
import urllib.request
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
   'Accept-Encoding': 'none',
   'Accept-Language': 'en-US,en;q=0.8',
   'Connection': 'keep-alive'
}
logging.basicConfig(filename='output.log',level=logging.DEBUG)

google = 'https://www.google.com/search?q=<INSERT_SUBSEARCH_HERE>'
directory = '/images'

def setUp():
	options = webdriver.ChromeOptions()
	# options.add_argument('headless')
	driver = webdriver.Chrome(chrome_options=options)
	driver.set_window_size(1120, 550)
	driver.get(google)

	return driver

def scrape():
	driver = setUp()
	page = driver.find_element(By.ID, 'isr_mc')
	images = page.find_elements(By.CLASS_NAME, 'rg_bx')
	main_window = driver.current_window_handle
	count = 0
	for image in images:
		filename = '/' + '<ITERABLE_IMG_TITLE>' + str(count) + '.jpg'
		count += 1
		imgurl = image.find_elements_by_tag_name('a')[0]
		boi = imgurl.get_attribute('href')
		imgurl.send_keys(Keys.COMMAND + Keys.RETURN)
		driver.switch_to_window(driver.window_handles[-1])
		driver.get(boi)
		img = driver.find_elements(By.CLASS_NAME, 'irc_mi')[1]
		img_src = img.get_attribute('src')
		print(img_src)
		imagefile = os.getcwd() + directory + filename
		driver.save_screenshot(os.getcwd() + directory + filename)
		request_=urllib.request.Request(img_src,None,headers) #The assembled request
		response = urllib.request.urlopen(request_)# store the response
		f = open(imagefile, 'wb')
		f.write(response.read())
		driver.close()
		driver.switch_to_window(main_window)
	driver.quit

scrape()
