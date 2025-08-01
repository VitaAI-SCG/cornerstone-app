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

# --- Main function to generate the folio ---
def generate_daily_folio():
    """
    Generates a daily folio JSON file using a generative AI model.
    """
    try:
        # Configure the generative AI model with the API key from GitHub Secrets
        api_key = os.environ.get('API_KEY')
        if not api_key:
            raise ValueError("API_KEY environment variable not set.")
        genai.configure(api_key=api_key)

        # Add safety settings to prevent overly aggressive blocking
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]

        # Set up the model with the new safety settings
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
        # Using the correct, specific model name
        model = genai.GenerativeModel(
            model_name="gemini-1.0-pro",
            generation_config=generation_config,
            safety_settings=safety_settings
        )

        # Randomly select a theme for the day
        today_theme = random.choice(THEMES)

        # Craft the prompt for the AI model
        prompt_parts = [
            f"You are The Digital Scribe, a warm, wise, and pastoral theologian creating a personal daily Bible folio for a man named Jeff. Your theme for today is: '{today_theme}'. Your response must be a valid, minified JSON object with NO markdown formatting.",
            "Generate the following keys:",
            "`theme`: The theme for today.",
            "`passages`: An array of two complementary scripture references (one OT, one NT) in 'Book Chapter:Verses' format that fit the theme.",
            "`location`: A JSON object with `name`, `lat`, and `lon` for the primary location in the NT passage.",
            "`context`: A brief, accessible note on the historical and literary context of the passages.",
            "`theology`: A short note on the theological history or meaning of the theme.",
            "`reflection`: A personal, gentle, and encouraging reflection (around 100 words) addressed directly to Jeff, ending with a thought-provoking question related to his life.",
            "`prayer_starter`: A one-sentence prayer starter for Jeff based on the reflection.",
        ]

        # Generate the content using the AI model
        response = model.generate_content(prompt_parts)

        # Clean the response to ensure it's valid JSON
        folio_content = response.text
        if folio_content.strip().startswith("```json"):
            folio_content = folio_content.strip()[7:-3]

        # Parse the JSON and save it to a file
        folio_data = json.loads(folio_content)
        with open('daily_folio.json', 'w') as f:
            json.dump(folio_data, f, indent=None)

        print("Successfully generated daily_folio.json")

    except Exception as e:
        print(f"An error occurred: {e}")
        # As a fallback, create a simple error folio
        error_folio = {
            "theme": "Connection Error",
            "passages": ["Psalm 46:10", "Matthew 11:28"],
            "location": {"name": "Sea of Galilee", "lat": 32.82, "lon": 35.58},
            "context": "There was a temporary issue connecting to the Digital Scribe.",
            "theology": "Even in moments of technical difficulty, we can find peace.",
            "reflection": "Jeff, there was an issue creating your folio today. Perhaps this is a moment to simply be still and know that He is God. What can you find in the quiet today?",
            "prayer_starter": "Lord, help me find you in the silence and stillness of this moment."
        }
        with open('daily_folio.json', 'w') as f:
            json.dump(error_folio, f, indent=None)
        print("Created a fallback error folio.")


if __name__ == "__main__":
    generate_daily_folio()