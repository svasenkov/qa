# author: Vasenkov Stanislav
# telegram: @iTerkin
#
# simple selenium script: go to page, fill forms, press buttons

import random
from string import letters
from string import digits
from time import sleep

from selenium import webdriver
from selenium.webdriver.support.ui import Select


DOWNLOAD_LINK = "https://smartbear.com/product/testcomplete/free-trial/"

print 'opening ' + DOWNLOAD_LINK + ' in FireFox...'


def get_random(data_type, data_length):
    return "".join([random.choice(data_type) for i in xrange(data_length)])


driver = webdriver.Firefox()
driver.get(DOWNLOAD_LINK)

elem = driver.find_element_by_name("FirstName")
some_text = get_random(letters, 15)
elem.send_keys(some_text)

elem = driver.find_element_by_name("LastName")
some_text = get_random(letters, 15)
elem.send_keys(some_text)

elem = driver.find_element_by_name("Email")
some_text = '%s@%s.com' % (get_random(letters, 10), get_random(letters, 10))
elem.send_keys(some_text)

elem = Select(driver.find_element_by_name('Country'))
elem.select_by_value("Russian Federation")

elem = driver.find_element_by_name("Company")
some_text = get_random(letters, 12)
elem.send_keys(some_text)

elem = driver.find_element_by_name("Phone")
some_text = get_random(digits, 10)
elem.send_keys(some_text)

driver.find_elements_by_class_name("mktoButton")[0].click()

sleep(20)
elem = driver.find_element_by_id('dldlink')
href = elem.get_attribute("href")
print href

#driver.close()
