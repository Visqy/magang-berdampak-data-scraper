# internship-data-scraper

**internship-data-scraper** is a Python project that automates the extraction of internship vacancy data from [simbelmawa.kemdikbud.go.id](https://simbelmawa.kemdikbud.go.id/) using Selenium WebDriver and processes the raw JSON into a structured CSV format.

This tool is particularly useful for researchers, education analysts, or academic organizations who need a comprehensive dataset of internship opportunities offered through the official Kampus Merdeka platform.

## 📌 Features

- 🔐 Login automation using Selenium
- 📄 Scrapes raw JSON from every paginated internship listing
- 🛠 Processes and structures key information:
  - Position details
  - Partner company/institution details
  - Internship criteria (technical, soft skills, etc.)
  - Responsibilities
  - Placement location and required number of interns
- 📦 Exports to CSV for further analysis or integration

## 🗂 Folder Structure

```
.
├── .env                       # Credentials file (not tracked in Git)
├── scraper.py                 # Main Selenium scraping script
├── processor.py               # JSON processor to clean & structure data
├── hasil_scraping_magang_selenium.csv   # Raw data output
├── hasil_olahan_magang_final.csv        # Final structured data output
└── README.md
```

## ⚙️ Requirements

- Python 3.8+
- Google Chrome
- ChromeDriver (managed automatically)

### Python Packages

```
selenium
pandas
python-dotenv
tqdm
```

Install all dependencies:
```bash
pip install -r requirements.txt
```

## 🔐 Setup Environment

Create a `.env` file in the root directory and add your Simbelmawa credentials:

```
MAGANG_USERNAME=your_username
MAGANG_PASSWORD=your_password
```

> ⚠️ Never commit your `.env` file to version control.


## 🚀 How to Use

### 1. Scrape Raw Data

Run the Selenium script to log in and scrape all available internship pages:

```bash
python scraper.py
```

This will generate a file: `hasil_scraping_magang_selenium.csv`

### 2. Process Structured Data

Run the processor to parse and clean the data into a structured format:

```bash
python processor.py
```

This will generate: `hasil_olahan_magang_final.csv`

## 📊 Output Preview

| posisi     | nama_mitra     | lokasi   | kriteria_teknis | tanggung_jawab | ... |
|------------|----------------|----------|------------------|----------------|-----|
| Data Analyst Intern | Telkom Indonesia | Bandung | Python, SQL     | Mengolah dan visualisasi data... | ... |

Each row represents a unique internship opportunity.

## 📝 Notes

- The scraper uses the `data-page` JSON embedded in the HTML, avoiding direct API use.
- Total pages scraped is hardcoded (`TOTAL_PAGES = 344`) — adjust if needed.
- All URLs generated point directly to the internship detail page.
