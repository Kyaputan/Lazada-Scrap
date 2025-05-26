import os
import re
import urllib.parse
import logging
import pandas as pd
import argparse
import sys
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Enhanced logging with colors
class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': Colors.OKBLUE,
        'INFO': Colors.OKGREEN,
        'WARNING': Colors.WARNING,
        'ERROR': Colors.FAIL,
        'CRITICAL': Colors.FAIL + Colors.BOLD,
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, '')
        record.levelname = f"{log_color}{record.levelname}{Colors.ENDC}"
        return super().format(record)

# Setup enhanced logging
def setup_logging():
    handler = logging.StreamHandler()
    formatter = ColoredFormatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

def print_banner():
    banner = f"""
{Colors.OKCYAN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════╗
║                       LAZADA SCRAPER v2.0                     ║
║                 Enhanced CLI & Interactive Mode               ║
╚═══════════════════════════════════════════════════════════════╝
{Colors.ENDC}
    """
    print(banner)

def print_separator():
    print(f"{Colors.OKCYAN}{'='*60}{Colors.ENDC}")

def print_success(message):
    print(f"{Colors.OKGREEN}✅ {message}{Colors.ENDC}")

def print_info(message):
    print(f"{Colors.OKBLUE}ℹ️  {message}{Colors.ENDC}")

def print_warning(message):
    print(f"{Colors.WARNING}⚠️  {message}{Colors.ENDC}")

def print_error(message):
    print(f"{Colors.FAIL}❌ {message}{Colors.ENDC}")

# --- Webdriver setup ---
def setup_driver(headless: bool = True) -> webdriver.Chrome:
    print_info("Setting up Chrome WebDriver...")
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    
    service = Service(ChromeDriverManager().install())
    print_success("WebDriver setup complete!")
    return webdriver.Chrome(service=service, options=options)

# --- Data extraction functions ---
def get_price(soup):
    return safe_find_text(soup, "span", {"class": "ooOxS"}, "N/A")

def get_brand(soup):
    try:
        text = soup.find("div", class_="RfADt").find("a").text.strip()
        return re.sub(r'[\u0E00-\u0E7F]', '', text)
    except:
        return "N/A"

def get_review_count(soup):
    return safe_find_text(soup, "span", {"class": "qzqFw"}, "N/A", clean_fn=lambda x: x.strip("()").strip())

def get_rating(soup):
    try:
        stars = soup.find_all("i", class_="_9-ogB Dy1nx")
        return len(stars)
    except:
        return "N/A"

def get_location(soup):
    return safe_find_text(soup, "span", {"class": "oa6ri"}, "Local", clean_fn=lambda x: x.strip("()").strip())

def get_link(soup):
    try:
        a_tag = soup.find("div", class_="_95X4G").find("a", href=True)
        href = a_tag["href"]
        return "https:" + href if href.startswith("//") else href
    except:
        return "N/A"

def clean_title(title):
    title = re.sub(r'[\[\]()!]', '', title)
    title = re.sub(r'[-/.,]{2,}', ' ', title)
    title = re.sub(r'[/.]+$', '', title)
    return re.sub(r'\s+', ' ', title).strip()

def safe_find_text(soup, tag, attrs, default, clean_fn=lambda x: x.strip()):
    try:
        return clean_fn(soup.find(tag, attrs=attrs).text)
    except:
        return default

# --- Enhanced progress display ---
def create_progress_bar(total_pages):
    return tqdm(
        range(1, total_pages + 1),
        desc=f"{Colors.OKCYAN}🔄 Scraping{Colors.ENDC}",
        bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]',
        colour='cyan'
    )

# --- Main scraping logic ---
def scrape_product_data(driver, query: str, total_pages: int):
    data = []
    encoded_query = urllib.parse.quote(query)
    
    print_separator()
    print_info(f"Starting to scrape '{query}' from {total_pages} pages")
    print_separator()

    progress_bar = create_progress_bar(total_pages)
    
    for i in progress_bar:
        url = f"https://www.lazada.co.th/catalog/?q={encoded_query}&sort=pricedesc&service=official&location=Local&rating=4&page={i}"
        
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "Bm3ON")))
        except Exception as e:
            logging.error(f"Error loading page {i}: {e}")
            continue

        soup = BeautifulSoup(driver.page_source, "html.parser")
        products = soup.find_all("div", class_="Bm3ON")
        
        page_products = 0
        for product in products:
            data.append({
                "Product_Page": i,
                "Price": get_price(product),
                "Brand": clean_title(get_brand(product)),
                "Review Count": get_review_count(product),
                "Rating": get_rating(product),
                "Location": get_location(product),
                "Link": get_link(product)
            })
            page_products += 1
        
        progress_bar.set_postfix({"Products": len(data), "Page Items": page_products})

    progress_bar.close()
    return pd.DataFrame(data)

def display_results_summary(df):
    print_separator()
    print(f"{Colors.BOLD}{Colors.OKGREEN}📊 SCRAPING RESULTS SUMMARY{Colors.ENDC}")
    print_separator()
    
    if df.empty:
        print_warning("No products found!")
        return
    
    print(f"{Colors.OKBLUE}📦 Total Products Found: {Colors.BOLD}{len(df)}{Colors.ENDC}")
    
    try:
        price_df = df[df["Price"] != "N/A"].copy()
        if not price_df.empty:
            price_df["Price_Numeric"] = price_df["Price"].replace('[฿,]', '', regex=True).astype(float)
            print(f"{Colors.OKBLUE}💰 Price Range: {Colors.BOLD}฿{price_df['Price_Numeric'].min():,.0f} - ฿{price_df['Price_Numeric'].max():,.0f}{Colors.ENDC}")
            print(f"{Colors.OKBLUE}📈 Average Price: {Colors.BOLD}฿{price_df['Price_Numeric'].mean():,.0f}{Colors.ENDC}")
    except:
        pass
    
    brand_counts = df[df["Brand"] != "N/A"]["Brand"].value_counts().head(3)
    if not brand_counts.empty:
        print(f"{Colors.OKBLUE}🏷️  Top Brands:{Colors.ENDC}")
        for brand, count in brand_counts.items():
            print(f"   • {brand}: {count} products")
    
    print_separator()

def get_user_input():
    """Interactive mode for getting user input"""
    print_info("Interactive Mode - Please provide the following information:")
    print()
    
    while True:
        product_name = input(f"{Colors.OKCYAN}🔍 Enter product name to search: {Colors.ENDC}").strip()
        if product_name:
            break
        print_warning("Product name cannot be empty!")
    
    while True:
        try:
            pages = int(input(f"{Colors.OKCYAN}📄 How many pages to scrape (1-50): {Colors.ENDC}").strip())
            if 1 <= pages <= 50:
                break
            print_warning("Please enter a number between 1 and 50!")
        except ValueError:
            print_warning("Please enter a valid number!")
    
    while True:
        headless_input = input(f"{Colors.OKCYAN}🖥️  Run in headless mode? (y/n) [default: y]: {Colors.ENDC}").strip().lower()
        if headless_input in ['', 'y', 'yes']:
            headless = True
            break
        elif headless_input in ['n', 'no']:
            headless = False
            break
        print_warning("Please enter 'y' for yes or 'n' for no!")
    
    return product_name, pages, headless

def setup_cli_parser():
    """Setup command line argument parser"""
    parser = argparse.ArgumentParser(
        description="🛒 Lazada Product Scraper - Extract product data from Lazada Thailand",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
                {Colors.OKCYAN}Examples:{Colors.ENDC}
                python lazada_scraper.py --query "smartphone" --pages 5
                python lazada_scraper.py -q "laptop" -p 10 --no-headless
                python lazada_scraper.py --interactive
        """)
    
    parser.add_argument('-q', '--query',type=str,help='Product name to search for')
    parser.add_argument('-p', '--pages',type=int,default=5,help='Number of pages to scrape (default: 5, max: 50)')
    parser.add_argument('--no-headless',action='store_true',help='Run browser in visible mode (default: headless)')
    parser.add_argument('-o', '--output',type=str,default='lazada_data.csv',help='Output CSV filename (default: lazada_data.csv)')
    parser.add_argument('--interactive',action='store_true',help='Run in interactive mode')
    parser.add_argument('--version',action='version',version='Lazada Scraper v2.0')
    
    return parser

def main():
    setup_logging()
    print_banner()
    
    parser = setup_cli_parser()
    args = parser.parse_args()
    
    if args.pages and (args.pages < 1 or args.pages > 50):
        print_error("Pages must be between 1 and 50!")
        sys.exit(1)
    
    if args.interactive or (not args.query and len(sys.argv) == 1):
        product_name, pages, headless = get_user_input()
        output_file = "lazada_data.csv"
    else:
        if not args.query:
            print_error("Product query is required! Use --query or --interactive")
            parser.print_help()
            sys.exit(1)
        
        product_name = args.query
        pages = args.pages
        headless = not args.no_headless
        output_file = args.output
    
    print_separator()
    print_info(f"Configuration:")
    print(f"  📦 Product: {Colors.BOLD}{product_name}{Colors.ENDC}")
    print(f"  📄 Pages: {Colors.BOLD}{pages}{Colors.ENDC}")
    print(f"  🖥️  Headless: {Colors.BOLD}{'Yes' if headless else 'No'}{Colors.ENDC}")
    print(f"  💾 Output: {Colors.BOLD}{output_file}{Colors.ENDC}")
    
    driver = setup_driver(headless=headless)
    try:
        df = scrape_product_data(driver, product_name, pages)
        
        if df.empty:
            print_warning("No data found!")
            return
        
        print_info("Processing scraped data...")
        df_processed = df.copy()
        try:
            df_processed["Price"] = df_processed["Price"].replace('[฿,]', '', regex=True).astype(float)
            df_processed.sort_values(by="Price", ascending=False, inplace=True)
        except:
            print_warning("Could not process price data for sorting")
        
        df_processed.to_csv(output_file, index=False)
        
        display_results_summary(df)
        print_success(f"Scraping complete! Data saved to '{output_file}'")
        
    except KeyboardInterrupt:
        print_warning("\nScraping interrupted by user!")
    except Exception as e:
        print_error(f"An error occurred: {e}")
        logging.error(f"Detailed error: {e}", exc_info=True)
    finally:
        print_info("Closing browser...")
        driver.quit()
        print_success("Done!")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    main()
    # python main.py --query "iPhone" --pages 3