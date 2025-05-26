from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
import urllib.parse
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re


def get_title(soup):
    try:
        title = soup.find("h1", attrs={"class": "JrAyI"})
        title_value = title.text
        title_string = title_value.strip()
    except AttributeError:
        title_string = "Product"
    return title_string

def get_price(soup):
    try:
        price = soup.find("span", attrs={'class':'ooOxS'}).string.strip()
    except AttributeError:
        price = "N/A"
    return price

def get_brand(soup):
    try:
        container = soup.find("div", class_="RfADt")
        a_tag = container.find("a")
        brand_value = a_tag.text
        brand_string = brand_value.strip()
        brand_string = re.sub(r'[\u0E00-\u0E7F]', '', brand_string)
    except AttributeError:
        brand_string = "N/A"

    return brand_string


def get_review_count(soup):
    try:
        span = soup.find("span", class_="qzqFw")
        review_count = span.text.strip("()").strip()
    except AttributeError:
        review_count = "N/A"
    return review_count

def get_rating(soup):
    try:
        stars = soup.find_all("i", class_="_9-ogB Dy1nx")
        return len(stars)
    except:
        return "N/A"

def get_location(soup):
    try:
        location = soup.find("span", class_="oa6ri")
        location_value = location.text.strip("()")
        location_string = location_value.strip()
    except AttributeError:
        location_string = "ในประเทศไทย"
    return location_string

if __name__ == "__main__":
    PRODUCT = "SAMSUNG Galaxy S24"
    ENCODED_PRODUCT = urllib.parse.quote(PRODUCT)
    data = []
    options = Options()
    options.add_argument("--headless=new")  # ถ้าไม่ต้องโชว์ browser
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    for i in range(1, 3):
        URL = f"https://www.lazada.co.th/catalog/?q={ENCODED_PRODUCT}&sort=pricedesc&service=official&location=Local&rating=4&page={i}"
        driver.get(URL)
        print(f"Loading page {i} ...")
        driver.implicitly_wait(10)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        products = soup.find_all("div", class_="Bm3ON")

        for product in products:
            title = get_title(product)
            price = get_price(product)
            brand = get_brand(product)
            review_count = get_review_count(product)
            rating = get_rating(product)
            location = get_location(product)

            data.append({
                "Title": title,
                "Price": price,
                "Brand": brand,
                "Review Count": review_count,
                "Rating": rating,
                "Location": location
            })
    
    df = pd.DataFrame(data)
    time.sleep(5)
    df["Price"] = df["Price"].replace('[฿,]', '', regex=True).astype(float)
    df.sort_values(by="Price", inplace=True, ascending=False)
    df.to_csv("lazada_data.csv", header=True, index=False)
    driver.quit()

