from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import json
import time
import os

# --- Configuration ---
INPUT_FILE = "hotels_for_deep_scrape.json"
OUTPUT_FILE = "hotel_contacts_final.json"  # Final output file
WAIT_TIME = 3  # Fixed wait time in seconds


# --- Function to Scrape ONLY Contact Details and Name ---

def scrape_contact_only(driver, url):
    """Navigates to the URL, waits 3s, clicks the phone button, and scrapes the number and name."""

    details = {
        'url': url,
        'property_name': 'N/A',  # Now mandatory
        'phone_number': 'N/A',
        'owner_name': 'N/A'
    }

    try:
        # 1. Open URL
        driver.get(url)
        print(f"  -> Opened URL.")

        # 2. Wait exactly 3 seconds
        print(f"  -> Waiting exactly {WAIT_TIME} seconds...")
        time.sleep(WAIT_TIME)

        # 1. Get Property Name (itemprop="name")
        try:
            # We use an explicit wait (1s) to ensure the main element is present
            name_element = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.XPATH, "//span[@itemprop='name']"))
            )
            details['property_name'] = name_element.text.strip()
        except Exception:
            print("  -> ERROR: Could not find Hotel Name.")
            return details  # Return if name is not found, as it's critical data

        # 3. Click the Phone Button
        print("  -> Attempting to click contact button...")
        try:
            # Targeting the <a> tag inside the specific phone div structure
            contact_button_locator = (By.XPATH, "//div[@class='phone vezitel']/a[@class='btn blue darken-1']")

            # Use minimal wait for clickability
            contact_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable(contact_button_locator))
            contact_button.click()

            # 4. Extract the Phone Number (class="telnr")
            phone_locator = (By.CLASS_NAME, "telnr")

            # Wait 1: Ensure the element is visible and number is revealed
            WebDriverWait(driver, 2).until(
                lambda driver: "XXX" not in driver.find_element(*phone_locator).text and driver.find_element(
                    *phone_locator).text.strip() != ''
            )

            # Retrieve the element after all checks pass
            phone_element = driver.find_element(*phone_locator)
            details['phone_number'] = phone_element.text.strip()

            # Extract owner name (optional)
            try:
                owner_name_element = driver.find_element(By.XPATH, "//div[contains(@class, 'contact-info')]//strong[1]")
                details['owner_name'] = owner_name_element.text.strip()
            except NoSuchElementException:
                pass

            # --- CONSOLE OUTPUT AS REQUESTED ---
            print(f"  -> SUCCESS! {details['property_name']}: {details['phone_number']}")
            # -----------------------------------

        except Exception as e:
            print(f"  -> FAILURE to Click/Extract Phone Number: {e}")

    except WebDriverException as e:
        print(f"  -> CRITICAL DRIVER ERROR during processing: {e}")
    except Exception as e:
        print(f"  -> An unexpected error occurred: {e}")

    return details


# --- Main Execution (Stealth Mode) ---
contact_data = []
driver = None

# 1. Load data from the JSON file
try:
    print(f"Loading URLs from {INPUT_FILE}...")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        all_hotels_data = json.load(f)
    print(f"Successfully loaded {len(all_hotels_data)} hotel URLs.")
except Exception as e:
    print(f"ERROR: Failed to load/parse input file '{INPUT_FILE}': {e}")
    all_hotels_data = []

# 2. START THE SINGLE BROWSER SESSION (Headless Stealth Mode)
try:
    print("\n🕵️ Starting SINGLE, Stealth Headless Browser Session...")

    chrome_options = webdriver.ChromeOptions()

    # Stealth Configuration (Kept for stability and speed)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    chrome_options.add_argument('--headless')  # Re-enabling the headless flag for speed

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    # 3. Process all URLs in the single session
    print(f"Starting Fast Scraping: {len(all_hotels_data)} URLs to process...")

    for i, hotel in enumerate(all_hotels_data):
        url = hotel.get('details_url')
        if not url or url == 'N/A':
            continue

        print(f"\n[{i + 1}/{len(all_hotels_data)}] -> Processing: {url}")

        # The processing logic that is known to work
        contact_data.append(scrape_contact_only(driver, url))

except Exception as e:
    print(f"\n!!! FATAL ERROR during single session run: {e}")

finally:
    # 4. Close the browser only ONCE at the very end
    if driver:
        print("\n\n✅ All URLs processed. Closing single browser session.")
        driver.quit()

# --- Final Output ---
print("\n--- Contact Scraping Complete ---")
print(f"Writing {len(contact_data)} results to {OUTPUT_FILE}...")
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(contact_data, f, ensure_ascii=False, indent=4)

print(f"✅ Data saved successfully to {OUTPUT_FILE}")