# TuristInfo.ro Hotel Scraper (Brașov County)

This is a high-performance, three-phase Python scraping and analysis project. It extracts detailed accommodation information from **turistinfo.ro**, processes the collected data, and generates visual insights through eight different graphs.

- **Phase 1:** Scrapes the entire “Brașov County” index to find all localities and their hotel URLs.  
- **Phase 2:** Performs a high-speed, parallel (multi-threaded) deep scrape on each URL to collect detailed hotel information.  
- **Phase 3:** Analyzes the final JSON dataset to parse key fields and generate eight visualizations using Matplotlib.

This project uses **Selenium**, **Pandas**, and **Matplotlib**.

---

## 🚀 Features

- **Phase 1 (Index Scraper):** Automatically discovers all localities in Brașov County and handles pagination.  
- **Phase 2 (Deep Scraper):** Runs multiple headless browsers in parallel to collect 12 key data points from each hotel page.  
- **Phase 3 (Data Analysis):** Extracts structured information from raw text (capacity, payment policies, etc.) and creates 8 different visualizations.  
- **JavaScript Handling:** Interacts dynamically with “Show Phone” and “Read More” buttons.  
- **Data Cleaning:** Automatically replaces blank fields with `"N/A"`.  

---

## 📊 Data Extracted & Analyzed

Each hotel record includes:

1. `url` – The source URL  
2. `property_name` – Hotel name  
3. `address` – Full address  
4. `phone_number` – Revealed contact number  
5. `full_description` – Full description text  
6. `capacity` – Raw capacity string  
7. `images` – List of full-resolution gallery images  
8. `politici_copii` – Child policy  
9. `politici_mese` – Meal policy  
10. `politici_rezervari` – Reservation policy  
11. `politici_plata` – Payment policy  
12. `facilities` – List of amenities  

The **analysis phase** (in `analiza_date.py`) parses this data into new analytical fields such as:  
`total_capacity`, `photo_count`, `payment_method`, and `accepts_children`.

---

## 🛠️ Technologies Used

- **Python 3.x**  
- **Selenium** — Browser automation  
- **webdriver-manager** — ChromeDriver auto management  
- **ThreadPoolExecutor** — For parallel scraping  
- **Pandas** — Data manipulation and analysis  
- **Matplotlib** — Graph generation and visualization  
- **JSON** — Data exchange and storage  

---

## ⚙️ Setup & Installation

Before starting, ensure that **Google Chrome** is installed.

### 1. Clone the Repository
```bash
git clone https://github.com/poprobert0412/TuristInfo.ro-Hotel-Scraper.git
cd TuristInfo.ro-Hotel-Scraper
```

### 2. Requirements File
Ensure your `requirements.txt` includes:
```
selenium
webdriver-manager
pandas
matplotlib
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🏃 How to Run

### Phase 1 — Collect Hotel URLs (`main_page_scraper.py`)
Builds a master list of all hotel URLs in Brașov County.

```bash
python main_page_scraper.py
```
**Output:** `hotels_for_deep_scrape.json`

---

### Phase 2 — Deep Scrape in Parallel (`every_page_scraper.py`)
Scrapes detailed hotel data using multithreading.

```bash
python every_page_scraper.py
```
**Output:** `hotel_full_details.json` and `hotel_contacts_final.json`

---

### Phase 3 — Analyze Data & Generate Graphs (`analiza_date.py`)
Loads the final JSON, performs analysis, and creates eight graphs.

```bash
python analiza_date.py
```

**Output (saved as PNG):**
- `graph_1_localities.png`
- `graph_2_payment_methods.png`
- `graph_3_child_policy.png`
- `graph_4_capacity_distribution.png`
- `graph_5_photo_count_distribution.png`
- `graph_6_top_10_photos.png`
- `graph_7_avg_capacity_locality.png`
- `graph_8_key_amenities.png`

---

## 🗂️ Project File Structure

```
.
├── .idea/                            # IDE configuration folder
├── README.md                         # Project documentation (this file)
│
├── analiza_date.py                   # Phase 3: Data analysis & plotting
├── every_page_scraper.py             # Phase 2: Parallel scraper
├── main_page_scraper.py              # Phase 1: Index scraper
├── phone_number_scraper.py           # Utility: phone number extraction
│
├── requirements.txt                  # Python dependencies
│
├── hotels_for_deep_scrape.json       # Output of Phase 1
├── hotel_full_details.json           # Output of Phase 2
├── hotel_contacts_final.json         # Contacts and merged dataset
│
├── graph_1_localities.png
├── graph_2_payment_methods.png
├── graph_3_child_policy.png
├── graph_4_capacity_distribution.png
├── graph_5_photo_count_distribution.png
├── graph_6_top_10_photos.png
├── graph_7_avg_capacity_locality.png
├── graph_8_key_amenities.png
├── grafic_localitati.png             # Alternate visualization
├── grafic_facilitati.png             # Alternate visualization
│
└── *.png                             # Generated analysis images
```

---

## 📈 Graphs Generated

1. **Localities Distribution** – Number of hotels per locality  
2. **Payment Methods** – Frequency of payment options  
3. **Child Policy** – Accommodation rules for children  
4. **Capacity Distribution** – Histogram of total capacity  
5. **Photo Count Distribution** – Histogram of photos per property  
6. **Top 10 by Photos** – Properties with most photos  
7. **Average Capacity per Locality** – Bar chart of mean capacities  
8. **Key Amenities** – Most common listed facilities  

---

## ⚠️ Disclaimer

This project is intended **for educational purposes only**.  
Web scraping may violate certain websites’ Terms of Service.  
Please be respectful of `turistinfo.ro` and avoid overloading their servers.  
Use at your own discretion and responsibility.
````
