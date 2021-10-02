import time

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

from shared.scraper import Scraper
from shared.selenium import get_driver

class CNNScraper(Scraper):
    def __init__(self, date_str, channel, category, driver, **kwargs):
        super().__init__(**kwargs)
        self.website = "cnn"
        self.date_str = date_str
        self.channel = channel
        self.category = category
        self.driver = driver

    def extract_info(self, current_url, page):
        # Get page generate all news
        driver = get_driver()
        driver.get(current_url)

        while(1):
            try:
                load_more = driver.find_element_by_class_name("btn__more")
                load_more.click()
                print("Add more result by clicking 'Selanjutnya' button")
                time.sleep(5)
            except NoSuchElementException as e:
                break
            except ElementClickInterceptedException as e:
                break

        new_page = BeautifulSoup(driver.page_source, "lxml")
        driver.quit()

        # Extract all news info
        article_list = new_page.find("div", class_="media_rows").find_all("article")

        list_of_info = []
        for article in article_list:
            info = {
                "title": article.find("h2", class_="title").text,
                "website": self.website,
                "channel": self.channel,
                "category": self.category,
                "native_category": article.find("span", class_="kanal").text,
                "url": article.find("a").get("href"),
                "publish_dt": self.date_str
            }
            list_of_info.append(info)

        return list_of_info