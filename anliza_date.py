import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import re  # Import regex for parsing

# --- Configuration ---
INPUT_FILE = "hotel_full_details.json"
# Set higher quality for saved images
FIGURE_SIZE = (15, 8)
FIGURE_DPI = 150


# --- Data Parsing Functions ---

def parse_locality(address_str):
    """A simple function to extract the locality from the address string."""
    if address_str == "N/A" or not isinstance(address_str, str):
        return "Unknown"

    parts = address_str.split(',')
    if len(parts) >= 3:
        locality = parts[-1].strip()
        return locality.split(' ')[-1]
    elif len(parts) == 2:
        return parts[-1].strip().split(' ')[-1]
    elif len(parts) == 1:
        return parts[0].strip().split(' ')[-1]
    else:
        return "Unknown"


def parse_capacity(text):
    """Parses capacity text to extract total number of adults and children."""
    if not isinstance(text, str):
        return 0

    adults = 0
    children = 0

    adults_match = re.search(r'(\d+)\s+adulți', text, re.IGNORECASE)
    if adults_match:
        adults = int(adults_match.group(1))

    children_match = re.search(r'(\d+)\s+copii', text, re.IGNORECASE)
    if children_match:
        children = int(children_match.group(1))

    # If no specific 'adulti' text, take the first number as capacity
    if adults == 0 and children == 0:
        first_num_match = re.search(r'(\d+)', text)
        if first_num_match:
            return int(first_num_match.group(1))

    return adults + children


def parse_payment_method(text):
    """Parses payment policy text to find card or cash."""
    if not isinstance(text, str):
        return "N/A"

    text_lower = text.lower()
    has_card = 'card' in text_lower
    has_cash = 'numerar' in text_lower

    if has_card and has_cash:
        return "Card or Cash"
    elif has_card:
        return "Card Only"
    elif has_cash:
        return "Cash Only"
    else:
        return "N/A"


def parse_children_policy(text):
    """Parses child policy to see if children are accepted."""
    if not isinstance(text, str):
        return "Not specified"

    text_lower = text.lower()
    if 'nu acceptăm copii' in text_lower:
        return "Children Not Accepted"
    if 'acceptăm copii' in text_lower:
        return "Children Accepted"
    else:
        return "Not specified"


def plot_pie_chart(ax, data_series, labels_map, colors, title):
    """Helper function to correctly plot a pie chart."""
    counts = data_series.value_counts()

    # Ensure all keys from the map are present, even if 0
    for key in labels_map.keys():
        if key not in counts:
            counts[key] = 0

    # Filter out 0-count entries to avoid clutter
    counts = counts[counts > 0]

    # Reorder labels and colors based on the data's index
    labels = [labels_map[val] for val in counts.index]
    pie_colors = [colors[val] for val in counts.index]

    ax.pie(counts, labels=labels, autopct='%1.1f%%', colors=pie_colors, startangle=90)
    ax.set_title(title, fontsize=16)


# --- Main Analysis Function ---

def main_analysis():
    print(f"--- Starting Phase 3: Data Analysis from {INPUT_FILE} ---")

    if not os.path.exists(INPUT_FILE):
        print(f"❌ ERROR: File '{INPUT_FILE}' not found.")
        print("Please run 'every_page_scraper.py' first to generate the data.")
        return

    # 1. Load Data into Pandas DataFrame
    try:
        df = pd.read_json(INPUT_FILE)
        print(f"✅ Data loaded successfully. Found {len(df)} property listings.")
    except Exception as e:
        print(f"❌ ERROR reading JSON file: {e}")
        return

    # 2. Data Cleaning and Feature Engineering
    print("Parsing and cleaning data...")
    df['locality'] = df['address'].apply(parse_locality)
    df['photo_count'] = df['images'].apply(len)
    df['total_capacity'] = df['capacity'].apply(parse_capacity)
    df['payment_method'] = df['politici_plata'].apply(parse_payment_method)
    df['accepts_children'] = df['politici_copii'].apply(parse_children_policy)

    # Simple boolean flags for amenities
    df['has_wifi'] = df['facilities'].str.contains('check WiFi gratuit', case=False, na=False)
    df['has_parking'] = df['facilities'].str.contains('check parcare', case=False, na=False)
    df['has_phone'] = df['phone_number'] != "N/A"

    # --- 3. Generate 8 Graphs ---

    # Graph 1: Top 15 Localities by Listing Count
    print("Generating Graph 1: Top 15 Localities...")
    plt.figure(figsize=FIGURE_SIZE)
    locality_counts = df['locality'].value_counts().nlargest(15)
    locality_counts.plot(kind='bar', color='skyblue')
    plt.title('Graph 1: Top 15 Localities by Number of Listings (Brașov County)', fontsize=18)
    plt.xlabel('Locality', fontsize=12)
    plt.ylabel('Number of Listings', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('graph_1_localities.png', dpi=FIGURE_DPI)
    print("  -> 'graph_1_localities.png' saved.")

    # Graph 2: Payment Methods Distribution (Pie Chart)
    print("Generating Graph 2: Payment Methods...")
    plt.figure(figsize=FIGURE_SIZE)
    payment_counts = df['payment_method'].value_counts()
    plt.pie(payment_counts, labels=payment_counts.index, autopct='%1.1f%%', startangle=90,
            colors=['#4CAF50', '#FFC107', '#2196F3', '#BDBDBD'])
    plt.title('Graph 2: Distribution of Payment Methods', fontsize=18)
    plt.tight_layout()
    plt.savefig('graph_2_payment_methods.png', dpi=FIGURE_DPI)
    print("  -> 'graph_2_payment_methods.png' saved.")

    # Graph 3: Child Policy Distribution (Pie Chart)
    print("Generating Graph 3: Child Policy...")
    plt.figure(figsize=FIGURE_SIZE)
    children_policy_counts = df['accepts_children'].value_counts()
    plt.pie(children_policy_counts, labels=children_policy_counts.index, autopct='%1.1f%%', startangle=90,
            colors=['#4CAF50', '#FF5252', '#BDBDBD'])
    plt.title('Graph 3: Child Acceptance Policy', fontsize=18)
    plt.tight_layout()
    plt.savefig('graph_3_child_policy.png', dpi=FIGURE_DPI)
    print("  -> 'graph_3_child_policy.png' saved.")

    # Graph 4: Distribution of Total Capacity (Histogram)
    print("Generating Graph 4: Property Capacity Distribution...")
    plt.figure(figsize=FIGURE_SIZE)
    # Filter for properties where capacity > 0 and < 100 (to remove outliers)
    capacity_data = df['total_capacity'][(df['total_capacity'] > 0) & (df['total_capacity'] < 100)]
    capacity_data.plot(kind='hist', bins=20, color='teal', edgecolor='black')
    plt.title('Graph 4: Distribution of Property Capacity (Max 100 Persons)', fontsize=18)
    plt.xlabel('Total Capacity (Adults + Children)', fontsize=12)
    plt.ylabel('Number of Properties', fontsize=12)
    plt.tight_layout()
    plt.savefig('graph_4_capacity_distribution.png', dpi=FIGURE_DPI)
    print("  -> 'graph_4_capacity_distribution.png' saved.")

    # Graph 5: Distribution of Photo Count (Histogram)
    print("Generating Graph 5: Photo Count Distribution...")
    plt.figure(figsize=FIGURE_SIZE)
    photo_data = df['photo_count'][df['photo_count'] > 0]
    photo_data.plot(kind='hist', bins=30, color='purple', edgecolor='black')
    plt.title('Graph 5: Distribution of Photo Count per Listing', fontsize=18)
    plt.xlabel('Number of Photos', fontsize=12)
    plt.ylabel('Number of Properties', fontsize=12)
    plt.tight_layout()
    plt.savefig('graph_5_photo_count_distribution.png', dpi=FIGURE_DPI)
    print("  -> 'graph_5_photo_count_distribution.png' saved.")

    # Graph 6: Top 10 Properties with Most Photos
    print("Generating Graph 6: Top 10 Properties by Photo Count...")
    plt.figure(figsize=FIGURE_SIZE)
    top_photos = df.nlargest(10, 'photo_count').set_index('property_name')['photo_count']
    top_photos.plot(kind='barh', color='indigo')  # Horizontal bar chart
    plt.title('Graph 6: Top 10 Properties with the Most Photos', fontsize=18)
    plt.xlabel('Number of Photos', fontsize=12)
    plt.ylabel('Property Name', fontsize=12)
    plt.gca().invert_yaxis()  # Show highest on top
    plt.tight_layout()
    plt.savefig('graph_6_top_10_photos.png', dpi=FIGURE_DPI)
    print("  -> 'graph_6_top_10_photos.png' saved.")

    # Graph 7: Average Capacity by Top 15 Localities
    print("Generating Graph 7: Average Capacity by Locality...")
    plt.figure(figsize=FIGURE_SIZE)
    # Get top 15 localities by *count* first
    top_localities_by_count = df['locality'].value_counts().nlargest(15).index
    # Filter DataFrame for only these localities
    df_top_localities = df[df['locality'].isin(top_localities_by_count)]
    # Calculate average capacity
    avg_capacity = df_top_localities.groupby('locality')['total_capacity'].mean().sort_values(ascending=False)

    avg_capacity.plot(kind='bar', color='coral')
    plt.title('Graph 7: Average Property Capacity in Top 15 Localities', fontsize=18)
    plt.xlabel('Locality', fontsize=12)
    plt.ylabel('Average Capacity (Persons)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('graph_7_avg_capacity_locality.png', dpi=FIGURE_DPI)
    print("  -> 'graph_7_avg_capacity_locality.png' saved.")

    # Graph 8: Key Amenities (Phone, WiFi, Parking)
    print("Generating Graph 8: Key Amenities...")
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 7))  # Wide figure for 3 pies

    # Define labels and colors
    phone_labels = {True: 'Has Phone', False: 'No Phone (N/A)'}
    phone_colors = {True: '#4CAF50', False: '#FF5252'}

    wifi_labels = {True: 'Has Free WiFi', False: 'No Free WiFi'}
    wifi_colors = {True: '#2196F3', False: '#BDBDBD'}

    parking_labels = {True: 'Has Parking', False: 'No Parking'}
    parking_colors = {True: '#FFC107', False: '#BDBDBD'}

    # Plot
    plot_pie_chart(ax1, df['has_phone'], phone_labels, phone_colors, 'Listings with Phone Number')
    plot_pie_chart(ax2, df['has_wifi'], wifi_labels, wifi_colors, 'Listings with "Free WiFi"')
    plot_pie_chart(ax3, df['has_parking'], parking_labels, parking_colors, 'Listings with "Parking"')

    fig.suptitle('Graph 8: Key Amenity Distribution', fontsize=20, y=1.05)
    plt.tight_layout()
    plt.savefig('graph_8_key_amenities.png', dpi=FIGURE_DPI)
    print("  -> 'graph_8_key_amenities.png' saved.")

    print("\n✅ Analysis complete! Check your project folder for 8 new '.png' graph files.")


if __name__ == '__main__':
    main_analysis()