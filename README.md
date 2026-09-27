# Magang Berdampak Data Scraper

A Python + Selenium pipeline for collecting and structuring internship vacancy data from the Simbelmawa platform into an analysis-ready CSV dataset.

## Why This Project Exists

Searching for internships based only on the **job title** can be misleading. Two vacancies with similar titles may require very different technical skills, responsibilities, qualifications, and working contexts.

This project was created to make internship mapping more systematic by extracting not only the position title, but also the underlying **job-description information** such as technical criteria, responsibilities, partner information, location, and other vacancy details.

The resulting structured dataset can then be used for downstream analysis such as:

- comparing internship opportunities beyond title similarity;
- mapping candidate skills against actual job requirements;
- filtering vacancies based on technical criteria and responsibilities;
- building a more informed shortlist of relevant internship opportunities;
- supporting further analysis, ranking, or matching workflows.

> This repository focuses on **data collection and structuring**. It does not itself perform candidate-to-job scoring or recommendation.

## What It Does

The workflow consists of two main stages:

1. **Scraping**: Selenium logs into the platform and collects vacancy data from paginated internship listings.
2. **Processing**: the raw data is parsed, cleaned, and transformed into a structured CSV format that is easier to analyze.


## 📌 Features

- 🔐 Login automation using Selenium WebDriver
- 📄 Scrapes raw JSON from paginated internship listings
- 🛠 Extracts and structures information such as:
  - position details;
  - partner company or institution;
  - technical and non-technical criteria;
  - responsibilities;
  - placement location;
  - required number of interns;
  - internship detail URL.
- 🛠 Cleans and transforms raw data using pandas
- 📄 Exports an analysis-ready CSV dataset
- 🔐 Uses environment variables for credentials instead of hardcoding them in the source code

## 🗂 Folder Structure

```text
.
├── .env                              # Credentials file (not tracked in Git)
├── scraper.py                        # Selenium-based scraping script
├── processor.py                      # Cleans and structures scraped data
├── hasil_scraping_magang_selenium.csv
├── hasil_olahan_magang_final.csv
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

### 1. Scrape Internship Data

Run the Selenium script to log in and scrape all available internship pages:

```bash
python scraper.py
```

This will generate a file: `hasil_scraping_magang_selenium.csv`

### 2. Process the Dataset

Run the processor to parse and clean the data into a structured format:

```bash
python processor.py
```

This will generate: `hasil_olahan_magang_final.csv`

## 📊 Example Output


| posisi | nama_mitra | lokasi | kriteria_teknis | tanggung_jawab | ... |
|---|---|---|---|---|---|
| Data Analyst Intern | Telkom Indonesia | Bandung | Python, SQL | Mengolah dan visualisasi data... | ... |

Each row represents one internship opportunity with structured attributes that can be used for further filtering, comparison, or matching analysis.

## Example Use Case

Instead of searching only for titles such as `Software Engineer Intern`, `Backend Intern`, or `Data Analyst Intern`, the structured output makes it possible to inspect the actual requirements behind each vacancy.

For example, two listings with the same title can be differentiated based on whether they require:

- Python or JavaScript;
- SQL or database experience;
- REST API development;
- data analysis or visualization;
- communication or project-management skills;
- specific responsibilities or placement constraints.

This makes the dataset more useful for evaluating **job-description alignment**, rather than relying only on title matching.

## 📝 Notes and Limitations

- The scraper reads the `data-page` JSON embedded in the HTML rather than using a direct API.
- The current implementation uses a hardcoded total page count (`TOTAL_PAGES = 344`), which may need to be adjusted if the number of listings changes.
- The project depends on the current structure of the target website, so changes to the page layout or authentication flow may require updates to the scraper.
- The generated dataset is intended for analysis and personal/research use; users should ensure that their use complies with the platform's applicable terms and policies.

## Possible Extensions

The structured dataset can be used as a foundation for future work such as:

- rule-based job matching;
- skill-to-job alignment scoring;
- semantic similarity between candidate profiles and job descriptions;
- internship recommendation systems;
- market analysis of frequently requested skills;
- dashboards for internship opportunity exploration.
