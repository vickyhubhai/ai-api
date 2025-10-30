from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv
from openai import OpenAI
import google.generativeai as genai
import requests

load_dotenv()

app = Flask(__name__)

providers = {
    'google': ['GOOGLE_GENERATIVE_AI_API_KEY', 'GOOGLE_API_KEY_1', 'GOOGLE_API_KEY_2'],
    'xai': [],
    'grok': [],
    'openrouter': ['OPENROUTER_API_KEY', 'OPENROUTER_API_KEY_2', 'OPENROUTER_API_KEY_3', 'OPENROUTER_API_KEY_4', 'OPENROUTER_API_KEY_5'],
    'all': ['GOOGLE_GENERATIVE_AI_API_KEY', 'GOOGLE_API_KEY_1', 'GOOGLE_API_KEY_2', 'OPENROUTER_API_KEY', 'OPENROUTER_API_KEY_2', 'OPENROUTER_API_KEY_3', 'OPENROUTER_API_KEY_4', 'OPENROUTER_API_KEY_5']
}

@app.route('/')
def home():
    return "API is running. Use POST to /api/<provider> with {'query': 'your prompt'}."

@app.route('/api/<provider>', methods=['GET', 'POST'])
def api_provider(provider):
    if request.method == 'POST':
        data = request.get_json()
        query = data.get('query') if data else None
    else:
        query = request.args.get('query')
    if not query:
        return jsonify({"error": "query required"}), 400
    if provider not in providers:
        return jsonify({"error": "invalid provider"}), 400
    keys = providers[provider]
    responses = []
    for key in keys:
        api_key = os.getenv(key)
        if not api_key:
            continue
        try:
            if key.startswith('GOOGLE'):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={api_key}"
                data = {"contents": [{"parts": [{"text": query}]}]}
                resp = requests.post(url, json=data)
                if resp.status_code == 200:
                    result = resp.json()
                    text = result['candidates'][0]['content']['parts'][0]['text']
                    responses.append(text)
                else:
                    error_text = resp.text
                    if "not found" in error_text.lower():
                        list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
                        list_resp = requests.get(list_url)
                        if list_resp.status_code == 200:
                            models_data = list_resp.json()
                            available = [m['name'] for m in models_data.get('models', []) if 'generateContent' in m.get('supportedGenerationMethods', [])]
                            responses.append(f"Available models: {available}")
                        else:
                            responses.append(f"List models error: {list_resp.text}")
                    else:
                        responses.append(f"Error: {error_text}")
            elif key.startswith('XAI') or key.startswith('GROK'):
                base_url = "https://api.x.ai/v1"
                client = OpenAI(api_key=api_key, base_url=base_url)
                response = client.chat.completions.create(
                    model="grok-beta",
                    messages=[{"role": "user", "content": query}]
                )
                responses.append(response.choices[0].message.content)
            elif key.startswith('OPENROUTER'):
                base_url = "https://openrouter.ai/api/v1"
                client = OpenAI(api_key=api_key, base_url=base_url)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": query}]
                )
                responses.append(response.choices[0].message.content)
            else:
                responses.append(f"Unknown key type: {key}")
        except Exception as e:
            responses.append(f"Error with {key}: {str(e)}")
    return jsonify({"responses": responses})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
