from selenium import webdriver
import os
import time
import urllib.request
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

logging.basicConfig(filename='output.log',level=logging.DEBUG)

google = 'https://www.google.com/search?q=<YOUR_GOOGLE_PAGE_SUBQUERY_HERE>'
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
		filename = '/' + '<ITERABLE_FILE_NAME_HERE>' + str(count) + '.png'
		count += 1
		imgurl = image.find_elements_by_tag_name('a')[0]
		boi = imgurl.get_attribute('href')
		imgurl.send_keys(Keys.COMMAND + Keys.RETURN)
		driver.switch_to_window(driver.window_handles[-1])
		driver.get(boi)
		imagefile = os.getcwd() + directory + filename
		urllib.request.urlretrieve(boi, imagefile)
		driver.close()
		driver.switch_to_window(main_window)
	driver.quit

scrape()
