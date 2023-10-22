from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
from dotenv import load_dotenv
load_dotenv()
import time

# Open up a website
web_url = "https://www.youtube.com/watch?v=z-Ydrphhu34&ab_channel=JakeEh"

# Create an instance of the Chrome WebDriver
options = webdriver.ChromeOptions() # webdriver.FirefoxOptions(), ...
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs", prefs)
# options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# Open the web page
# driver.get(web_url)
# time.sleep(5)
# driver.quit()

# Get the views from the page

# XPath Target
# Basically the child elements count for each one - NOT 0 indexed

# target = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[4]/div[1]/div/div[1]/yt-formatted-string/span[1]"

# # Navigate to the YouTube channel page
# driver.get(web_url)
# time.sleep(1)

# wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
# # wait = FluentWait(driver, timeout=30, poll_frequency=5, ignored_exceptions=[NoSuchElementException])

# view_count_element = wait.until(EC.visibility_of_element_located((By.XPATH, target)))

# # Find the view count element
# # view_count_element = driver.find_element("xpath", target)
# view_count = int(view_count_element.text.replace(" views", "").replace(",", ""))

# print(view_count)

# print(driver.title[0:-10])

# driver.quit()
















# Login to a website

loginPath = "/html[1]/body[1]/shreddit-app[1]/reddit-header-large[1]/reddit-header-action-items[1]/header[1]/nav[1]/div[3]/span[3]/faceplate-tracker[1]/faceplate-tooltip[1]/a[1]/span[1]/span[1]"
username_input_id = "login-username"
password_input_id = "login-password"
web_url = "https://reddit.com"
driver.get(web_url)
wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds

login_element = wait.until(EC.visibility_of_element_located((By.XPATH, loginPath)))
login_element.click()

username_input = wait.until(EC.visibility_of_element_located((By.ID, username_input_id)))
# username_input.send_keys("Jake is Cool!")
username_input.send_keys("JakeEhTests")

password_input = wait.until(EC.visibility_of_element_located((By.ID, password_input_id)))
# password_input.send_keys("subscribe!123")
password_input.send_keys(os.getenv("REDDIT_PASSWORD"))

password_input.send_keys(Keys.ENTER)


time.sleep(10)
# Take a screenshot of the page

element = driver.find_element(By.XPATH, '/html/body')
element.screenshot('reddit.png')

driver.quit()

# Get the front page titles

posts = driver.find_elements(By.CSS_SELECTOR, 'h3._3wqmjmv3tb_k-PROt7qFZe')
for i in range(len(posts)):
    print(posts[i].get_attribute('textContent')) # .text only returns text for elements that are visible

driver.quit()















# # Get both the text and the URL to the post

# posts_parent = driver.find_elements(By.CSS_SELECTOR, 'a.SQnoC3ObvgnGjWt90zD9Z')

# for i in range(len(posts_parent)):
#     print(posts_parent[i].get_attribute('href'))
#     print(posts_parent[i].find_element(By.CSS_SELECTOR, 'h3._3wqmjmv3tb_k-PROt7qFZe').get_attribute('textContent'))

# print('done')

# time.sleep(15)

# driver.quit()


















# Log prices

web_url = "https://www.amazon.ca/Skyward-Brandon-Sanderson/dp/0399555773/ref=tmm_hrd_swatch_0?_encoding=UTF8&qid=&sr="
price_xpath = "/html[1]/body[1]/div[2]/div[1]/div[3]/div[1]/div[4]/div[4]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/h5[1]/div[2]/div[1]/div[1]/div[1]/span[1]/span[2]"

driver.get(web_url)
wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds

price = wait.until(EC.visibility_of_element_located((By.XPATH, price_xpath)))

print(price.text)
print(float(price.text[1:]))
print(float(price.text[1:]) + 2.1)

driver.quit()


