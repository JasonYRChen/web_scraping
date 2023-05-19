import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains


url = 'https://pythonscraping.com/pages/files/form.html'
with webdriver.Safari() as driver:
    driver.get(url)
    firstname = driver.find_element(By.NAME, 'firstname')
    lastname = driver.find_element(By.NAME, 'lastname')
    submit = driver.find_element(By.ID, 'submit')

    actions = ActionChains(driver) \
              .click(firstname).send_keys('hehe') \
              .click(lastname).send_keys('haha') \
              .click(submit)
    actions.perform()
    
    time.sleep(3)
    result = driver.find_element(By.TAG_NAME, 'body')
    print(result.text)
