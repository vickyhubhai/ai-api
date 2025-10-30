# Python API for AI Providers

This is a Flask API that loads API keys from `.env` and provides endpoints to interact with various AI providers, fetching responses from all available keys for each provider.

## Installation

1. Install Python (if not already installed).
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the API

```
python api.py
```

The API will run on `http://localhost:5000`.

## Endpoints

- `GET /`: Returns a welcome message.
- `GET /api/<provider>?query=<your_prompt>` or `POST /api/<provider>` with JSON body `{"query": "your prompt"}`: Interacts with AI providers using their API keys. Supported providers: `google`, `xai`, `grok`, `openrouter`, `all`. Returns `{"responses": [list of answers from each available API key]}`.

## Supported Providers

- `google`: Uses Google Generative AI with keys `GOOGLE_GENERATIVE_AI_API_KEY`, `GOOGLE_API_KEY_1`, `GOOGLE_API_KEY_2`.
- `xai`: Currently unavailable (invalid API keys).
- `grok`: Currently unavailable (invalid API keys).
- `openrouter`: Uses OpenRouter API with `OPENROUTER_API_KEY` to `OPENROUTER_API_KEY_5`.
- `all`: Uses all available API keys from working providers.

## Example Usage

Using GET with query parameter:

```
curl "http://localhost:5000/api/google?query=What%20is%20the%20capital%20of%20France%3F"
```

Or using POST with JSON body:

```
curl -X POST http://localhost:5000/api/google \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the capital of France?"}'
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

## Notes

- This API makes external API calls and may incur costs based on your API key usage.
- Ensure your API keys have sufficient credits/quota.
- For `xai`, `grok`, and `openrouter`, the code uses "gpt-3.5-turbo" as the model, but availability may vary. You can modify the code to use different models if needed.
- Use with caution in secure environments only, as it involves API keys.