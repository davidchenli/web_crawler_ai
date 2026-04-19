import re
import time

from concurrent.futures import as_completed
from concurrent.futures import ThreadPoolExecutor

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class Crawler:

    def __init__(self, target_url: str):
        self.url = target_url

    @staticmethod
    def get_chrome_options():
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--blink-settings=imagesEnabled=false")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.page_load_strategy = 'eager'
        return chrome_options

    @staticmethod
    def parse_is_within_12_hours(update_time_str):
        try:
            if "分鐘" in update_time_str:
                return True
            if "小時" in update_time_str:
                hours = int(re.search(r'\d+', update_time_str).group())
                return hours <= 12
            if "分鐘" in update_time_str:
                return True
            return False
        except:
            return False

    def get_all_news_list(self):
        main_driver = webdriver.Chrome(options=self.get_chrome_options())
        try:
            main_driver.get(self.url)
            time.sleep(3)
            news_list = self.scrape_news_list(main_driver)
            print(f"清單抓取完成，共 {len(news_list)} 則。")
            return news_list

        finally:
            main_driver.quit()

    def scrape_news_list(self, driver):
        check_ids = []
        news_list = []
        limit_reached = False
        same_check = 0
        while not limit_reached:
            news_row_list = driver.find_elements(By.CLASS_NAME, "StreamMegaItem")
            print(f"目前 DOM 數量: {len(news_row_list)} | 已收集: {len(news_list)}")

            for news in news_row_list:
                news_id = news.id
                if news_id in check_ids:
                    continue
                check_ids.append(news_id)

                try:
                    source_update_text = news.find_element(By.XPATH, ".//div[contains(@class, 'C(#959595)')]").text
                    source_update = source_update_text.split(" • ")
                    source = source_update[0]
                    update_time = source_update[1]

                    if self.parse_is_within_12_hours(update_time):
                        link_tag = news.find_element(By.CSS_SELECTOR, "h3 a")
                        title = link_tag.text
                        full_url = link_tag.get_attribute("href")

                        news_list.append({
                            "id": news_id,
                            "title": title,
                            "url": full_url,
                            "source": source
                        })
                    else:
                        limit_reached = True
                        break
                except:
                    continue

            if not limit_reached:
                driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                time.sleep(6)
                current_rows = driver.find_elements(By.CLASS_NAME, "StreamMegaItem")
                if len(current_rows) == len(news_row_list):
                    same_check += 1
                    if same_check >= 3:
                        break
        return news_list

    def fetch_news_content(self, news_id, url):
        driver = None
        try:
            driver = webdriver.Chrome(options=self.get_chrome_options())
            driver.get(url)
            time.sleep(2)
            articles = driver.find_elements(By.TAG_NAME, "article")
            if articles:
                paragraphs = articles[0].find_elements(By.TAG_NAME, "p")
                content = "\n".join([p.text.strip() for p in paragraphs if len(p.text.strip()) > 15])
                return {"id": news_id, "content": content}
        except:
            return None
        finally:
            if driver:
                print(news_id)
                driver.quit()

    def run_multithreaded_scraper(self, news_list, max_workers=6):
        print(f"開始並行抓取 {len(news_list)} 則新聞內文...")
        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_news = {executor.submit(self.fetch_news_content, news["id"], news["url"]): news for news in
                              news_list}
            for future in as_completed(future_to_news):
                res = future.result()
                if res:
                    results.append(res)
        return results
