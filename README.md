# TuristInfo.ro Hotel Scraper (Brașov)

This is a high-performance, two-phase Python scraping project designed to extract comprehensive accommodation details from `turistinfo.ro`. It navigates the main Brașov index, finds all hotel URLs, and then scrapes the detailed information for each hotel in parallel.

This project uses Selenium and `webdriver-manager` to automate a Chrome browser, handling JavaScript-driven elements (like clicking buttons to reveal phone numbers) and pagination.

## 🚀 Features

* **Phase 1 (Main Page Scraper):** Scrapes all hotel URLs from the main Brașov listings page.
* **Phase 2 (Deep Scraper):** Runs in a fast, multi-threaded (parallel) mode to scrape detailed data from all URLs.
* **JavaScript Interaction:** Clicks "Show Phone" and "Read More" buttons to reveal hidden dynamic content.
* **Data Cleanliness:** Ensures that blank fields (e.g., `""`) are correctly populated with `"N/A"`.
* **Robust & Stable:** Manages browser sessions per-thread to ensure stability during the high-speed parallel scrape.

## 📊 Data Extracted

The project includes two different scrapers for Phase 2:

1.  **`every_page_scraper.py` (Full Scrape):** Gathers 12 key data points:
    * `url`, `property_name`, `address`, `phone_number`
    * `full_description`, `capacity`, `images` (list)
    * `politici_copii`, `politici_mese`, `politici_rezervari`, `politici_plata`
    * `facilities`
2.  **`phone_number_scraper.py` (Contact-Only Scrape):** A lighter, faster script that only extracts:
    * `url`, `property_name`, `phone_number`

## 🛠️ Technologies Used

* **Python 3.x**
* **Selenium:** For browser automation and interacting with JavaScript.
* **webdriver-manager:** For automatically downloading and managing the correct ChromeDriver.
* **concurrent.futures (ThreadPoolExecutor):** For high-speed parallel scraping in `every_page_scraper.py`.
* **JSON:** For storing the intermediate and final datasets.

## ⚙️ Setup & Installation

Before you begin, ensure you have **Google Chrome** installed on your system.

**1. Clone the Repository:**
```bash
git clone https://github.com/poprobert0412/TuristInfo.ro-Hotel-Scraper.git
cd TuristInfo.ro-Hotel-Scraper
```

**2. Install Dependencies:**
This project requires two main Python libraries. You can install them directly using `pip`:

```bash
pip install selenium webdriver-manager
```

*(Alternatively, you can create a `requirements.txt` file with the contents below and run `pip install -r requirements.txt`)*

```text
selenium
webdriver-manager
```

## 🏃 How to Use

This project **must** be run in two distinct phases.

### Phase 1: Collect All Hotel URLs (`main_page_scraper.py`)

This script will browse the main Brașov listings page to build a master list of all hotel URLs.

1.  Run the `main_page_scraper.py` script:
    ```bash
    python main_page_scraper.py
    ```
2.  **Output:** A file named `hotels_for_deep_scrape.json` will be created. This file is the **input** for Phase 2.

### Phase 2: Scrape Detailed Data

After Phase 1 is complete, you can choose which scraper to run.

#### Option A: Full Data Scrape (Recommended)

This runs the fast, parallel scraper to get *all* 12 data points.

1.  Run the `every_page_scraper.py` script:
    ```bash
    python every_page_scraper.py
    ```
2.  **Output:** A file named `hotel_full_details.json` (or similar) will be created with the complete dataset.

#### Option B: Contact-Only Scrape

This runs a sequential (slower) scraper to get *only* the property name and phone number.

1.  Run the `phone_number_scraper.py` script:
    ```bash
    python phone_number_scraper.py
    ```
2.  **Output:** A file named `hotel_contacts_final.json` will be created.

## 🗂️ Project File Structure

```
.
├── main_page_scraper.py               # Phase 1: Main Page URL Scraper
├── every_page_scraper.py              # Phase 2: Parallel Full Data Scraper
├── phone_number_scraper.py            # Phase 2 (Alternative): Contact-Only Scraper
├── README.md                          # This file
│
├── hotels_for_deep_scrape.json        # (Generated) Output of Phase 1
├── hotel_full_details.json            # (Generated) Output of the full scraper
└── hotel_contacts_final.json          # (Generated) Output of the contact-only scraper
```

## ⚠️ Disclaimer

This project is intended for educational purposes only. Web scraping may be against the terms of service of the website. Please be respectful of the website's servers and do not send too many requests in a short period. The user assumes all responsibility for any use of this script.
