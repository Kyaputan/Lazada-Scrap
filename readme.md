# 🛒 Lazada Web Scraper

This Python script scrapes product information from [Lazada Thailand](https://www.lazada.co.th) using Selenium and BeautifulSoup. It extracts data such as title, price, brand, review count, rating, and location for a specified product and saves the result to a CSV file.

## 📚 Table of Contents

- [🛒 Lazada Web Scraper](#-lazada-web-scraper)
- [📦 Features](#-features)
- [🚀 Getting Started](#-getting-started)
- [📖 Command Line Options](#-command-line-options)
- [🎯 Usage Examples](#-usage-examples)
- [📊 Output Data Structure](#-output-data-structure)
- [🔧 Requirements](#-requirements)
- [🔍 Troubleshooting](#-troubleshooting)
- [🚨 Legal Notice](#-legal-notice)
- [📁 File Structure](#-file-structure)
- [📝 License](#-license)


## 📦 Features

- 🎨 **Beautiful Terminal Interface** - Colorful output with progress bars and icons
- 💻 **CLI & Interactive Modes** - Use via command line or interactive prompts
- 📊 **Smart Data Collection** - Scrapes product info from Lazada search results
- 🔄 **Pagination Support** - Handles multiple pages automatically
- 📁 **CSV Export** - Outputs data to `lazada_data.csv` sorted by price (descending)

### Data Collected:
- Product Title
- Price (Thai Baht)
- Brand
- Review Count
- Rating (number of stars)
- Shipping Location
- Product Links

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

#### Interactive Mode (Beginner Friendly)
```bash
python main.py
```

#### CLI Mode (Advanced)
```bash
# Basic usage
python main.py --query "iPhone" --pages 5

# Advanced usage with custom output
python main.py -q "Samsung Galaxy" -p 10 --no-headless -o "samsung_data.csv"
```

### 4. View the Output
The script will create a CSV file (default: `lazada_data.csv`) in the same directory, containing the scraped data sorted by price (descending).

## 📖 Command Line Options
<p align="center"><b>Available CLI Parameters</b></p>

<div align="center">
  <table>
    <thead>
      <tr>
        <th>Option</th>
        <th>Short</th>
        <th>Description</th>
        <th>Default</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>--query</code></td>
        <td><code>-q</code></td>
        <td>Product name to search for</td>
        <td>Required*</td>
      </tr>
      <tr>
        <td><code>--pages</code></td>
        <td><code>-p</code></td>
        <td>Number of pages to scrape (1–50)</td>
        <td>5</td>
      </tr>
      <tr>
        <td><code>--no-headless</code></td>
        <td>-</td>
        <td>Run browser in visible mode</td>
        <td>headless</td>
      </tr>
      <tr>
        <td><code>--output</code></td>
        <td><code>-o</code></td>
        <td>Output CSV filename</td>
        <td>lazada_data.csv</td>
      </tr>
      <tr>
        <td><code>--interactive</code></td>
        <td>-</td>
        <td>Run in interactive mode</td>
        <td>-</td>
      </tr>
      <tr>
        <td><code>--version</code></td>
        <td>-</td>
        <td>Show version information</td>
        <td>-</td>
      </tr>
    </tbody>
  </table>
  <p><small>*Required unless using <code>--interactive</code> mode</small></p>
</div>



## 🎯 Usage Examples

### Example 1: Interactive Mode
```bash
python main.py --interactive
```

### Example 2: Quick Product Search
```bash
python main.py --query "smartphone" --pages 3
```

### Example 3: Advanced Search with Custom Output
```bash
python main.py -q "gaming laptop" -p 8 -o "laptops_2024.csv"
```

### Example 4: Debug Mode (Visible Browser)
```bash
python main.py -q "iPhone 15" -p 5 --no-headless
```

## 🎨 Terminal Interface Preview

```console
╔═══════════════════════════════════════════════════════════════╗
║                       LAZADA SCRAPER v2.0                     ║
║                 Enhanced CLI & Interactive Mode               ║
╚═══════════════════════════════════════════════════════════════╝

ℹ️  Configuration:
  📦 Product: iPhone 15
  📄 Pages: 5
  🖥️  Headless: Yes
  💾 Output: lazada_data.csv

🔄 Scraping: 100%|████████████| 5/5 [00:45<00:00, Products: 240]

📊 SCRAPING RESULTS SUMMARY
════════════════════════════════════════════════════════════════
📦 Total Products Found: 240
💰 Price Range: ฿15,990 - ฿45,990
📈 Average Price: ฿28,456
🏷️  Top Brands:
   • Apple: 89 products
   • Samsung: 45 products

✅ Scraping complete! Data saved to 'lazada_data.csv'
```

## 📊 Output Data Structure

| Column | Description | Example |
|--------|-------------|---------|
| `Product_Page` | Page number where product was found | 1 |
| `Price` | Product price in Thai Baht | 25990.0 |
| `Brand` | Product brand/manufacturer | Apple |
| `Review Count` | Number of customer reviews | 1250 |
| `Rating` | Star rating (1-5) | 5 |
| `Location` | Seller location | Bangkok |
| `Link` | Direct product URL | https://... |

## 🔧 Requirements

### System Requirements
- Python 3.7+
- Chrome browser installed
- Internet connection
- >512MB RAM recommended

### Python Dependencies
```txt
selenium>=4.0.0
beautifulsoup4>=4.9.0
pandas>=1.3.0
tqdm>=4.60.0
webdriver-manager>=3.8.0
```

## 🔍 Troubleshooting

### Common Issues

#### Chrome Driver Issues
```bash
# If you see Chrome driver errors:
pip install --upgrade webdriver-manager
```

#### No Products Found
- Check product name spelling
- Try more general search terms
- Verify Lazada website accessibility

#### Connection Timeout
```bash
# Try reducing pages or check internet connection
python main.py -q "product" -p 3
```

## 🚨 Legal Notice

This tool is for educational and research purposes only. Please ensure you comply with:
- Lazada's Terms of Service
- Robots.txt guidelines
- Local data protection laws
- Rate limiting best practices

**Recommendation**: Use responsibly with reasonable delays between requests.

## 📁 File Structure

```
lazada-scraper/
├── main.py                   # Main scraper script
├── requirements.txt          # Python dependencies
├── README.md                 # This documentation
└── lazada_data.csv

```


## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

⭐ **Star this repo if you find it helpful!** ⭐
