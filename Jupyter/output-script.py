import bs4
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# %%
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

driver.get('https://liquipedia.net/leagueoflegends/World_Championship/2023')

time.sleep(3)

page_source = driver.find_element(By.TAG_NAME, 'body').get_attribute('outerHTML')

driver.quit()

# %%
page = bs4.BeautifulSoup(page_source)

# %%
spans = page.find_all('span', class_='team-template-text')

teams = []
for span in spans:
	teams.append(span.find('a').contents[0])


# %%
print(teams)