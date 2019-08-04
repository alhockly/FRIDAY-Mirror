from selenium import webdriver



driver = webdriver.Firefox()
driver.get('http://raspberrypi.stackexchange.com/')
driver.quit()