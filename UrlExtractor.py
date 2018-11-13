import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome("D:\chromedriver.exe")
driver.implicitly_wait(30)
# driver.maximize_window()

WEBSITE_NAME = "https://www.youtube.com"
SEARCH_QUERY = "healthy living"
SEARCH_QUERY = SEARCH_QUERY.replace(" ", "+")
driver.get(f'{WEBSITE_NAME}/results?search_query={SEARCH_QUERY}')
urls = []
breaker = 0
while True:

    breaker += 1
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    result_set = soup.find_all('a', href=True, id="thumbnail")
    print(len(result_set))
    if len(urls) < len(result_set):

        for a in result_set:
            href = a['href']
            if "/watch?v=" in href:
                if WEBSITE_NAME not in href:
                    href = WEBSITE_NAME + href
                if href not in urls:
                    breaker = 0
                    urls.append(href)
                    print(f"Total list size: {len(urls)}")
    print(f"breaker:{breaker}")

    if breaker > 20:
        break
    elem = driver.find_element_by_tag_name('a')
    elem.send_keys(Keys.PAGE_DOWN)

driver.close()

data = pd.DataFrame(urls)
print(data.head)
data.to_csv(f'{SEARCH_QUERY}_urls.csv')
print('created')