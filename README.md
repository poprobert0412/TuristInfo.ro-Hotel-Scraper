# TuristInfo.ro Hotel Scraper (Brașov)

This is a high-performance, two-phase Python scraping project designed to extract comprehensive accommodation details from `turistinfo.ro`. It navigates the main Brașov index, finds all hotel URLs, and then scrapes the detailed information for each hotel in parallel.

This project uses Selenium and `webdriver-manager` to automate a Chrome browser in headless (invisible) mode, handling JavaScript-driven elements (like clicking buttons to reveal phone numbers) and pagination.

*(Note: The `main_page_scraper.py` in this repository is configured for the main Brașov page. A more advanced version, `all_hotels_scrap.py` (not included), can be used to scrape the entire county index.)*

## 🚀 Features

* **Phase 1 (Main Page Scraper):** Scrapes all hotel URLs from the main Brașov listings page.
* **Phase 2 (Deep Scraper):** Runs in a fast, multi-threaded (parallel) mode to scrape detailed data from all URLs.
* **JavaScript Interaction:** Clicks "Show Phone" and "Read More" buttons to reveal hidden dynamic content.
* **Data Cleanliness:** Ensures that blank fields (e.g., `""`) are correctly populated with `"N/A"`.
* **Robust & Stable:** Manages browser sessions per-thread to ensure stability during the high-speed parallel scrape.

## 📊 Data Extracted

For each hotel, the script gathers the following 12 key data points:

1.  `url`: The source URL of the hotel's detail page.
2.  `property_name`: The name of the hotel.
3.  `address`: The full street address.
4.  `phone_number`: The revealed contact phone number.
5.  `full_description`: The complete, expanded description text.
6.  `capacity`: The guest capacity details.
7.  `images`: A list of all full-resolution gallery image URLs.
8.  `politici_copii`: The child policy text.
9.  `politici_mese`: The meal policy text.
10. `politici_rezervari`: The reservation policy text.
11. `politici_plata`: The payment policy text.
12. `facilities`: The full list of amenities.

## 🛠️ Technologies Used

* **Python 3.x**
* **Selenium:** For browser automation and interacting with JavaScript.
* **webdriver-manager:** For automatically downloading and managing the correct ChromeDriver.
* **concurrent.futures (ThreadPoolExecutor):** For high-speed parallel scraping.
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
2.  **Output:** A file named `hotels_for_deep_scrape.json` will be created, containing a list of all hotel URLs from the Brașov page.

### Phase 2: Scrape Detailed Data in Parallel (`every_page_scraper.py`)

This script reads the URL list from Phase 1 and runs multiple browsers in parallel to scrape the final, detailed data at high speed.

1.  Run the `every_page_scraper.py` script:
    ```bash
    python every_page_scraper.py
    ```
2.  This will launch 4 (or your configured number) of headless (invisible) browsers. You will see progress in your console as it scrapes URLs concurrently.
3.  **Output:** A file named `hotel_full_details.json` (or similar) will be created containing the final, detailed data for all properties.

## 🗂️ Project File Structure

```
.
├── main_page_scraper.py               # Phase 1: Main Page URL Scraper
├── every_page_scraper.py              # Phase 2: Parallel Deep Scraper
├── README.md                          # This file
│
├── hotels_for_deep_scrape.json        # (Generated) Output of Phase 1
└── hotel_full_details.json            # (Generated) Final output of Phase 2
```

## ⚠️ Disclaimer

This project is intended for educational purposes only. Web scraping may be against the terms of service of the website. Please be respectful of the website's servers and do not send too many requests in a short period. The user assumes all responsibility for any use of this script.
