# app.py

import requests
import json
from flask import Flask, render_template, request

app = Flask(__name__)

# No API credentials needed for this free version.

def get_unlimited_suggestions(topic):
    """
    This function gets unlimited keyword suggestions from the free
    Google Suggest API.
    """
    try:
        # 1. Construct the Google Suggest API URL
        api_url = f"http://suggestqueries.google.com/complete/search?client=firefox&q={topic}"

        # 2. Make the API request
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        # 3. Get the list of suggestions from the response
        # The response is a list within a list, so we parse it and take the second element
        suggestions = json.loads(response.text)[1]
        return suggestions

    except requests.exceptions.RequestException as e:
        print(f"API Request Error: {e}")
        return None
    except (json.JSONDecodeError, IndexError) as e:
        print(f"API Response Parsing Error: {e}")
        return None


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        topic = request.form['keyword']
        
        suggestions = get_unlimited_suggestions(topic)
        
        # If the API call fails, suggestions will be None
        if suggestions is None:
            suggestions = [] # Pass an empty list to the template to avoid errors

        return render_template('results.html', keywords=suggestions, topic=topic)

    # For a GET request, just show the homepage
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
