import requests
from bs4 import BeautifulSoup
import json
import pprint
import os  # Added for path operations (though not strictly necessary here, good practice)

# --- Configuration ---
# The URL you want to scrape
URL = "https://www.turistinfo.ro/brasov/cazare-hoteluri-vile-pensiuni-brasov.html"
BASE_URL = "https://www.turistinfo.ro"
# Define the output file name
OUTPUT_FILE = "hotels_for_deep_scrape.json"

# Set a User-Agent header
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

print(f"Attempting to fetch {URL}...")

try:
    response = requests.get(URL, headers=headers)
    response.raise_for_status()
    print("Successfully fetched the page.")

    soup = BeautifulSoup(response.text, 'html.parser')
    main_list = soup.find('ul', class_='liste-cazare')

    if not main_list:
        print("Could not find the main listings container.")
    else:
        hotel_listings = main_list.find_all('li', class_='liste-unitate')
        print(f"Found {len(hotel_listings)} hotel listings.")

        all_hotels_data = []

        for hotel in hotel_listings:

            # --- Name ---
            name_tag = hotel.find('span', itemprop='name')
            name = name_tag.text.strip() if name_tag else "N/A"

            # --- Unique URL (FIXED) ---
            details_url = "N/A"
            if name_tag:
                link_tag = name_tag.find_parent('a', href=True)
                if link_tag:
                    details_url = f"{BASE_URL}{link_tag['href']}"

            # --- Star Rating ---
            stars_container = hotel.find('span', style="white-space: nowrap;")
            star_rating = "N/A"
            if stars_container:
                star_icons = stars_container.find_all('i', class_='stars')
                star_count = len(star_icons)
                if star_count > 0:
                    star_rating = f"{star_count} stars"

            # --- Address ---
            address_tag = hotel.find('span', itemprop='address')
            address = address_tag.get_text(separator=" ", strip=True) if address_tag else "N/A"

            # --- Reviews (Cleaned Spacing) ---
            review_tag = hotel.find('div', class_='ucrecenzii')
            reviews = "N/A"
            if review_tag:
                reviews = review_tag.get_text(strip=True)
                reviews = reviews.replace("question_answer", "").strip()
                reviews = ' '.join(reviews.split())

            # --- Capacity (Cleaned Spacing) ---
            capacity_tag = hotel.find('div', class_='uclocuri')
            capacity = "N/A"
            if capacity_tag:
                capacity = capacity_tag.get_text(strip=True)
                capacity = capacity.replace("supervisor_account", "").strip()
                capacity = ' '.join(capacity.split())
                capacity = capacity.replace('spatiude cazare', 'spatiu de cazare')

            # --- Description ---
            description_tag = hotel.find('p', itemprop='description')
            description = description_tag.get_text(strip=True) if description_tag else "N/A"

            # --- Price ---
            price_tag = hotel.find('div', itemprop='priceRange')
            price = price_tag.get_text(strip=True) if price_tag else "N/A"

            # --- Image ---
            image_tag = hotel.find('img', itemprop='image')
            image_src = image_tag['src'] if image_tag and image_tag.has_attr('src') else None
            if image_src:
                image_url = f"{BASE_URL}{image_src}".replace(BASE_URL + BASE_URL, BASE_URL)
            else:
                image_url = "N/A"

            # 6. Add all found data to a dictionary, with URL at the end
            hotel_data = {
                'name': name,
                'star_rating': star_rating,
                'address': address,
                'reviews': reviews,
                'capacity': capacity,
                'description': description,
                'price': price,
                'image_url': image_url,
                'details_url': details_url,
            }
            all_hotels_data.append(hotel_data)

        # 7. Print verification (optional but helpful)
        print("\n--- Verification of First Detail URL ---")
        print(f"Name: {all_hotels_data[0]['name']}")
        print(f"Corrected Detail URL: {all_hotels_data[0]['details_url']}")

        # 8. Save the data to a JSON file
        print(f"\nSaving {len(all_hotels_data)} hotel entries to {OUTPUT_FILE}...")
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            # Use ensure_ascii=False to preserve Romanian characters correctly
            json.dump(all_hotels_data, f, indent=4, ensure_ascii=False)

        print(f"✅ Data successfully saved to {OUTPUT_FILE}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred while fetching the URL: {e}")