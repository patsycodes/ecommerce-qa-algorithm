from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import random
import csv

# phase 1: get data via webscraping

base_url = "https://www.hktvmall.com/hktv/en/search_a?keyword=beverages"
cur_page_num = 0


with sync_playwright() as playwright:
    chromium = playwright.chromium 
    browser = chromium.launch(headless=False)
    context = browser.new_context(user_agent="learning-webscaping")
    page = context.new_page()

    with open('unmatched.csv', mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Product Name', "Product Spec"])
    

    while True:

        page_url = "&page=" + str(cur_page_num)
        page.goto(base_url + page_url)
        parsed = []
        page.wait_for_selector(".product-brief-wrapper", timeout=50000)
        soup = BeautifulSoup(page.content(), "html.parser")    
        for i in soup.select(".upper-wrapper"):
            name = i.select_one(".brand-product-name h4")
            spec = i.select_one(".packing-spec span")
            if name:
                name = name.get_text(strip=True)
            if spec:
                spec = spec.get_text(strip=True)
            else:
                spec = ""

            parsed.append([name, spec])

        if parsed:
            with open('unmatched.csv', mode='a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(parsed)

        print(f"Total entries til page {cur_page_num}: {len(parsed)}")

        if page.locator("button#paginationMenu_nextBtn.disabled").count() > 0:
            break

        cur_page_num += 1

        delay = random.uniform(5.5, 10.5)
        time.sleep(delay)

    print("Scraped results are now in unmatched.csv")

    browser.close()


