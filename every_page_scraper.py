from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from urllib.parse import urljoin
import json
import time
import os
import concurrent.futures  # 🚀 NEW IMPORT for parallel processing
import threading

# --- Configuration ---
INPUT_FILE = "hotels_for_deep_scrape.json"
OUTPUT_FILE = "hotel_full_details.json"
MAX_WORKERS = 4  # ⚡ Run 4 browser sessions (URLs) concurrently
WAIT_TIME = 1  # Optimized initial wait time

# --- Thread-Safe Printing ---
# Use a lock to prevent print statements from jumbling when multiple threads run simultaneously
print_lock = threading.Lock()


def safe_print(message):
    with print_lock:
        print(message)


# --- WebDriver Initialization Function ---
def get_new_driver():
    """Initializes and returns a new WebDriver instance with stealth options."""
    chrome_options = webdriver.ChromeOptions()

    # Stealth Configuration (Headless)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    chrome_options.add_argument('--headless')

    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)


# --- Helper Functions (UNCHANGED logic) ---

def extract_text_or_default(driver, by_method, locator, default_value="N/A"):
    """Safely extracts text and ensures an empty string is converted to N/A."""
    try:
        element = driver.find_element(by_method, locator)
        text = element.text.strip()
        if not text:
            return default_value
        return text
    except (NoSuchElementException, Exception):
        return default_value


def extract_policy_details_v2(driver, policy_name):
    """Extracts text from the element following the specific <h2> policy title and ensures an empty string is converted to N/A."""
    try:
        label_xpath = f"//h2[@class='titlu' and contains(text(), '{policy_name}')]/following-sibling::*[1]"
        try:
            policy_detail_element = driver.find_element(By.XPATH, label_xpath)
            text = policy_detail_element.text.strip()
            if not text:
                return "N/A"
            return text
        except NoSuchElementException:
            return "N/A"
    except Exception:
        return "N/A"


# --- Core Scraping Function (UNCHANGED logic) ---

def scrape_url_parallel(url, total_urls, current_index):
    """Initializes driver, scrapes one URL, logs details, and quits driver."""

    driver = None
    details = {
        'url': url, 'property_name': 'N/A', 'address': 'N/A', 'phone_number': 'N/A',
        'full_description': 'N/A', 'capacity': 'N/A', 'images': [],
        'politici_copii': 'N/A', 'politici_mese': 'N/A', 'politici_rezervari': 'N/A',
        'politici_plata': 'N/A', 'facilities': 'N/A'
    }

    try:
        # 1. Initialize driver for this thread
        driver = get_new_driver()
        safe_print(f"\n[{current_index}/{total_urls}] -> Processing: {url}")

        # 2. Open URL and wait
        driver.get(url)
        safe_print(f"  -> Opened URL: {url} | Waiting {WAIT_TIME} second...")
        time.sleep(WAIT_TIME)

        # --- Property Name (Critical) ---
        try:
            name_element = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.XPATH, "//span[@itemprop='name']"))
            )
            details['property_name'] = name_element.text.strip()
        except Exception:
            safe_print("  -> ERROR: Could not find Hotel Name. Skipping.")
            return details

            # --- Data Extraction ---
        details['address'] = extract_text_or_default(driver, By.XPATH, "//span[@itemprop='address']")
        details['capacity'] = extract_text_or_default(driver, By.CLASS_NAME, "capacitate")
        details['facilities'] = extract_text_or_default(driver, By.CLASS_NAME, "facilitylist")

        # Images Extraction
        gallery_links = driver.find_elements(By.XPATH, "//div[contains(@class, 'picture')]//a[@rel='gallery-2']")
        details['images'] = [urljoin(url, link.get_attribute('href')) for link in gallery_links if
                             link.get_attribute('href')]
        safe_print(f"  -> Images: {'✅ SUCCESS' if details['images'] else '❌ FAILURE'}")

        # Description (Force Click & N/A check)
        try:
            desc_button = driver.find_element(By.ID, "sLongDesc")
            driver.execute_script("arguments[0].click();", desc_button)
            time.sleep(0.5)
            text = driver.find_element(By.XPATH, "//div[@itemprop='description']").text.strip()
            if text:
                details['full_description'] = text
        except (NoSuchElementException, Exception):
            details['full_description'] = extract_text_or_default(driver, By.XPATH, "//div[@itemprop='description']")

        safe_print(
            f"  -> Description: {'✅ SUCCESS' if details['full_description'] != 'N/A' and len(details['full_description']) > 100 else '❌ FAILURE'}")

        # Policies Extraction
        details['politici_copii'] = extract_policy_details_v2(driver, 'Copiii')
        details['politici_mese'] = extract_policy_details_v2(driver, 'Mesele')
        details['politici_rezervari'] = extract_policy_details_v2(driver, 'Politica de rezervări')
        details['politici_plata'] = extract_policy_details_v2(driver, 'Plata')

        safe_print(
            f"  -> Policies: Copii {'✅' if details['politici_copii'] != 'N/A' else '❌'} | Mese {'✅' if details['politici_mese'] != 'N/A' else '❌'} | Rezervari {'✅' if details['politici_rezervari'] != 'N/A' else '❌'} | Plata {'✅' if details['politici_plata'] != 'N/A' else '❌'}")

        # Contact Information (Click Phone Button)
        try:
            contact_button_locator = (By.XPATH, "//div[@class='phone vezitel']/a[@class='btn blue darken-1']")
            contact_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable(contact_button_locator))
            contact_button.click()

            phone_locator = (By.CLASS_NAME, "telnr")
            WebDriverWait(driver, 2).until(
                lambda driver: "XXX" not in driver.find_element(*phone_locator).text and driver.find_element(
                    *phone_locator).text.strip() != ''
            )

            phone_element = driver.find_element(*phone_locator)
            phone_number = phone_element.text.strip()
            if phone_number:
                details['phone_number'] = phone_number

            safe_print(f"  -> Contact: ✅ SUCCESS! {details['property_name']}: {details['phone_number']}")

        except Exception:
            safe_print(f"  -> Contact: ❌ FAILURE to Click/Extract Phone Number.")

    except Exception as e:
        safe_print(f"  -> CRITICAL ERROR while scraping {url}: {e}")

    finally:
        # 3. Quit the browser session for this thread
        if driver:
            driver.quit()

    return details


# --- Main Execution (PARALLEL RUN - CORRECTED) ---

if __name__ == '__main__':
    all_urls_data = []

    # 1. Load data
    try:
        safe_print(f"Loading URLs from {INPUT_FILE}...")
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            all_hotels_data = json.load(f)

        # Prepare the list of URLs and their indices for the parallel function
        all_urls_to_process = [
            (hotel.get('details_url'), len(all_hotels_data), i + 1)
            for i, hotel in enumerate(all_hotels_data) if hotel.get('details_url') and hotel.get('details_url') != 'N/A'
        ]

        # 🐛 CORRECTED LINE: Using all_urls_to_process for the count
        safe_print(f"Successfully loaded {len(all_urls_to_process)} hotel URLs. Starting parallel scrape...")

    except Exception as e:
        safe_print(f"ERROR: Failed to load/parse input file '{INPUT_FILE}': {e}")
        exit()

    # 2. START PARALLEL PROCESSING
    start_time = time.time()

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # Map the function to the list of arguments (url, total_urls, index)
            results = list(executor.map(lambda args: scrape_url_parallel(*args), all_urls_to_process))

            contact_data = [r for r in results if r is not None]

    except Exception as e:
        safe_print(f"\n!!! FATAL CRITICAL ERROR during parallel execution: {e}")
        contact_data = []

        # --- Final Output ---
    end_time = time.time()
    total_time = end_time - start_time

    safe_print("\n--- Full Data Scraping Complete ---")
    safe_print(f"Total time taken: {total_time:.2f} seconds.")
    safe_print(f"Writing {len(contact_data)} results to {OUTPUT_FILE}...")

    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(contact_data, f, ensure_ascii=False, indent=4)
        safe_print(f"✅ Data saved successfully to {OUTPUT_FILE}")
    except Exception as e:
        safe_print(f"❌ ERROR: Could not write final output file: {e}")