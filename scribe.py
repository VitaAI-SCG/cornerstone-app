import os
import json
import random
import google.generativeai as genai

# A list of themes for the AI to choose from.
THEMES = [
    "Grace in Failure", "The Nature of Forgiveness", "Finding Strength in Humility",
    "Leadership and Servanthood", "The Power of Prayer", "Love for One's Neighbor",
    "Dealing with Anxiety", "The Meaning of Faith", "Parables of the Kingdom",
    "Justice and Righteousness", "The Promise of Redemption", "The Cost of Discipleship",
    "Finding Joy in Suffering", "The Wisdom of Listening", "The Nature of True Wealth",
    "Creation and Stewardship", "Conflict and Peacemaking", "Light in the Darkness",
    "The Shepherd and His Flock", "The Coming of the Holy Spirit"
]

def generate_daily_folio():
    """
    Generates a daily folio with a standard devotional and an optional deeper academic dive.
    """
    folio_data = {}
    try:
        api_key = os.environ.get('API_KEY')
        if not api_key:
            raise ValueError("API_KEY environment variable not set.")
        genai.configure(api_key=api_key)

        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        generation_config = { "temperature": 0.8, "top_p": 1, "top_k": 1, "max_output_tokens": 4096 }
        model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config, safety_settings=safety_settings)

        # --- STEP 1: GENERATE THE PASTORAL FOLIO ---
        today_theme = random.choice(THEMES)
        pastoral_prompt = [
            f"You are The Digital Scribe, a warm, wise, and pastoral theologian creating a personal daily Bible folio for a man named Jeff. Your theme for today is: '{today_theme}'. Your response must be a valid, minified JSON object with NO markdown formatting.",
            "Generate the following keys:",
            "`theme`, `passages` (an array of two scripture references), `location` (a JSON object with name, lat, lon), `context`, `theology`, `reflection`, `prayer_starter`."
        ]
        
        response = model.generate_content(pastoral_prompt)
        folio_content = response.text
        if folio_content.strip().startswith("```json"):
            folio_content = folio_content.strip()[7:-3]
        folio_data = json.loads(folio_content)
        print("Successfully generated pastoral folio.")

        # --- STEP 2: GENERATE THE ACADEMIC 'DEEPER DIVE' ---
        try:
            passages_for_dive = " and ".join(folio_data.get('passages', []))
            if passages_for_dive:
                academic_prompt = [
                    f"You are a university-level biblical scholar providing a 'Deeper Dive' on {passages_for_dive} for a student named Jeff. The theme is '{folio_data.get('theme', '')}'. Your response must be a single string using markdown for formatting.",
                    "Structure your response with the following markdown H3 headings (###):",
                    "### Key Term Analysis: Analyze one key term from the passages in its original Hebrew or Greek.",
                    "### Historical Insight: Provide a surprising or little-known historical fact that illuminates the context.",
                    "### Theological Connection: Connect the passages to a major systematic theological concept.",
                    "### A Scholar's Question: Pose one challenging, open-ended question for deep reflection."
                ]
                deeper_dive_response = model.generate_content(academic_prompt)
                folio_data['deeper_dive'] = deeper_dive_response.text
                print("Successfully generated academic 'Deeper Dive'.")
        except Exception as dive_error:
            print(f"Could not generate Deeper Dive: {dive_error}")
    
    except Exception as e:
        print(f"An error occurred in the main folio generation: {e}")
        folio_data = { "theme": "Connection Error", "passages": ["Psalm 46:10", "Matthew 11:28"], "location": {"name": "Sea of Galilee", "lat": 32.82, "lon": 35.58}, "context": "There was a temporary issue connecting to the Digital Scribe.", "theology": "Even in moments of technical difficulty, we can find peace.", "reflection": "Jeff, there was an issue creating your folio today. Perhaps this is a moment to simply be still and know that He is God. What can you find in the quiet today?", "prayer_starter": "Lord, help me find you in the silence and stillness of this moment."}
        print("Created a fallback error folio.")
    
    with open('daily_folio.json', 'w') as f:
        json.dump(folio_data, f, indent=None)
    print("Folio generation process complete.")

if __name__ == "__main__":
    generate_daily_folio()