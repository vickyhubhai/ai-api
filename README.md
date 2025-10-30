# Python API for AI Providers

This is a Flask API that loads API keys from `.env` and provides endpoints to interact with various AI providers, fetching responses from all available keys for each provider.

## Live API

The API is deployed at: https://ai-api-bfap.onrender.com

## Supported Providers

- `google`: Uses Google Generative AI (Gemini) with multiple API keys
- `xai`: Uses xAI (Grok) API
- `grok`: Uses xAI (Grok) API  
- `openrouter`: Uses OpenRouter API with multiple keys
- `all`: Uses all available providers and API keys

## Installation

1. Install Python (if not already installed).
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Environment Variables

Create a `.env` file in the root directory with your API keys:

```
GOOGLE_GENERATIVE_AI_API_KEY=your_key_here
GOOGLE_API_KEY_1=your_key_here
GOOGLE_API_KEY_2=your_key_here
OPENROUTER_API_KEY=your_key_here
OPENROUTER_API_KEY_2=your_key_here
OPENROUTER_API_KEY_3=your_key_here
OPENROUTER_API_KEY_4=your_key_here
OPENROUTER_API_KEY_5=your_key_here
```

For production deployment, set `FLASK_DEBUG=false` to disable debug mode.

## Running the API

For local development:
```
python api.py
```

For production deployment (e.g., on Render.com):
```
gunicorn --bind 0.0.0.0:$PORT api:app
```

The API will run on the specified port and host.

## Endpoints

- `GET /`: Returns a welcome message.
- `GET /api/<provider>?query=<your_prompt>` or `POST /api/<provider>` with JSON body `{"query": "your prompt"}`: Interacts with AI providers using their API keys. Supported providers: `google`, `xai`, `grok`, `openrouter`, `all`. Returns `{"responses": [list of answers from each available API key]}`.

## Example Usage

Using GET with query parameter:

```
curl "https://ai-api-bfap.onrender.com/api/google?query=What%20is%20the%20capital%20of%20France%3F"
```

Or using POST with JSON body:

```
curl -X POST https://ai-api-bfap.onrender.com/api/google \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the capital of France?"}'
```

For all providers:

```
curl "https://ai-api-bfap.onrender.com/api/all?query=Hello%20World"
```

Response:
```json
{
  "responses": [
    "The capital of France is Paris.",
    "Paris is the capital city of France.",
    "France's capital is Paris."
  ]
}
```

## Environment Variables

Create a `.env` file in the root directory with your API keys:

```
GOOGLE_GENERATIVE_AI_API_KEY=your_key_here
GOOGLE_API_KEY_1=your_key_here
GOOGLE_API_KEY_2=your_key_here
OPENROUTER_API_KEY=your_key_here
OPENROUTER_API_KEY_2=your_key_here
OPENROUTER_API_KEY_3=your_key_here
OPENROUTER_API_KEY_4=your_key_here
OPENROUTER_API_KEY_5=your_key_here
```

For production deployment, set `FLASK_DEBUG=false` to disable debug mode.

## Notes

- This API makes external API calls and may incur costs based on your API key usage.
- Ensure your API keys have sufficient credits/quota.
- For `xai`, `grok`, and `openrouter`, the code uses "gpt-3.5-turbo" as the model, but availability may vary. You can modify the code to use different models if needed.
- Use with caution in secure environments only, as it involves API keys.