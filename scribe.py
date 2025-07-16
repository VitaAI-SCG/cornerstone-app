# scribe.py - The Scribe's Snowfall (v2.1 - Corrected)
import json
import urllib.request
import urllib.parse
from datetime import datetime

CODEX_FILE = "codex.json"
OUTPUT_FILE = "daily_folio.json"
BIBLE_API_URL = "https://bible-api.com"

def fetch_passage_text(passage, translation):
    """Fetches the full text of a scripture passage in a specific translation."""
    try:
        # URL-encode the passage reference to handle spaces and special characters
        url_encoded_passage = urllib.parse.quote(passage)
        # The API requires a translation parameter for non-KJV versions
        url = f"{BIBLE_API_URL}/{url_encoded_passage}?translation={translation}"
        
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                # API returns text with newlines; we will preserve them for the JS to handle
                return data.get("text", "Passage not found.")
            else:
                return "Passage not found."
    except Exception as e:
        print(f"Error fetching {passage} ({translation}): {e}")
        return "Error retrieving scripture."

def main():
    """The main function for the daily Scribe task."""
    print(f"[{datetime.now().isoformat()}] The Scribe begins its daily work...")

    # Load the AI's brain
    with open(CODEX_FILE, 'r', encoding='utf-8') as f:
        codex = json.load(f)

    # Determine the day of the year (1-366) to select today's theme
    # We use modulo to loop through our sample codex for demonstration
    day_of_year = datetime.now().timetuple().tm_yday
    theme_key = str((day_of_year - 1) % len(codex) + 1)
    
    daily_theme_data = codex.get(theme_key)

    if not daily_theme_data:
        print(f"Error: No theme found for key {theme_key}")
        return

    # Correctly fetch both KJV and WEB versions for each passage
    passages_with_text = []
    for passage_ref in daily_theme_data.get("passages", []):
        passage_data = {
            "reference": passage_ref,
            "kjv_text": fetch_passage_text(passage_ref, "kjv"),
            "web_text": fetch_passage_text(passage_ref, "web")
        }
        passages_with_text.append(passage_data)

    # Assemble the final folio for the day
    daily_folio = {
        "date": datetime.now().strftime("%B %d, %Y"),
        "theme": daily_theme_data.get("theme"),
        "passages": passages_with_text,
        "notes": daily_theme_data.get("notes")
    }

    # Write the output file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(daily_folio, f, indent=4)
    
    print(f"Success: Daily Folio for '{daily_folio['theme']}' has been created.")

if __name__ == "__main__":
    main()