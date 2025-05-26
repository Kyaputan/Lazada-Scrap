# Lazada Web Scraper

This Python script scrapes product information from [Lazada Thailand](https://www.lazada.co.th) using Selenium and BeautifulSoup. It extracts data such as title, price, brand, review count, rating, and location for a specified product and saves the result to a CSV file.

## 📦 Features

- Scrapes product info from Lazada search results
- Supports pagination
- Collects:
  - Product Title
  - Price
  - Brand
  - Review Count
  - Rating (number of stars)
  - Shipping Location
- Outputs data to `lazada_data.csv` sorted by price (descending)

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/lazada-scraper.git
cd lazada-scraper
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Script

```bash
python main.py
```

### 4. View the Output

The script will create a `lazada_data.csv` file in the same directory, containing the scraped data sorted by price (descending).

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
