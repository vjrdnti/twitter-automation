from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import pandas as pd


options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')


def scrape_tweets(url):
    # Open the Twitter account page
    driver2 = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver2.get(url)
    i=14
    user = ""
    while True:
        if str(url)[i] != '/':
            user+= str(url)[i]
            i+=1
        else:
            break
        
    # Allow time for the page to load
    time.sleep(3)

    # Get the page source and parse it with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Find all tweets
    text_obj = soup.find('div', {'data-testid': 'tweetText'})
    article_obj = soup.find('article')
    text = ""
    spans = text_obj.find_all('span')
    for span in spans:
        text+= " " + span.text
    t = article_obj.find('time')
    driver2.quit()
    return text,t.text,user


if __name__=="__main__":
    users = ['ugc_india', 'ncert', 'NTA_Exams', 'EduMinOfIndia']
    data = []
    for user in users:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        user_url = f'https://twitter.com/{user}'
        driver.get(user_url)

        time.sleep(3)

        body = driver.find_element(By.CSS_SELECTOR, 'body')
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)

        tweets = driver.find_elements(By.XPATH, '//article[@role="article"]')

        tweet_links = []
        for tweet in tweets[:3]:
            link = tweet.find_element(By.XPATH, './/time/parent::a').get_attribute('href')
            tweet_links.append(link)

        
        for linkt in tweet_links:
            text,time_stamp,user = scrape_tweets(linkt)
            row = {'user': user, 'text': text, 'time': time_stamp, 'link': linkt}
            data.append(row)
    df = pd.DataFrame(data)
    driver.quit()
    df.to_csv('./tweets.csv')
    
