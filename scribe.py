import os
import google.generativeai as genai

print("--- RUNNING DIAGNOSTIC SCRIPT ---")
try:
    api_key = os.environ.get('API_KEY')
    if not api_key:
        raise ValueError("API_KEY not found in environment.")

    genai.configure(api_key=api_key)
    # Use the most basic model name for the test
    model = genai.GenerativeModel('gemini-pro') 

    print("Model configured. Sending simple test prompt...")
    response = model.generate_content("Why is the sky blue? Explain it simply.")

    print("--- RESPONSE RECEIVED FROM GOOGLE ---")
    print(response.text)
    print("-----------------------------------")

    # Create a dummy folio file so the rest of the workflow doesn't fail
    with open('daily_folio.json', 'w') as f:
        f.write('{"theme": "Diagnostic Test Complete. Check logs."}')
    print("Diagnostic complete.")

except Exception as e:
    print("---!!! AN ERROR OCCURRED DURING THE TEST !!!---")
    print(e)
    print("-----------------------------------------------")
    # Create a dummy folio file to prevent workflow failure
    with open('daily_folio.json', 'w') as f:
        f.write('{"theme": "Diagnostic Test Failed. Check logs."}')