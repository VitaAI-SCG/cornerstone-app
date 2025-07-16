# scribe.py - The Scribe's Snowfall (v2.0)
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
        url_encoded_passage = urllib.parse.quote(passage)
        url = f"{BIBLE_API_URL}/{url_encoded_passage}?translation={translation}"
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                # API returns text with newlines, replace for HTML
                return data.get("text", "Passage not found.").replace("\n", " ")
            return "Passage not found."
    except Exception as e:
        print(f"Error fetching {passage} ({translation}): {e}")
        return "Error retrieving scripture."

def main():
    """The main function for the daily Scribe task."""
    print(f"[{datetime.now().isoformat()}] The Scribe begins its daily work...")

    with open(CODEX_FILE, 'r', encoding='utf-8') as f:
        codex = json.load(f)

    day_of_year = datetime.now().timetuple().tm_yday
    theme_key = str((day_of_year - 1) % len(codex) + 1)
    
    daily_theme_data = codex.get(theme_key)

    if not daily_theme_data:
        print(f"Error: No theme found for key {theme_key}"); return

    # Fetch both KJV and WEB versions for each passage
    passages_with_text = []
    for passage_ref in daily_theme_data.get("passages", []):
        passage_data = {
            "reference": passage_ref,
            "kjv_text": fetch_passage_text(passage_ref, "kjv"),
            "web_text": fetch_passage_text(passage_ref, "web")
        }
        passages_with_text.append(passage_data)

    daily_folio = {
        "date": datetime.now().strftime("%B %d, %Y"),
        "theme": daily_theme_data.get("theme"),
        "passages": passages_with_text,
        "notes": daily_theme_data.get("notes")
    }

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(daily_folio, f, indent=4)
    
    print(f"Success: Daily Folio for '{daily_folio['theme']}' has been created.")

if __name__ == "__main__":
    main()
